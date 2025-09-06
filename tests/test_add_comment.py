from tools import add_comment as mod


def test_add_comment_ok(monkeypatch, dummy_resp):
    def fake_post(url, data=None, timeout=30):
        return dummy_resp({"id": 99, "created": "2025-01-01T00:00:00Z"})

    monkeypatch.setattr(mod.requests, "post", fake_post)
    out = mod.invoke(
        {"issueIdOrKey": "PRJ-10", "content": "hi"},
        {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"},
        {},
    )
    assert out["commentId"] == 99
