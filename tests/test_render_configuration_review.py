"""The Render configuration review reports key names, never API values."""

from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import render_configuration_review as review


class RenderConfigurationReviewTests(unittest.TestCase):
    def test_direct_keys_discard_values_and_follow_cursor(self):
        secret = "private-token-must-not-appear"
        first = [{"envVar": {"key": f"KEY_{i}", "value": secret}, "cursor": str(i)}
                 for i in range(100)]
        second = [{"envVar": {"key": "FINAL_KEY", "value": secret}, "cursor": "end"}]
        paths = []

        def get(path, _token):
            paths.append(path)
            return first if len(paths) == 1 else second

        names = review.direct_keys("srv-example", "credential", get)
        self.assertEqual(len(names), 101)
        self.assertIn("FINAL_KEY", names)
        self.assertNotIn(secret, repr(names))
        self.assertIn("cursor=99", paths[1])

    def test_remote_only_is_not_a_deletion_instruction(self):
        class FakeSource:
            def __init__(self, *_args):
                pass

        old = {"keys": [{"name": "OLD_KEY"}, {"name": "SHARED_KEY"}], "blockers": []}
        candidate = {"keys": [{"name": "NEW_KEY", "phase": "build", "sources": ["example"]},
                              {"name": "SHARED_KEY", "phase": "build", "sources": ["example"]}],
                     "blockers": []}
        original_source, original_catalog = review.GitSource, review.config_catalog
        try:
            review.GitSource = FakeSource
            review.config_catalog = lambda *_args: old
            result = review.build_review("animation", {"service_id": "srv-example", "sha": "a" * 40,
                                                        "configuration": {"catalog": candidate}},
                                         "b" * 40, ["OLD_KEY", "SHARED_KEY", "EXTERNAL_KEY"], [], "now")
        finally:
            review.GitSource, review.config_catalog = original_source, original_catalog
        self.assertEqual(result["new_candidate_keys_absent_from_direct_render_configuration"], ["NEW_KEY"])
        self.assertEqual(result["formerly_referenced_keys_still_on_render"], ["OLD_KEY"])
        self.assertEqual(result["render_keys_outside_candidate_catalog"], ["EXTERNAL_KEY", "OLD_KEY"])
        self.assertFalse(result["reviewed"])
        self.assertIn("not approved for deletion", result["interpretation"])

    def test_incomplete_environment_group_inventory_refused(self):
        with self.assertRaisesRegex(review.ReviewError, "incomplete"):
            review.group_links("tea-example", {"srv-example"}, "credential",
                               lambda *_args: [{}] * 100)

    def test_request_collection_writes_names_only_and_keeps_review_pending(self):
        root = Path(__file__).resolve().parents[1]
        inventory = review.release.read_json(root / review.release.INVENTORY)["environments"]["demo"]
        service = inventory["services"]["animation"]
        service_id = service["render_service_id_verified"]
        secret = "private-render-value-must-not-appear"
        candidate = review.release.quality.snapshot(root, review.release.quality.load_registry(root))["localeo-animation"]["sha"]
        request = {"schema_version": 1, "environment": "demo", "applications": {"animation": candidate},
                   "documentation_sha": "a" * 40}

        def get(path, _token):
            if path.startswith("/env-groups?"):
                return []
            if path == f"/services/{service_id}":
                return {"id": service_id, "ownerId": inventory["render_workspace_id_verified"],
                        "branch": "demo", "name": service["render_name_verified"],
                        "environmentId": service["render_environment_id_verified"],
                        "type": service["render_type_verified"]}
            if path.startswith(f"/services/{service_id}/env-vars?"):
                return [{"envVar": {"key": "VITE_API_URL", "value": secret}, "cursor": "one"}]
            raise AssertionError("Unexpected API path")

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "request.json"
            path.write_text(json.dumps(request), encoding="utf-8")
            output = Path(directory) / "output"
            result = review.collect_request(root, path, None, output, "fake-token", get,
                                            check_output=False)
            self.assertEqual(result["applications"]["animation"]["direct_keys"], ["VITE_API_URL"])
            evidence = json.loads((output / "evidence.with-render-configuration.json").read_text(encoding="utf-8"))
            self.assertEqual(evidence["configuration"]["animation"]["present_keys"], ["VITE_API_URL"])
            self.assertFalse(evidence["configuration"]["animation"]["reviewed"])
            self.assertNotIn(secret, "".join(p.read_text(encoding="utf-8") for p in output.iterdir()))


if __name__ == "__main__":
    unittest.main()
