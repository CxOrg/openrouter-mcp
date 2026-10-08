# openrouter-mcp

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

## License

[MIT](LICENSE)
