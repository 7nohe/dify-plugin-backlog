from tools import list_priorities as mod


def test_list_priorities_ok(monkeypatch, dummy_resp):
    def fake_get(url, params=None, timeout=30):
        return dummy_resp(
            [
                {"id": 2, "name": "Normal"},
                {"id": 3, "name": "High"},
            ]
        )

    monkeypatch.setattr(mod.requests, "get", fake_get)
    out = mod.invoke({}, {"SPACE_DOMAIN": "ex.backlog.jp", "API_KEY": "k"}, {})
    assert "priorities" in out and len(out["priorities"]) == 2
    assert out["priorities"][0]["name"] == "Normal"
