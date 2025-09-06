from tools import list_projects as mod


def test_list_projects_ok(monkeypatch, dummy_resp):
    def fake_get(url, params=None, timeout=30):
        return dummy_resp(
            [
                {"id": 1, "projectKey": "PRJ", "name": "Proj"},
                {"id": 2, "projectKey": "OPS", "name": "Ops"},
            ]
        )

    monkeypatch.setattr(mod.requests, "get", fake_get)

    out = mod.invoke({"archived": False}, {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"}, {})
    assert "projects" in out and len(out["projects"]) == 2
    assert out["projects"][0]["projectKey"] == "PRJ"
