import sys
import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "codebase"))

from local_data import (  # noqa: E402
    DATA_ROOT,
    load_discord_golden_candidates,
    load_vlearn_sources,
    retrieve_sources,
)


class LocalDataTest(unittest.TestCase):
    def test_expected_data_packs_exist(self):
        self.assertTrue((DATA_ROOT / "discord-pack").is_dir())
        self.assertTrue((DATA_ROOT / "vlearn-pack").is_dir())
        self.assertTrue((DATA_ROOT.parent / "codebase").is_dir())
        self.assertTrue((DATA_ROOT.parent / "eval").is_dir())

    def test_loads_real_vlearn_sources_with_stable_ids(self):
        sources = load_vlearn_sources()

        self.assertGreaterEqual(len(sources), 100)
        self.assertTrue(all(source["id"].startswith("VLEARN_") for source in sources))
        self.assertTrue(all(source["provenance"].startswith("data/vlearn-pack/") for source in sources))
        self.assertTrue(any("_SEG_" in source["id"] for source in sources))
        self.assertTrue(any("_SLIDE_" in source["id"] for source in sources))

    def test_retrieval_returns_only_top_k_relevant_snippets(self):
        sources = retrieve_sources("LLM hoat dong nhu the nao?", top_k=5)

        self.assertGreater(len(sources), 0)
        self.assertLessEqual(len(sources), 5)
        self.assertTrue(all(source["id"].startswith("VLEARN_") for source in sources))

    def test_ambiguous_query_does_not_retrieve_context(self):
        self.assertEqual(retrieve_sources("cai nay la sao?", top_k=5), [])

    def test_discord_candidates_are_short_references_not_raw_pack_copy(self):
        candidates = load_discord_golden_candidates(limit=10)

        self.assertGreaterEqual(len(candidates), 10)
        self.assertTrue(all(candidate["msg_id"].startswith("M") for candidate in candidates))
        self.assertTrue(all(len(candidate["excerpt"]) <= 180 for candidate in candidates))

    def test_golden_set_has_required_size_origin_and_categories(self):
        cases = json.loads((ROOT / "eval" / "golden_set.json").read_text(encoding="utf-8"))

        self.assertGreaterEqual(len(cases), 20)
        discord_cases = [
            case for case in cases if case.get("source_provenance") == "discord-pack/k4_messages.csv"
        ]
        self.assertGreaterEqual(len(discord_cases), 10)
        self.assertTrue(all(case.get("chatlog_ref", "").startswith("M") for case in discord_cases))
        self.assertTrue(all(len(case.get("chat_excerpt", "")) <= 180 for case in discord_cases))
        self.assertGreaterEqual(
            {case["category"] for case in cases},
            {"normal", "source_truth", "ambiguous", "out_of_scope", "domain", "rare"},
        )


if __name__ == "__main__":
    unittest.main()
