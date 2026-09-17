import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUN_EVAL_PATH = ROOT / "eval" / "run_eval.py"


def load_run_eval_module():
    spec = importlib.util.spec_from_file_location("run_eval_module", RUN_EVAL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RunEvalTest(unittest.TestCase):
    def test_detects_invalid_api_key_errors(self):
        module = load_run_eval_module()

        self.assertTrue(module.is_api_key_error("Gemini HTTP 400: API_KEY_INVALID"))
        self.assertTrue(module.is_api_key_error("API key not valid. Please pass a valid API key."))
        self.assertFalse(module.is_api_key_error("Gemini HTTP 429: rate limit"))


if __name__ == "__main__":
    unittest.main()
