from typing import Any

import requests

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

# Reuse helpers to normalize inputs and build URLs
try:  # Local/unit-test friendly import
    from tools._utils import base_url, sanitize_api_key, sanitize_space
except Exception:  # pragma: no cover
    def sanitize_space(space: str) -> str:  # fallback (very small subset)
        s = (space or "").strip()
        if s.startswith("http://") or s.startswith("https://"):
            s = s.split("://", 1)[1]
        return s.strip("/ ")

    def sanitize_api_key(api_key: str) -> str:
        return (api_key or "").strip()

    def base_url(space: str) -> str:
        return f"https://{sanitize_space(space)}/api/v2"


class BacklogProvider(ToolProvider):

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            # Basic presence & format checks
            space = sanitize_space(str((credentials or {}).get("SPACE_DOMAIN", "")))
            api_key = sanitize_api_key(str((credentials or {}).get("API_KEY", "")))

            if not space:
                raise ValueError("SPACE_DOMAIN is required (e.g. yourspace.backlog.jp)")
            if "/" in space or space.startswith(":"):
                # After sanitize, remaining slashes or leading colon indicate malformed host
                raise ValueError("SPACE_DOMAIN must be a host without path (e.g. yourspace.backlog.jp)")
            if not api_key:
                raise ValueError("API_KEY is required")

            # Optional: DEFAULT_PROJECT (if provided, allow non-empty string or int)
            default_project = (credentials or {}).get("DEFAULT_PROJECT")
            if default_project is not None and default_project != "":
                if not isinstance(default_project, (str, int)):
                    raise ValueError("DEFAULT_PROJECT must be string (key) or integer (ID)")
                if isinstance(default_project, str) and not default_project.strip():
                    raise ValueError("DEFAULT_PROJECT must be non-empty when provided")

            # Live verification against Backlog API: GET /space
            # - Verifies domain reachability and API key validity
            # https://developer.nulab.com/docs/backlog/api/2/get-space/
            url = base_url(space) + "/space"
            try:
                resp = requests.get(url, params={"apiKey": api_key}, timeout=10)
            except requests.exceptions.RequestException as re:  # network/timeout errors
                raise ValueError(f"Failed to reach Backlog ({space}): {re}")

            if resp.status_code in (401, 403):
                raise ValueError("Invalid API key or insufficient permissions")
            if resp.status_code == 404:
                # Usually indicates wrong space domain
                raise ValueError("Backlog space not found. Check SPACE_DOMAIN")
            resp.raise_for_status()

            # Ensure response is valid JSON (guards against HTML error pages)
            try:
                _ = resp.json()
            except ValueError:
                raise ValueError("Unexpected response from Backlog API while validating credentials")

        except Exception as e:
            # Normalize all validation failures to Dify's expected exception
            raise ToolProviderCredentialValidationError(str(e))

    #########################################################################################
    # If OAuth is supported, uncomment the following functions.
    # Warning: please make sure that the sdk version is 0.4.2 or higher.
    #########################################################################################
    # def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
    #     """
    #     Generate the authorization URL for backlog OAuth.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR AUTHORIZATION URL GENERATION HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return ""

    # def _oauth_get_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    # ) -> Mapping[str, Any]:
    #     """
    #     Exchange code for access_token.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR CREDENTIALS EXCHANGE HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return dict()

    # def _oauth_refresh_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    # ) -> OAuthCredentials:
    #     """
    #     Refresh the credentials
    #     """
    #     return OAuthCredentials(credentials=credentials, expires_at=-1)
