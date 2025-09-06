import time
import urllib.parse
from typing import Any, Callable, Dict, Optional

import requests


def sanitize_space(space: str) -> str:
    s = (space or "").strip()
    if s.startswith("http://") or s.startswith("https://"):
        s = s.split("://", 1)[1]
    return s.strip("/ ")


def sanitize_api_key(api_key: str) -> str:
    return (api_key or "").strip()


def base_url(space: str) -> str:
    return f"https://{sanitize_space(space)}/api/v2"


def credentials_space_api_key(credentials: Dict[str, Any]) -> tuple[str, str]:
    space = sanitize_space(str((credentials or {}).get("SPACE_DOMAIN", "")))
    api_key = sanitize_api_key(str((credentials or {}).get("API_KEY", "")))
    return space, api_key


def build_params(
    credentials: Dict[str, Any],
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    _, api_key = credentials_space_api_key(credentials)
    params: Dict[str, Any] = {"apiKey": api_key}
    if extra:
        params.update({k: v for k, v in extra.items() if v is not None})
    return params


def _join_url_params(url: str, params: Optional[Dict[str, Any]]) -> str:
    if not params:
        return url
    q = urllib.parse.urlencode(params, doseq=True)
    sep = "&" if ("?" in url) else "?"
    return f"{url}{sep}{q}"


def http_get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    *,
    retries: int = 3,
    timeout: int = 30,
    get_func: Optional[Callable[..., Any]] = None,
):
    getter = get_func or requests.get
    for i in range(retries + 1):
        r = getter(url, params=params, timeout=timeout)
        if getattr(r, "status_code", 200) == 429 and i < retries:
            time.sleep(2**i)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("Rate limited")


def http_post(
    url: str,
    data: Any,
    params: Optional[Dict[str, Any]] = None,
    *,
    retries: int = 2,
    timeout: int = 30,
    post_func: Optional[Callable[..., Any]] = None,
):
    poster = post_func or requests.post
    for i in range(retries + 1):
        url2 = _join_url_params(url, params)
        r = poster(url2, data=data, timeout=timeout)
        if getattr(r, "status_code", 200) == 429 and i < retries:
            time.sleep(2**i)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("Rate limited")


def to_int_if_numberish(value):
    try:
        if isinstance(value, str) and value.strip().isdigit():
            return int(value.strip())
        return value
    except Exception:
        return value


def coerce_array(value: Any):
    """Coerce incoming value into a list of ids/strings for Backlog array params.

    Accepts list, number, numeric-like string, JSON array string,
    or comma/space-separated strings.
    """
    import json

    v = value
    if v is None:
        return None
    if isinstance(v, list):
        return [
            int(x)
            if isinstance(x, (int, float)) or (isinstance(x, str) and x.strip().isdigit())
            else str(x)
            for x in v
        ]
    if isinstance(v, (int, float)):
        return [int(v)]
    if isinstance(v, str):
        s = v.strip()
        if not s:
            return None
        if (s.startswith("[") and s.endswith("]")) or (
            s.startswith("\"") and s.endswith("\"")
        ):
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return [
                        int(x)
                        if isinstance(x, (int, float))
                        or (isinstance(x, str) and x.strip().isdigit())
                        else str(x)
                        for x in parsed
                    ]
            except Exception:
                pass
        tokens = [p.strip() for p in s.replace(";", ",").replace("\n", ",").split(",")]
        if len(tokens) == 1 and " " in s and "," not in s:
            tokens = [p for p in s.split(" ") if p]
        tokens = [t for t in tokens if t]
        return [int(t) if t.isdigit() else t for t in tokens]
    return [str(v)]
