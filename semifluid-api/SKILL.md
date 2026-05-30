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

## Fast Path

For common operations shown in Quick Start or `references/api-reference.md`, call `scripts/semifluid_api.py` directly. Do not read `references/api-reference.md`, fetch the live spec, or run `operations` unless the endpoint/body shape is unclear, the request fails with a schema error, or the user asks for an uncommon endpoint.

Expected efficient paths:

- Health check: one `health` command.
- List tables: one `get /tables` command.
- Show rows from a known table: one `get /tables/{tableId}/rows --query limit=N --query properties='*'` command.
- Find a table by name, then read rows: `get /tables`, then one rows command.
- Simple row/property/table write: make the smallest read-only request needed to identify the target, write with `--json @file.json`, then report the result.

## Workflow

1. Use the Fast Path first for common requests.
2. For unfamiliar endpoint shape, read `references/api-reference.md`.
3. For exact current schemas, run `python3 scripts/semifluid_api.py spec` or inspect the live spec URL only when the local reference is insufficient.
4. Prefer targeted read-only requests (`GET /tables`, `GET /tables/{tableId}`, `GET /tables/{tableId}/rows`) before mutating data.
5. For write operations, build a small JSON file and call with `--json @file.json`.
6. Report status codes and concise results. Do not include secrets in outputs.

## Evaluation

Use trace logging when measuring the skill:

```bash
SEMIFLUID_API_TRACE=/tmp/semifluid-api-trace.jsonl python3 scripts/semifluid_api.py get /tables
python3 scripts/evaluate_skill_run.py --task list_tables --trace /tmp/semifluid-api-trace.jsonl --success yes --elapsed-seconds 12 --commands 1
```

Score agent runs on correctness first, then efficiency:

- `success`: did the requested Semifluid action happen correctly?
- `time_to_first_api_call`: how quickly the agent used the helper.
- `total_elapsed_time`: end-to-end run time.
- `shell_command_count`: local commands/tool calls needed.
- `api_request_count`: Semifluid requests made by the helper.
- `doc_reads` and `spec_fetches`: extra reference/spec steps before acting.
- `mutation_safety`: enough targeted read context before writes.
- `final_answer_noise`: concise status without secrets or excessive internals.

## Script Notes

- The helper uses only Python standard library.
- Authenticated requests send `x-api-key: <key>` by default.
- Every API request reports elapsed time to stderr, leaving response bodies on stdout.
- Set `SEMIFLUID_API_TRACE=/path/to/trace.jsonl` or pass `--trace-output /path/to/trace.jsonl` to append machine-readable request timing events. Trace events never include API keys, request bodies, response bodies, or query values.
- Use `--no-auth` only for public endpoints such as `/health`.
- Use `--base-url` if targeting a non-production Semifluid API.
- Use `--output path` for large responses or files.
