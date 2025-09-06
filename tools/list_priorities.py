import requests

from ._utils import base_url, build_params, credentials_space_api_key, http_get

try:
    from dify_plugin import Tool
except Exception:  # pragma: no cover

    class Tool:
        pass


def invoke(tools_input, credentials, context):
    space, _ = credentials_space_api_key(credentials)
    url = base_url(space) + "/priorities"
    params = build_params(credentials)
    data = http_get(url, params, get_func=requests.get)
    priorities = [{"id": p["id"], "name": p["name"]} for p in data]
    return {"priorities": priorities}


class ListPrioritiesTool(Tool):
    def _invoke(self, tool_parameters):
        creds = self.runtime.credentials
        result = invoke(tool_parameters or {}, creds, {})
        # Structured result
        yield self.create_json_message(result)

        # Human-readable text
        items = result.get("priorities", [])
        if items:
            lines = [
                "Priorities:",
                *[f"- {p.get('id')}: {p.get('name')}" for p in items],
            ]
            yield self.create_text_message("\n".join(lines))
        else:
            yield self.create_text_message("No priorities found.")
