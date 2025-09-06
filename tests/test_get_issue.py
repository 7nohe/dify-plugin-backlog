from tools import get_issue as mod


def test_get_issue_basic_ok(monkeypatch, dummy_resp):
    def fake_get(url, params=None, timeout=30):
        assert "/issues/PRJ-1" in url
        assert params and "apiKey" in params
        return dummy_resp(
            {
                "id": 1,
                "issueKey": "PRJ-1",
                "summary": "S",
                "description": "D",
                "status": {"name": "Open"},
                "priority": {"name": "High"},
                "issueType": {"name": "Bug"},
                "assignee": {"name": "U"},
                "createdUser": {"name": "C"},
                "created": "2025-01-01",
                "updated": "2025-01-02",
                "startDate": "2025-01-03",
                "dueDate": "2025-01-04",
                "estimatedHours": 1.5,
                "actualHours": 1.0,
            }
        )

    monkeypatch.setattr(mod.requests, "get", fake_get)
    out = mod.invoke(
        {"issueIdOrKey": "PRJ-1"},
        {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"},
        {},
    )
    it = out["issue"]
    assert it["issueKey"] == "PRJ-1"
    assert it["status"] == "Open"
    assert it["priority"] == "High"
    assert it["issueType"] == "Bug"
    assert it["assignee"] == "U"
    assert it["createdUser"] == "C"
    assert it["url"].endswith("/view/PRJ-1")


def test_get_issue_only_yaml_param(monkeypatch, dummy_resp):
    monkeypatch.setattr(mod.requests, "get", lambda *a, **kw: dummy_resp({}))
    try:
        mod.invoke(
            {"parameters": {"issue_id_or_key": "PRJ-2"}},
            {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"},
            {},
        )
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_get_issue_missing_param_raises():
    try:
        mod.invoke({}, {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"}, {})
        assert False, "expected ValueError"
    except ValueError:
        pass
