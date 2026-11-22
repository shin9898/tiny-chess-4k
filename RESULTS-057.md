---
ticket: 057
status: stopped_at_step_3
stopped_at_step: 3
fail_items: [license_osi, transcripts_present]
at: 2026-11-22 JST
---

# 057 結果: D1 提出 — 手順3で停止（未提出）

- 提出: **未実施**。submission id・ステータスなし。現行の有効提出は保険の engine-v3 のまま。
- 止まった手順: **3（bundle 作成）**。bundle は作っていない（dry-run のみ）。
- kit check の fail 項目: `license_osi`、`transcripts_present`

## 手順1: kit 再取得と bundle_sha256 照合 — 一致

- 取得元: `https://make.fun/c/tiny-chess-01/kit`（HTTP 200、9,293,454 バイト、tar.gz の sha256 `4b87f488…399c398b`）
- CLI: `0.1.0 (kit level 36, build 79d7b7dbf92d)`

| 照合対象 | kit 側（kit.json） | サイト側 |
|---|---|---|
| bundle_sha256 | `86e0db42be25db06131cdc33f5a2cc521092e5b9d49a303c4eff7ee8239055b4` | `/api/competitions/tiny-chess-01` の `bundleSha256`、`/kit` の `bundle_sha256` とも同値 |

## 手順2: 提出プログラムの確定 — 完了

- `origin/maint/chess-pdca-r2-051:.r051/d1-main.py` を `main.py` として配置。コミット `ef77b22`。
- 3,537 バイト（4,096 未満）、sha256 `7b3bece7…2ddbc`、`py_compile` 通過。
- engine-v3 の main.py（3,454 バイト）と差分あり（1行の差し替え）。

## 手順3: bundle 作成 — 停止

`makefun bundle --dry-run`（`--prompt-origin handed-off`、prompt-file は 033 と同じ `prompt-user-instruction.md`）の結果、指示書どおりには作れない点が2つある。

1. **settings.json を bundle から外せない。** kit level 36 の bundle には `--no-context` が無く、ヘルプは「every file it finds goes up: redact what you would rather keep private, never leave one out」としている。dry-run は `context/user/claude-code/settings.json`（`~/.claude/settings.json`）を収録すると表示した。033 の前例（`--no-context` + `--context` 個別指定）は今の kit では使えない（056 と同じ事象）。
2. **handed-off の親チャットが無い。** dry-run は `missing: the parent chats` を返し、この状態では bundle を書き出さない。見つかった47セッション（リポジトリ一致41、関連6）のどれも、本人がプロンプトを打ったセッションまで連鎖しない。Muse の親チャットを `--parent-session` で渡す必要がある（046・047・056 と同じ原因）。

（`--effort` 未指定の missing も出たが、フラグを足せば済むもので停止理由ではない。）

### kit check（bundle なし、`--repo` HEAD=`ef77b22`）

`5 passed, 2 failed, 14 skipped, 5 checked at submission`

| 結果 | 項目 |
|---|---|
| pass | competition_open, snapshot, entrypoint, entry_size（5,708 / 8,192 バイト、main.py 3,537）, committed_provider_key |
| **FAIL** | **license_osi**: LICENSE に `SPDX-License-Identifier:` 行が無い |
| **FAIL** | **transcripts_present**: transcripts 未添付（手順3の停止による） |
| skip | strategy_note, committed_secret, transcripts_recorded, thinking_wellformed, thinking_in_window, thinking_committed, thinking_reproduces, thinking_on_task, thinking_turns, thinking_priced, thinking_revised, thinking_fresh, transcripts_run_record, thinking_own_work |
| 提出時に判定 | repo_public, repo_owner, repo_created_after_open, commit_in_repo（ef77b22 は未 push）, duplicate_snapshot |

LICENSE は engine-v3 と同一 blob（`d5f0867a`）。回避策（LICENSE 編集など）は作っていない。

## 手順4に進んでも止まる点（読み取りだけで確認）

- `~/.makefun` にあるのは `compress.json` だけ。`credentials`・`keypairs/` は無く、`MAKEFUN_API_KEY` / `MAKEFUN_CREDENTIALS` も未設定。指示書の「~/.makefun の既存の資格情報と鍵素材」は存在しない。対話的 login はしていない。
- repo@commit 提出には ef77b22 が GitHub 上にある必要がある（commit_in_repo）。push は本チケットの担当外。

## 判断が要ること

1. settings.json の扱い: 今の kit では外せない。収録して `--redact` で伏せるか、方針を変えるか。
2. 親チャット: Muse の該当チャットを書き出して `--parent-session` で渡せるか。
3. license_osi: LICENSE 先頭に `SPDX-License-Identifier: MIT` を足すか。
4. 認証: 資格情報の実際の場所、または本人による `makefun login` 承認。
5. ef77b22 の push タイミング。
