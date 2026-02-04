# dify-plugin-backlog (Dify Plugin for Backlog)

## Overview
This package exposes the Backlog (Nulab) API as a tool-type plugin for Dify v1. With API Key authentication, it supports fetching projects/issues, creating issues, and adding comments.

## Features
- Backlog API Key authentication (generated from Personal Settings -> API)
- Seven tools included:
  - List Projects: `GET /api/v2/projects`
  - List Issues: `GET /api/v2/issues` (pagination via count/offset)
  - Get Issue: `GET /api/v2/issues/{issueIdOrKey}`
  - Create Issue: `POST /api/v2/issues`
  - Add Comment: `POST /api/v2/issues/{issueIdOrKey}/comments`
  - List Priorities: `GET /api/v2/priorities`
  - List Issue Types: `GET /api/v2/projects/{projectIdOrKey}/issueTypes`
- Uses `requests` with exponential backoff retries on `429 Too Many Requests`
- Works with Dify v1 (runner=python 3.12)
- Each tool returns structured JSON plus a human-readable summary

## Requirements
- Python 3.12
- Dify environment with plugin v1 support
- Backlog API Key
- Space domain examples: `yourspace.backlog.jp` / `yourspace.backlog.com` / `yourspace.backlogtool.com`

## Setup
Development and verification tasks are provided in the Makefile.

```bash
make venv
make fmt lint test
```

## Debugging

.env

```
INSTALL_METHOD=remote
REMOTE_INSTALL_URL=debug.dify.ai:5003
REMOTE_INSTALL_KEY=<your-debug-key>
```

Install the plugin in Dify and run from the Tools screen.

```
.venv/bin/activate # for bash/zsh
.venv/bin/activate.fish # for fish shell
python3 main.py
```

## Packaging
Generate `.difypkg` with the Dify plugin CLI.

```bash
# Example if dify CLI is installed
dify plugin package ./

# Makefile helper target (documentation only)
make package
```

Upload the generated `.difypkg` from Dify -> Plugins -> Install from local file.

## Parameter Naming
- Tool parameters must match the YAML-defined camelCase names (e.g. `issueIdOrKey`, `projectId`, `assigneeId`, `statusId`, `projectIdOrKey`).
- No aliases or nested key resolution is performed. Pass the YAML names from workflows.

## How to Use in Dify
1. Install the plugin by uploading the `.difypkg` file
2. Configure the provider credentials (Backlog Provider)
   - `SPACE_DOMAIN`: e.g. `yourspace.backlog.jp` (no scheme)
   - `API_KEY`: Backlog API key
3. Select the needed tools in Workflow or Agent

### Tools
- **List Projects** (`tools/list_projects.py`)
  - Input: `archived` (bool), `all` (bool)
  - Output: `{ "projects": [...] }` and a text list
- **List Issues** (`tools/list_issues.py`)
  - Input: `projectId` (int[]), `assigneeId` (int[]), `statusId` (int[]), `keyword` (str), `count` (1..100)
  - Note: Paginates via `count`/`offset` to return all items
  - Output: `{ "issues": [...] }` and a text summary (max 20 items)
- **Get Issue** (`tools/get_issue.py`)
  - Input: `issueIdOrKey` (required)
  - Output: `{ "issue": { id, issueKey, summary, url, ... } }`
- **Create Issue** (`tools/create_issue.py`)
  - Input: `projectId` (required), `summary` (required), `issueTypeId` (required), `priorityId` (required), `description`, `assigneeId`, `dueDate (YYYY-MM-DD)`
  - Output: `{ "issue": { id, issueKey, summary, url } }`
- **Add Comment** (`tools/add_comment.py`)
  - Input: `issueIdOrKey` (required), `content` (required)
  - Output: `{ "commentId": number, "created": ISO8601 }`
- **List Priorities** (`tools/list_priorities.py`)
  - Input: none
  - Output: `{ "priorities": [...] }`
- **List Issue Types** (`tools/list_issue_types.py`)
  - Input: `projectIdOrKey` (required)
  - Output: `{ "issueTypes": [...] }`
  - Note: If provider `DEFAULT_PROJECT` is set, it is used when input is empty

## Error Handling
- HTTP errors are delegated to `response.raise_for_status()`
- `429 Too Many Requests` uses exponential backoff (2^n seconds)
- Common errors:
  - 401/403: invalid API key or insufficient permissions
  - 404: wrong domain, project, or issue key
  - 400: missing required parameters or invalid formats

## Security Notes
- Credentials (`SPACE_DOMAIN`, `API_KEY`) are stored securely by Dify and used only at runtime
- The plugin avoids logging sensitive data
- Use least-privilege API keys whenever possible

## Project Structure
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
  ├─ get_issue.yaml     / get_issue.py
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

## Development Tasks
```bash
make fmt
make lint
make test
```

## Notes
- `SPACE_DOMAIN` must not include a scheme (https://)
- List Issues fetches all items with paging (max 100 per page)
- Backlog array params use `k[]=v` format (requests expands list values)
- All parameters use YAML camelCase names

## Acceptance Criteria
- `make venv && make test` succeeds
- `dify plugin package ./` can generate `.difypkg`
- Provider authentication passes and all tools run in the Dify UI
- List Issues can page beyond 100 items
- Create Issue returns `https://{SPACE_DOMAIN}/view/{ISSUE_KEY}`

## Changelog
- 0.0.3: Update Dify Plugin SDK version (dify_plugin 0.7.1 range)
- 0.0.2: Update Dify Plugin SDK version
- 0.0.1: Initial release

## License
MIT License. See `LICENSE` for details.

## Code of Conduct
Contributor Covenant v2.1. See `CODE_OF_CONDUCT.md`. Please do not include sensitive information in reports.

## See Also
- Backlog API v2 documentation (Nulab)
- Dify plugin development guide
