# dify-plugin-backlog (Dify Plugin for Backlog)

[日本語](#日本語) | [English](#english)

## 日本語

### 概要
Backlog (Nulab) の API を Dify v1 の「ツール型」プラグインとして利用できるようにするパッケージです。API Key 認証を用い、プロジェクトや課題の取得、課題の作成、コメント追加をサポートします。

### 特長 / Features
- Backlog API Key 認証（個人設定 → API で発行）
- 6 つのツールを提供：
  - List Projects: `GET /api/v2/projects`
  - List Issues: `GET /api/v2/issues`（count/offset でページング）
  - Create Issue: `POST /api/v2/issues`
  - Add Comment: `POST /api/v2/issues/{issueIdOrKey}/comments`
  - List Priorities: `GET /api/v2/priorities`
  - List Issue Types: `GET /api/v2/projects/{projectIdOrKey}/issueTypes`
- HTTP クライアントには `requests` を使用し、`429 Too Many Requests` を指数バックオフでリトライ
- Dify v1（runner=python 3.12）対応
- すべてのツールで JSON 出力に加えて、人間向けのテキスト要約も提供

### 必要要件 / Requirements
- Python 3.12
- Dify（プラグイン v1 対応環境）
- Backlog API Key
- Space ドメイン（例）: `yourspace.backlog.jp` / `yourspace.backlog.com` / `yourspace.backlogtool.com`

### インストール / Setup
開発・検証用の仮想環境と基本タスクは `Makefile` で提供しています。

```bash
make venv
make fmt lint test
```

### デバッグ

.env

```
INSTALL_METHOD=remote
REMOTE_INSTALL_URL=debug.dify.ai:5003
REMOTE_INSTALL_KEY=<your-debug-key>
```

プラグインを Dify にインストールし、「ツール」から選択して実行します。

```
.venv/bin/activate # for bash/zsh
.venv/bin/activate.fish # for fish shell
python3 main.py
```

### パッケージング / Packaging
`.difypkg` は Dify のプラグイン CLI で生成します。

```bash
# dify CLI が導入済みの場合の例
dify plugin package ./

# Makefile の補助ターゲット（案内のみ）
make package
```

生成された `.difypkg` は Dify の「プラグイン」画面 → 「プラグインをインストール」→「ローカルファイルから」でインストールします。

### パラメータ命名 / Parameter Naming
- ツールのパラメータは YAML に定義した camelCase 名に厳密に従います（例: `issueIdOrKey`, `projectId`, `assigneeId`, `statusId`, `projectIdOrKey`）。
- エイリアス（別名）や入れ子キーによる解決は行いません。ワークフローからは YAML 名で渡してください。

### Dify での利用手順 / How to Use
1. プラグインをインストール（`.difypkg` をアップロード）
2. Provider 認証を設定（Backlog Provider）
   - `SPACE_DOMAIN`: 例 `yourspace.backlog.jp`（https:// を付けない）
   - `API_KEY`: Backlog の API キー
3. Workflow / Agent の「ツール」から必要なツールを選択

#### ツール一覧
- **List Projects** (`tools/list_projects.py`)
  - 入力: `archived` (bool), `all` (bool)
  - 出力: `{ "projects": [...] }` とテキスト一覧
- **List Issues** (`tools/list_issues.py`)
  - 入力: `projectId` (int[]), `assigneeId` (int[]), `statusId` (int[]), `keyword` (str), `count` (1..100)
  - 備考: `count`/`offset` でページングし全件返却
  - 出力: `{ "issues": [...] }` とテキスト要約（最大 20 件）
- **Create Issue** (`tools/create_issue.py`)
  - 入力: `projectId` (必須), `summary` (必須), `issueTypeId` (必須), `priorityId` (必須), `description`, `assigneeId`, `dueDate (YYYY-MM-DD)`
  - 出力: `{ "issue": { id, issueKey, summary, url } }`
- **Add Comment** (`tools/add_comment.py`)
  - 入力: `issueIdOrKey` (必須), `content` (必須)
  - 出力: `{ "commentId": number, "created": ISO8601 }`
- **List Priorities** (`tools/list_priorities.py`)
  - 入力: なし
  - 出力: `{ "priorities": [...] }`
- **List Issue Types** (`tools/list_issue_types.py`)
  - 入力: `projectIdOrKey` (必須)
  - 出力: `{ "issueTypes": [...] }`
  - 備考: Provider の `DEFAULT_PROJECT` を設定しておくと入力が空でも既定値を使用

### エラーハンドリング / Error Handling
- HTTP エラーは `response.raise_for_status()` に委譲
- `429 Too Many Requests` は指数バックオフ（2^n 秒）でリトライ
- よくあるエラー:
  - 401/403: API キー不正または権限不足
  - 404: ドメイン/プロジェクト/課題キーの誤り
  - 400: 必須パラメータ不足や形式不正

### セキュリティ / Security Notes
- 認証情報（`SPACE_DOMAIN`, `API_KEY`）は Dify 側で安全に保管され、実行時にのみ利用
- ログへ機密情報を出力しない方針
- 可能な限り最小権限の API キーを使用

### ディレクトリ構成 / Project Structure
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

### 開発タスク / Development Tasks
```bash
make fmt
make lint
make test
```

### 既知の注意点 / Notes
- `SPACE_DOMAIN` にはスキーム（https://）を含めない
- List Issues は最大 100 件/ページで全件取得
- Backlog の配列クエリは `k[]=v` 形式（`requests` は list を渡すと自動展開）
- すべてのパラメータは YAML の camelCase 名を使用

### 受け入れ基準 / Acceptance Criteria
- `make venv && make test` が成功する
- `dify plugin package ./` で `.difypkg` を生成できる
- Dify 上で Provider 認証設定が通り、6 ツールが UI から実行可能
- List Issues で 100 件超をページング取得できる
- Create Issue 実行後に `https://{SPACE_DOMAIN}/view/{ISSUE_KEY}` を返す

### 変更履歴 / Changelog
- 0.0.1: 初版

### ライセンス / License
MIT License。詳細は `LICENSE` を参照してください。

### 行動規範 / Code of Conduct
Contributor Covenant v2.1 に準拠。詳細は `CODE_OF_CONDUCT.md` を参照し、懸念点は Issue へ（機微情報は含めないでください）。

### 関連 / See Also
- Backlog API v2 ドキュメント（Nulab）
- Dify プラグイン開発ガイド

---

## English

### Overview
This package exposes the Backlog (Nulab) API as a tool-type plugin for Dify v1. With API Key authentication, it supports fetching projects/issues, creating issues, and adding comments.

### Features
- Backlog API Key authentication (generated from Personal Settings → API)
- Six tools included:
  - List Projects: `GET /api/v2/projects`
  - List Issues: `GET /api/v2/issues` (pagination via count/offset)
  - Create Issue: `POST /api/v2/issues`
  - Add Comment: `POST /api/v2/issues/{issueIdOrKey}/comments`
  - List Priorities: `GET /api/v2/priorities`
  - List Issue Types: `GET /api/v2/projects/{projectIdOrKey}/issueTypes`
- Uses `requests` with exponential backoff retries on `429 Too Many Requests`
- Works with Dify v1 (runner=python 3.12)
- Each tool returns structured JSON plus a human-readable summary

### Requirements
- Python 3.12
- Dify environment with plugin v1 support
- Backlog API Key
- Space domain (e.g. `yourspace.backlog.jp` / `.com` / `.backlogtool.com`)

### Setup
A virtual environment and common tasks are provided via `Makefile`.

```bash
make venv
make fmt lint test
```

### Debugging

.env

```
INSTALL_METHOD=remote
REMOTE_INSTALL_URL=debug.dify.ai:5003
REMOTE_INSTALL_KEY=<your-debug-key>
```

The plugin can be installed in Dify and executed from "Tools".

```
.venv/bin/activate # for bash/zsh
.venv/bin/activate.fish # for fish shell
python3 main.py
```

### Packaging
Generate a `.difypkg` using the Dify plugin CLI.

```bash
# Example when dify CLI is installed
dify plugin package ./

# Makefile helper (informational)
make package
```

Import the generated `.difypkg` from Dify → Plugins → Install Plugin → From Local File.

### Parameter Naming
- Tool parameters strictly follow the camelCase names defined in YAML (e.g., `issueIdOrKey`, `projectId`, `assigneeId`, `statusId`, `projectIdOrKey`).
- No aliases or nested keys are resolved; workflows must provide the YAML names directly.

### How to Use in Dify
1. Install the plugin (upload the `.difypkg`).
2. Configure the Backlog Provider credentials:
   - `SPACE_DOMAIN`: e.g. `yourspace.backlog.jp` (without `https://`)
   - `API_KEY`: Backlog API key
3. Select any of the tools from Workflow/Agent.

#### Tool Details
- **List Projects** (`tools/list_projects.py`)
  - Inputs: `archived` (bool), `all` (bool)
  - Outputs: `{ "projects": [...] }` plus a text summary
- **List Issues** (`tools/list_issues.py`)
  - Inputs: `projectId` (int[]), `assigneeId` (int[]), `statusId` (int[]), `keyword` (str), `count` (1..100)
  - Notes: paginates via `count`/`offset`, returns all results
  - Outputs: `{ "issues": [...] }` plus textual summary (max 20 items)
- **Create Issue** (`tools/create_issue.py`)
  - Inputs: `projectId` (required), `summary` (required), `issueTypeId` (required), `priorityId` (required), `description`, `assigneeId`, `dueDate (YYYY-MM-DD)`
  - Output: `{ "issue": { id, issueKey, summary, url } }`
- **Add Comment** (`tools/add_comment.py`)
  - Inputs: `issueIdOrKey` (required), `content` (required)
  - Output: `{ "commentId": number, "created": ISO8601 }`
- **List Priorities** (`tools/list_priorities.py`)
  - Inputs: none
  - Output: `{ "priorities": [...] }`
- **List Issue Types** (`tools/list_issue_types.py`)
  - Input: `projectIdOrKey` (required)
  - Output: `{ "issueTypes": [...] }`
  - Note: if `DEFAULT_PROJECT` is set in Provider config, it is used when the input is empty.

### Error Handling
- Relies on `response.raise_for_status()` for HTTP errors.
- Retries `429 Too Many Requests` with exponential backoff (`2^n` seconds).
- Common errors:
  - 401/403: invalid API key or insufficient permissions
  - 404: wrong domain/project/issue key
  - 400: missing required parameters or invalid format

### Security Notes
- Credentials (`SPACE_DOMAIN`, `API_KEY`) are stored securely by Dify and used only at runtime.
- The implementation avoids logging sensitive data.
- Use the least-privileged API key possible.

### Project Structure
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

### Development Tasks
```bash
make fmt
make lint
make test
```

### Notes
- Do not include the scheme (`https://`) in `SPACE_DOMAIN`.
- List Issues fetches all items by paginating at 100 items per page.
- Backlog array queries use `k[]=v` (handled automatically when passing lists to `requests`).
- Always use the camelCase names from YAML; aliases are not supported.

### Acceptance Criteria
- `make venv && make test` passes locally.
- `dify plugin package ./` produces a `.difypkg`.
- Provider authentication works in Dify UI and all six tools run successfully.
- List Issues retrieves more than 100 items via pagination.
- Create Issue returns `https://{SPACE_DOMAIN}/view/{ISSUE_KEY}`.

### Changelog
- 0.0.1: Initial release.

### License
Released under the MIT License (see `LICENSE`).

### Code of Conduct
Adheres to Contributor Covenant v2.1. See `CODE_OF_CONDUCT.md` and report concerns via Issues (omit sensitive information).

### See Also
- Backlog API v2 Documentation (Nulab)
- Dify Plugin Development Guide
