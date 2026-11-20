"""Session 1 receiver checks: real DOCX, real runner and literal provenance."""
from copy import deepcopy
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import zipfile

from fastapi.testclient import TestClient

from backend.main import app
from backend.demo import ROOT, SAMPLES
from backend.app.pipeline import AnalysisOutcome, DocumentInput, run_comparison
from backend.app.schemas.report_validation import validate_report
from test.demo_suite.test_web_demo import base_docx, amendment_docx


class SessionOneBackendTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    def compare(self, base, amendment):
        response = self.client.post('/api/compare', files={
            'base_file': ('v1.docx', base), 'amendment_file': ('s.docx', amendment)})
        self.assertEqual(response.status_code, 200, response.text[:500])
        report = response.json()
        validate_report(report)
        return report

    def test_real_cases_via_main_api_and_canonical_fields(self):
        expected = {'case_01': (2, 1), 'case_02': (1, 1), 'case_03': (13, 13)}
        for case, sample in SAMPLES.items():
            with self.subTest(case=case):
                directory = ROOT / 'data/raw' / case
                report = self.compare((directory / sample['v1']).read_bytes(),
                                      (directory / sample['s']).read_bytes())
                self.assertEqual(report['status'], 'PARTIAL')
                self.assertEqual((len(report['results']), sum(r['text_diff'] is not None
                                                             for r in report['results'])), expected[case])
                if case == 'case_02':
                    item = report['results'][0]['amendment']
                    self.assertEqual(item['target_locator'], 'Điều 16 / khoản 5')
                    self.assertTrue(item['context']['general_context'])
                    self.assertTrue(any(e['document_id'] == 'v1' for e in item['context']['evidence']))
                if case == 'case_01':
                    self.assertIn('OTHER_DOCUMENT', {r['amendment']['applicability'] for r in report['results']})

    def test_inline_replacement_does_not_use_payload_locator(self):
        report = self.compare(base_docx('Điều 2. Nội dung', '2. Nội dung cũ.'),
            amendment_docx('Sửa đổi khoản 2 Điều 2 như sau: “2. Áp dụng Điều 99.”'))
        item = report['results'][0]['amendment']
        self.assertEqual(item['target_locator'], 'Điều 2 / khoản 2')
        self.assertEqual(item['after_text'], '2. Áp dụng Điều 99.')
        self.assertEqual(item['after_basis'], 'QUOTED')
        self.assertIsNotNone(report['results'][0]['text_diff'])

    def test_phrase_payload_mentions_article_without_changing_target(self):
        report = self.compare(base_docx('Điều 2. Nội dung', 'Áp dụng Điều 3.'),
            amendment_docx('Thay cụm từ “Điều 3” bằng “Điều 4” tại Điều 2.'))
        self.assertEqual(report['results'][0]['amendment']['after_text'], 'Điều 2. Nội dung\nÁp dụng Điều 4.')

    def test_scope_and_parent_are_readable_after_request_cleanup(self):
        report = self.compare(base_docx('Điều 2. Phạm vi', 'Câu dẫn.', '1. Trong 30 ngày.'),
            amendment_docx('Thay cụm từ “30 ngày” bằng “15 ngày” tại khoản 1 Điều 2.'))
        item = report['results'][0]['amendment']
        refs = item['context']['evidence']
        self.assertTrue(any('Câu dẫn.' in e['quote'] for e in refs))
        self.assertTrue(any('Văn bản mẫu A' in e['quote'] and e['document_id'] == 's' for e in refs))
        # Derived output never becomes a fabricated source quote.
        self.assertFalse(any(e['quote'] == item['after_text'] for e in refs))

    def test_missing_alias_and_duplicate_alias_are_rejected(self):
        self.assertEqual(self.client.post('/api/compare').status_code, 422)
        response = self.client.post('/api/compare', files={
            'base_file': ('a.docx', base_docx('Điều 1. A')),
            'doc_v1': ('b.docx', base_docx('Điều 1. B')),
            'amendment_file': ('s.docx', amendment_docx('Bãi bỏ Điều 1.'))})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail']['code'], 'AMBIGUOUS_INPUT')

    def test_failed_business_report_is_200_and_retains_instruction(self):
        report = self.compare(base_docx('Điều 2. A', 'Nội dung.'),
                              amendment_docx('Bãi bỏ Điều 2.'))
        self.assertEqual(report['status'], 'FAILED')
        self.assertEqual(report['results'][0]['amendment']['instruction']['quote'], 'Bãi bỏ Điều 2.')
        self.assertFalse(report['errors'])

    def test_corrupt_docx_container_reports_input_error(self):
        stream = BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive:
            archive.writestr('unrelated.txt', 'not a DOCX document')
        response = self.client.post('/api/compare', files={
            'base_file': ('invalid.docx', stream.getvalue()),
            'amendment_file': ('s.docx', amendment_docx('Bãi bỏ Điều 2.'))})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail']['code'], 'UNREADABLE_DOCUMENT')

    def test_one_module_failure_keeps_instruction_and_usable_sibling(self):
        # Test-only failure injection; raw acceptance cases use the real modules.
        from backend.app.change_analysis.text_diff import compute_text_diff
        def fail_first(item):
            if item['amendment_id'].endswith('_1'):
                raise RuntimeError('test-only module failure')
            return compute_text_diff(item)
        with patch('backend.app.demo_runner.compute_text_diff', side_effect=fail_first):
            report = self.compare(base_docx('Điều 2. Nội dung', '30 ngày.'),
                amendment_docx('Thay cụm từ “30 ngày” bằng “15 ngày” tại Điều 2.',
                               'Thay cụm từ “30 ngày” bằng “20 ngày” tại Điều 2.'))
        self.assertEqual(report['status'], 'PARTIAL')
        self.assertEqual(len(report['results']), 2)
        self.assertIsNone(report['results'][0]['text_diff'])
        self.assertIsNotNone(report['results'][1]['text_diff'])
        self.assertIn('ANALYSIS_UNRESOLVED', {w['code'] for w in report['warnings']})

    def test_pipeline_rejects_runner_with_forged_provenance(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            a, b = root / 'a.docx', root / 'b.docx'
            a.write_bytes(base_docx('Điều 2. Nội dung', '30 ngày.'))
            b.write_bytes(amendment_docx('Thay cụm từ “30 ngày” bằng “15 ngày” tại Điều 2.'))
            documents = [DocumentInput('v1', 'BASE', a.name, a), DocumentInput('s', 'AMENDMENT', b.name, b)]
            from backend.app.demo_runner import run_demo_analysis
            def forged(parsed, comparison_id, deadline):
                outcome = deepcopy(run_demo_analysis(parsed, comparison_id, deadline))
                outcome.results[0]['amendment']['instruction']['source_refs'] = ['block:999999']
                return outcome
            report = run_comparison(documents, 'forged-source', analysis_runner=forged)
        self.assertEqual(report['status'], 'FAILED')
        self.assertEqual(report['results'], [])
        self.assertIn('PROCESSING_FAILED', {e['code'] for e in report['errors']})


if __name__ == '__main__':
    unittest.main()
