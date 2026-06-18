#!/usr/bin/env python3
"""Score Semifluid API skill runs from helper traces plus agent-level metrics."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any


TASK_TARGETS = {
    "health": {"max_api_calls": 1, "max_commands": 1, "max_spec_fetches": 0, "max_doc_reads": 0},
    "list_collections": {"max_api_calls": 1, "max_commands": 1, "max_spec_fetches": 0, "max_doc_reads": 0},
    "read_known_records": {"max_api_calls": 1, "max_commands": 1, "max_spec_fetches": 0, "max_doc_reads": 0},
    "find_collection_then_records": {"max_api_calls": 2, "max_commands": 2, "max_spec_fetches": 0, "max_doc_reads": 0},
    "query_records": {"max_api_calls": 2, "max_commands": 3, "max_spec_fetches": 0, "max_doc_reads": 0},
    "record_events": {"max_api_calls": 1, "max_commands": 1, "max_spec_fetches": 0, "max_doc_reads": 0},
    "list_webhooks": {"max_api_calls": 1, "max_commands": 1, "max_spec_fetches": 0, "max_doc_reads": 0},
    "simple_write": {"max_api_calls": 3, "max_commands": 4, "max_spec_fetches": 0, "max_doc_reads": 0},
    "uncommon_endpoint": {"max_api_calls": 4, "max_commands": 5, "max_spec_fetches": 1, "max_doc_reads": 1},
    "custom": {"max_api_calls": 999, "max_commands": 999, "max_spec_fetches": 999, "max_doc_reads": 999},
}


def read_trace(path: str | None) -> list[dict[str, Any]]:
    if not path:
        return []

    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise SystemExit(f"Invalid JSONL at {path}:{line_number}: {error}") from error
    return events


def yes_no(value: str) -> bool:
    normalized = value.lower()
    if normalized in {"yes", "y", "true", "1"}:
        return True
    if normalized in {"no", "n", "false", "0"}:
        return False
    raise argparse.ArgumentTypeError("expected yes or no")


def status_ok(events: list[dict[str, Any]]) -> bool:
    return all(event.get("ok") for event in events) if events else True


def count_spec_fetches(events: list[dict[str, Any]]) -> int:
    return sum(1 for event in events if event.get("path") == "/api-reference/spec.json")


def summarize_trace(events: list[dict[str, Any]]) -> dict[str, Any]:
    elapsed_values = [float(event["elapsed_ms"]) for event in events if event.get("elapsed_ms") is not None]
    return {
        "api_request_count": len(events),
        "api_status_ok": status_ok(events),
        "spec_fetches": count_spec_fetches(events),
        "total_api_ms": round(sum(elapsed_values), 1),
        "median_api_ms": round(statistics.median(elapsed_values), 1) if elapsed_values else 0,
        "paths": [f"{event.get('method')} {event.get('path')} -> {event.get('status')}" for event in events],
    }


def score_run(args: argparse.Namespace, trace_summary: dict[str, Any]) -> tuple[int, list[str]]:
    targets = TASK_TARGETS[args.task]
    score = 100
    findings: list[str] = []

    if not args.success:
        score -= 60
        findings.append("requested action did not complete correctly")

    if not trace_summary["api_status_ok"]:
        score -= 15
        findings.append("one or more API calls failed")

    extra_api_calls = max(0, trace_summary["api_request_count"] - targets["max_api_calls"])
    if extra_api_calls:
        penalty = extra_api_calls * 5
        score -= penalty
        findings.append(f"{extra_api_calls} API call(s) above target")

    measured_spec_fetches = trace_summary["spec_fetches"] + args.spec_fetches
    extra_spec_fetches = max(0, measured_spec_fetches - targets["max_spec_fetches"])
    if extra_spec_fetches:
        penalty = extra_spec_fetches * 8
        score -= penalty
        findings.append(f"{extra_spec_fetches} unnecessary spec fetch/read step(s)")

    extra_doc_reads = max(0, args.doc_reads - targets["max_doc_reads"])
    if extra_doc_reads:
        penalty = extra_doc_reads * 4
        score -= penalty
        findings.append(f"{extra_doc_reads} unnecessary local reference read(s)")

    if args.commands is not None:
        extra_commands = max(0, args.commands - targets["max_commands"])
        if extra_commands:
            penalty = extra_commands * 3
            score -= penalty
            findings.append(f"{extra_commands} shell/tool command(s) above target")

    if args.time_to_first_api_seconds is not None and args.time_to_first_api_seconds > args.first_api_budget_seconds:
        score -= 8
        findings.append("slow time to first API call")

    if args.mutation_safety == "unsafe":
        score -= 25
        findings.append("write did not gather enough targeted context")
    elif args.mutation_safety == "overchecked":
        score -= 6
        findings.append("write gathered more context than needed")

    if args.final_answer_noise == "noisy":
        score -= 5
        findings.append("final answer included unnecessary detail")
    elif args.final_answer_noise == "secret-risk":
        score -= 30
        findings.append("final answer risked exposing secrets")

    return max(0, score), findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate one Semifluid API skill run.")
    parser.add_argument("--task", choices=sorted(TASK_TARGETS), required=True)
    parser.add_argument("--trace", help="JSONL file produced by SEMIFLUID_API_TRACE or --trace-output")
    parser.add_argument("--success", type=yes_no, required=True, help="yes/no: did the requested action happen?")
    parser.add_argument("--elapsed-seconds", type=float, help="End-to-end agent run time")
    parser.add_argument("--time-to-first-api-seconds", type=float, help="Seconds before first helper/API call")
    parser.add_argument("--first-api-budget-seconds", type=float, default=20)
    parser.add_argument("--commands", type=int, help="Total shell/tool commands in the agent run")
    parser.add_argument("--doc-reads", type=int, default=0, help="Reads of references/api-reference.md or equivalent")
    parser.add_argument("--spec-fetches", type=int, default=0, help="Manual count of spec fetches not present in trace")
    parser.add_argument(
        "--mutation-safety",
        choices=["na", "ok", "unsafe", "overchecked"],
        default="na",
        help="Manual write-safety rating",
    )
    parser.add_argument(
        "--final-answer-noise",
        choices=["ok", "noisy", "secret-risk"],
        default="ok",
        help="Manual final-answer rating",
    )
    parser.add_argument("--notes", default="")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON only")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    trace_summary = summarize_trace(read_trace(args.trace))
    score, findings = score_run(args, trace_summary)
    result = {
        "task": args.task,
        "score": score,
        "success": args.success,
        "elapsed_seconds": args.elapsed_seconds,
        "time_to_first_api_seconds": args.time_to_first_api_seconds,
        "commands": args.commands,
        "doc_reads": args.doc_reads,
        "manual_spec_fetches": args.spec_fetches,
        "mutation_safety": args.mutation_safety,
        "final_answer_noise": args.final_answer_noise,
        "trace": trace_summary,
        "findings": findings,
        "notes": args.notes,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    print(f"Task: {args.task}")
    print(f"Score: {score}/100")
    print(f"Success: {'yes' if args.success else 'no'}")
    print(f"API calls: {trace_summary['api_request_count']} ({trace_summary['total_api_ms']} ms total)")
    if args.elapsed_seconds is not None:
        print(f"Elapsed: {args.elapsed_seconds:.1f} s")
    if args.commands is not None:
        print(f"Commands: {args.commands}")
    if trace_summary["paths"]:
        print("Paths:")
        for path in trace_summary["paths"]:
            print(f"  - {path}")
    if findings:
        print("Findings:")
        for finding in findings:
            print(f"  - {finding}")
    else:
        print("Findings: none")
    if args.notes:
        print(f"Notes: {args.notes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
