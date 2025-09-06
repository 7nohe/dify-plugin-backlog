import urllib.parse

import requests

from ._utils import (
    base_url,
    build_params,
    credentials_space_api_key,
    http_get,
    http_post,
    to_int_if_numberish,
)

try:
    from dify_plugin import Tool
except Exception:  # pragma: no cover

    class Tool:
        pass


def invoke(tools_input, credentials, context):
    space, _ = credentials_space_api_key(credentials)
    url = base_url(space) + "/issues"

    payload = {}
    params = build_params(credentials)

    # Some runtimes may nest parameters under an `inputs` key.
    src = tools_input or {}
    nested = src.get("inputs") if isinstance(src.get("inputs"), dict) else {}

    def _get_param(name):
        if name in src and src[name] is not None and src[name] != "":
            return src[name]
        if name in nested and nested[name] is not None and nested[name] != "":
            return nested[name]
        return None
    for k in (
        "projectId",
        "summary",
        "description",
        "issueTypeId",
        "priorityId",
        "assigneeId",
        "dueDate",
    ):
        v = _get_param(k)
        if v is not None:
            if k == "projectId":
                # Accept numeric, numeric-like string, or project key string
                v2 = to_int_if_numberish(v)
                if isinstance(v2, int):
                    payload[k] = v2
                else:
                    # Treat as project key and resolve to ID via API
                    proj_url = base_url(space) + f"/projects/{urllib.parse.quote(str(v2))}"
                    proj = http_get(proj_url, params=params, get_func=requests.get)
                    payload[k] = proj["id"]
            else:
                payload[k] = v

    # Fallback: if projectId still missing, try provider default
    if "projectId" not in payload:
        default_pid = (
            (credentials or {}).get("DEFAULT_PROJECT")
            or (credentials or {}).get("PROJECT_ID")
            or (credentials or {}).get("PROJECT_KEY")
        )
        if default_pid:
            v2 = to_int_if_numberish(default_pid)
            if isinstance(v2, int):
                payload["projectId"] = v2
            else:
                proj_url = base_url(space) + f"/projects/{urllib.parse.quote(str(v2))}"
                proj = http_get(proj_url, params=params, get_func=requests.get)
                payload["projectId"] = proj["id"]

    created = http_post(url, payload, params=params, post_func=requests.post)
    return {
        "issue": {
            "id": created["id"],
            "issueKey": created["issueKey"],
            "summary": created["summary"],
            "url": f"https://{space}/view/{created['issueKey']}",
        }
    }


class CreateIssueTool(Tool):
    def _invoke(self, tool_parameters):
        creds = self.runtime.credentials
        result = invoke(tool_parameters or {}, creds, {})
        # Structured result
        yield self.create_json_message(result)

        # Human-readable text
        issue = (result or {}).get("issue") or {}
        if issue:
            text = (
                f"Created issue {issue.get('issueKey')}: {issue.get('summary')}\n"
                f"{issue.get('url')}"
            )
            yield self.create_text_message(text)
        else:
            yield self.create_text_message("Issue created.")
