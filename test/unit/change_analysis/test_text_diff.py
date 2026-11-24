import unittest

from backend.app.change_analysis.text_diff import compute_text_diff


class TextDiffTests(unittest.TestCase):
    def diff(self, before, after):
        return compute_text_diff({
            "amendment_id": "s:amendment_7",
            "before_text": before,
            "after_text": after,
        })

    def assert_reconstructs(self, before, after, result):
        self.assertEqual(result["amendment_id"], "s:amendment_7")
        old_cursor = new_cursor = 0
        parts = []
        for change in result["changes"]:
            old_start, old_end = change["old_start"], change["old_end"]
            new_start, new_end = change["new_start"], change["new_end"]
            self.assertTrue(old_cursor <= old_start <= old_end <= len(before), change)
            self.assertTrue(new_cursor <= new_start <= new_end <= len(after), change)
            unchanged = before[old_cursor:old_start]
            self.assertEqual(unchanged, after[new_cursor:new_start])
            self.assertEqual(before[old_start:old_end], change["old_text"])
            self.assertEqual(after[new_start:new_end], change["new_text"])
            parts.extend((unchanged, change["new_text"]))
            old_cursor, new_cursor = old_end, new_end
        parts.append(before[old_cursor:])
        self.assertEqual("".join(parts), after)

    def test_missing_either_side_skips_diff(self):
        for before, after in ((None, "Điều 1"), ("Điều 1", None)):
            with self.subTest(before=before, after=after):
                self.assertIsNone(self.diff(before, after))

    def test_identical_inputs_have_no_changes(self):
        for text in ("Điều 1\nNội dung.", ""):
            with self.subTest(text=text):
                self.assertEqual(
                    self.diff(text, text),
                    {"amendment_id": "s:amendment_7", "changes": []},
                )

    def test_insert_and_delete_use_zero_width_ranges_on_the_empty_side(self):
        cases = (
            ("nộp", "phải nộp", ("INSERT", "", "phải ", 0, 0, 0, 5)),
            ("nộp.", "nộp", ("DELETE", ".", "", 3, 4, 3, 3)),
            ("", "Điều 1", ("INSERT", "", "Điều 1", 0, 0, 0, 6)),
            ("Điều 1", "", ("DELETE", "Điều 1", "", 0, 6, 0, 0)),
        )
        keys = ("type", "old_text", "new_text", "old_start", "old_end", "new_start", "new_end")
        for before, after, expected in cases:
            with self.subTest(before=before, after=after):
                result = self.diff(before, after)
                self.assertEqual(result["changes"], [dict(zip(keys, expected))])
                self.assert_reconstructs(before, after, result)

    def test_repeated_phrases_keep_unchanged_text_between_edits(self):
        before = "A: 30 ngày. B: 30 ngày."
        after = "A: 15 ngày. B: 20 ngày."
        result = self.diff(before, after)

        self.assert_reconstructs(before, after, result)
        separator = " ngày. B: "
        old_start, new_start = before.index(separator), after.index(separator)
        for change in result["changes"]:
            self.assertTrue(change["old_end"] <= old_start or
                            change["old_start"] >= old_start + len(separator), change)
            self.assertTrue(change["new_end"] <= new_start or
                            change["new_start"] >= new_start + len(separator), change)

    def test_offsets_use_python_code_points_in_original_multiline_text(self):
        before = "Điều 2\n📄 đie\u0302\u0300u, hạn: 30 ngày."
        after = "Điều 2\n📄 đie\u0302\u0300u, hạn: 15 ngày."
        result = self.diff(before, after)

        self.assertEqual(result["changes"], [{
            "type": "REPLACE",
            "old_text": "30",
            "new_text": "15",
            "old_start": 22,
            "old_end": 24,
            "new_start": 22,
            "new_end": 24,
        }])
        self.assert_reconstructs(before, after, result)
