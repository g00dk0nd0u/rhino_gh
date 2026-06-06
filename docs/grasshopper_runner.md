# Grasshopper Python Script runner

Rhino 8 / Grasshopper の Python Script ノードには、実処理を書かずに以下のような最小コードだけを貼ります。

```python
import sys

repo_path = r"C:\path\to\rhino_gh"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

import gh_loader

result, log = gh_loader.run_command(command)
```

## ノード入出力

- 入力 `command`: Panel などから渡すコマンド文字列
- 出力 `result`: tool が返す Rhino / Grasshopper 用データ
- 出力 `log`: 実行ログ。成功時も失敗時も返ります。

入力例:

```text
test_line length=1000 count=5
```
