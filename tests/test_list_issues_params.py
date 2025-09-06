from tools import list_issues as mod


def test_list_issues_param_coercion(monkeypatch, dummy_resp):
    captured = {}

    def fake_get(url, params=None, timeout=30):
        # Capture the first call only; subsequent pagination will be empty
        if not captured:
            captured.update({"url": url, "params": dict(params or {})})
            return dummy_resp([])
        return dummy_resp([])

    monkeypatch.setattr(mod.requests, "get", fake_get)

    mod.invoke(
        {
            "projectId": "1,2",
            "assigneeId": "[3, 4]",
            "statusId": 5,
            "keyword": "bug",
        },
        {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"},
        {},
    )

    p = captured["params"]
    assert p["projectId[]"] == [1, 2]
    assert p["assigneeId[]"] == [3, 4]
    assert p["statusId[]"] == [5]
    assert p["keyword"] == "bug"
    assert p["count"] == 100
    assert p["offset"] == 0

