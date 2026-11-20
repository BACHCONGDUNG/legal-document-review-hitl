# HCI-02 — Kế hoạch hiện thực hợp đồng dữ liệu

| Thuộc tính | Nội dung |
| --- | --- |
| Người phụ trách | Dương Đức Anh |
| Trạng thái | Draft |
| Đặc tả | [spec.md](./spec.md) |

## 1. Hướng triển khai

Sử dụng các model Python để định nghĩa và kiểm tra dữ liệu trao đổi giữa các module.

Đề xuất sử dụng Pydantic cho schema vì backend mục tiêu sử dụng FastAPI. Dependency và phiên bản cụ thể sẽ được ghi trong cấu hình môi trường khi triển khai.

Các fixture JSON được kiểm tra bằng schema trước khi bàn giao cho các thành viên.

HCI-02 chưa triển khai API chạy thật hoặc thuật toán phân tích tài liệu.

## 2. Tổ chức file

Các đường dẫn dưới đây tính từ thư mục gốc repository.

| Đường dẫn dự kiến | Trách nhiệm |
| --- | --- |
| `backend/app/schemas.py` | Model dữ liệu chung và các ràng buộc trong từng đối tượng |
| `backend/app/contract_validation.py` | Kiểm tra quan hệ giữa các đối tượng, nguồn và báo cáo |
| `tests/fixtures/contracts/` | Fixture JSON và hướng dẫn sử dụng |
| `tests/test_contracts.py` | Kiểm tra fixture hợp lệ và các trường hợp dữ liệu sai |
| `docs/specs/hci-02-contract/api-contract.md` | Chi tiết đầu vào API, response và lỗi |
| `docs/specs/hci-02-contract/decisions.md` | Quyết định đề xuất, nội dung review và vấn đề còn mở |

Đây là cấu trúc đề xuất. Nếu thay đổi khi triển khai, cập nhật kế hoạch để phản ánh cấu trúc thực tế.

## 3. Các nhóm schema

### 3.1. Nguồn và dữ liệu Reader/Parser

Xác định model cho:

- Định danh tài liệu.
- Khối nguồn và vị trí nguồn.
- Cấu trúc Điều, Khoản, Điểm và nội dung trích dẫn.
- Cảnh báo đọc và tách cấu trúc.

Đọc đầu ra parser hiện tại trước khi quyết định model chung.

Giữ nguyên nội dung và vị trí nguồn khi ánh xạ. Không sửa thuật toán parser trong HCI-02 nếu chưa có nhu cầu được xác định và review với Dũng.

### 3.2. Dữ liệu bàn giao cho phân tích

Xác định model cho:

- Chỉ dẫn sửa đổi và bằng chứng.
- Văn bản, vị trí đích và trạng thái áp dụng.
- Thao tác sửa đổi.
- Nội dung trước–sau và trạng thái tương ứng.
- Ngữ cảnh, tham chiếu và cảnh báo.

Review một mẫu cụ thể với Nam để xác nhận dữ liệu đủ dùng trước khi tích hợp module phân tích.

### 3.3. Kết quả phân tích và báo cáo

Hiện thực các đối tượng theo SRS mục 3:

- DocumentIdentity
- EvidenceRef
- ReferenceRequirement
- ProcessingIssue
- EffectInfo
- ReviewItem
- ChangeAspect
- TextChange
- ComparisonReport

Bổ sung cấu trúc chứa nội dung nguồn trong response sau khi thống nhất với Tùng Dương.

Không đưa nhận xét người dùng vào model đầu ra phân tích.

## 4. Chiến lược kiểm tra dữ liệu

### 4.1. Kiểm tra trong từng đối tượng

Schema kiểm tra:

- Trường bắt buộc và kiểu dữ liệu.
- Giá trị enum.
- Các trường cho phép null.
- Sự nhất quán giữa nội dung trước–sau và trạng thái.
- Lý do khi có bất định hoặc mức tác động.
- Giới hạn vị trí ký tự của TextChange.

Không đặt giá trị mặc định khiến dữ liệu thiếu bị hiểu thành phân tích thành công hoặc không có thay đổi.

### 4.2. Kiểm tra quan hệ giữa các đối tượng

Bộ kiểm tra hợp đồng kiểm tra:

- Định danh tài liệu và mục kết quả không bị trùng trong phạm vi quy định.
- Bằng chứng tham chiếu tới tài liệu và khối nguồn tồn tại.
- Đoạn trích khớp nội dung nguồn theo quy ước đã thống nhất.
- Danh sách mục bị ảnh hưởng tham chiếu tới các mục tồn tại.
- Vị trí TextChange phù hợp với nội dung trước–sau.
- Báo cáo giữ được lỗi và phần chưa xử lý theo spec.

Kiểm tra hợp đồng không chứng minh nhận định pháp lý hoặc kết quả AI là đúng.

## 5. Xây dựng fixture

Hiện thực các trường hợp FX-01 đến FX-07 trong spec.

Mỗi fixture phải có:

- Mô tả tình huống.
- Kết quả mong đợi.
- Nguồn đủ để kiểm tra bằng chứng.
- Ghi chú dữ liệu giả lập hoặc nguồn mẫu thật.

Các trường hợp phân tích lại sử dụng cặp báo cáo trước và sau. Dữ liệu nhận xét mẫu, nếu cần, được lưu riêng theo hợp đồng frontend.

Bổ sung mẫu dữ liệu sai để kiểm tra ít nhất:

- Thiếu trường bắt buộc.
- Enum không hợp lệ.
- Bằng chứng trỏ tới nguồn không tồn tại.
- Trạng thái nội dung mâu thuẫn với giá trị.
- Vị trí TextChange vượt giới hạn chuỗi.

## 6. Hợp đồng API

Ghi chi tiết trong api-contract.md:

- Request multipart cho POST /api/compare.
- Cấu trúc response có báo cáo và nội dung nguồn.
- Cấu trúc error body.
- Quy tắc ánh xạ lỗi sang mã HTTP.
- Giới hạn đầu vào còn cần quyết định.
- Cách phân biệt lỗi request với trạng thái báo cáo.

Các lựa chọn chưa được review phải được ghi là đề xuất.

Không triển khai endpoint thật trong bước này.

## 7. Thứ tự thực hiện

1. Đọc SRS và đầu ra parser hiện tại; ghi các điểm thiếu hoặc chưa thống nhất.
2. Đề xuất cấu trúc dữ liệu và ghi quyết định còn mở.
3. Viết một fixture minh họa nhỏ để kiểm tra luồng bàn giao.
4. Hiện thực schema và bộ kiểm tra hợp đồng.
5. Hoàn thiện các fixture FX-01 đến FX-07.
6. Hoàn thiện hợp đồng API.
7. Chạy kiểm tra dữ liệu hợp lệ và dữ liệu sai.
8. Review với Dũng, Nam và Tùng Dương.
9. Cập nhật hợp đồng, fixture và tài liệu theo kết quả review.

Có thể phát triển trên bản Draft trong lúc chờ review. Không ghi nhận hợp đồng đã thống nhất nếu chưa có xác nhận thực tế.

## 8. Điều kiện hoàn thành

Áp dụng checklist nghiệm thu trong spec.md.

Bàn giao kèm:

- Schema và bộ kiểm tra.
- Fixture và hướng dẫn sử dụng.
- Lệnh chạy kiểm tra cùng kết quả thực tế.
- Các quyết định đã review.
- Những giới hạn và vấn đề còn mở.