# Chạy demo HCI
Tạo venv và cài requirements-demo.txt từ thư mục gốc. Chạy ứng dụng bằng lệnh bên dưới.
    python -m uvicorn backend.demo:app --host 127.0.0.1 --port 8001
Mở http://127.0.0.1:8001. Chạy lại ba bộ DOCX bằng lệnh sau.
    python -m test.demo_suite.run_raw_demo --base-url http://127.0.0.1:8001 --output data/demo-results
Demo cục bộ nhận V1 và S. Demo web dùng chung hỗ trợ nhận S để tra đích trước khi đối chiếu. Đọc trạng thái PARTIAL hoặc FAILED cùng nguồn, cảnh báo và lỗi.

Giao diện phân biệt lỗi đầu vào, lỗi kết nối và lỗi máy chủ. Báo cáo giữ kết quả từng phần và cảnh báo. Trạng thái chưa đủ căn cứ, chưa xử lý được và không đổi nghĩa được hiển thị riêng. Mở [hướng dẫn demo web dùng chung](shared-web-demo.md) để thử tra đích từ S và truy xuất LightRAG.
