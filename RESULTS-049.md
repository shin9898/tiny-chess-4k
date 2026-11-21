# 049 C3 の提出 — needs_decision（未提出）

## 結論（2026-11-21）
**提出はしていない。** C3 のコミット `b3d7f39` が GitHub 上に存在しないため。GitHub リポジトリの entry では、サーバーが提出時に GitHub から指定コミットの snapshot を取る（RULES「Submitting」）。ところがこのコミットは push されていない（`git ls-remote origin` に無く、GitHub API `GET /repos/shin9898/tiny-chess-4k/commits/b3d7f39…` は 422）。実装役は push しない取り決めなので、ここで止めた。

| 手順 | 結果 |
|---|---|
| 1. C3 の main.py | `b3d7f39dc948ce39d59768c576fb6860e3bb4620`（ブランチ `engine-v4-exp`）の main.py、**3,485 B**、sha256 `0835e9c0…6fdb168`。verify-c3-fullbudget（PR #4）には main.py が無い（`RESULTS-038.md` だけ）。043 と同じずれ |
| 2. バンドル作成 | **未作成**（理由は下） |
| 3. 決定性・完走 | 下の「提出前検証」 |
| 4. GitHub About | 設定済み: website `https://make.fun/bounty/tiny-chess-01`、topics に `makefun` あり、public（API で確認） |
| 5. 提出 | **未実行**。提出数は 1 件（保険）のまま |

## 代表の操作（これで再開できる）
1. C3 のコミットを GitHub に push する（main にはマージしない）:
   `cd /Users/apple/dev/tiny-chess-4k && git push origin engine-v4-exp`
   - `engine-v4-exp` の HEAD は b3d7f39。その下には C1 `b594cc3`・C2 `cfb5fed` の 2 コミットがあり、一緒に公開される。C3 だけを載せたい場合は `git push origin b3d7f39:refs/heads/submit-c3` でも中身は同じ（C1・C2 は親コミットなのでどちらにしても公開される）
   - b3d7f39 の README は 84c52ee のまま（バッジ 3 つあり）。snapshot は LICENSE 1,065 + README 1,106 + main.py 3,485 = 5,656 B（上限 8,192）
2. push の後に 049 を再投入する（または同じ手順で続ける）。バンドル作成からやり直す

## バンドルを作らなかった理由
- バンドルの manifest は `--repo` に渡したチェックアウトのコミットを記録する。033 は提出コミットのチェックアウト `~/dev/tiny-chess-submit` を使った。C3 用のチェックアウトを作るか切り替えるには、この worktree の外を変えることになる
- 出力先（033 では `~/claude-queue/artifacts/`）も worktree の外にある
- push 前に作っても提出できない。push の後に作れば、`kit check` まで一度に通せる

## 次のバンドルで追加するセッション
- 033 の 7 セッション（013・017・019・021）に、C1〜C3 を書いた 034 のセッションを足す:
  `~/.claude/projects/-Users-apple-claude-queue-worktrees-034/3213e01c-bfaf-46a9-b405-b853871bf136.jsonl`（1.6 MB。034 は rc=137 で異常終了したが、ログは C3 のコミット 00:34 まで残っている）
- 038・043 は計測だけで main.py を書いていないが、`engine-v4-exp` の作業に関わったセッションとして入れるかは代表が決める（入れても gate には影響しない見込み）
- `--notes` の「Submitted commit is the head of branch engine-v3」と ticket の並びは、C3 用に書き換える必要がある
- 未確認: 047 では news-image 側の kit（level 31）で、handed-off のプロンプトに親チャットの連鎖が求められていた。チェス側の手元 kit（level 19）の RULES にはこの規則が無いが、サイト側の規則は新しい可能性がある（RULES 冒頭「Each entry is held to the checks in force when it is checked」）。バンドルの前にキットを取り直すのが安全

## 提出前検証（C3 の main.py そのまま）
- 方法: `git show b3d7f39:main.py` を `.sub049/c3-main.py` に取り出し、043 と同じランナー（`~/dev/makefun-tiny-chess-work/run_trial.py`）で practice trial pt0 を 2 本並列で実行した（ポート 18490 / 18590）。スクリプトは `.sub049/run.sh`
- 完走: 2 本とも rc=0、6 局すべて詰みで終局。5 勝 1 敗（nodes-500k に負け）、Elo 1,654（043 の pt0 と同じ）。engine.err は 0 バイト
- 決定性: 2 本の `moves.json` がバイト単位で一致した。sha256 `b45e02b79a11ed2ab32d87f0a296fa5e6484eb747bb565fefc550b4b9416d2d1`（`cmp` でも一致）
- 1 手の最大実時間は 1.352 s / 1.353 s（低負荷、2 本並列）
- この「2 回実行してハッシュ一致」はエンジンの出力で確かめた。バンドル（transcripts.tar.gz）の 2 回作成は、バンドルを作っていないので未実施

## 指示書とのずれ
- C3 の main.py はブランチ verify-c3-fullbudget ではなく `engine-v4-exp`（b3d7f39）にある
- 手順 5 は「CLI で提出」だが、b3d7f39 は GitHub に無く、実装役は push できない。この組み合わせでは提出できない

## やっていないこと
- push、submit、login、バンドル作成、`kit check`
- 鍵ペアと `~/.makefun/credentials` の読み取り
- verify-c3-fullbudget のマージ、engine-v4-exp と engine-v3 の変更
- コミットしていないもの: `.sub049/runs/`、`log-*.txt`、`progress.txt`、`c3-main.py`（b3d7f39 から再生成できる）
