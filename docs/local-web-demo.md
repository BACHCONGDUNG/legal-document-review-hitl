# Chạy demo HCI
Tạo venv và cài requirements-demo.txt từ thư mục gốc. Chạy ứng dụng bằng lệnh bên dưới.
    python -m uvicorn backend.demo:app --host 127.0.0.1 --port 8001
Mở http://127.0.0.1:8001. Chạy lại ba bộ DOCX bằng lệnh sau.
    python -m test.demo_suite.run_raw_demo --base-url http://127.0.0.1:8001 --output data/demo-results
Demo nhận V1 và S. API chỉ S thuộc thiết kế cần triển khai. Đọc trạng thái PARTIAL hoặc FAILED cùng nguồn, cảnh báo và lỗi.
