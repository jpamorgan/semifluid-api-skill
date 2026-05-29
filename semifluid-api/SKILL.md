---
name: semifluid-api
description: Interact with the Semifluid HTTP API directly, without MCP, using a local helper script and OpenAPI-derived endpoint notes. Use when Codex needs to inspect or change Semifluid tables, rows, properties, API keys, attachments, changes, health/version status, or any endpoint from https://api.semifluid.ai/api-reference/spec.json.
---

# Semifluid API

Use this skill to call the Semifluid API from the local shell without an MCP connector.

## Auth

Use `scripts/semifluid_api.py`; it reads the API key from `SEMIFLUID_API_KEY` first, then from macOS Keychain:

- service: `ai.semifluid.api-key`
- account: `semifluid-api`

Do not write API keys into skill files, repo files, shell history, or final answers. If auth fails, verify keychain access with:

```bash
security find-generic-password -a semifluid-api -s ai.semifluid.api-key -w >/dev/null
```

## Quick Start

Run commands from this skill directory or pass the absolute script path:

```bash
python3 scripts/semifluid_api.py health
python3 scripts/semifluid_api.py operations
python3 scripts/semifluid_api.py get /tables
python3 scripts/semifluid_api.py get /tables/{tableId}/rows --query limit=10 --query properties='*'
python3 scripts/semifluid_api.py post /tables/{tableId}/rows/query --json '{"limit":10,"q":"search text"}'
```

Use `--json @file.json` for request bodies that are too large or sensitive for the command line.

## Workflow

1. For endpoint shape, read `references/api-reference.md` first.
2. For exact current schemas, run `python3 scripts/semifluid_api.py spec` or inspect the live spec URL.
3. Prefer read-only requests first (`GET /tables`, `GET /tables/{tableId}`, `GET /tables/{tableId}/rows`) before mutating data.
4. For write operations, build a small JSON file and call with `--json @file.json`.
5. Report status codes and concise results. Do not include secrets in outputs.

## Script Notes

- The helper uses only Python standard library.
- Authenticated requests send `x-api-key: <key>` by default.
- Every API request reports elapsed time to stderr, leaving response bodies on stdout.
- Use `--no-auth` only for public endpoints such as `/health`.
- Use `--base-url` if targeting a non-production Semifluid API.
- Use `--output path` for large responses or files.
