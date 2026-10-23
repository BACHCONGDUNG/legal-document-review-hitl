# HCI-02 — Danh sách công việc

**Người phụ trách:** Dương Đức Anh  
**Trạng thái:** Đang thực hiện

## Tài liệu liên quan

- [Đặc tả](./spec.md)
- [Kế hoạch hiện thực](./plan.md)

## 1. Khảo sát đầu ra hiện tại

- [ ] T01 — Đọc hàm parse_docx và file kết quả parser mẫu.
- [ ] T02 — Ghi nhận cấu trúc nguồn, cây Điều/Khoản/Điểm và cảnh báo.
- [ ] T03 — Đối chiếu với SRS, ghi các trường còn thiếu và quyết định cần review trong decisions.md.

**Đầu ra:** Có mô tả đầu ra hiện tại và các điểm cần thống nhất; không thay đổi thuật toán parser.

## 2. Đề xuất hợp đồng dữ liệu

- [ ] T04 — Đề xuất cách ánh xạ đầu ra Reader/Parser sang dữ liệu chung.
- [ ] T05 — Đề xuất cấu trúc đầu vào và đầu ra module phân tích.
- [ ] T06 — Đề xuất cách trả báo cáo cùng nội dung nguồn.
- [ ] T07 — Viết một fixture nhỏ để minh họa luồng chỉ dẫn → trước–sau → kết quả → bằng chứng.

**Đầu ra:** Các đề xuất và mẫu dữ liệu có thể dùng để review với Dũng, Nam và Tùng Dương.

## 3. Hiện thực schema và kiểm tra hợp đồng

- [ ] T08 — Chuẩn bị môi trường Python, ghi dependency và lệnh cài đặt.
- [ ] T09 — Hiện thực model định danh tài liệu, nguồn và dữ liệu Reader/Parser.
- [ ] T10 — Hiện thực model dữ liệu bàn giao cho phân tích.
- [ ] T11 — Hiện thực model kết quả phân tích và báo cáo theo SRS.
- [ ] T12 — Hiện thực các ràng buộc trong từng đối tượng.
- [ ] T13 — Hiện thực kiểm tra quan hệ giữa báo cáo, tài liệu, mục kết quả và bằng chứng.

**Đầu ra:** Schema và bộ kiểm tra chạy được trên fixture minh họa.

## 4. Hoàn thiện fixture và hợp đồng API

- [ ] T14 — Hoàn thiện fixture FX-01 đến FX-05.
- [ ] T15 — Hoàn thiện cặp báo cáo trước–sau cho FX-06 và FX-07.
- [ ] T16 — Ghi mô tả, kết quả mong đợi và nguồn gốc của từng fixture.
- [ ] T17 — Viết api-contract.md: request, response, error body và mã HTTP đề xuất.
- [ ] T18 — Ghi các giới hạn cấu hình còn cần quyết định.

**Đầu ra:** Bộ fixture và hợp đồng API; phân biệt rõ nội dung đề xuất với quyết định đã thống nhất.

## 5. Kiểm chứng

- [ ] T19 — Kiểm tra toàn bộ fixture hợp lệ được chấp nhận.
- [ ] T20 — Kiểm tra từ chối trường bắt buộc bị thiếu và enum không hợp lệ.
- [ ] T21 — Kiểm tra phát hiện bằng chứng trỏ tới nguồn không tồn tại.
- [ ] T22 — Kiểm tra phát hiện trạng thái nội dung mâu thuẫn với giá trị.
- [ ] T23 — Kiểm tra phát hiện vị trí TextChange vượt giới hạn chuỗi.
- [ ] T24 — Ghi lệnh chạy, kết quả thực tế và giới hạn của việc kiểm tra.

**Đầu ra:** Kết quả kiểm tra có thể chạy lại.

## 6. Review và bàn giao

- [ ] T25 — Review hợp đồng Reader/Parser với Dũng.
- [ ] T26 — Review đầu vào và đầu ra phân tích với Nam.
- [ ] T27 — Review báo cáo, nguồn và dữ liệu phân tích lại với Tùng Dương.
- [ ] T28 — Cập nhật schema, fixture và tài liệu theo kết quả review.
- [ ] T29 — Chạy lại các kiểm tra bị ảnh hưởng.
- [ ] T30 — Đối chiếu checklist nghiệm thu trong spec.md và ghi các vấn đề còn mở.

**Đầu ra:** Hợp đồng bàn giao được các bên sử dụng; những phần chưa thống nhất vẫn được ghi rõ.

## Quy tắc cập nhật

- Chỉ đánh dấu hoàn thành khi đã có đầu ra tương ứng.
- Không đánh dấu review hoàn thành khi chưa có phản hồi thực tế.
- Có thể triển khai trên bản Draft trong lúc chờ review.
- Khi thay đổi cách hiện thực, cập nhật plan.md và các task bị ảnh hưởng.