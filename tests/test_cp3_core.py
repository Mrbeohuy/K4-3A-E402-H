import json
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "codebase"))

from cp3_core import (
    DEFAULT_MODEL,
    DecisionResult,
    MissingApiKeyError,
    answer_question,
    build_model_request,
    grade_case_result,
    get_configured_api_key,
    call_gemini,
    load_sources,
    validate_model_output,
)


class CP3CoreTest(unittest.TestCase):
    def test_validate_answer_requires_known_source_id(self):
        raw = json.dumps(
            {
                "decision": "ANSWER",
                "answer": "ReAct alternates reasoning and action.",
                "source_ids": ["DAY3_REACT_01"],
                "reason": "The provided source defines ReAct.",
            }
        )
        result = validate_model_output(raw, {"DAY3_REACT_01"})

        self.assertEqual(result.decision, "ANSWER")
        self.assertEqual(result.source_ids, ["DAY3_REACT_01"])
        self.assertTrue(result.success)

    def test_validate_answer_with_unknown_source_fails_safe(self):
        raw = json.dumps(
            {
                "decision": "ANSWER",
                "answer": "Unsupported answer.",
                "source_ids": ["MADE_UP_SOURCE"],
                "reason": "Bad source.",
            }
        )
        result = validate_model_output(raw, {"DAY3_REACT_01"})

        self.assertEqual(result.decision, "OUT_OF_SCOPE")
        self.assertFalse(result.success)
        self.assertIn("hợp lệ", result.answer)

    def test_build_model_request_includes_sources_and_json_instruction(self):
        sources = [
            {
                "id": "DAY3_REACT_01",
                "title": "Day 3 - ReAct Agent",
                "content": "ReAct alternates reasoning and action.",
                "provenance": "synthetic",
            }
        ]
        payload = build_model_request("ReAct Agent là gì?", sources)
        text = payload["contents"][0]["parts"][0]["text"]

        self.assertIn("DAY3_REACT_01", text)
        self.assertIn("ANSWER", text)
        self.assertIn("CLARIFY", text)
        self.assertIn("OUT_OF_SCOPE", text)
        self.assertIn("JSON", text)

    def test_grade_case_result_checks_decision_and_source_grounding(self):
        case = {
            "id": "TC01",
            "expected_decision": "ANSWER",
            "expected_source_ids": ["DAY3_REACT_01"],
        }
        result = DecisionResult(
            decision="ANSWER",
            answer="ReAct alternates reasoning and action.",
            source_ids=["DAY3_REACT_01"],
            reason="Grounded.",
            success=True,
            raw_text="{}",
        )

        grade = grade_case_result(case, result, {"DAY3_REACT_01"})

        self.assertTrue(grade["passed"])
        self.assertEqual(grade["reason"], "Decision and grounding match expected behavior.")

    def test_load_sources_marks_demo_knowledge_as_synthetic(self):
        sources = load_sources(ROOT / "codebase" / "knowledge_sources.json")

        self.assertGreaterEqual(len(sources), 4)
        self.assertTrue(all(source["provenance"] == "synthetic/demo" for source in sources))

    def test_answer_question_sends_only_retrieved_sources_to_gemini(self):
        retrieved_sources = [
            {
                "id": "VLEARN_T04_SEG_001",
                "title": "VLearn transcript T04-001",
                "content": "LLM course content.",
                "provenance": "data/vlearn-pack/transcript/transcript-04-clean.md#[T04-001]",
            }
        ]
        raw = json.dumps(
            {
                "decision": "ANSWER",
                "answer": "Grounded answer.",
                "source_ids": ["VLEARN_T04_SEG_001"],
                "reason": "The retrieved source supports it.",
            }
        )

        with patch("cp3_core.retrieve_sources", return_value=retrieved_sources) as retrieve, patch(
            "cp3_core.call_gemini", return_value=(raw, "gemini-3.6-flash", 12)
        ) as call, patch("cp3_core.write_trace"):
            result = answer_question("LLM la gi?", api_key="REAL_KEY_FOR_TEST")

        retrieve.assert_called_once_with("LLM la gi?", top_k=5)
        self.assertEqual(call.call_args.args[1], retrieved_sources)
        self.assertEqual(result.decision, "ANSWER")
        self.assertEqual(result.source_ids, ["VLEARN_T04_SEG_001"])

    def test_placeholder_api_key_is_treated_as_missing(self):
        with self.assertRaises(MissingApiKeyError):
            get_configured_api_key("YOUR_KEY_HERE")

    def test_default_model_uses_current_gemini_flash(self):
        self.assertEqual(DEFAULT_MODEL, "gemini-3.6-flash")

    def test_call_gemini_retries_once_on_transient_http_error(self):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback):
                return False

            def read(self):
                return json.dumps(
                    {
                        "candidates": [
                            {
                                "content": {
                                    "parts": [
                                        {
                                            "text": json.dumps(
                                                {
                                                    "decision": "CLARIFY",
                                                    "answer": "Bạn muốn hỏi phần nào?",
                                                    "source_ids": [],
                                                    "reason": "Missing context.",
                                                }
                                            )
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ).encode("utf-8")

        transient_error = urllib.error.HTTPError(
            url="https://example.invalid",
            code=503,
            msg="Unavailable",
            hdrs=None,
            fp=None,
        )
        calls = [transient_error, FakeResponse()]

        def fake_urlopen(request, timeout):
            result = calls.pop(0)
            if isinstance(result, Exception):
                raise result
            return result

        with patch("cp3_core.urllib.request.urlopen", side_effect=fake_urlopen), patch(
            "cp3_core.time.sleep"
        ):
            text, model, latency = call_gemini(
                "cái này là sao?",
                [
                    {
                        "id": "DAY3_REACT_01",
                        "title": "Day 3",
                        "content": "ReAct content.",
                        "provenance": "synthetic/demo",
                    }
                ],
                api_key="REAL_KEY_FOR_TEST",
                model="gemini-3.6-flash",
            )

        self.assertIn("CLARIFY", text)
        self.assertEqual(model, "gemini-3.6-flash")
        self.assertIsInstance(latency, int)


if __name__ == "__main__":
    unittest.main()
