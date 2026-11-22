---
ticket: 064
status: done
submission_commit: 46b35c6fb7d6b190f13a6afb5252f8bf31f46034
base_commit: d69a5783be6b58033eff7230bf2c027072f0983a
main_py_bytes: 3532
---

# 064: Repack chess D1 with kit compress

Submission tree: `46b35c6` (this file is a separate commit on top of it, following the 061 convention).

- Kit: re-fetched `https://make.fun/c/tiny-chess-01/kit` on 2026-11-22 (tarball sha256 `b02d975a…93c7`, header x-kit-sha256 `22a70a14…8f4a`, kit.json bundle_sha256 `86e0db42…55b4`, phase dev). Unpacked outside the repository; CLI = `<kit>/cli/makefun.mjs`, run on node v22.18.0.
- Source: `origin/maint/chess-pdca-r2-051:.r051/d1.py` written out as `d1.py` (blob `60787c10`, 7320 bytes, sha256 `c108e000…f7cc`). Not edited.
- Compress (run once, as the last change): `node <kit>/cli/makefun.mjs compress d1.py --out main.py` -> main.py 3532 bytes, sha256 `506a7be4…0c78` (the expected value was about 3,532 bytes, and it matches). Recorded by the kit in `~/.makefun/compress.json`.
- Round trip: decompressing the lzma payload of main.py (without running it) gives 7320 bytes with sha256 `c108e000…f7cc` = d1.py.
- `d1.py` was deleted, never committed. `git diff --name-only d69a578 46b35c6` -> `main.py` only. Tree total 5733 bytes (LICENSE 1095, README.md 1106, main.py 3532).
- Not done: submit and bundle.
- Note for the submit step: compress says that `makefun bundle` sends `d1.py` along with the sessions. Restore d1.py from the source blob above before bundling.
