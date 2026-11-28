# Nhóm 6 — Legal Document Change Detection

**HCI, Nhóm 6 — cập nhật 22/11/2026.** Phạm vi chỉ S, kho dân sự, nhiều đích và tác động gián tiếp là thiết kế mục tiêu. Hiện trạng mã và kết quả kiểm tra HCI được ghi tại [nền HCI](common-baseline.md). Phân công theo [module](module.md). Công việc nghiên cứu ngắn hạn được theo dõi trong tài liệu tiến độ của nhóm.


Mục tiêu HCI: từ một S, tự tìm đích/phiên bản trong kho dân sự nhóm chuẩn bị, giải thích thay đổi trực tiếp và kiểm chứng tác động gián tiếp. Nền đang chạy vẫn là demo V1 + S; xem [nền chung](common-baseline.md) để phân biệt code với mục tiêu.

- [BRD](brd.md), [SRS](srs.md), [Architecture](architecture.md)
- [Module](module.md), [Decision](module-owner-decisions-hci.md), [Workflow](workflow.md)
- [Kế hoạch theo phiên code](implementation-plan-hci.md), [Kế hoạch kiểm thử và đánh giá](test_evaluation_plan.md)
- [Hướng dẫn gán nhãn](data-annotation-guide-hci.md), [Tích hợp và kiểm tra schema](schema-integration.md)
- [Nền chung đang chạy và việc còn thiếu](common-baseline.md), [Cách mở web demo](local-web-demo.md)
- [Fixture bàn giao](../data/module_handoff_fixtures/README.md), [Báo cáo schema lịch sử](schema-verification-report.md)

Luồng mục tiêu nhận S, bối cảnh/nguồn bổ sung tùy chọn và trả báo cáo cấp S. Request đồng bộ là phương án dự kiến, cần đo trên ca nhiều đích và tác động gián tiếp. Các module backend bàn giao theo schema chung. LightRAG là dịch vụ retrieval riêng qua HTTP. Xem [luồng xử lý](architecture.md) để tra sơ đồ và vòng đời nguồn.

Cấu trúc chuẩn lấy từ `main`. [Architecture §3](architecture.md) định vị code hiện có và phân biệt các chức năng mục tiêu chưa có file.

Change F1 ≥ 90% và Critical Change Recall ≥ 95% là các ngưỡng dự tính. Xem [kế hoạch đánh giá](test_evaluation_plan.md) để tra phương pháp đo và mốc xác nhận.

- [Docker và cấu hình LightRAG](../deploy/lightrag/README.md)
- [Demo web dùng chung](shared-web-demo.md)
- [Hợp đồng và kiểm thử Context](context-handoff.md)

## Bổ sung nghiệp vụ quan hệ — 27/11/2026

[BRD §8.7](brd.md#87-hai-loại-quan-hệ-giữa-các-văn-bản) và [SRS §1.9](srs.md#19-đặc-tả-mục-tiêu-cho-nút-và-hai-loại-quan-hệ) phân biệt quan hệ văn bản A nhắc B với quan hệ ngữ nghĩa dựa trên nội dung, cùng dữ liệu nguồn và quy tắc kiểm chứng tác động. Xem [quyết định và điểm còn mở](decision.md#bổ-sung-nghiệp-vụ-hai-loại-quan-hệ--27112026), [gán nhãn](data-annotation-guide-hci.md#48-thuộc-tính-và-hai-loại-quan-hệ-giữa-các-văn-bản), [điểm nối schema](schema-integration.md#đặc-tả-mở-rộng-quan-hệ-ngày-27112026) và [ca kiểm chứng RG](test_evaluation_plan.md#ca-kiểm-chứng-hai-loại-quan-hệ--27112026). Đây là đặc tả mục tiêu, không xác nhận đã có code cho mọi yêu cầu.

- [Đồ thị văn bản DOCX](document-graph-pilot.md)
- [Bàn giao khảo sát xử lý văn bản](document-processing-progress.md)

- [Demo đồ thị toàn kho trên web](document-relation-graph.md)
