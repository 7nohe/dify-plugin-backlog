import os
import sys
import types

import pytest

# Ensure project root is importable for 'tools' package during pytest collection
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Provide a lightweight stub for dify_plugin to avoid importing the real package
# during tests (which triggers gevent monkey-patching warnings, etc.).
stub = types.ModuleType("dify_plugin")

class _Tool:  # minimal stub used by tools/* modules under test
    pass

class _Plugin:  # minimal stub for main.py (not used by tests but harmless)
    def __init__(self, *_args, **_kwargs):
        self.env = None

    def run(self):  # pragma: no cover
        pass

class _DifyPluginEnv:  # pragma: no cover
    def __init__(self, **_kwargs):
        pass

setattr(stub, "Tool", _Tool)
setattr(stub, "Plugin", _Plugin)
setattr(stub, "DifyPluginEnv", _DifyPluginEnv)

# Also provide nested error types used by provider/* (not imported in tests but safe)
errors_mod = types.ModuleType("dify_plugin.errors")
tool_errors_mod = types.ModuleType("dify_plugin.errors.tool")

class ToolProviderCredentialValidationError(Exception):
    pass

setattr(
    tool_errors_mod,
    "ToolProviderCredentialValidationError",
    ToolProviderCredentialValidationError,
)
setattr(errors_mod, "tool", tool_errors_mod)

sys.modules["dify_plugin"] = stub
sys.modules["dify_plugin.errors"] = errors_mod
sys.modules["dify_plugin.errors.tool"] = tool_errors_mod


class DummyResp:
    def __init__(self, json_data=None, status_code=200):
        self._json = json_data or {}
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


@pytest.fixture
def dummy_resp():
    return DummyResp
