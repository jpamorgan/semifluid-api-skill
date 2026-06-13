# Semifluid API Skill Evaluation

Use this rubric to measure whether agents use the skill quickly, correctly, and with minimal extra reasoning.

## Run Setup

For each eval run, set a unique trace path before asking the agent to use the skill:

```bash
export SEMIFLUID_API_TRACE=/tmp/semifluid-api-evals/run-001.jsonl
```

After the run, score it:

```bash
python3 scripts/evaluate_skill_run.py \
  --task list_tables \
  --trace /tmp/semifluid-api-evals/run-001.jsonl \
  --success yes \
  --elapsed-seconds 12 \
  --time-to-first-api-seconds 4 \
  --commands 1
```

The trace records Semifluid API timing automatically. Add `elapsed`, `commands`, `doc_reads`, `mutation_safety`, and final-answer ratings from the Codex transcript.

## Benchmark Prompts

Run each prompt 3-5 times against the current skill, then again after instruction/script changes.

| Task | Prompt | Target Trace |
| --- | --- | --- |
| `health` | Use `$semifluid-api` to check Semifluid health. | 1 command, 1 API call, no docs/spec. |
| `list_tables` | Use `$semifluid-api` to list my Semifluid tables. | 1 command, 1 API call, no docs/spec. |
| `read_known_rows` | Use `$semifluid-api` to show 10 rows from table `<tableId>`. | 1 API call, no docs/spec. |
| `find_table_then_rows` | Use `$semifluid-api` to find the table named `<name>` and show 10 rows. | `GET /tables`, then rows call. |
| `query_rows` | Use `$semifluid-api` to search table `<name or id>` for `<query>`. | Usually table lookup plus query call. |
| `row_activity` | Use `$semifluid-api` to show recent activity for row `<rowId>` in table `<tableId>`. | 1 API call, no docs/spec. |
| `list_webhooks` | Use `$semifluid-api` to list my Semifluid webhooks. | 1 command, 1 API call, no docs/spec. |
| `simple_write` | Use `$semifluid-api` to add one row to table `<name or id>` with these values: `<values>`. | Small context read, one write, concise result. |
| `simple_write` | Use `$semifluid-api` to update row `<rowId>` in table `<tableId>`: `<field>=<value>`. | Optional row/table read, one patch, concise result. |
| `uncommon_endpoint` | Use `$semifluid-api` to inspect recent workspace changes. | Docs/spec allowed only if shape is unclear. |

## Metrics

- `success`: requested action happened correctly.
- `time_to_first_api_call`: seconds before the first helper/API command.
- `total_elapsed_time`: full agent-run time.
- `shell_command_count`: commands/tool calls the agent used.
- `api_request_count`: requests in the helper trace.
- `doc_reads`: local reference reads before acting.
- `spec_fetches`: live spec fetches before acting.
- `mutation_safety`: `ok`, `unsafe`, `overchecked`, or `na`.
- `final_answer_noise`: `ok`, `noisy`, or `secret-risk`.

## Scoring Interpretation

- `90-100`: efficient and reliable.
- `75-89`: works, but wastes a few steps.
- `60-74`: succeeds with clear instruction-following friction.
- `<60`: unreliable, unsafe, or too slow for routine use.

## What Good Looks Like

Good agents call the helper first for common tasks, avoid reference/spec reads unless needed, and keep final answers short. Writes should use the smallest read-only context needed to avoid changing the wrong table, row, or field.
