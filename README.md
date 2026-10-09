# openrouter-mcp (Devin MCP Server)

A dependency-free MCP (Model Context Protocol) server that exposes an
`openrouter_chat` tool, letting your AI agent send prompts to any model hosted
on [OpenRouter](https://openrouter.ai) — billed through your own OpenRouter
key, not your agent's credits.

Single Python file, standard library only. No pip installs, no Node, no build
step.

## Features

- **One tool** (`openrouter_chat`) with `prompt`, `model`, `system`, and
  `max_tokens` arguments
- **Model aliases** — `luna`, `sonnet`, `opus`, `haiku`, `gemini`, `deepseek`,
  `kimi`, `glm`, `mistral`, `qwen` — or any full OpenRouter id (`vendor/model`)
- **Zero dependencies** — Python 3 standard library only
- **User-level install for Devin** — available in every project after one
  install

## Quick start

**From PyPI** (after first publish — see [PUBLISHING.md](PUBLISHING.md)):

```bash
uvx openrouter-mcp        # run directly
# or: pip install openrouter-mcp-server
```

**From source:**

```bash
git clone https://github.com/CxOrg/openrouter-mcp.git
cd openrouter-mcp
./install.sh
```

The script copies the server to `~/.config/devin/mcp/`, asks for your
OpenRouter key (input hidden), and merges the server into
`~/.config/devin/mcp_config.json`. Restart your Devin session and ask the
agent to *list MCP servers*.

See [install.md](install.md) for manual installation, other clients, and
uninstalling.

## Usage in Devin

After installing, type this in your local Devin prompt:

```text
Use openrouter_chat to ask sonnet: <your question>
```

Shorter phrasing such as `Ask openrouter sonnet: <your question>` usually
works too — the server name plus an alias is enough for the agent to find
the tool — but naming `openrouter_chat` explicitly guarantees the request
is routed to OpenRouter instead of Devin's own model.

Recommended patterns:

| Goal | Prompt |
|---|---|
| Second opinion on a plan or diff | `Use openrouter_chat to get a second opinion from glm on: <paste plan/diff>` |
| Offload a self-contained subtask | `Ask deepseek via openrouter_chat to <self-contained task>` |
| Pick a specific model | `Use openrouter_chat with model opus to ...` |

Use an alias (`sonnet`, `glm`, `deepseek`, ...) or any full OpenRouter id
(`vendor/model`). Add `system` for a role/tone and `max_tokens` for long
answers — see [install.md](install.md#usage) for the full argument table.

## License

[MIT](LICENSE)
