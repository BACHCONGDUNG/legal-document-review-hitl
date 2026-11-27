# Tình trạng tích hợp LightRAG HCI
Client HTTP, mapping nguồn và kiểm thử mô phỏng nằm trong backend/app/context và test/context_suite. Cấu hình mẫu dùng HCI_LIGHTRAG_*, cổng 9622, workspace hci_comparison_a và Compose project hci-lightrag.
Demo web hỗ trợ nạp metadata mẫu và truy xuất trong từng lượt đối chiếu. Việc xác minh trên Docker với provider thật, nạp kho dân sự bền vững và đo tác động gián tiếp được thực hiện riêng. Mỗi lần thử cần ghi commit, phiên bản dịch vụ/model, snapshot dữ liệu, cấu hình không chứa key, lệnh chạy và output có mapping nguồn.
Ba mục đích retrieval gồm tìm đích/phiên bản, ngữ cảnh và ứng viên B. Cleanup theo lượt phải bảo vệ kho dùng chung. Xem [Architecture](architecture.md) và [kế hoạch kiểm thử](test_evaluation_plan.md).

[Docker và cấu hình LightRAG](../deploy/lightrag/README.md) mô tả demo web và CLI. [Hợp đồng Context](context-handoff.md) ghi đầu vào, truy xuất và kiểm tra nguồn.
