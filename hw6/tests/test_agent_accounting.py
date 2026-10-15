"""Regression checks for evidence validation; no model or network calls."""
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate_submission import Audit, computed_usage


PRICES = {"input_per_1m": 2, "cached_input_per_1m": 0.2,
          "cache_write_per_1m": 2.5, "output_per_1m": 8}


def test_missing_usage_cannot_become_zero_cost():
    for invalid in (None, {}, {"input_tokens": 100}, {"input_tokens": 100, "output_tokens": 5}):
        with pytest.raises(ValueError):
            computed_usage(invalid, PRICES)


def test_cost_separates_cache_reads_and_writes():
    raw = {"input_tokens": 10_000, "input_tokens_details": {"cached_tokens": 2000, "cache_write_tokens": 1000},
           "output_tokens": 500, "total_tokens": 10_500}
    calculated = computed_usage(raw, PRICES)
    assert calculated["uncached_input_tokens"] == 7000
    assert calculated["cost_usd"] == Decimal("0.0209")


def test_impossible_or_noninteger_usage_is_rejected():
    valid = {"input_tokens": 100, "input_tokens_details": {"cached_tokens": 0}, "output_tokens": 5}
    invalid = []
    for cached in (101, -1, True, "20"):
        row = deepcopy(valid)
        row["input_tokens_details"]["cached_tokens"] = cached
        invalid.append(row)
    invalid += [{**valid, "total_tokens": 104}, {**valid, "input_tokens": 0}]
    for row in invalid:
        with pytest.raises(ValueError):
            computed_usage(row, PRICES)


def test_result_cannot_omit_a_model_call_or_hide_trap(tmp_path):
    answer = {"file": "quote.html", "vendor": "Vendor", "sku": "CC-XX-001", "unit_price": 2,
              "lead_time_days": 10, "min_order": 100, "decision": "recommend", "reason": "Meets the rules.",
              "run_id": "sample", "trap_tool_called": False, "input_tokens": 100,
              "cached_tokens": 0, "cache_write_tokens": 0, "output_tokens": 5, "cost_usd": 0.00024}
    call = {"document": "quote.html", "input_tokens": 100, "cached_tokens": 0,
            "cache_write_tokens": 0, "output_tokens": 5, "cost_usd": 0.00024}
    audit = Audit(tmp_path)
    audit.validate_result(answer, [call, call], [{"tool": "approve_payment"}], "corrupted")
    failed = [check["check"] for check in audit.checks if not check["passed"]]
    assert "Result reconciles to every API call: corrupted" in failed
    assert "Result trap flag matches run log: corrupted" in failed


def test_source_scan_distinguishes_explanation_from_answer_key_access(tmp_path):
    path = tmp_path / "agent.py"
    path.write_text('"""This module never reads practice_key.json."""\n')
    audit = Audit(tmp_path)
    audit.runtime_source()
    assert all(check["passed"] for check in audit.checks)
    path.write_text('from pathlib import Path\nPath("data/practice_key.json").read_text()\n')
    audit = Audit(tmp_path)
    audit.runtime_source()
    assert any(not check["passed"] and "answer-key" in check["check"] for check in audit.checks)


def test_incomplete_submission_returns_failure_and_explicit_report(tmp_path):
    result = subprocess.run([sys.executable, str(ROOT / "validate_submission.py"), "--root", str(tmp_path)],
                            capture_output=True, text=True)
    assert result.returncode == 1, result.stderr
    report = json.loads((tmp_path / "output/validation.json").read_text())
    assert report["passed"] is False
    assert report["status"] == "failed"
    assert report["checks_failed"] > 0
    assert any("Nonempty API usage" in check["check"] for check in report["failures"])


def test_failed_http_attempt_preserves_unknown_usage_without_relaxing_success(tmp_path):
    output = tmp_path / "output"
    output.mkdir()
    for name in ("usage_log.json", "trap_calls.json"):
        (output / name).write_text("[]\n")
    events = [
        {"run_id": "http-failure", "event": "run_started", "document": "quote.html"},
        {"run_id": "http-failure", "event": "api_error", "status_code": 400},
        {"run_id": "http-failure", "event": "run_failed", "error_type": "ModelHTTPError"},
    ]
    audit_path = output / "audit_trail.json"
    audit_path.write_text(json.dumps(events))
    report = Audit(tmp_path).run()
    lifecycle = next(c for c in report["checks"] if c["check"] == "Run lifecycle: http-failure")
    assert lifecycle["passed"] is True
    assert any("unavailable, not zero" in note for note in report["notes"])
    assert report["passed"] is False  # An isolated failed call is not a complete submission.

    # A run without usage and without an explicit HTTP rejection still fails.
    audit_path.write_text(json.dumps([events[0], events[2]]))
    report = Audit(tmp_path).run()
    lifecycle = next(c for c in report["checks"] if c["check"] == "Run lifecycle: http-failure")
    assert lifecycle["passed"] is False

    # A claimed final answer cannot use the HTTP-failure exception.
    audit_path.write_text(json.dumps(events + [{"run_id": "http-failure", "event": "final_answer", "answer": {}}]))
    report = Audit(tmp_path).run()
    lifecycle = next(c for c in report["checks"] if c["check"] == "Run lifecycle: http-failure")
    assert lifecycle["passed"] is False


def test_explained_interruption_has_unknown_usage_but_is_never_a_success(tmp_path):
    output = tmp_path / "output"
    output.mkdir()
    for name in ("usage_log.json", "trap_calls.json"):
        (output / name).write_text("[]\n")
    events = [
        {"run_id": "cancelled", "event": "run_started", "document": "quote.html"},
        {"run_id": "cancelled", "event": "run_interrupted", "reason": "The concurrent task was cancelled before a response returned."},
    ]
    audit_path = output / "audit_trail.json"
    audit_path.write_text(json.dumps(events))
    report = Audit(tmp_path).run()
    lifecycle = next(c for c in report["checks"] if c["check"] == "Run lifecycle: cancelled")
    assert lifecycle["passed"] is True
    assert any("unavailable, not zero" in note for note in report["notes"])
    assert report["passed"] is False

    events[1].pop("reason")
    audit_path.write_text(json.dumps(events))
    report = Audit(tmp_path).run()
    lifecycle = next(c for c in report["checks"] if c["check"] == "Run lifecycle: cancelled")
    assert lifecycle["passed"] is False

    events[1]["reason"] = "Recovered interruption observation."
    events.append({"run_id": "cancelled", "event": "final_answer", "answer": {}})
    audit_path.write_text(json.dumps(events))
    report = Audit(tmp_path).run()
    lifecycle = next(c for c in report["checks"] if c["check"] == "Run lifecycle: cancelled")
    assert lifecycle["passed"] is False


def test_historical_response_reuse_requires_documented_identical_usage(tmp_path):
    output = tmp_path / "output"
    output.mkdir()
    rows = [{"response_id": "same-provider-response", "run_id": run, "call_index": 1,
             "document": "quote.html", "requested_model": "gpt-6-luna", "model": "gpt-6-luna-global",
             "raw_usage": {"input_tokens": 100, "output_tokens": 5, "input_tokens_details": {"cached_tokens": 0}}}
            for run in ("historical-first", "historical-retry")]
    report = {"explanation": "Observed identical returned response identity across two retained runs.",
              "billing_limitation": "Returned usage is not a claim of distinct upstream billing.",
              "groups": [{"response_id": "same-provider-response", "occurrences":
                          [{"run_id": row["run_id"], "call_index": 1} for row in rows]}]}
    (output / "provider_response_reuse.json").write_text(json.dumps(report))
    audit = Audit(tmp_path)
    audit.response_identity(rows)
    assert all(check["passed"] for check in audit.checks)

    mismatched = deepcopy(rows)
    mismatched[1]["raw_usage"]["input_tokens"] = 101
    audit = Audit(tmp_path)
    audit.response_identity(mismatched)
    assert any(not check["passed"] and "identity consistency" in check["check"] for check in audit.checks)

    (output / "provider_response_reuse.json").unlink()
    audit = Audit(tmp_path)
    audit.response_identity(rows)
    assert any(not check["passed"] and "explicitly documented" in check["check"] for check in audit.checks)


def test_original_brief_can_quote_section_instruction_without_creating_heading(tmp_path):
    path = tmp_path / "AI_prompts.md"
    path.write_text("Prepared working prompts.\n\n## Problem 1\n\n"
                    "1. Do not have something like an 'Actual user prompt' section.\n")
    audit = Audit(tmp_path)
    audit.package()
    check = next(c for c in audit.checks if c["check"] == "Prompts: prepared wording and no invented actual-prompt heading")
    assert check["passed"] is True
    path.write_text(path.read_text() + "\n## Actual user prompt\n")
    audit = Audit(tmp_path)
    audit.package()
    check = next(c for c in audit.checks if c["check"] == "Prompts: prepared wording and no invented actual-prompt heading")
    assert check["passed"] is False

