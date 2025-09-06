import requests

from ._utils import base_url, build_params, credentials_space_api_key, http_get

try:
    from dify_plugin import Tool
except Exception:  # pragma: no cover - only used outside pytest

    class Tool:  # minimal stub for local tests
        pass


def invoke(tools_input, credentials, context):
    space, _ = credentials_space_api_key(credentials)
    params = build_params(credentials, {
        "archived": tools_input.get("archived"),
        "all": tools_input.get("all"),
    })

    url = base_url(space) + "/projects"
    data = http_get(url, params, get_func=requests.get)
    projects = [{"id": p["id"], "projectKey": p["projectKey"], "name": p["name"]} for p in data]
    return {"projects": projects}


class ListProjectsTool(Tool):  # runtime for Dify plugin SDK
    def _invoke(self, tool_parameters):
        creds = self.runtime.credentials
        result = invoke(tool_parameters or {}, creds, {})
        # JSON output (for structured consumption)
        yield self.create_json_message(result)

        # Also provide a concise text view for humans
        projects = result.get("projects", [])
        if projects:
            lines = [
                "Projects:",
                *[f"- {p.get('projectKey')}: {p.get('name')} (id={p.get('id')})" for p in projects],
            ]
            yield self.create_text_message("\n".join(lines))
        else:
            yield self.create_text_message("No projects found.")
