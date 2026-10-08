# Publishing openrouter-mcp-server to PyPI

Two ways to publish. Trusted Publishing (Option B) is recommended — no tokens
to manage, and it runs automatically on every GitHub release.

## One-time: PyPI account

1. Create an account at <https://pypi.org/account/register/>
2. Verify your email

## Option A — Manual publish (twine + API token)

1. Create an API token: <https://pypi.org/manage/account/token/>
   (scope: "Entire account" for the first upload)

2. Build and upload:

```bash
cd /home/www/DEV-trunk/OpenRouter
python3 -m pip install --upgrade build twine
python3 -m build
twine check dist/*
twine upload dist/*
```

3. When prompted, use:
   - username: `__token__`
   - password: `pypi-...` (your API token)

## Option B — Automated publish (Trusted Publishing, recommended)

The repo already contains `.github/workflows/publish.yml`, which builds and
publishes on every GitHub release (and on manual `workflow_dispatch`).

One-time setup on PyPI:

1. Go to <https://pypi.org/manage/account/publishing/>
2. Add a "pending" trusted publisher:
   - Owner: `CxOrg`
   - Repository: `openrouter-mcp`
   - Workflow name: `publish.yml`
   - Environment: leave blank

Then publish a release:

```bash
git tag v1.0.0
git push origin v1.0.0
gh release create v1.0.0 --title "v1.0.0" --notes "First PyPI release" --repo CxOrg/openrouter-mcp
```

The workflow builds the sdist/wheel and uploads them via OIDC — no token
stored anywhere.

## Verify the publish

```bash
curl -s https://pypi.org/pypi/openrouter-mcp-server/json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['info']['version'])"
```

Or test the installed tool:

```bash
uvx openrouter-mcp-server
```

Naming note: the **PyPI package** is `openrouter-mcp-server`. The package
installs two equivalent console commands: `openrouter-mcp` and
`openrouter-mcp-server` (the latter matches the package name so
`uvx openrouter-mcp-server` works without `--from`).

## After publishing

- The package becomes listable on MCP registries (Smithery, PulseMCP, Glama)
  by submitting the repo/package URL on their sites
- Bump `version` in `pyproject.toml` for each release
