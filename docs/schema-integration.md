# Hợp đồng schema và tích hợp HCI
## Hợp đồng đang chạy
Nguồn chuẩn của kiểu dữ liệu và validator nằm tại [contracts.py](../backend/app/schemas/contracts.py), [validation.py](../backend/app/schemas/validation.py) và [report_validation.py](../backend/app/schemas/report_validation.py).
Ứng dụng backend.demo:app nhận doc_v1, doc_s và reference_files. ComparisonReport giữ comparison_id, base_document, amendment_document, reference_documents, status, results, warnings và errors. Mỗi results là một AmendmentResult chứa amendment, context và kết quả theo từng module. semantic_diff.changes và scoring nối theo change_id.
## Phân nhóm và mức tác động
Tám field_group gồm SUBJECT_OBJECT, RIGHTS_DUTIES_ACTIONS, CONDITIONS_EXCEPTIONS, TIME_QUANTITY, PROCEDURE_AUTHORITY, CONSEQUENCES_SANCTIONS, DEFINITIONS_REFERENCES và SCOPE_EFFECT_TRANSITION.
ScoringResult dùng category, significance, is_critical, needs_review và review_reason theo validator. Trường hợp chỉ đổi diễn đạt dùng WORDING_ONLY và LOW. Khi thiếu căn cứ chấm mức, significance và is_critical giữ null cùng lý do review.
## Định danh và bằng chứng
v1/s/ref_* có nghĩa trong một báo cáo cục bộ. EvidenceRef giữ document_id, source_refs và quote. Quote phải khớp nguồn. Nội dung được dựng từ chỉ dẫn giữ nhãn DERIVED, tách với nguyên văn QUOTED.
Fixture giao nhận ở [data/module_handoff_fixtures](../data/module_handoff_fixtures/README.md). Wrapper dùng trong fixture không tự trở thành trường runtime. Đáp án ngữ nghĩa giả định cần được review trước khi dùng làm gold.
## Báo cáo cấp S cần bổ sung
[SRS mục 1.8](srs.md) mô tả lớp bao cho nhiều đích, kho/phiên bản, yêu cầu chưa giải quyết và tác động gián tiếp. Cần chốt kiểu dữ liệu, ID liên kết, null/lỗi, validator và fixture trước khi API/UI nhận hợp đồng mới.
Mỗi đích cần mapping từ ID cục bộ sang văn bản, phiên bản và snapshot kho. Các liên kết tác động gián tiếp cần trỏ đúng target_id, amendment_id và change_id nếu có. Validator cục bộ không xác nhận các liên kết xuyên đích hoặc độ đúng của nhận định tác động.
## Phân công giao nhận
Đức Anh phụ trách schema, Context/LightRAG, linker và Pipeline/API. Nam bàn giao Text Diff, Semantic Diff, Scorer và AI Adapter. Dũng kiểm tra nguồn, đáp án và nghiệp vụ. Tùng Dương đọc báo cáo và biểu diễn bằng chứng trên UI. Hai bên kiểm tra fixture trước khi đổi hợp đồng chung.
## Kiểm chứng và giới hạn
Kết quả tại mốc HCI đã kiểm tra nằm ở [nền HCI](common-baseline.md) và [báo cáo schema](schema-verification-report.md). Hai expected failures ghi giới hạn change_id xuyên chỉ dẫn và tái dựng text từ diff. Chưa có nghiệm thu báo cáo cấp S hoặc dịch vụ thật.
Chạy bốn bộ kiểm thử trong test/schema_suite, test/context_suite, test/demo_suite và test/handoff_suite. Ghi rõ commit, lệnh, kết quả và phần mock hoặc dịch vụ thật.
## Cách chạy
Cài requirements-demo.txt để chạy demo, khởi động backend.demo:app trên cổng 8001 theo [hướng dẫn demo](local-web-demo.md). backend.main:app mặc định chưa gắn runner và trả HTTP 501 với ANALYSIS_NOT_CONFIGURED khi đầu vào hợp lệ. HTTP 200 vẫn có thể chứa báo cáo FAILED.
