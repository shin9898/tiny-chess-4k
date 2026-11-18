#!/usr/bin/python3
"""One-off helper for ticket 032 (run on the Mac that hosts ~/x-queue).

1. Verifies that @shachikutanaka follows @jtc_ojisan2 (connection_status).
2. Saves up to 100 accounts that @jtc_ojisan2 follows to
   ~/x-queue/results/cho-following.json (username / name / description).

Auth reuses x-poster.py's load_keys/get_signed; key values are never printed.
If the API refuses (tier, rate limit, protected account), the reason is written
to the result file and the step is skipped — no workaround is attempted.
"""

import importlib.util
import json
import sys
from pathlib import Path

BASE = Path.home() / "x-queue"
TARGET = "jtc_ojisan2"
OUT = BASE / "results" / "cho-following.json"

spec = importlib.util.spec_from_file_location("xposter", BASE / "x-poster.py")
xp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(xp)


def main():
    keys = xp.load_keys()
    if keys is None:
        print("keys not set — abort")
        return 1
    calls = []
    report = {"ts": xp.now_iso(), "target": TARGET}

    # 1. follow verification via connection_status
    try:
        user = xp.lookup_user(TARGET, keys, fields="username,name,connection_status,protected")
        calls.append("GET users/by/username (1 user)")
        report["target_user_id"] = user["id"]
        report["connection_status"] = user.get("connection_status")
        report["verified_following"] = "following" in (user.get("connection_status") or [])
    except RuntimeError as e:
        calls.append("GET users/by/username (failed)")
        report["verify_error"] = str(e)
        user = None

    # 2. following list of the target (max 100, single page)
    if user is None:
        report.update(status="skipped", reason="target lookup failed")
    elif user.get("protected") and not report.get("verified_following"):
        report.update(status="skipped", reason="target account is protected")
    else:
        try:
            _, resp = xp.get_signed(
                f"{xp.USERS_URL}/{user['id']}/following",
                {"max_results": "100", "user.fields": "username,name,description"},
                keys,
            )
            data = (resp or {}).get("data") or []
            calls.append(f"GET users/:id/following ({len(data)} users)")
            report.update(
                status="ok",
                count=len(data),
                has_more=bool(((resp or {}).get("meta") or {}).get("next_token")),
                following=[
                    {
                        "username": u.get("username"),
                        "name": u.get("name"),
                        "description": u.get("description", ""),
                    }
                    for u in data
                ],
            )
            if not data and resp.get("errors"):
                report["api_errors"] = resp["errors"]
        except RuntimeError as e:
            calls.append("GET users/:id/following (failed)")
            report.update(status="skipped", reason=str(e))

    report["api_calls"] = calls
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {k: report.get(k) for k in ("verified_following", "connection_status", "status", "count", "has_more", "reason", "verify_error")}
    summary["api_calls"] = calls
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
