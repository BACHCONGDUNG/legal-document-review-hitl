# Context/LightRAG — bàn giao và chạy kiểm chứng

## Phạm vi

**Cập nhật web chung:** xem [shared-web-demo.md](shared-web-demo.md). CLI bên dưới vẫn dành cho một lượt kiểm chứng độc lập; web chung có lifecycle riêng cho corpus metadata và từng comparison. Không dùng CLI cleanup để dọn kho chung.

Xem [README triển khai LightRAG](../deploy/lightrag/README.md) để chuẩn bị môi trường HCI.

Đã có bộ nhận dữ liệu ca nguồn, runner Context và CLI chạy một LightRAG Server thật qua HTTP trong container riêng. Runner dùng client HTTP, registry nguồn, chunk builder và bước truy xuất Context trong backend HCI. Không làm thay Parser, tìm V1, dựng trước/sau, Semantic hoặc Scorer. CLI chỉ chạy sau khi đã có AmendmentItem và V1 được giải quyết; không phải endpoint chỉ S.

## Đầu vào và đầu ra

[Ca giả định](../test/fixtures/context_cases/synthetic_civil.json) là mẫu `hci-context-case-v1` do dự án tự tạo; KHÔNG phải ca lấy từ hai dataset hoặc văn bản pháp luật thật.

| Trường | Ý nghĩa |
| --- | --- |
| format, case_id, snapshot_id | Phiên bản điểm nối nội bộ, mã ca và phiên bản bộ nguồn |
| source_kind | SYNTHETIC, LOCAL_UNREVIEWED, DATASET_UNREVIEWED hoặc DATASET_REVIEWED; là nhãn của bên giao, không tự chứng minh pháp lý đúng |
| documents | Danh sách ExtractedDocument hiện có, giữ nguyên block/text/source_ref; v1/BASE, s/AMENDMENT, ref_*/REFERENCE |
| provenance | Theo ID cục bộ: source_identity, version_id, content_sha256 và unit_paths cho mọi block. Không dùng filename làm định danh |
| dataset, dataset_id, revision, source_url | Với nguồn dataset, ghi tên đầy đủ và commit 40 ký tự; không dùng main/latest. Hai nguồn ID giống nhau chưa phải cùng văn bản |
| origin=UPLOAD | Nguồn tải lên có thể đi cùng V1 từ dataset; không gán nguồn tải lên thành bản ghi dataset |
| amendment | AmendmentItem có trước/sau đủ căn cứ; trước có bằng chứng V1; QUOTED phải có nguyên văn S. Không tự dựng khi thiếu V1 |
| candidate_query | Tùy chọn, truy xuất ứng viên B; không xác nhận tác động |

Hai dataset được chấp nhận là th1nhng0/vietnamese-legal-documents (chính) và vohuutridung/vietnamese-legal-documents (bổ sung). Chưa tự tải hoặc trộn dataset. Dũng bàn giao nguồn/phiên bản đã xác minh, cùng adapter nội dung HTML/Markdown sang blocks; không giả DOCX để qua kiểm tra. Kiểu file/source locator từ dataset phải được review với hợp đồng nguồn hiện có trước khi nối toàn Pipeline.

`ContextCase.from_dict()` kiểm tra ID/phiên bản, digest nguyên văn, vai trò, vị trí và bằng chứng. `content_digest(document)` tính SHA-256 trên JSON canonical của blocks (UTF-8, sort_keys, separators không khoảng trắng). Nhãn version là căn cước bên giao cung cấp; code không tự xác minh hiệu lực pháp lý.

`run_case(case, client, registry)` trả:
- TextDiffResult dùng tạo query; context trước/sau retrieval và ProcessingIssue tương ứng.
- source_trace: EvidenceRef + định danh nguồn/phiên bản, dataset/revision và vị trí. Không dùng entity description hoặc câu trả lời LLM làm quote.
- Ứng viên B có evidence đã đối chiếu, luôn legal_impact_confirmed=false.
- Chỉ số thời gian, graph nguồn dự án và nhãn giới hạn; CLI real thêm KG trích xuất thật và audit metadata của graph.

Mỗi block là một chunk. Quá giới hạn số lượng/độ dài thì từ chối, không âm thầm cắt. Không thay đổi ReferenceRequirement thành AVAILABLE chỉ vì retrieval thành công, không xác nhận context đầy đủ hay bật chấm mức độ.

## Chạy kiểm thử độc lập

Từ repo root, dùng Python đã cài `requirements-demo.txt`:

```powershell
python -m unittest discover -s test/context_suite -v
python -m backend.context_cli --mode contract --input test/fixtures/context_cases/synthetic_civil.json --output runtime/lightrag/context-contract.json
```

Contract mode dùng HTTP double có nhãn, không phải LightRAG. Real mode không tự fallback sang double.

## Chạy LightRAG thật

Cần Docker Desktop, image upstream đã ghim và key/model được phép sử dụng. Mỗi lần chạy sinh container, workspace, endpoint, storage và ledger mới. Không gắn volume hoặc endpoint kho dùng chung.

Nếu chưa có image, build upstream nguyên bản (cần mạng và có thể mất thời gian):

```powershell
docker build -t hci-lightrag:28ff1b05 https://github.com/HKUDS/LightRAG.git#28ff1b05f2ac3f3e6fa14dd2cd33656579bd0c9c
Copy-Item deploy/lightrag/context-provider.env.example deploy/lightrag/.env.context
```

Điền cấu hình vào `.env.context` đã được Git bỏ qua. Mẫu hỗ trợ native Gemini hoặc OpenAI của upstream; model ví dụ không phải quyết định chung của nhóm. Không gửi key vào chat hoặc commit. Khi chạy real, nội dung ca được gửi cho provider đã cấu hình và có thể phát sinh quota/chi phí.

```powershell
python -m backend.context_cli --mode real --input test/fixtures/context_cases/synthetic_civil.json --provider-env-file deploy/lightrag/.env.context --output runtime/lightrag/context-live.json --budget 600
```

Một đến ba query ngữ cảnh có thể chọn bằng --repeats (mặc định 1). Chỉ chạy thêm khi cần đánh giá độ ổn định, không tự tăng lượt gọi model.

Khi ghép runner, bên Pipeline quản lý một client/registry trong phạm vi comparison và cleanup trong finally; không tạo client mới cho từng item. Input mới phải qua ContextCase/registry trước khi nhập. Xem `backend/context_cli.py` về lifecycle; không dùng test double ở runner thật.

## Lỗi và vòng đời

- Index chưa sẵn sàng, sai nguồn/phiên bản, retrieval rỗng hoặc lỗi đều giữ lý do; không chuyển thành không có tài liệu/thay đổi.
- Timeout được giữ là RETRIEVAL_TIMEOUT. GET và POST /query/data chỉ đọc được retry tối đa một lần với lỗi tạm thời; không tự replay nhập/xóa sau ACK không rõ.
- Chỉ xóa doc IDs trong ledger của client đã dành server riêng. Không gọi purge/global delete.
- Chỉ stop/rm container khi ownership label khớp đúng UUID. Lỗi HTTP cleanup vẫn cố dừng đúng container sở hữu; không thao tác dịch vụ khác.
- Storage/ledger demo giữ ở runtime/lightrag để audit, được Git bỏ qua. Không coi giữ storage này là đã có kho dùng chung bền vững. Không tự dùng lại endpoint/ledger cũ.
- Khóa chỉ được ghi vào file env tạm cho Docker rồi xóa file đó; Docker vẫn giữ environment của container tới khi container được xóa. Không xuất key ra report/log của ứng dụng.

## Đề xuất báo cáo cấp S cần review

[Fixture đề xuất](../test/fixtures/context_cases/analysis_report_draft.json) có nhãn DRAFT, không được API nhập hoặc trả như hợp đồng chính thức. Bao analysis_id, corpus_snapshot_id/coverage, targets, unresolved_amendments, indirect_impacts và trạng thái/lỗi theo SRS §1.8. Mỗi target giữ ComparisonReport hiện có và source_bindings từ ID cục bộ về nguồn/phiên bản thật. Báo cáo cục bộ qua validator hiện có; lớp bao chưa có validator chính thức.

Dũng, Đức Anh và Tùng Dương cần chốt kiểu dữ liệu đầy đủ, bằng chứng khi thiếu V1, mapping xuyên đích, trạng thái và định nghĩa kết quả hữu ích trước khi nối API/UI. Không thêm trường hoặc sửa nghĩa contract cũ trong đợt này.

## Phần còn chờ

- Chọn ca S–V1–B có đáp án và căn cứ xác minh phiên bản từ kho DOCX. Dũng phụ trách dữ liệu, Đức Anh kiểm tra điểm nối Context.
- Nam kiểm tra cách dùng bằng chứng trong Semantic Diff và Scorer. Tùng Dương dùng kết quả đã đối chiếu để trình bày nguồn trên UI.
- Nghiệm thu LightRAG trên HCI cần chạy riêng qua Docker với cấu hình nhà cung cấp.
