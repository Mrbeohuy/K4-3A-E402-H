from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DotenvConfigTest(unittest.TestCase):
    def test_requirements_include_python_dotenv(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")

        self.assertIn("python-dotenv", requirements)

    def test_requirements_include_pdf_reader_for_local_slides(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")

        self.assertIn("pypdf", requirements)

    def test_gitignore_ignores_local_env_but_allows_example(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

        self.assertIn(".env", gitignore)
        self.assertIn(".env.*", gitignore)
        self.assertIn("!.env.example", gitignore)

    def test_env_example_is_safe(self):
        env_example = (ROOT / ".env.example").read_text(encoding="utf-8")

        self.assertEqual(
            env_example,
            "GEMINI_API_KEY=YOUR_KEY_HERE\nGEMINI_MODEL=gemini-3.6-flash\n",
        )

    def test_entry_points_load_project_root_dotenv_before_cp3_core_import(self):
        for relative_path in ("codebase/server.py", "eval/run_eval.py"):
            source = (ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn('load_dotenv(PROJECT_ROOT / ".env")', source)
            dotenv_index = source.index('load_dotenv(PROJECT_ROOT / ".env")')
            core_import_index = source.index("from cp3_core import")

            self.assertLess(dotenv_index, core_import_index)


if __name__ == "__main__":
    unittest.main()
