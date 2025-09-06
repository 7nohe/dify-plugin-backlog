from tools import list_issues as mod


def test_list_issues_paging(monkeypatch, dummy_resp):
    calls = {"n": 0}

    def fake_get(url, params=None, timeout=30):
        calls["n"] += 1
        if calls["n"] == 1:
            return dummy_resp(
                [
                    {
                        "id": 1,
                        "issueKey": "PRJ-1",
                        "summary": "a",
                        "status": {"name": "Open"},
                        "assignee": {"name": "U"},
                        "updated": "2025-01-01",
                    }
                ]
            )
        return dummy_resp([])

    monkeypatch.setattr(mod.requests, "get", fake_get)

    out = mod.invoke({"count": 1}, {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"}, {})
    assert len(out["issues"]) == 1
    assert out["issues"][0]["issueKey"] == "PRJ-1"
