# HCI — Hệ thống hỗ trợ rà soát thay đổi văn bản pháp luật

## 1. Giới thiệu dự án

Dự án hỗ trợ rà soát thay đổi trong văn bản quy phạm pháp luật tiếng Việt, hướng tới luật sư, người làm pháp chế và người nghiên cứu luật. Mục tiêu là giúp người dùng nhận biết thay đổi về nội dung quy định, phân biệt với thay đổi diễn đạt và đối chiếu kết quả với bằng chứng nguồn.

## 2. Chức năng và phạm vi

Đầu vào gồm văn bản ban đầu **V1**, văn bản sửa đổi **S** và tài liệu tham chiếu nếu cần. S chứa chỉ dẫn sửa đổi, không phải bản đầy đủ sau sửa đổi V2.

Hệ thống được thiết kế để:

- Nhận diện yêu cầu sửa đổi, bổ sung hoặc bãi bỏ trong S và tìm nội dung đích trong V1.
- Đối chiếu nội dung trước/sau cục bộ, phân tích thay đổi nghĩa và mức tác động.
- Cung cấp bằng chứng, thông tin hiệu lực/chuyển tiếp được nêu trong nguồn và cảnh báo khi thiếu căn cứ.
- Hỗ trợ DOCX và PDF có lớp chữ; bổ sung truy xuất ngữ cảnh bằng LightRAG.

Phiên bản đầu không hỗ trợ OCR/PDF scan, không bắt buộc dựng V2 đầy đủ và không tự xác minh hiệu lực pháp lý thực tế. Kết quả phục vụ rà soát, cần được người dùng kiểm chứng.

## 3. Bản demo hiện tại

POST `/api/compare` nhận multipart `doc_v1`, `doc_s` và `reference_files` tùy chọn. `ComparisonReport` gồm `comparison_id`, `base_document`, `amendment_document`, `reference_documents`, `status`, `results`, `warnings` và `errors`. Mỗi phần tử `results` là một `AmendmentResult`.

Demo xử lý DOCX bằng quy tắc cục bộ. Kết quả còn thiếu căn cứ được hiển thị cùng cảnh báo và lý do. PDF có lớp chữ đi qua bộ chuyển PDF → DOCX và cần kiểm chứng xuyên luồng. Nhận xét trong phiên và kiểm tra lại là phần mở rộng HCI.

## 4. Cài đặt và chạy

Chạy từ thư mục gốc bằng Python 3.11 trở lên. Khuyến nghị Python 3.12.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-demo.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m uvicorn backend.demo:app --host 127.0.0.1 --port 8001
```

Mở [giao diện demo](http://127.0.0.1:8001) để tải V1, S và tài liệu tham chiếu hoặc chọn bộ DOCX mẫu. [OpenAPI](http://127.0.0.1:8001/docs) mô tả API đang chạy. `backend.main:app` cũng đã gắn runner DOCX cục bộ của Phiên 1. API nhận thêm `base_file`/`amendment_file` tương ứng với `doc_v1`/`doc_s`; không gửi đồng thời hai tên cho cùng vai trò. Contract báo cáo `results` của baseline được giữ nguyên.

Ngữ cảnh cục bộ gồm nguồn chỉ dẫn, tiêu đề phạm vi và đơn vị chứa đích khi nằm trong giới hạn. Trích dẫn giữ nguyên văn và `block:N`; không suy ra trang Word/PDF. ADD, REPEAL và nhiều đích còn chờ chốt phạm vi, được giữ cùng lý do chưa xử lý. Model và LightRAG không được gọi trong Phiên 1. Báo cáo nghiệp vụ `FAILED` vẫn có thể đi cùng HTTP 200; lỗi vận hành dùng HTTP lỗi. Giao diện giữ báo cáo trước khi lượt gửi lại thất bại.

Chạy bốn bộ kiểm thử bằng PowerShell.

```powershell
foreach ($suite in 'schema_suite', 'context_suite', 'demo_suite', 'handoff_suite') {
    .\.venv\Scripts\python.exe -m unittest discover -s "test/$suite" -p "test_*.py" -v
    if ($LASTEXITCODE -ne 0) { break }
}
node --test test/frontend_suite/report-retention.test.cjs
```

LightRAG và model mặc định tắt. Cấu hình mẫu dùng Compose project `hci-lightrag`, cổng host `9622` và workspace `hci_comparison_a`. Compose tạo volume theo tên project. Backend dùng biến `HCI_LIGHTRAG_*` theo mẫu trong repo.

## 5. Tài liệu dự án

- [BRD](docs/brd.md)
- [SRS và hợp đồng API](docs/srs.md)
- [Kiến trúc](docs/architecture.md)
- [Phân công theo module](docs/module.md)
- [Kế hoạch triển khai](docs/implementation-plan-hci.md)
- [Quyết định của module owner](docs/module-owner-decisions-hci.md)
- [Hướng dẫn gán nhãn](docs/data-annotation-guide-hci.md)
- [Fixture bàn giao](data/module_handoff_fixtures/README.md)
- [Kế hoạch kiểm thử và đánh giá](docs/test_evaluation_plan.md)

## 7. Nhóm thực hiện

**Học phần và nhóm:** 2627I_INT2041_1 — Nhóm 6 (HCI)
**Nhóm trưởng:** Bạch Công Dũng

| Thành viên | Phụ trách chính |
| --- | --- |
| Bạch Công Dũng | Điều phối, tài liệu và dữ liệu; xử lý đầu vào, nghiên cứu và đánh giá người dùng |
| Dương Đức Anh | Backend, schema và Pipeline; chỉ dẫn sửa đổi, liên kết, ngữ cảnh và tích hợp |
| Lê Tùng Dương | Thiết kế tương tác, prototype và frontend; đối chiếu, kiểm chứng và nhận xét trong phiên |
| Vương Thành Nam | Text Diff, Semantic Diff, AI Adapter và Scorer; đánh giá kỹ thuật chất lượng phân tích |
