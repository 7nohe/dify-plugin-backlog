import requests

from ._utils import base_url, build_params, coerce_array, credentials_space_api_key, http_get

try:
    from dify_plugin import Tool
except Exception:  # pragma: no cover

    class Tool:
        pass


def invoke(tools_input, credentials, context):
    space, _ = credentials_space_api_key(credentials)
    url = base_url(space) + "/issues"

    params = build_params(credentials)

    # Backlogは配列クエリに [] を付ける形式
    for k in ("projectId", "assigneeId", "statusId"):
        v = tools_input.get(k)
        if v is not None and v != "":
            arr = coerce_array(v)
            if arr:
                # requests は list を与えると k[]=v&k[]=v... と展開してくれる
                params[f"{k}[]"] = arr

    if tools_input.get("keyword"):
        params["keyword"] = tools_input["keyword"]
    params["count"] = max(1, min(int(tools_input.get("count", 100)), 100))
    params["offset"] = 0

    results = []
    while True:
        data = http_get(url, params, get_func=requests.get)
        results.extend(
            [
                {
                    "id": it["id"],
                    "issueKey": it["issueKey"],
                    "summary": it["summary"],
                    "status": it["status"]["name"],
                    "assignee": (it.get("assignee") or {}).get("name"),
                    "updated": it["updated"],
                }
                for it in data
            ]
        )
        if len(data) < params["count"]:
            break
        params["offset"] += params["count"]

    return {"issues": results}


class ListIssuesTool(Tool):
    def _invoke(self, tool_parameters):
        creds = self.runtime.credentials
        result = invoke(tool_parameters or {}, creds, {})
        # Structured result
        yield self.create_json_message(result)

        # Human-readable text summary
        issues = result.get("issues", [])
        if not issues:
            yield self.create_text_message("No issues found.")
            return
        limit = 20
        shown = issues[:limit]
        heading = f"Issues: {len(issues)} found"
        if len(issues) > limit:
            heading += f", showing first {len(shown)}"
        lines = [heading]
        for it in shown:
            status = it.get("status")
            assignee = it.get("assignee")
            parts = [f"- {it.get('issueKey')} [{status}] {it.get('summary')}"]
            if assignee:
                parts.append(f"@{assignee}")
            lines.append(" ".join(parts))
        yield self.create_text_message("\n".join(lines))
