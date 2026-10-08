# Installing openrouter-mcp

## Requirements

- Python 3.8+ (`python3` on PATH)
- An MCP client that supports stdio servers (instructions below use
  [Devin](https://devin.ai); the config format is standard MCP and works with
  other clients)
- An OpenRouter API key from <https://openrouter.ai/keys>

## Option 1 — Install script (recommended)

```bash
./install.sh
```

What it does:

1. Copies `mcp/openrouter_mcp.py` to `~/.config/devin/mcp/`
2. Prompts for your OpenRouter API key (input hidden; or pass it with
   `--key sk-or-v1-...`)
3. Merges an `openrouter` entry into `~/.config/devin/mcp_config.json`,
   preserving any other servers you already have

Non-interactive:

```bash
./install.sh --key sk-or-v1-your-key-here
```

Then **restart your Devin session** and verify by asking the agent to
*list MCP servers* — `openrouter` should appear.

## Option 2 — Manual install

```bash
mkdir -p ~/.config/devin/mcp
cp mcp/openrouter_mcp.py ~/.config/devin/mcp/
```

Add the server to `~/.config/devin/mcp_config.json` (create the file if it
does not exist). **Use an absolute path** — `~` is not expanded inside JSON
config files:

```json
{
  "mcpServers": {
    "openrouter": {
      "command": "python3",
      "args": ["/home/YOURUSER/.config/devin/mcp/openrouter_mcp.py"],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-v1-your-key-here"
      }
    }
  }
}
```

A template is provided in [mcp_config.example.json](mcp_config.example.json).

## Other MCP clients

The server speaks MCP over stdio and works with any client. For clients that
read other config files (e.g. Claude Desktop's `claude_desktop_config.json`),
use the same `command`/`args`/`env` structure with that client's absolute
script path.

## Usage

Ask your agent to call `openrouter_chat` with:

| Argument | Description |
|---|---|
| `prompt` | The prompt to send (required) |
| `model` | Alias (`luna`, `sonnet`, `opus`, `haiku`, `gemini`, `deepseek`, `kimi`, `glm`, `mistral`, `qwen`) or full OpenRouter id (`vendor/model`) |
| `system` | Optional system prompt |
| `max_tokens` | Maximum completion tokens (default 2048) |

## Uninstall

```bash
./install.sh --uninstall
```

This removes the server script and the `openrouter` entry from
`~/.config/devin/mcp_config.json`. Restart your Devin session afterwards.

## Troubleshooting

- **Server not listed** — check `~/.config/devin/mcp_config.json` is valid
  JSON and the `args` path is absolute, then restart the session.
- **`OPENROUTER_API_KEY is empty`** — the key env var is missing or blank;
  re-run `./install.sh --key ...` or edit the config file.
- **OpenRouter HTTP 401** — the key is invalid or revoked; create a new one
  at <https://openrouter.ai/keys>.
