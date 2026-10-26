import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

_RESOURCES_DIR = Path(__file__).resolve().parents[2] / "Resources"
if str(_RESOURCES_DIR) not in sys.path:
    sys.path.insert(0, str(_RESOURCES_DIR))

from mvcnn import api


class ModelIntegrityTest(unittest.TestCase):
    def test_every_model_config_pins_a_sha256_digest(self):
        config_paths = sorted(api._CONFIGS_DIR.glob("*/config.json"))
        self.assertEqual(len(config_paths), 8)
        for config_path in config_paths:
            with self.subTest(model=config_path.parent.name):
                config = api._load_config_dict(config_path.parent)
                expected_sha256 = (config.get("predict") or {}).get("model_sha256")
                self.assertEqual(len(api._validate_expected_sha256(expected_sha256)), 64)

    def test_model_digest_matches_expected(self):
        content = b"test model weights"
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / "model.pth"
            model_path.write_bytes(content)

            valid, error = api._validate_model_digest(
                model_path, hashlib.sha256(content).hexdigest()
            )

        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_model_digest_rejects_changed_weights(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / "model.pth"
            model_path.write_bytes(b"changed weights")

            valid, error = api._validate_model_digest(model_path, "0" * 64)

        self.assertFalse(valid)
        self.assertIn("SHA-256 mismatch", error)

    def test_download_rejects_mismatched_digest_without_installing_weights(self):
        content = b"downloaded model weights"
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "model_best.pth"

            def write_download(_curl_exe, _url, partial_path):
                partial_path.write_bytes(content)

            with mock.patch.object(api.shutil, "which", return_value="curl.exe"), mock.patch.object(
                api, "_download_with_curl", side_effect=write_download
            ):
                with self.assertRaisesRegex(RuntimeError, "SHA-256 mismatch"):
                    api._download_model_weights(
                        "https://example.invalid/model.pth",
                        destination,
                        expected_sha256="0" * 64,
                    )

            self.assertFalse(destination.exists())
            self.assertFalse(destination.with_suffix(".pth.part").exists())

    def test_download_installs_weights_after_digest_matches(self):
        content = b"verified model weights"
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "model_best.pth"

            def write_download(_curl_exe, _url, partial_path):
                partial_path.write_bytes(content)

            with mock.patch.object(api.shutil, "which", return_value="curl.exe"), mock.patch.object(
                api, "_download_with_curl", side_effect=write_download
            ):
                result = api._download_model_weights(
                    "https://example.invalid/model.pth",
                    destination,
                    expected_sha256=hashlib.sha256(content).hexdigest(),
                )

            self.assertEqual(result, destination)
            self.assertEqual(destination.read_bytes(), content)


if __name__ == "__main__":
    unittest.main()
