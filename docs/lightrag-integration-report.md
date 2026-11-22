# Tình trạng tích hợp LightRAG HCI
Client HTTP, mapping nguồn và kiểm thử mô phỏng nằm trong backend/app/context và test/context_suite. Cấu hình mẫu dùng HCI_LIGHTRAG_*, cổng 9622, workspace hci_comparison_a và Compose project hci-lightrag.
Chưa xác nhận LightRAG thật, model, nhập/query kho dân sự bền vững hoặc tác động gián tiếp trên HCI. Mỗi lần thử cần ghi commit, phiên bản dịch vụ/model, snapshot dữ liệu, cấu hình không chứa key, lệnh chạy và output có mapping nguồn.
Ba mục đích retrieval gồm tìm đích/phiên bản, ngữ cảnh và ứng viên B. Cleanup theo lượt phải bảo vệ kho dùng chung. Xem [Architecture](architecture.md) và [kế hoạch kiểm thử](test_evaluation_plan.md).
