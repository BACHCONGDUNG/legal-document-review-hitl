import unittest

from backend.app.context.civil_semantic_graph import extract_block, extract_attributes, relate, verify_change


class CivilSemanticGraphTests(unittest.TestCase):
    def test_source_spans_and_absent_fields(self):
        text = "Người yêu cầu phải nộp hồ sơ nếu có thay đổi, trừ trường hợp luật có quy định khác."
        attrs = extract_block(text)
        self.assertEqual(attrs["actor"]["value"], "Người yêu cầu")
        self.assertEqual(attrs["modality"]["value"], "phải")
        self.assertEqual(attrs["activity"]["value"], "nộp hồ sơ")
        self.assertTrue(attrs["right_or_duty"]["value"].startswith("phải nộp hồ sơ"))
        self.assertEqual(attrs["condition"]["value"], "nếu có thay đổi")
        self.assertIsNone(attrs["territory"]["value"])
        self.assertEqual(attrs["territory"]["status"], "NOT_FOUND")
        for value in attrs.values():
            if value["value"] is not None:
                self.assertEqual(text[value["start"]:value["end"]], value["value"])

    def test_amendment_payload_is_not_an_active_rule(self):
        tree = {"source_blocks": [{"source_ref": "block:1", "kind": "PARAGRAPH",
                                   "text": "Người yêu cầu phải nộp hồ sơ."}],
                "articles": [{"kind": "ARTICLE", "label": "1", "segments": [], "children": [
                    {"kind": "QUOTATION", "label": None, "segments": [
                        {"source_ref": "block:1", "start": 0, "end": 29}], "children": []}]}]}
        self.assertEqual(list(extract_attributes(tree, "test")), [])

    def test_unrelated_change_does_not_confirm_impact(self):
        edge = {"type": "SEMANTIC", "status": "SUPPORTED", "source": {"article": "6", "document_id": "a"}}
        change = {"kind": "RENAME_ONLY", "target_id": "a", "article": "10",
                  "evidence": {"quote": "Đổi tên cơ quan tại Điều 10"}}
        self.assertEqual(verify_change(edge, change)["status"], "NO_IMPACT_SHOWN")
        change["article"] = "6"
        self.assertEqual(verify_change(edge, change)["status"], "NEEDS_REVIEW")

    def test_same_number_needs_a_grounded_provision(self):
        documents = [{"number": "99/2022/NĐ-CP", "attributes": []},
                     {"number": "21/2021/NĐ-CP", "attributes": []}]
        self.assertEqual(relate(documents), [])
