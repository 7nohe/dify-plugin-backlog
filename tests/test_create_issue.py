from tools import create_issue as mod


def test_create_issue_ok(monkeypatch, dummy_resp):
    def fake_post(url, data=None, timeout=30):
        return dummy_resp({"id": 10, "issueKey": "PRJ-10", "summary": "s"})

    monkeypatch.setattr(mod.requests, "post", fake_post)
    out = mod.invoke(
        {"projectId": 1, "summary": "s", "issueTypeId": 2, "priorityId": 3},
        {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"},
        {},
    )
    assert out["issue"]["issueKey"] == "PRJ-10"
    assert out["issue"]["url"].endswith("/view/PRJ-10")


def test_create_issue_project_key_string(monkeypatch, dummy_resp):
    # Resolve project by key string and then create
    def fake_get(url, params=None, timeout=30):
        assert "/projects/PRJ" in url
        return dummy_resp({"id": 123, "projectKey": "PRJ", "name": "Proj"})

    def fake_post(url, data=None, timeout=30):
        # Ensure projectId was resolved to numeric ID
        assert data.get("projectId") == 123
        return dummy_resp({"id": 11, "issueKey": "PRJ-11", "summary": "s2"})

    monkeypatch.setattr(mod.requests, "get", fake_get)
    monkeypatch.setattr(mod.requests, "post", fake_post)

    out = mod.invoke(
        {"projectId": "PRJ", "summary": "s2", "issueTypeId": 2, "priorityId": 3},
        {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"},
        {},
    )
    assert out["issue"]["issueKey"] == "PRJ-11"


def test_create_issue_params_nested_inputs(monkeypatch, dummy_resp):
    def fake_get(url, params=None, timeout=30):
        assert "/projects/PRJ" in url
        return dummy_resp({"id": 9, "projectKey": "PRJ", "name": "Proj"})

    def fake_post(url, data=None, timeout=30):
        assert data.get("projectId") == 9
        assert data.get("summary") == "s3"
        assert data.get("issueTypeId") == 2
        assert data.get("priorityId") == 3
        return dummy_resp({"id": 12, "issueKey": "PRJ-12", "summary": "s3"})

    monkeypatch.setattr(mod.requests, "get", fake_get)
    monkeypatch.setattr(mod.requests, "post", fake_post)

    out = mod.invoke(
        {"inputs": {"projectId": "PRJ", "summary": "s3", "issueTypeId": 2, "priorityId": 3}},
        {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"},
        {},
    )
    assert out["issue"]["issueKey"] == "PRJ-12"
