#!/usr/bin/env bash
# Install the openrouter-mcp server for Devin (user-level, available in all projects)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$HOME/.config/devin/mcp"
TARGET_FILE="$TARGET_DIR/openrouter_mcp.py"
CONFIG_FILE="$HOME/.config/devin/mcp_config.json"

usage() {
  cat <<EOF
Usage: ./install.sh [--key OPENROUTER_API_KEY] [--uninstall]

  --key KEY    OpenRouter API key (sk-or-v1-...). If omitted, you will be
               prompted securely (input hidden).
  --uninstall  Remove the server and its config entry.
EOF
}

require_python() {
  command -v python3 >/dev/null 2>&1 || { echo "Error: python3 is required." >&2; exit 1; }
}

uninstall() {
  require_python
  rm -f "$TARGET_FILE"
  python3 - "$CONFIG_FILE" <<'PY'
import json, os, sys
path = sys.argv[1]
if not os.path.exists(path):
    print("No config file found; nothing to do")
    sys.exit(0)
cfg = json.load(open(path))
if cfg.get("mcpServers", {}).pop("openrouter", None) is not None:
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")
    print(f"Removed 'openrouter' from {path}")
else:
    print("No 'openrouter' entry found in config")
PY
  echo "openrouter-mcp uninstalled. Restart your Devin session."
}

merge_config() {
  KEY="$1" python3 - "$CONFIG_FILE" "$TARGET_FILE" <<'PY'
import json, os, sys
config_path, script_path = sys.argv[1], sys.argv[2]
key = os.environ["KEY"]
cfg = {}
if os.path.exists(config_path):
    cfg = json.load(open(config_path))
cfg.setdefault("mcpServers", {})
cfg["mcpServers"]["openrouter"] = {
    "command": "python3",
    "args": [script_path],
    "env": {"OPENROUTER_API_KEY": key},
}
with open(config_path, "w") as f:
    json.dump(cfg, f, indent=2)
    f.write("\n")
print(f"Wrote {config_path} (servers: {', '.join(cfg['mcpServers'])})")
PY
}

KEY=""
UNINSTALL=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --key) KEY="${2:-}"; shift 2 ;;
    --uninstall) UNINSTALL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ "$UNINSTALL" == "1" ]]; then
  uninstall
  exit 0
fi

require_python
mkdir -p "$TARGET_DIR"
install -m 755 "$SCRIPT_DIR/mcp/openrouter_mcp.py" "$TARGET_FILE"
echo "Installed server to $TARGET_FILE"

if [[ -z "$KEY" ]]; then
  echo -n "OpenRouter API key (input hidden, from openrouter.ai/keys): "
  read -rs KEY
  echo
fi
if [[ -z "$KEY" ]]; then
  echo "Warning: no key provided - re-run install.sh with --key later." >&2
fi

merge_config "$KEY"
echo
echo "Done. Restart your Devin session, then ask the agent to 'list MCP servers'."
