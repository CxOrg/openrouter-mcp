#!/usr/bin/env python3
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-sonnet-5.5"

ALIASES = {
    "luna": "~openai/gpt-luna-latest",
    "sonnet": "anthropic/claude-sonnet-5.5",
    "opus": "anthropic/claude-opus-5.5",
    "haiku": "anthropic/claude-haiku-5.5",
    "gemini": "google/gemini-3.8-flash",
    "deepseek": "deepseek/deepseek-v4-flash",
    "kimi": "moonshotai/kimi-k2.7-code",
    "glm": "~z-ai/glm-flash-latest",
    "mistral": "mistralai/mistral-medium-3-5",
    "qwen": "qwen/qwen3.8-max-prime",
}

TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "prompt": {"type": "string", "description": "The prompt to send to the model"},
        "model": {
            "type": "string",
            "description": (
                "Short alias or full OpenRouter id (vendor/model). "
                f"Aliases: {', '.join(f'{k}={v}' for k, v in ALIASES.items())}."
            ),
            "default": DEFAULT_MODEL,
        },
        "system": {"type": "string", "description": "Optional system prompt"},
        "max_tokens": {"type": "integer", "description": "Maximum completion tokens", "default": 2048},
    },
    "required": ["prompt"],
}


def write(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def reply(msg_id, result):
    write({"jsonrpc": "2.0", "id": msg_id, "result": result})


def error(msg_id, code, message):
    write({"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}})


def resolve_model(model):
    name = (model or "").strip()
    if not name:
        return DEFAULT_MODEL
    if "/" in name:
        return name
    return ALIASES.get(name.lower(), name)


def chat(args):
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        return {
            "content": [{"type": "text", "text": "OPENROUTER_API_KEY is empty. Set it in your MCP client config (e.g. ~/.config/devin/mcp_config.json) or re-run install.sh."}],
            "isError": True,
        }
    messages = []
    if args.get("system"):
        messages.append({"role": "system", "content": args["system"]})
    messages.append({"role": "user", "content": args["prompt"]})
    body = {
        "model": resolve_model(args.get("model")),
        "messages": messages,
        "max_tokens": args.get("max_tokens") or 2048,
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://devin.ai",
            "X-Title": "devin-mcp",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        return {"content": [{"type": "text", "text": f"OpenRouter HTTP {e.code}: {detail}"}], "isError": True}
    except (urllib.error.URLError, TimeoutError) as e:
        return {"content": [{"type": "text", "text": f"OpenRouter request failed: {e}"}], "isError": True}

    choices = data.get("choices") or []
    if not choices:
        return {"content": [{"type": "text", "text": f"Unexpected OpenRouter response: {json.dumps(data)[:500]}"}], "isError": True}
    message = choices[0]["message"]
    text = message.get("content") or message.get("reasoning") or ""
    if not text:
        return {"content": [{"type": "text", "text": f"Model returned empty content: {json.dumps(data)[:500]}"}], "isError": True}
    usage = data.get("usage") or {}
    stats = ", ".join(f"{k} {v}" for k, v in usage.items() if isinstance(v, int))
    if stats:
        text += f"\n\n---\n{data.get('model', body['model'])} | {stats}"
    return {"content": [{"type": "text", "text": text}]}


def handle(req):
    method = req.get("method")
    msg_id = req.get("id")
    if method == "initialize":
        return reply(msg_id, {
            "protocolVersion": req.get("params", {}).get("protocolVersion", "2025-06-18"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "openrouter", "version": "1.0.0"},
        })
    if method == "ping":
        return reply(msg_id, {})
    if method == "tools/list":
        return reply(msg_id, {"tools": [{
            "name": "openrouter_chat",
            "description": (
                "Send a prompt to a model hosted on OpenRouter and return its response. "
                "Use for second opinions from a different model family or for self-contained subtasks. "
                "Billing goes through the user's own OpenRouter key, not Devin credits. "
                f"The 'model' argument accepts short aliases ({', '.join(ALIASES)}) or any full OpenRouter id like 'vendor/model'."
            ),
            "inputSchema": TOOL_SCHEMA,
        }]})
    if method == "tools/call":
        params = req.get("params", {})
        if params.get("name") != "openrouter_chat":
            return error(msg_id, -32602, f"Unknown tool: {params.get('name')}")
        return reply(msg_id, chat(params.get("arguments") or {}))
    return error(msg_id, -32601, f"Method not found: {method}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        if req.get("id") is None:
            continue
        try:
            handle(req)
        except Exception as e:
            error(req["id"], -32603, f"internal error: {e}")


if __name__ == "__main__":
    main()
