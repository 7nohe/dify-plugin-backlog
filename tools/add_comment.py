import requests

from ._utils import base_url, build_params, credentials_space_api_key, http_post

try:
    from dify_plugin import Tool
except Exception:  # pragma: no cover

    class Tool:
        pass


def invoke(tools_input, credentials, context):
    space, _ = credentials_space_api_key(credentials)
    issue = tools_input["issueIdOrKey"]
    url = base_url(space) + f"/issues/{issue}/comments"
    params = build_params(credentials)
    res = http_post(
        url,
        {"content": tools_input["content"]},
        params=params,
        post_func=requests.post,
    )
    return {"commentId": res["id"], "created": res["created"]}


class AddCommentTool(Tool):
    def _invoke(self, tool_parameters):
        creds = self.runtime.credentials
        result = invoke(tool_parameters or {}, creds, {})
        # Structured result
        yield self.create_json_message(result)

        # Human-readable text
        cid = (result or {}).get("commentId")
        created = (result or {}).get("created")
        target = (tool_parameters or {}).get("issueIdOrKey")
        if cid:
            if target:
                yield self.create_text_message(f"Added comment {cid} to {target} at {created}.")
            else:
                yield self.create_text_message(f"Added comment {cid} at {created}.")
        else:
            yield self.create_text_message("Comment added.")
