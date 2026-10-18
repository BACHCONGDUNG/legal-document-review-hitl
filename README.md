# Human-in-the-Loop System for Reviewing Legal Document Changes with Explainable AI

## 1. Giới thiệu dự án

**Học phần:** Tương tác người máy (HCI)  
**Nhóm:** 2627I_INT2041_1 Nhóm 6

Dự án xây dựng hệ thống hỗ trợ đối chiếu văn bản pháp luật gốc với văn bản sửa đổi, trình bày thay đổi cùng giải thích và bằng chứng để người dùng kiểm tra. Trọng tâm HCI là giúp người dùng tìm đúng nội dung, hiểu kết quả và ghi nhận xét trong quá trình rà soát.

## 2. Chức năng và phạm vi

Các chức năng mục tiêu:

- Nhận văn bản gốc **V1**, văn bản sửa đổi **S** và tài liệu tham chiếu khi cần. S chứa chỉ dẫn sửa đổi V1, không phải bản V2 đầy đủ.
- Xác định vị trí và thao tác sửa đổi; trình bày nội dung trước–sau tại phần bị tác động.
- Phân tích các loại thay đổi có thể kiểm chứng như thời hạn, giá trị định lượng, điều kiện, chủ thể và quyền/nghĩa vụ; hiển thị giải thích, bằng chứng và phần chưa chắc chắn.
- Hỗ trợ xem nguồn, lọc kết quả, ghi nhận xét và rà soát lại sau khi bổ sung tài liệu.
- Trả kết quả ban đầu kèm danh sách tài liệu còn thiếu nếu chưa đủ căn cứ phân tích.

**Dữ liệu đầu vào:** DOCX hoặc PDF có lớp chữ. PDF được chuyển thành file DOCX; các module tiếp theo làm việc với DOCX. PDF scan chưa được hỗ trợ. Bộ chuyển đổi hoạt động chỉ với PDF, không yêu cầu có sẵn DOCX đối chiếu.

Hệ thống hỗ trợ người dùng kiểm chứng; không đặt mục tiêu tự hiểu toàn bộ ý nghĩa pháp lý hoặc tự kết luận mọi thay đổi đều đã được phân tích đầy đủ.

## 3. Cấu trúc thư mục

Các đường dẫn dùng để tổ chức mã nguồn, tài liệu và chạy thử:

| Đường dẫn | Mục đích |
| --- | --- |
| `README.md` | Giới thiệu và hướng dẫn bắt đầu; đặt tại thư mục gốc repository |
| `docs/` | BRD, SRS, Architecture, Implementation Plan và các tài liệu chuyên trách |
| `backend/app/document_processing/pdf_to_docx.py` | Bộ chuyển đổi PDF có lớp chữ sang DOCX |
| `data/test_pdf_to_docx/case_01/` | Dữ liệu và kết quả chạy thử bộ chuyển đổi |

`frontend/` dành cho giao diện và `tests/` dành cho kiểm thử tự động sẽ được bổ sung khi triển khai các phần tương ứng. Cấu trúc module chi tiết được mô tả trong [Architecture](docs/architecture.md).

## 4. Cài đặt và chạy thử

Hướng dẫn hiện tại dành cho bộ chuyển đổi PDF → DOCX. Mở terminal tại thư mục gốc repository và bảo đảm file Python đã nằm đúng đường dẫn ở mục 3.

### 4.1. Chuẩn bị môi trường

Sử dụng Python 3.12 và môi trường ảo riêng. Trên Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pdf2docx python-docx "pymupdf>=1.24.2"
```

Các lệnh dưới đây gọi trực tiếp Python trong môi trường ảo, không cần kích hoạt `.venv`. Bộ chuyển đổi không yêu cầu API key hoặc dịch vụ AI.

### 4.2. Chuẩn bị dữ liệu và chuyển đổi

Đặt PDF có lớp chữ tại `data/test_pdf_to_docx/case_01/input.pdf`, rồi chạy:

```powershell
.\.venv\Scripts\python.exe backend/app/document_processing/pdf_to_docx.py "data/test_pdf_to_docx/case_01/input.pdf" "data/test_pdf_to_docx/case_01/converted.docx"
```

Với văn bản sửa đổi S hoặc tài liệu tham chiếu, thêm `--kind other` để không áp dụng bước tách nhãn và nối đoạn dành cho V1:

```powershell
.\.venv\Scripts\python.exe backend/app/document_processing/pdf_to_docx.py "data/test_pdf_to_docx/case_01/input.pdf" "data/test_pdf_to_docx/case_01/converted_other.docx" --kind other
```

Mỗi lần chạy thành công tạo **hai file**:

- `converted.docx`: văn bản sau chuyển đổi và chuẩn hóa.
- `converted.report.json`: các thay đổi đã áp dụng, vị trí liên quan và nội dung cần kiểm tra.

File trung gian được tạo tạm và tự xóa khi kết thúc; không xuất file `converted.raw.docx`. Chương trình không ghi đè kết quả đã có: khi chạy lại, chọn tên mới như `converted_v2.docx`.

Sau khi chạy, kiểm tra DOCX và các mục `warnings`, `pdf_alignment.needs_review` trong report. Tạo được file chưa đồng nghĩa mọi nội dung và bố cục đều chính xác. DOCX đối chiếu, nếu có trong bộ thử nghiệm, chỉ phục vụ đánh giá bên ngoài bộ chuyển đổi.

## 5. Tình trạng triển khai và giới hạn

| Thành phần | Tình trạng |
| --- | --- |
| Bộ chuyển đổi PDF → DOCX | Đã có mã nguồn và chạy thử trên case 01; xử lý khoảng trắng theo PDF, số trang thừa, đoạn tiếp diễn qua trang và bố cục đầu văn bản của mẫu đã kiểm tra |
| Reader DOCX và tách cấu trúc V1 | Đang trong giai đoạn triển khai nền tảng; chưa xác nhận hoàn tất bàn giao |
| Xử lý chỉ dẫn S, diff/AI, API/Pipeline và frontend | Theo kế hoạch triển khai; chưa công bố bản tích hợp đầu-cuối đã nghiệm thu |
| Đánh giá người dùng | Chưa thực hiện trên sản phẩm hoàn chỉnh; kế hoạch và hạn bàn giao nằm trong Implementation Plan |

Giới hạn hiện tại:

- Kết quả tốt trên case 01 chưa chứng minh chất lượng trên mọi PDF; cần mở rộng mẫu có cấu trúc, bảng và bố cục khác nhau.
- Chưa bảo đảm giữ nguyên toàn bộ bố cục, thứ tự nhiều cột, dấu và chữ ký đồ họa. Phần nơi nhận/chữ ký của case 01 còn hạn chế về thứ tự đọc.
- Các vùng ngoài thân bài đã có đánh dấu hỗ trợ, nhưng Reader/Parser vẫn cần xử lý chúng đúng cách để không lẫn vào Điều/Khoản/Điểm.
- Việc tách paragraph trong bộ chuyển đổi chưa thay thế module tạo cấu trúc V1 và vị trí nguồn cho Pipeline.

Hướng dẫn chạy backend/frontend và cấu hình AI sẽ được bổ sung khi có phiên bản tích hợp chạy được.

## 6. Tài liệu và thành viên

### 6.1. Tài liệu dự án

| Tài liệu | Nội dung chính |
| --- | --- |
| [BRD](docs/brd.md) | Mục tiêu, người dùng và phạm vi nghiệp vụ |
| [SRS](docs/srs.md) | Yêu cầu chức năng và điều kiện nghiệm thu |
| [Architecture](docs/architecture.md) | Thiết kế module, luồng xử lý và giao diện bàn giao |
| [Implementation Plan](docs/implementation-plan.md) | Phân công, phụ thuộc, lịch tuần 6–14 và hạn bàn giao |
| [User Research](docs/user-research.md) | Kết quả nghiên cứu người dùng làm căn cứ thiết kế |
| [Data Annotation Guide](docs/data-annotation-guide.md) | Quy tắc chuẩn bị dữ liệu, gán nhãn và kiểm tra đáp án |

### 6.2. Thành viên

| Thành viên | Vai trò chính |
| --- | --- |
| **Bạch Công Dũng — Nhóm trưởng** | Chuẩn bị tài liệu, dữ liệu và xử lý đầu vào; tổ chức đánh giá sản phẩm với người dùng |
| **Dương Đức Anh** | Xây dựng backend, xử lý chỉ dẫn sửa đổi và tích hợp luồng phân tích |
| **Lê Tùng Dương** | Thiết kế tương tác và frontend, hỗ trợ đối chiếu và ghi nhận xét trong phiên |
| **Vương Thành Nam** | Xây dựng diff, phân tích AI, mức tác động và đánh giá chất lượng phân tích |
