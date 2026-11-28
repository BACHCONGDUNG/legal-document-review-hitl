# Bàn giao khảo sát xử lý văn bản

## 1. Mục tiêu

Phụ trách dữ liệu, tìm kiếm văn bản V1 và kết nối Adapter/Linker cho luồng phân tích văn bản pháp luật dân sự.

## 2. Phần đã có trong main

- Các thay đổi Parser từ PR trước đã được tích hợp vào main.

## 3. Phần đang thực hiện

- Khảo sát dữ liệu hiện có trong `data/raw`.
- Khảo sát dataset `th1nhng0/vietnamese-legal-documents`.
- Kiểm tra cấu trúc metadata và relationships để tìm cặp văn bản sửa đổi – văn bản gốc.
- Xác định một ca dân sự thực tế phù hợp với khả năng xử lý hiện tại.
- Chuẩn bị dữ liệu và nguồn đối chiếu để gửi Dũng duyệt.

## 4. Hạng mục còn mở tại thời điểm khảo sát

- Chưa chọn được cặp S–V1 dân sự chính thức.
- Chưa hoàn thành kho dữ liệu dân sự nhỏ có metadata và nguồn đối chiếu.
- Chưa hoàn thành chức năng tự tìm V1 từ chỉ dẫn trong S.
- Chưa có kết quả AmendmentItem thật cho ca dân sự.
- Chưa kiểm chứng các trường hợp thiếu V1 và mơ hồ về đích/phiên bản.
- Chưa ghép kiểm thử với Pipeline và LightRAG.

## 5. Kế hoạch tiếp theo

1. Chọn và gửi Dũng duyệt ca S–V1 dân sự.
2. Chuẩn bị dữ liệu, metadata và bằng chứng nguồn.
3. Tích hợp tìm V1 với Adapter/Linker hiện có.
4. Kiểm tra nội dung trước/sau và nguồn bằng chứng.
5. Bàn giao output cho nhóm phân tích, Context và dữ liệu để ghép luồng.

Xem [demo tìm V1 từ S](shared-web-demo.md) và [pilot đồ thị DOCX](document-graph-pilot.md) để theo dõi tình trạng HCI hiện tại.
