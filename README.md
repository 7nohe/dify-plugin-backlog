# dify-plugin-backlog (Dify Plugin for Backlog)

Backlog (Nulab) の API を、Dify v1 の「ツール型」プラグインとして利用できるようにするパッケージです。API Key 認証で、プロジェクト/課題の取得、課題の作成、コメント追加を行います。

## 特長 / Features
- Backlog API Key 認証（個人設定→API で発行）
- 6 つのツールを提供：
  - List Projects: `GET /api/v2/projects`
  - List Issues: `GET /api/v2/issues`（count/offset でページング）
  - Create Issue: `POST /api/v2/issues`
  - Add Comment: `POST /api/v2/issues/{issueIdOrKey}/comments`
  - List Priorities: `GET /api/v2/priorities`
  - List Issue Types: `GET /api/v2/projects/{projectIdOrKey}/issueTypes`
- HTTP クライアントは `requests` を使用し、`429 Too Many Requests` を指数バックオフで再試行
- Dify v1（runner=python 3.12）対応
- すべてのツールは JSON（構造化）に加えて、人間向けのテキストも出力（一覧/要約）。

## 必要要件 / Requirements
- Python 3.12
- Dify（プラグイン v1 対応環境）
- Backlog API Key
- Space ドメイン（例）: `yourspace.backlog.jp` / `yourspace.backlog.com` / `yourspace.backlogtool.com`

## インストール / Setup
開発・検証用の仮想環境と基本タスクは `Makefile` で提供しています。

```bash
make venv
make fmt lint test
```

## パッケージング / Packaging
`.difypkg` は Dify のプラグイン CLI で生成します。

```bash
# dify CLI が導入済みの場合の例
# 参考: https://github.com/langgenius/dify#plugins （導入方法は環境により異なります）
dify plugin package ./

# Makefile の補助ターゲット（案内のみ）
make package
```

生成された `.difypkg` は、Dify の「プラグイン」画面 → 「プラグインをインストール」→「ローカルファイルから」でインストールします。

## パラメータ命名 / Parameter Naming
- ツールのパラメータは YAML に定義した camelCase 名に厳密に従います（例: `issueIdOrKey`, `projectId`, `assigneeId`, `statusId`, `projectIdOrKey`）。
- エイリアス（別名）や入れ子キー（`inputs`/`parameters` など）による解決は行いません。ワークフローからは YAML 名で渡してください。

## Dify での利用手順 / How to Use in Dify
1) プラグインをインストール（.difypkg をアップロード）
2) Provider 認証を設定（Backlog Provider）
   - `SPACE_DOMAIN`: 例 `yourspace.backlog.jp`（https:// を付けない）
   - `API_KEY`: Backlog の API キー
3) Workflow / Agent の「ツール」から以下のツールを選択し、必要パラメータを入力

### ツール詳細 / Tools
- List Projects（`tools/list_projects.py`）
  - 入力: `archived`(bool), `all`(bool)
  - 出力: `{ "projects": [{ id, projectKey, name }, ...] }` に加えて、人間向けの簡易テキスト一覧も同時に出力

- List Issues（`tools/list_issues.py`）
  - 入力: `projectId`(int[]), `assigneeId`(int[]), `statusId`(int[]), `keyword`(str), `count`(1..100)
  - 備考: `count`/`offset` でページングし、全件をまとめて返却
  - 出力: `{ "issues": [{ id, issueKey, summary, status, assignee, updated }, ...] }` とテキスト要約（最大 20 件表示）

- Create Issue（`tools/create_issue.py`）
  - 入力: `projectId`(必須, ID もしくは projectKey 文字列), `summary`(必須), `issueTypeId`(必須), `priorityId`(必須), `description`, `assigneeId`, `dueDate(YYYY-MM-DD)`
  - 出力: `{ "issue": { id, issueKey, summary, url } }`（url は `https://{SPACE_DOMAIN}/view/{ISSUE_KEY}`）

- Add Comment（`tools/add_comment.py`）
  - 入力: `issueIdOrKey`(必須), `content`(必須)
  - 出力: `{ "commentId": number, "created": ISO8601 }`

- List Priorities（`tools/list_priorities.py`）
  - 入力: なし
  - 出力: `{ "priorities": [{ id, name }, ...] }`

- List Issue Types（`tools/list_issue_types.py`）
  - 入力: `projectIdOrKey`(必須, ID もしくは projectKey 文字列)
  - 出力: `{ "issueTypes": [{ id, name, color }, ...] }`
  - 備考: Provider の `DEFAULT_PROJECT` を設定しておくと、入力が空でもその値を使用します

## エラーハンドリング / Error Handling
- HTTP エラーは `response.raise_for_status()` に委譲（Dify 側のデフォルト処理に従います）
- `429 Too Many Requests` の場合は指数バックオフ（2^n 秒）で所定回数リトライ
- よくあるエラー:
  - 401/403: API キー不正または権限不足
  - 404: ドメイン/プロジェクト/課題キーの誤り
  - 400: 必須パラメータ不足や形式不正

## セキュリティ / Security Notes
- 認証情報（`SPACE_DOMAIN`, `API_KEY`）は Dify 側で安全に保管され、本プラグインは実行時にのみ利用します
- ログへ機密情報を出力しない実装方針
- 可能な限り最小権限の API キーを使用してください

## ディレクトリ構成 / Project Structure
```
manifest.yaml
_assets/
  └─ icon.svg
provider/
  ├─ backlog.yaml
  └─ backlog.py
tools/
  ├─ list_projects.yaml / list_projects.py
  ├─ list_issues.yaml   / list_issues.py
  ├─ create_issue.yaml  / create_issue.py
  ├─ add_comment.yaml   / add_comment.py
  ├─ list_priorities.yaml / list_priorities.py
  └─ list_issue_types.yaml / list_issue_types.py
tests/
  ├─ conftest.py
  ├─ test_list_projects.py
  ├─ test_list_issues.py
  ├─ test_create_issue.py
  ├─ test_add_comment.py
  ├─ test_get_issue.py
  └─ test_list_issues_params.py
Makefile
pyproject.toml
requirements.txt
README.md
PRIVACY.md
```

## 開発タスク / Development Tasks
```bash
# フォーマット / Format
make fmt

# Lint（ruff）
make lint

# テスト（pytest）
make test
```

## 既知の注意点 / Notes
- `SPACE_DOMAIN` にはスキーム（https://）を含めないでください
- List Issues は最大 100 件/ページで全件をループ取得します
- Backlog の配列クエリは `k[]=v` 形式（`requests` は list を渡すと自動展開）
- すべてのパラメータは YAML の camelCase 名を使用してください（別名は非対応）。

## 受け入れ基準 / Acceptance Criteria
- `make venv && make test` がローカルで成功する
- `dify plugin package ./` 実行で `.difypkg` が生成できる
- Dify 上で Provider 認証設定が通り、6 ツールが UI から実行できる
- List Issues で 100 件超をページング取得できる
- Create Issue 実行後に `https://{SPACE_DOMAIN}/view/{ISSUE_KEY}` 形式の URL を返す

## 変更履歴 / Changelog
- 0.0.1: 初版

## ライセンス / License
本リポジトリは MIT License です。詳細は `LICENSE` を参照してください。

## 行動規範 / Code of Conduct
本プロジェクトは Contributor Covenant v2.1 に準拠した行動規範を採用しています。詳細は `CODE_OF_CONDUCT.md` を参照してください。違反や懸念の報告は、本リポジトリの Issue で受け付けます（機微情報は記載しないでください）。

## 関連 / See Also
- Backlog API v2 ドキュメント（Nulab）
- Dify プラグイン開発ガイド
