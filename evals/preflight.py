"""Read-only, no-inference routing/tool check in Hermes's own interpreter.

Never print runtime credential values or the whole config/runtime dictionary.
"""
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit

source = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(source))
from cli import CLI_CONFIG
from hermes_cli.config import load_config
from hermes_cli.fallback_config import get_fallback_chain
from hermes_cli.runtime_provider import resolve_runtime_provider
from model_tools import get_tool_definitions
from toolsets import validate_toolset

import os
from hermes_cli.model_switch import resolve_startup_model_route
from hermes_constants import get_hermes_home

# Match CLI startup alias resolution as well as its final credential resolver.
startup = resolve_startup_model_route(
    "gpt-6.1-sol", explicit_provider="openai-codex", current_provider="openai-codex",
    user_providers=CLI_CONFIG.get("providers"), custom_providers=CLI_CONFIG.get("custom_providers"))
model = startup.model if startup else "gpt-6.1-sol"
if model != "gpt-6.1-sol" or (startup and (startup.base_url or startup.api_key)):
    raise RuntimeError("Model alias or explicit credential/endpoint override is not allowed")
runtime = resolve_runtime_provider(requested="openai-codex", target_model=model)
endpoint = urlsplit(runtime.get("base_url", ""))
if endpoint.username or endpoint.password or endpoint.query or endpoint.fragment:
    raise RuntimeError("Unexpected credential/query/fragment in runtime endpoint")
data = {
    "model": model,
    "scheme": endpoint.scheme,
    "path": endpoint.path.rstrip("/"),
    "safe_mode": os.environ.get("HERMES_SAFE_MODE") == "1",
    "ignore_user_config": os.environ.get("HERMES_IGNORE_USER_CONFIG") == "1",
    "ignore_rules": os.environ.get("HERMES_IGNORE_RULES") == "1",
    "session_db": str(get_hermes_home() / "state.db"),
    "provider": runtime.get("provider"),
    "api_mode": runtime.get("api_mode"),
    "host": urlsplit(runtime.get("base_url", "")).hostname,
    "source": runtime.get("source"),
    "valid_toolset": validate_toolset("bot_room"),
    "tool_count": len(get_tool_definitions(enabled_toolsets=["bot_room"], quiet_mode=True)),
    "fallback_count": len(get_fallback_chain(load_config())),
    "cli_fallback_count": len(get_fallback_chain(CLI_CONFIG)),
}
revision = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"], capture_output=True, text=True)
data["hermes_revision"] = revision.stdout.strip() if revision.returncode == 0 else "unknown"
print("EVAL_PREFLIGHT_JSON=" + json.dumps(data, sort_keys=True))
