# rhino_gh

Rhino 8 / Grasshopper Python 3.9 用の Python ツール群です。

## 目的

Grasshopper 側の Python Script ノードには runner としての薄い呼び出しコードだけを書き、実処理はこのリポジトリ内の Python モジュールから呼び出します。

## 使い方

Grasshopper 側は runner として使い、`gh_loader.run_command(command)` を呼び出します。最小コード例は [`docs/grasshopper_runner.md`](docs/grasshopper_runner.md) を参照してください。

## ツール追加の運用

新しい処理は `tools/*.py` に追加します。各 tool は必ず次の関数を持ちます。

```python
def run(inputs, logger):
    ...
```

`logger` に書いた内容は Grasshopper の `log` として返ります。外部 pip ライブラリは使わず、Rhino 8 / Grasshopper Python 3.9 の標準環境で動く実装にします。

## command Panel 入力例

```text
test_line length=1000 count=5
```

先頭語 `test_line` が `tools/test_line.py` に対応し、後続の `key=value` が `inputs` として渡されます。

## 更新運用

このリポジトリを更新したら `git pull` し、Grasshopper で Python Script ノードを再実行します。
