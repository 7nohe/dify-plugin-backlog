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

    # Strict: rely on YAML-defined parameter only (top-level)
    issue = (tools_input or {}).get("issueIdOrKey")
    if not issue:
        raise ValueError("issueIdOrKey is required")

    enc = urllib.parse.quote(str(issue))
    url = base_url(space) + f"/issues/{enc}"
    params = build_params(credentials)

    it = http_get(url, params, get_func=requests.get)

    # Normalize selected fields
    issue_detail = {
        "id": it.get("id"),
        "issueKey": it.get("issueKey"),
        "summary": it.get("summary"),
        "description": it.get("description"),
        "status": (it.get("status") or {}).get("name"),
        "priority": (it.get("priority") or {}).get("name"),
        "issueType": (it.get("issueType") or {}).get("name"),
        "assignee": (it.get("assignee") or {}).get("name"),
        "createdUser": (it.get("createdUser") or {}).get("name"),
        "created": it.get("created"),
        "updated": it.get("updated"),
        "startDate": it.get("startDate"),
        "dueDate": it.get("dueDate"),
        "estimatedHours": it.get("estimatedHours"),
        "actualHours": it.get("actualHours"),
        "url": f"https://{space}/view/{it.get('issueKey')}" if it.get("issueKey") else None,
    }

    return {"issue": issue_detail}


class GetIssueTool(Tool):
    def _invoke(self, tool_parameters):
        creds = self.runtime.credentials
        result = invoke(tool_parameters or {}, creds, {})
        # Structured result
        yield self.create_json_message(result)

        # Human-readable text
        it = (result or {}).get("issue") or {}
        if not it:
            yield self.create_text_message("Issue not found.")
            return
        lines = [
            f"{it.get('issueKey')} [{it.get('status')}] {it.get('summary')}",
        ]
        if it.get("assignee"):
            lines.append(f"Assignee: {it.get('assignee')}")
        if it.get("issueType"):
            lines.append(f"Type: {it.get('issueType')}")
        if it.get("description"):
            lines.append(f"Description: {it.get('description')}")
        if it.get("priority"):
            lines.append(f"Priority: {it.get('priority')}")
        if it.get("dueDate") or it.get("startDate"):
            dates = []
            if it.get("startDate"):
                dates.append(f"start {it.get('startDate')}")
            if it.get("dueDate"):
                dates.append(f"due {it.get('dueDate')}")
            lines.append("Dates: " + ", ".join(dates))
        if it.get("url"):
            lines.append(f"URL: {it.get('url')}")
        yield self.create_text_message("\n".join(lines))
