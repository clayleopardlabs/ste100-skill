#!/usr/bin/env python3
"""STE100 graded-test supervisor: launches a subagent run with EXTERNAL loop enforcement.

The subagent cannot self-enforce limits (untrustworthy model). This supervisor
is the enforcement: it launches the agent as a child process and kills it on:
  - wall-clock cap (default 900s)
  - total tool-call cap (default 40)
  - identical-consecutive-command cap (default 6)

Usage:
  python ste100_supervisor.py --test test-10 --round 1 [--max-time 900] [--max-tools 40] [--max-repeats 6]

The supervisor writes a run report to <repo>/STE100 tests/runs/<test>-round-<n>.json
and grades the final draft (lint + --details + line count).
"""
import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

REPO = Path(r"C:\Users\Omen\AppData\Local\Temp\opencode\ste100-skill-repo")
DB = Path(r"C:\Users\Omen\.local\share\opencode\opencode.db")
DRAFT = Path(r"C:\Users\Omen\AppData\Local\Temp\opencode\ste100-draft.md")
LINTER = Path(r"C:\Users\Omen\.config\opencode\skills\ste100\references\ste_check.py")
RUNS = REPO / "STE100 tests" / "runs"
RUNS.mkdir(parents=True, exist_ok=True)

PROMPT = """Correct a test paragraph to comply with ASD-STE100 Simplified Technical English.

1. Read C:\\Users\\Omen\\.config\\opencode\\skills\\ste100\\SKILL.md in full. Read rules files under C:\\Users\\Omen\\.config\\opencode\\skills\\ste100\\references\\rules\\ when a rule applies.
2. Read the input: {TEST_PATH}
3. Run the linter on the input and save output: python C:\\Users\\Omen\\.config\\opencode\\skills\\ste100\\references\\ste_check.py "{TEST_PATH}" > C:\\Users\\Omen\\AppData\\Local\\Temp\\opencode\\lint-original.txt 2>&1 ; then Get-Content -Raw C:\\Users\\Omen\\AppData\\Local\\Temp\\opencode\\lint-original.txt
4. Write your corrected version to C:\\Users\\Omen\\AppData\\Local\\Temp\\opencode\\ste100-draft.md (overwrite it). Keep every action and every technical detail of the original (Rule 4.2). Split any sentence over 20 words. One action per sentence - no "and"/"then"/"while" joins. No -ing forms (use the same verb as an imperative: "while holding the valve" -> "Hold the valve."). No passives. No noun clusters over 3 words (keep the head noun and the sentence verb; use prepositions). For unapproved words run python C:\\Users\\Omen\\.config\\opencode\\skills\\ste100\\references\\lookup.py <word> and use the dictionary alternative exactly.
5. Re-lint the draft until the last output line reads exactly "0 errors, 0 warnings": python C:\\Users\\Omen\\.config\\opencode\\skills\\ste100\\references\\ste_check.py C:\\Users\\Omen\\AppData\\Local\\Temp\\opencode\\ste100-draft.md
6. Run the detail check: python C:\\Users\\Omen\\.config\\opencode\\skills\\ste100\\references\\ste_check.py --details "{TEST_PATH}" C:\\Users\\Omen\\AppData\\Local\\Temp\\opencode\\ste100-draft.md - last line must read "0 errors, 0 warnings".
7. When both checks pass, run: Get-FileHash C:\\Users\\Omen\\AppData\\Local\\Temp\\opencode\\ste100-draft.md ; Get-Content -Raw C:\\Users\\Omen\\AppData\\Local\\Temp\\opencode\\ste100-draft.md

Do not modify the test file.

Final message: the verbatim lint-original.txt content, the hash, the final lint output, the --details output, and the draft text copied exactly from Get-Content -Raw."""


def db_connect():
    return sqlite3.connect(DB, timeout=30)


def find_session(con, title, after_ms):
    rows = con.execute(
        "SELECT id, title, time_created, time_updated FROM session "
        "WHERE title LIKE ? AND time_created >= ? ORDER BY time_created DESC LIMIT 1",
        (f"%{title}%", after_ms),
    ).fetchall()
    return rows[0] if rows else None


def count_tools(con, sid):
    rows = con.execute(
        "SELECT data FROM part WHERE session_id=?", (sid,)
    ).fetchall()
    n = 0
    for (data,) in rows:
        try:
            if json.loads(data).get("type") == "tool":
                n += 1
        except Exception:
            pass
    return n


def last_commands(con, sid, n):
    rows = con.execute(
        "SELECT data FROM part WHERE session_id=? "
        "ORDER BY time_created DESC LIMIT ?",
        (sid, n),
    ).fetchall()
    cmds = []
    for (data,) in rows:
        try:
            d = json.loads(data)
            if d.get("type") != "tool":
                continue
            state = d.get("state") or {}
            inp = state.get("input") or {}
            cmd = inp.get("command")
            if cmd:
                cmds.append(str(cmd)[:120])
        except Exception:
            pass
    return cmds


def last_repeat_run(con, sid):
    cmds = last_commands(con, sid, 16)
    if not cmds:
        return 0
    from collections import Counter
    top, count = Counter(cmds).most_common(1)[0]
    return count if count >= 6 else 0


def lint_draft():
    r = subprocess.run(
        [sys.executable, str(LINTER), str(DRAFT)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    out = r.stdout.strip().splitlines()
    last = out[-1] if out else ""
    return last, r.stdout


def details_draft(test_path):
    r = subprocess.run(
        [sys.executable, str(LINTER), "--details", str(test_path), str(DRAFT)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    out = r.stdout.strip().splitlines()
    last = out[-1] if out else ""
    return last


def kill_tree(pid):
    subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                   capture_output=True, text=True)
    print(f"[supervisor] killed process tree {pid}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", required=True, help="test file name, e.g. test-10")
    ap.add_argument("--round", required=True, help="round label, e.g. 1")
    ap.add_argument("--max-time", type=int, default=900)
    ap.add_argument("--max-tools", type=int, default=40)
    ap.add_argument("--max-repeats", type=int, default=6)
    args = ap.parse_args()

    test_path = REPO / "STE100 tests" / f"{args.test}.md"
    title = f"STE10 {args.test} round {args.round}"
    report = {"test": args.test, "round": args.round,
              "start": datetime.now().isoformat(timespec="seconds"),
              "outcome": "ERROR", "detail": ""}

    prompt = PROMPT.format(TEST_PATH=test_path)
    log = RUNS / f"{args.test}-round-{args.round}.log"
    with open(log, "w", encoding="utf-8") as f:
        f.write(f"=== supervisor run {args.round} ===" + "\n")

    env = dict(os.environ)
    env.pop("OPENCODE_SERVER_PASSWORD", None)
    env.pop("OPENCODE_SERVER_USERNAME", None)

    proc = subprocess.Popen(
        ["opencode", "run", "--agent", "omnicoder", "--title", title, prompt],
        stdout=open(log, "a", encoding="utf-8"),
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        env=env,
    )
    launched_ms = int(time.time() * 1000)
    print(f"[supervisor] launched pid={proc.pid} title={title}", flush=True)

    con = db_connect()
    sid = None
    t0 = time.time()
    outcome = "RUNNING"
    try:
        while time.time() - t0 < args.max_time:
            time.sleep(4)
            if not sid:
                s = find_session(con, title, launched_ms - 5000)
                if s:
                    sid = s[0]
                    print(f"[supervisor] session {sid}", flush=True)
            if sid:
                tools = count_tools(con, sid)
                if tools > args.max_tools:
                    outcome = "TOOL_CAP"
                    report["detail"] = f"tool calls {tools} > {args.max_tools}"
                    break
                repeats = last_repeat_run(con, sid)
                if repeats >= args.max_repeats:
                    outcome = "REPEAT_LOOP"
                    report["detail"] = f"{repeats} identical consecutive commands"
                    break
                print(f"[supervisor] tools={tools} repeats={repeats}", flush=True)
            else:
                print("[supervisor] waiting for session...", flush=True)
            if proc.poll() is not None:
                outcome = "COMPLETED" if not sid else "COMPLETED"
                report["detail"] = "process exited"
                break
        else:
            outcome = "WALL_CLOCK"
            report["detail"] = f"exceeded {args.max_time}s"
    finally:
        con.close()

    if outcome != "COMPLETED" and proc.poll() is None:
        kill_tree(proc.pid)
    proc.wait(timeout=20)

    if outcome == "RUNNING":
        outcome = "WALL_CLOCK"
        report["detail"] = f"exceeded {args.max_time}s"
    report["outcome"] = outcome

    lint_line, lint_full = lint_draft()
    report["draft_lint"] = lint_line
    report["draft_details"] = details_draft(test_path)
    if DRAFT.exists():
        report["draft_lines"] = len(DRAFT.read_text(encoding="utf-8", errors="replace").splitlines())
        report["draft_hash"] = __import__("hashlib").sha256(
            DRAFT.read_bytes()).hexdigest()[:16]
    else:
        report["draft_lines"] = 0
        report["draft_hash"] = ""

    report["end"] = datetime.now().isoformat(timespec="seconds")
    out = RUNS / f"{args.test}-round-{args.round}.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[supervisor] {json.dumps(report)}", flush=True)


if __name__ == "__main__":
    main()
