# RESULTS-061: D1 提出ツリーの確定

- 提出コミット: `d69a5783be6b58033eff7230bf2c027072f0983a`（LICENSE 修正）
  - 親 `aa42c47` のツリー `dd7a86b` は 057 の `ef77b22` と一致
- main.py: `origin/maint/chess-pdca-r2-051:.r051/d1-main.py` と `cmp` で一致、3,537 バイト、blob `ccd7bac`
- LICENSE の先頭行: `SPDX-License-Identifier: MIT`（その後に空行が1行。blob `79837bb`。news-image `e74523d` の LICENSE と同じ blob）
- サイズ（d69a578 時点）: LICENSE 1,095 / README.md 1,106 / main.py 3,537、合計 5,738 バイト（上限: 8,192、各ファイル 4,096）
- 提出・push はしていない

## 指示書との食い違い
- 「ベースは origin/maint/chess-pdca-r2-051」: そのまま使うと `.r051/` が含まれて上限を超え、057 のツリーとも合わない。そのため 057 と同じく `84c52ee` の上に main.py を置いた
- 「.makefun/owner.json 等」: 057 のツリーには無いので追加していない
- 「ef77b22 未push」: 実際は `origin/maint/chess-submit-d1-057` に push 済み
