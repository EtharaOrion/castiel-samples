#!/usr/bin/env python3
"""Castiel differential reward verifier (stdlib only).

Reward 1.0 iff vul_exit signals a sanitizer crash AND fix_exit is safe.
Timeout/OOM codes {124, 137, -9} count as benign on the fix side and
neutralise the vul side.
"""
import json
import sys

TIMEOUT_OOM = {124, 137, -9}
FIX_STATUS_CLEAN = 0
FIX_STATUS_CRASH = 1
FIX_STATUS_TIMEOUT = 2
FIX_STATUS_RESOURCE = 3


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"reward": 0.0, "vul_exit": None, "fix_exit": None,
                          "fix_status": FIX_STATUS_CRASH,
                          "error": "missing exit codes"}))
        sys.exit(2)
    try:
        vul_exit = int(sys.argv[1])
        fix_exit = int(sys.argv[2])
    except (TypeError, ValueError):
        print(json.dumps({"reward": 0.0, "vul_exit": None, "fix_exit": None,
                          "fix_status": FIX_STATUS_CRASH,
                          "error": "non-integer exit code"}))
        sys.exit(2)

    vul_crashed = (vul_exit != 0) and (vul_exit not in TIMEOUT_OOM)
    fix_safe    = (fix_exit == 0) or (fix_exit in TIMEOUT_OOM)
    reward      = 1.0 if (vul_crashed and fix_safe) else 0.0

    if fix_exit == 0:
        fix_status = FIX_STATUS_CLEAN
    elif fix_exit == 124:
        fix_status = FIX_STATUS_TIMEOUT
    elif fix_exit in (137, -9):
        fix_status = FIX_STATUS_RESOURCE
    else:
        fix_status = FIX_STATUS_CRASH

    print(json.dumps({"reward": reward, "vul_exit": vul_exit,
                      "fix_exit": fix_exit, "fix_status": fix_status}))


if __name__ == "__main__":
    main()
