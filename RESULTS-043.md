# 043 C3 の practice Elo（2026-11-21）

## 結論
C3（b3d7f39 の main.py、3,485 B）の practice Elo は **1,654 / 1,809 / 1,451、平均 1,638**。engine-v3 の既測値（1,809 / 1,451 / 1,654、平均 1,638）と平均は同じで、practice trial では差が出なかった。

| trial | C3（今回） | engine-v3（021 の既測値。今回の再計測でも同じ） |
|---|---|---|
| pt0 | **1,654**（5/6：勝5・敗1。nodes-500k に詰まされて負け） | 1,809（5.5/6） |
| pt1 | **1,809**（5.5/6：勝5・分1。nodes-250k と判定引分） | 1,451（4/6） |
| pt2 | **1,451**（4/6：勝4・敗2。nodes-250k と nodes-500k に負け） | 1,654（5/6） |
| 平均 | **1,638**（14.5/18） | 1,638（14.5/18） |

1 trial が 6 局なので、半点の違いで Elo が 100〜200 動く。18 局では ±50 Elo 程度の差は見分けられない（017 の記録と同じ）。採用判断の主な材料は 038 の直接対戦（200 局で 56.25%）になる。

## 最悪局面の CPU 時間
| 計測 | C3 | engine-v3 |
|---|---|---|
| 今回の practice trial 3 本の 1 手最大 CPU（`process_time`、load 3〜5） | **1.57 s**（pt2 の 209 手目） | 0.51 s |
| 1 手平均 CPU | 0.29〜0.30 s | 0.14〜0.15 s |
| 既測（038 の直接対戦、load 15〜27） | 4.51 s | 1.47 s |

- 今回は低負荷で計測したため、最大値は 038 の 4.51 s より小さい。038 では、同じ手を低負荷で再生すると 2.18 s だった。本番の上限の目安としては、高負荷で測った 4.51 s を使い続けるのが安全
- 同じ条件で比べると、C3 の CPU 時間は v3 の約 2〜3 倍（最大 3.1 倍、平均 2.0 倍）

## 計測方法（engine-v3 と同じ）
- ランナー: `~/dev/makefun-tiny-chess-work/run_trial.py`（ticket 021 で v3 の 1,809 / 1,451 / 1,654 を出したもの）。キットの env サーバー（`program/env/server.mjs`）とキットのスコアラー（`program/scorer/score.mjs`）を使う。表の Elo はスコアラーの出力（`elo NNNN`）
- trial: `~/dev/makefun-tiny-chess-work/trials/pt0..pt2`。キットの `practice/trial-0..2` のコピーで、違いは `move_limit_ms` を 10000 から 600000 に上げた点だけ（Mac の負荷で時間切れ負けが出ないようにするため。021 と同じ）
- エンジン: `git show b3d7f39:main.py` をそのまま実行した。CPU 時間を測るため `.pt043/cpuwrap.py` で包んでいる。ラッパーは `urllib.request.urlopen` に時刻の記録を足すだけで、エンジンのコードは変えていない
- 3 本を並列で実行した（ポートは別）。ノード数で探索を打ち切り、時計は使わないので、並列にしても指し手は変わらない
- 方法が再現できるかの確認: 同じランナー・同じラッパーで engine-v3（58bb1ce の main.py）を 3 本回した。Elo は 1,809 / 1,451 / 1,654 で、`moves.json` も 021 の h2 の記録（`t021/runs/h2-pt0a`、`h2-pt1`、`h2-pt2`）とバイト単位で一致した
- 決定性: C3 の pt0 を 2 回実行し、`moves.json` が一致した（`cmp`）

## キットの level
- ローカルのキット（`~/dev/makefun-tiny-chess-work/kit/tiny-chess-01-kit`）の CLI は `KIT_LEVEL = 19`（`cli/makefun.mjs`）
- サイト側の level（指示書では 20）は確認していない。make.fun には接続していない。ずれている可能性はあるが、practice trial は手元の env とスコアラーだけで完結するので、今回の Elo には影響しない。ただし、サイト側でスコアの付け方や gauntlet が変わっていても、それは今回の結果に反映されていない

## 前提とのずれ
- 指示書には「C3 は verify-c3-fullbudget ブランチの main.py」とあるが、このブランチには `RESULTS-038.md` しかない。b3d7f39 の実体はブランチ `engine-v4-exp` にある。今回はコミット b3d7f39 を直接使った（038 が使ったものと同じ）
- ローカルの node は v22.18.0、キットの `harness_version` は node v26.13.1。v3 の指し手が 021 の記録と完全に一致したので、結果への影響はないと判断した

## ファイル
- コミットしたもの: `RESULTS-043.md`、`.pt043/cpuwrap.py`、`.pt043/run.sh`（C3 の 3 本）、`.pt043/run2.sh`（C3 pt0 の再実行と v3 の 3 本）
- コミットしていないもの（worktree の `.pt043/`）: `runs/{c3,v3}-pt*/`（summary.txt、games.log、moves.json、state、scores）、`cpu-*.tsv`（1 手ごとの CPU）、`log-*.txt`、`progress*.txt`、`c3-main.py` と `v3-main.py`（git show で取り出したコピー）
- 提出・バンドル作成・マージはしていない。engine-v3 と engine-v4-exp には触れていない。資格情報ファイルも読んでいない
