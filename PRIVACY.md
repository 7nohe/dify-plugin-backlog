# dify-plugin-backlog Privacy Policy

Last updated: 2025-09-06 / Version: 0.0.1

This privacy policy explains how the Dify v1 tool plugin "dify-plugin-backlog" ("the Plugin") handles information and describes its usage and protection practices. The Plugin connects to the Backlog (Nulab) REST API and offers the following capabilities:

- Project listing (GET /api/v2/projects)
- Issue listing (GET /api/v2/issues)
- Issue creation (POST /api/v2/issues)
- Comment creation (POST /api/v2/issues/{issueIdOrKey}/comments)
- Priority listing (GET /api/v2/priorities)
- Issue type listing (GET /api/v2/projects/{projectIdOrKey}/issueTypes)

## Scope
This policy applies to the data processed while the Plugin is running (provider credential entry in Dify, tool inputs, API requests and responses to Backlog, and execution logs). Data processing, retention, or policies of the Dify platform itself and of Backlog are governed by their respective providers.

## Information We Collect and Use
- Provider credentials
  - SPACE_DOMAIN (e.g. yourspace.backlog.jp)
  - API_KEY (Backlog API key generated under Personal Settings -> API)
  - These values are entered on Dify's plugin authentication screen and stored securely by Dify. The Plugin receives them only at runtime and uses them exclusively for Backlog API calls.
- Tool input parameters
  - Values entered by users, such as project and issue filters, issue summaries/descriptions/due dates, and comment bodies.
  - Each input is used only to build Backlog API requests.
- API requests and responses
  - The Plugin communicates with Backlog over HTTPS, exchanging only the minimum data necessary to fulfill user actions.
  - Responses are transformed so that only the required fields (e.g. projectKey, issueKey, summary, status, assignee) are returned to Dify in both JSON and human-readable summaries.

The Plugin does not collect, analyze, or track personal data for any other purpose. If your inputs include personal or confidential information, limit them to what is necessary and follow your organization's security policies.

## Recipients (Third-party Disclosure)
Data is transmitted solely to the Backlog space domain specified by the user (e.g. https://yourspace.backlog.jp). No data is sent to the developers or any other third-party services.

## Data Storage and Retention
- The Plugin itself does not persist credentials, tool inputs, or API responses.
- Credentials (SPACE_DOMAIN, API_KEY) are stored and managed by the Dify platform, subject to Dify's retention, encryption, and access control policies.
- Data handled during execution is processed in memory; the Plugin does not write files or perform custom persistence.

## Logging and Audit
- The Plugin does not emit telemetry to external services and avoids excessive standard output logging.
- However, Dify's runtime logging or audit features may record invocation metadata and error messages. To avoid sensitive information appearing in logs, refrain from including credentials or confidential content in tool inputs or comments.

## Safeguards
- All communication uses HTTPS (TLS).
- Credentials are attached to API requests in minimal form, and the implementation avoids logging them even on errors.
- When a 429 (Too Many Requests) response is received, the Plugin retries with exponential backoff without collecting or storing additional data.

## Data Location
Data resides in the following environments:
- Backlog: on the Backlog infrastructure operated by Nulab for the customer's organization.
- Dify: depends on your deployment (self-hosted or Dify Cloud). For Dify Cloud, data handling follows the provider's region and policies.

## User Responsibilities and Recommendations
- Issue API keys with the least privileges required, and manage regular rotation and revocation.
- Avoid putting unnecessary personal or confidential information in issue titles, descriptions, or comments.
- If you no longer need the Plugin, disable or remove it from Dify and revoke the associated Backlog API key.

## Policy Changes
This policy may be updated without prior notice for improvements. Significant changes will be communicated via the repository's changelog or commit history.

## Contact
For privacy-related questions about the Plugin, please open an issue in the repository. If your organization has legal or security requirements, review the policies of both Dify and Backlog alongside this document.
