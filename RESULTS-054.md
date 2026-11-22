---
ticket: 054
status: stopped_at_step_1
at: 2026-11-22 JST
---

# 054 結果: D1 提出 — 手順1で停止（未提出）

- 提出: **未実施**。submission id・ステータスなし。現行の有効提出は保険の engine-v3（提出1件目）のまま。
- 止まった手順: **1（kit 再取得・level 照合）**
- kit check: 未実行（手順3に到達していない）。fail 項目名: なし（未実行）

## 手順1の結果

最新 kit を `https://make.fun/c/tiny-chess-01/kit` から再取得した（HTTP 200、9,293,091 バイト、CLI ソースが使う配布 URL と同じ）。

| 照合対象 | kit 側 | サイト側 |
|---|---|---|
| level | **フィールドなし**（kit.json・competition.yaml に `level` が1件もない） | **フィールドなし**（`/api/competitions/tiny-chess-01` と `/api/competitions/tiny-chess-01/kit` に `level` が1件もない） |

指示書の「kit の level がサイトの level と一致すること」を確認できないため、ここで止めた。
代わりの項目（phase や bundle_sha256）で照合するのは手順の変更にあたるので、判定には使っていない。参考値だけ記録する:

- phase: kit `dev` / サイト kit API `dev`
- bundle_sha256: kit `86e0db42…055b4` / サイト `bundleSha256` `86e0db42…055b4`（一致）
- 手元の旧 kit（2026-11-17 取得）からの変化: harness_version、scorer_version、pricing_rev が変わっている（bundle_sha256 と program は同じ）。kit.json の sha256 は旧 `b424dada…` → 新 `8a88a14d…`

## 手順2以降で止まる見込みの点（読み取りだけで確認、変更はしていない）

1. **origin/maint/chess-pdca-r2-051 にルートの main.py がない**。D1 の実体は `.r051/d1-main.py`（3,537 バイト、4KB 未満）。指示書の「…の main.py を取り出す」とパスが合わない。
2. **署名・認証の素材が ~/.makefun にない**。中身は `compress.json` だけで、`credentials` も `keypairs/` もない。`$MAKEFUN_API_KEY` も未設定。`submit` は API キー（register/login で保存されるもの）が要るので、このままでは手順4で失敗する。
3. 指示書の「kit check」「run-record --prompt-origin」は、CLI ではそれぞれ `makefun check` と `makefun bundle … --prompt-origin handed-off` にあたる。名前の対応だけで、手順の中身は変わらない。

## DECIDE で決めてほしいこと

- 手順1の照合を何で行うか（例: bundle_sha256 の一致でよいか）
- 手順2の取り出し元を `.r051/d1-main.py` としてよいか
- 手順4の認証: `makefun login` で本人のアカウントに接続する（本人のブラウザ承認が要る）か、別の鍵素材の場所を指示するか
