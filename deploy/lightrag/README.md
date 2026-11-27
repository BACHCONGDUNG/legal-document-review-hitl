# Chạy LightRAG cho HCI

Chạy các lệnh PowerShell từ thư mục gốc của repo. Bật Docker Desktop và dùng Python 3.12. Lệnh `docker info` cần kết nối được với Docker Engine.

## Demo web

```powershell
python -m pip install -r requirements-demo.txt
docker build -t hci-lightrag:28ff1b05 'https://github.com/HKUDS/LightRAG.git#28ff1b05f2ac3f3e6fa14dd2cd33656579bd0c9c'
Copy-Item -LiteralPath deploy/lightrag/context-provider.env.example -Destination deploy/lightrag/.env.groq-jina
```

Điền `GROQ_API_KEY` và `JINA_API_KEY` vào tệp `.env.groq-jina` trên máy chạy. Tệp này được Git bỏ qua. Chọn model và số chiều embedding phù hợp với tài khoản. Bản mẫu dùng Groq để trích xuất và Jina để tạo embedding.

```powershell
python -m backend.shared_demo --provider-env-file deploy/lightrag/.env.groq-jina --check-providers
python -m backend.shared_demo --provider-env-file deploy/lightrag/.env.groq-jina --host 127.0.0.1 --port 8002
```

Mở [demo HCI](http://127.0.0.1:8002). Nạp S của ca Ngân hàng rồi chọn **Tìm văn bản gốc** để thử đối chiếu. Mục **Index metadata thật** dùng hai bản ghi mẫu và cho thử truy xuất khi trạng thái là `READY`. Hai thao tác dùng các container riêng. Khi kết thúc, dừng web bằng Ctrl+C để backend dọn container của phiên.

Kho 409 DOCX có tại `data/legal-dataset-study/data/lightrag/`. Demo hiện dùng hai bản ghi metadata và Context của từng lượt đối chiếu. Xem [luồng web và API](../../docs/shared-web-demo.md) để biết cách đọc bằng chứng và trạng thái.

## Kiểm thử Context với dữ liệu mô phỏng

```powershell
python -m unittest discover -s test/context_suite -v
python -m backend.context_cli --mode contract --input test/fixtures/context_cases/synthetic_civil.json --output runtime/lightrag/context-contract.json
```

Chế độ `contract` dùng dữ liệu giả định và HTTP mô phỏng. Xem [hướng dẫn CLI chạy thật](../../docs/context-handoff.md#chạy-lightrag-thật) để kiểm chứng riêng một ca qua Docker.

## Server Compose riêng

Để chạy một server cố định cho client HCI, sao chép `.env.example` thành `.env`, điền các khóa, cấu hình nhà cung cấp và workspace. Compose dùng project `hci-lightrag`, volume theo project và cổng loopback `9622`.

```powershell
Copy-Item -LiteralPath deploy/lightrag/.env.example -Destination deploy/lightrag/.env
docker compose --env-file deploy/lightrag/.env -f deploy/lightrag/compose.yaml up -d --build
docker compose --env-file deploy/lightrag/.env -f deploy/lightrag/compose.yaml logs --tail 50 lightrag
```

Khi kiểm tra client, đặt biến `HCI_LIGHTRAG_URL`, `HCI_LIGHTRAG_WORKSPACE` và `HCI_LIGHTRAG_API_KEY` theo [mẫu backend](../../backend/.env.lightrag.example).

```powershell
docker compose --env-file deploy/lightrag/.env -f deploy/lightrag/compose.yaml down
```
