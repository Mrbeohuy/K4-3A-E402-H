import json
import sys
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "codebase"))

PROJECT_ROOT = ROOT
load_dotenv(PROJECT_ROOT / ".env")

from cp3_core import (
    MissingApiKeyError,
    answer_question,
    get_configured_api_key,
    grade_case_result,
    load_sources,
    result_to_dict,
    safe_error_text,
    source_id_set,
)


GOLDEN_SET_PATH = ROOT / "eval" / "golden_set.json"
RESULTS_PATH = ROOT / "eval" / "run1-results.json"
SUMMARY_PATH = ROOT / "eval" / "run1-summary.md"
TRACE_PATH = ROOT / "eval" / "traces" / "cp3-run1.jsonl"


def is_api_key_error(message):
    return "API_KEY_INVALID" in message or "API key not valid" in message


def load_cases():
    with GOLDEN_SET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_summary(total, passed, failed, pass_rate, category_counts):
    lines = [
        "# CP3 Run 1 Summary",
        "",
        "This summary is generated only after calling the real AI pipeline.",
        "",
        f"Total: {total}",
        f"Passed: {passed}",
        f"Failed: {failed}",
        f"Pass rate: {pass_rate:.2f}%",
        "",
        "## Category Counts",
        "",
    ]
    for category, count in sorted(category_counts.items()):
        lines.append(f"- {category}: {count}")
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            f"- Results: `{RESULTS_PATH.as_posix()}`",
            f"- Trace: `{TRACE_PATH.as_posix()}`",
        ]
    )
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    try:
        get_configured_api_key()
    except MissingApiKeyError:
        print("CHƯA HOÀN THÀNH CP3 — cần API key thật để chạy Run 1.")
        print("Copy .env.example to .env and fill GEMINI_API_KEY with a real key.")
        return 2

    cases = load_cases()
    if len(cases) < 20:
        raise RuntimeError("Golden set must contain at least 20 cases.")

    if TRACE_PATH.exists():
        TRACE_PATH.unlink()

    sources = load_sources()
    valid_ids = source_id_set(sources)
    results = []
    passed = 0

    for case in cases:
        try:
            result = answer_question(case["input"], case_id=case["id"], trace_path=TRACE_PATH)
            grade = grade_case_result(case, result, valid_ids)
        except Exception as exc:
            error_text = safe_error_text(exc)
            if is_api_key_error(error_text):
                if TRACE_PATH.exists():
                    TRACE_PATH.unlink()
                print("CHƯA HOÀN THÀNH CP3 — GEMINI_API_KEY không hợp lệ.")
                print("Update .env with a real Gemini API key, then run eval again.")
                return 2
            result = None
            grade = {"passed": False, "reason": f"Exception while running case: {error_text}"}

        if grade["passed"]:
            passed += 1

        results.append(
            {
                "case_id": case["id"],
                "category": case["category"],
                "input": case["input"],
                "expected_decision": case["expected_decision"],
                "expected_source_ids": case.get("expected_source_ids", []),
                "output": result_to_dict(result) if result else None,
                "passed": grade["passed"],
                "reason": grade["reason"],
            }
        )

    total = len(cases)
    failed = total - passed
    pass_rate = (passed / total) * 100 if total else 0
    category_counts = Counter(case["category"] for case in cases)

    RESULTS_PATH.write_text(
        json.dumps(
            {
                "total": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": pass_rate,
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_summary(total, passed, failed, pass_rate, category_counts)

    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Pass rate: {pass_rate:.2f}%")
    print(f"Results: {RESULTS_PATH}")
    print(f"Trace: {TRACE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
