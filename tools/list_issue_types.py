import urllib.parse

import requests

from ._utils import base_url, build_params, credentials_space_api_key, http_get

try:
    from dify_plugin import Tool
except Exception:  # pragma: no cover

    class Tool:
        pass


def invoke(tools_input, credentials, context):
    space, _ = credentials_space_api_key(credentials)

    # Strict: rely on YAML-defined parameter only (camelCase)
    pid = (tools_input or {}).get("projectIdOrKey")
    if not pid:
        # fallback to provider credentials default if provided
        pid = (
            (credentials or {}).get("DEFAULT_PROJECT")
            or (credentials or {}).get("PROJECT_ID")
            or (credentials or {}).get("PROJECT_KEY")
        )
    if not pid:
        raise ValueError("projectIdOrKey is required")

    enc = urllib.parse.quote(str(pid))
    url = base_url(space) + f"/projects/{enc}/issueTypes"
    params = build_params(credentials)
    data = http_get(url, params, get_func=requests.get)
    types = [{"id": t["id"], "name": t["name"], "color": t.get("color")} for t in data]
    return {"issueTypes": types}


class ListIssueTypesTool(Tool):
    def _invoke(self, tool_parameters):
        # Optional: minimal debug log for remote install sessions
        try:
            self.create_log_message(f"list_issue_types params: {tool_parameters}")
        except Exception:
            pass
        creds = self.runtime.credentials
        result = invoke(tool_parameters or {}, creds, {})
        # Structured result
        yield self.create_json_message(result)

        # Human-readable text
        types = result.get("issueTypes", [])
        if types:
            lines = [
                "Issue Types:",
                *[
                    (
                        f"- {t.get('id')}: {t.get('name')}"
                        + (f" (color {t.get('color')})" if t.get("color") else "")
                    )
                    for t in types
                ],
            ]
            yield self.create_text_message("\n".join(lines))
        else:
            yield self.create_text_message("No issue types found.")
