# Tài liệu HCI

Nội dung được duy trì tại [module-owner-decisions-hci.md](module-owner-decisions-hci.md).

## Bổ sung nghiệp vụ hai loại quan hệ — 27/11/2026

Căn cứ yêu cầu Dũng đã chốt trong lần cập nhật tài liệu này; không ghi thành xác nhận mới của Đức Anh hoặc bằng chứng code đã hoàn thành. [BRD §8.7](brd.md#87-hai-loại-quan-hệ-giữa-các-văn-bản) quy định nghiệp vụ; [SRS §1.9](srs.md#19-đặc-tả-mục-tiêu-cho-nút-và-hai-loại-quan-hệ) quy định dữ liệu mục tiêu.

- Giữ hai loại cạnh có hướng độc lập: quan hệ văn bản A nhắc B và quan hệ ngữ nghĩa dựa trên quy định/thuộc tính có nguồn của cả hai. Ưu tiên dựng quan hệ văn bản trước; một cặp nút có thể mang cả hai loại.
- Nút vẫn là văn bản; thuộc tính ngữ nghĩa truy về quy định cụ thể. S → V1 là quan hệ văn bản, cần kiểm chứng đúng đích/phiên bản và thao tác. Có cạnh chưa chứng minh có tác động.
- Tách trạng thái nguồn nút, xác minh cạnh, kiểm chứng tác động và hoàn tất lượt chạy. Giữ dữ liệu thiếu/chưa rõ để rà soát, không tự xác nhận từ similarity, màu hoặc hash.
- Không thay `architecture.md`, phân công LK-01, code, runtime schema hoặc API trong PR tài liệu này. Pilot đồ thị từ hai DOCX và ba bản ghi index không chứng minh đã có kho quan hệ ngữ nghĩa hoặc luồng chỉ S tự tìm V1.

**Còn mở, cần owner/nghiệp vụ chốt trước triển khai:** nghĩa thống nhất A → B ở cạnh ngữ nghĩa (phụ thuộc hay tác động), tiêu chí xanh/vàng/đỏ và chuyển màu, thuật toán/ngưỡng tìm liên hệ, contract/validator/fixture chi tiết. Không mặc định tạo cạnh ngược hoặc lan truyền tác động khi chưa có quy ước và căn cứ.
