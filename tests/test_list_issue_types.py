from tools import list_issue_types as mod


def test_list_issue_types_ok(monkeypatch, dummy_resp):
    def fake_get(url, params=None, timeout=30):
        assert "/projects/PRJ/issueTypes" in url
        return dummy_resp(
            [
                {"id": 1, "name": "Bug", "color": "#e30000"},
                {"id": 2, "name": "Task", "color": "#7ea800"},
            ]
        )

    monkeypatch.setattr(mod.requests, "get", fake_get)
    out = mod.invoke(
        {"projectIdOrKey": "PRJ"},
        {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"},
        {},
    )
    assert "issueTypes" in out and len(out["issueTypes"]) == 2
    assert out["issueTypes"][0]["name"] == "Bug"
    # Strict: only project_id is accepted by tool
