# dify-plugin-backlog Privacy Policy

[日本語](#日本語) | [English](#english)

## 日本語

### プライバシーポリシー（dify-plugin-backlog）

最終更新日: 2025-09-06 / バージョン: 0.0.1

本プライバシーポリシーは、Dify v1 ツール型プラグイン「dify-plugin-backlog」（以下「本プラグイン」）において取り扱う情報と、その利用・保護方針を示します。本プラグインは Backlog（Nulab）の REST API を利用して、以下の機能を提供します。

- プロジェクト一覧取得（GET /api/v2/projects）
- 課題一覧取得（GET /api/v2/issues）
- 課題作成（POST /api/v2/issues）
- コメント追加（POST /api/v2/issues/{issueIdOrKey}/comments）
- 優先度一覧取得（GET /api/v2/priorities）
- 課題種別一覧取得（GET /api/v2/projects/{projectIdOrKey}/issueTypes）

### 対象範囲
本ポリシーは、本プラグインの実行時に取り扱われるデータ（Dify の認証情報入力、ツール入力、Backlog への API リクエスト/レスポンス、実行ログ）に適用されます。Dify プラットフォーム自体のデータ処理や保持、Backlog サービス側のポリシーは各提供者の規約・ポリシーに従います。

### 収集・利用する情報
- 認証情報（プロバイダ資格情報）
  - SPACE_DOMAIN（例: yourspace.backlog.jp）
  - API_KEY（Backlog の個人設定で発行された API キー）
  - これらは Dify のプラグイン認証設定画面で入力され、Dify 側に安全に保管されます。本プラグインは実行時に Dify から受け取り、Backlog API 呼び出しのみに使用します。
- ツール入力パラメータ
  - プロジェクト/課題の検索条件、課題のタイトル・説明・期限、コメント本文など、ユーザーが入力する値。
  - 各入力は Backlog API へのリクエスト生成のためにのみ利用されます。
- API リクエスト/レスポンス
  - 本プラグインは HTTPS 経由で Backlog API と通信し、ユーザーが要求した操作に必要な最小限のデータを送受信します。
  - レスポンスからは、Dify に返却するために必要なフィールド（例: projectKey, issueKey, summary, status, assignee など）のみを整形して JSON とテキストの両形式で出力します。

本プラグインは、上記以外の目的で個人情報を収集・分析・追跡しません。入力内容に個人情報や機密情報を含める場合は、必要最小限とし、組織の情報セキュリティ方針に従って取り扱ってください。

### 送信先（第三者提供）
本プラグインがデータを送信する相手は、ユーザーが指定した Backlog のスペースドメイン配下（例: https://yourspace.backlog.jp）に限定されます。開発者や第三者サービスへの送信は行いません。

### データの保存・保持
- 本プラグイン自身は、認証情報やツール入力、API レスポンスの永続的な保存を行いません。
- 認証情報（SPACE_DOMAIN, API_KEY）は Dify プラットフォーム側で保管・管理されます。保持ポリシー・暗号化・アクセス制御は Dify の仕様に準拠します。
- 実行時に扱うデータはメモリ上で処理され、プラグイン側でファイル出力や独自の永続化は行いません。

### ログ・監査
- 本プラグインは外部へのテレメトリ送信を行わず、標準出力への過度なログ出力を行いません。
- ただし、Dify プラットフォームの実行ログや監査機能により、呼び出しのメタ情報やエラーメッセージが保存される場合があります。ログに機密情報が含まれないよう、ツール入力やコメント本文に認証情報や秘匿情報を記載しない運用を推奨します。

### 安全管理措置
- 通信は HTTPS（TLS）で実施します。
- 認証情報は API リクエストのクエリ/ボディに最小限の形で付与し、エラー時も認証情報をログに出力しない実装としています。
- 429（Too Many Requests）時は指数バックオフで再試行しますが、再試行により追加情報を収集・保存することはありません。

### データ所在
データの所在は以下の通りです。
- Backlog 側: ユーザー組織が契約する Backlog インフラ上（Nulab 社）。
- Dify 側: 利用形態（セルフホスト/クラウド）に依存します。Dify Cloud を利用する場合は、その提供リージョンやポリシーに従います。

### ユーザーの責任と推奨事項
- API キーは最小権限で発行・管理し、定期的なローテーションと失効運用を行ってください。
- チケットのタイトル/説明/コメントには、不要な個人情報や秘匿情報を含めないでください。
- プラグインを不要と判断した場合は、Dify から本プラグインを無効化/削除し、Backlog 側の API キーも失効させてください。

### ポリシーの変更
本ポリシーは改善のため予告なく更新される場合があります。重要な変更がある場合は、リポジトリの変更履歴（CHANGELOG/コミット履歴）等で周知します。

### お問い合わせ
本プラグインのプライバシーに関するご質問は、リポジトリの Issue でお知らせください。組織の法務・セキュリティ要件がある場合は、Dify と Backlog の各提供者のポリシーも併せてご確認ください。

---

## English

### Privacy Policy (dify-plugin-backlog)

Last updated: 2025-09-06 / Version: 0.0.1

This privacy policy explains how the Dify v1 tool plugin “dify-plugin-backlog” ("the Plugin") handles information, and describes its usage and protection practices. The Plugin connects to the Backlog (Nulab) REST API and offers the following capabilities:

- Project listing (GET /api/v2/projects)
- Issue listing (GET /api/v2/issues)
- Issue creation (POST /api/v2/issues)
- Comment creation (POST /api/v2/issues/{issueIdOrKey}/comments)
- Priority listing (GET /api/v2/priorities)
- Issue type listing (GET /api/v2/projects/{projectIdOrKey}/issueTypes)

### Scope
This policy applies to the data processed while the Plugin is running (provider credential entry in Dify, tool inputs, API requests/responses to Backlog, and execution logs). Data processing, retention, or policies of the Dify platform itself and of Backlog are governed by their respective providers.

### Information We Collect and Use
- Provider credentials
  - SPACE_DOMAIN (e.g., yourspace.backlog.jp)
  - API_KEY (Backlog API key generated under Personal Settings → API)
  - These values are entered on Dify’s plugin authentication screen and stored securely by Dify. The Plugin receives them only at runtime and uses them exclusively for Backlog API calls.
- Tool input parameters
  - Values entered by users, such as project/issue filters, issue summaries/descriptions/due dates, and comment bodies.
  - Each input is used only to build Backlog API requests.
- API requests and responses
  - The Plugin communicates with Backlog over HTTPS, exchanging only the minimum data necessary to fulfill user actions.
  - Responses are transformed so that only the required fields (e.g., projectKey, issueKey, summary, status, assignee) are returned to Dify in both JSON and human-readable summaries.

The Plugin does not collect, analyze, or track personal data for any other purpose. If your inputs include personal or confidential information, limit them to what is necessary and follow your organization’s security policies.

### Recipients (Third-party Disclosure)
Data is transmitted solely to the Backlog space domain specified by the user (e.g., https://yourspace.backlog.jp). No data is sent to the developers or any other third-party services.

### Data Storage and Retention
- The Plugin itself does not persist credentials, tool inputs, or API responses.
- Credentials (SPACE_DOMAIN, API_KEY) are stored and managed by the Dify platform, subject to Dify’s retention, encryption, and access control policies.
- Data handled during execution is processed in memory; the Plugin does not write files or perform custom persistence.

### Logging and Audit
- The Plugin does not emit telemetry to external services and avoids excessive standard output logging.
- However, Dify’s runtime logging or audit features may record invocation metadata and error messages. To avoid sensitive information appearing in logs, refrain from including credentials or confidential content in tool inputs or comments.

### Safeguards
- All communication uses HTTPS (TLS).
- Credentials are attached to API requests in minimal form, and the implementation avoids logging them even on errors.
- When a 429 (Too Many Requests) response is received, the Plugin retries with exponential backoff without collecting or storing additional data.

### Data Location
Data resides in the following environments:
- Backlog: on the Backlog infrastructure operated by Nulab for the customer’s organization.
- Dify: depends on your deployment (self-hosted or Dify Cloud). For Dify Cloud, data handling follows the provider’s region and policies.

### User Responsibilities and Recommendations
- Issue API keys with the least privileges required, and manage regular rotation and revocation.
- Avoid putting unnecessary personal or confidential information in issue titles, descriptions, or comments.
- If you no longer need the Plugin, disable or remove it from Dify and revoke the associated Backlog API key.

### Policy Changes
This policy may be updated without prior notice for improvements. Significant changes will be communicated via the repository’s changelog or commit history.

### Contact
For privacy-related questions about the Plugin, please open an issue in the repository. If your organization has legal or security requirements, review the policies of both Dify and Backlog alongside this document.
