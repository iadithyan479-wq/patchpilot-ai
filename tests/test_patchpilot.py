import io
import json
import unittest
from argparse import Namespace
from unittest.mock import patch

import patchpilot


class DiffTests(unittest.TestCase):
    def test_stdin_diff(self):
        with patch("sys.stdin", io.StringIO("diff --git a/a b/a\n+hello\n")):
            self.assertIn("+hello", patchpilot.get_diff(Namespace(stdin=True, range=None, base=None)))

    def test_empty_diff_is_rejected(self):
        with patch("sys.stdin", io.StringIO("  ")):
            with self.assertRaisesRegex(patchpilot.PatchPilotError, "No diff found"):
                patchpilot.get_diff(Namespace(stdin=True, range=None, base=None))

    def test_oversized_diff_is_rejected(self):
        with patch("sys.stdin", io.StringIO("x" * (patchpilot.MAX_DIFF_CHARS + 1))):
            with self.assertRaisesRegex(patchpilot.PatchPilotError, "limit"):
                patchpilot.get_diff(Namespace(stdin=True, range=None, base=None))


class ReviewTests(unittest.TestCase):
    def test_review_extracts_message(self):
        response = {"choices": [{"message": {"content": "No actionable findings."}}]}

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return None

            def read(self):
                return json.dumps(response).encode()

        with patch("urllib.request.urlopen", return_value=FakeResponse()) as call:
            result = patchpilot.review("+ code", "test-key", "https://example.test/v1/", "test-model", 5)
        self.assertEqual(result, "No actionable findings.")
        self.assertEqual(call.call_args.args[0].full_url, "https://example.test/v1/chat/completions")

    def test_bad_response_is_reported(self):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return None

            def read(self):
                return b"{}"

        with patch("urllib.request.urlopen", return_value=FakeResponse()):
            with self.assertRaisesRegex(patchpilot.PatchPilotError, "unexpected response"):
                patchpilot.review("+ code", "test-key", "https://example.test/v1", "test-model", 5)


if __name__ == "__main__":
    unittest.main()
