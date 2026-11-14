# MODULE — Phân công cấu trúc và bàn giao

**Học phần và nhóm:** 2627I_INT2041_1 — Nhóm 6

**Phiên bản:** Bản khung bổ sung

**Trạng thái:** Tổng hợp theo tài liệu HCI hiện có; lựa chọn triển khai còn chờ owner đề xuất tại [Module Owner Decisions](module-owner-decisions-hci.md).

## 1. Mục đích và quy định chung

Tài liệu tập hợp nhiệm vụ, trách nhiệm, file mục tiêu, điểm nối và điều kiện bàn giao. Căn cứ là [Architecture](architecture.md), [SRS](srs.md), [Implementation Plan HCI](implementation-plan-hci.md) và [Module Owner Decisions](module-owner-decisions-hci.md). Nội dung chưa được quyết định không được ghi như implementation hoặc lựa chọn đã hoàn thành.

- Giữ ranh giới mục tiêu backend/app/ và test/ theo Architecture. Cây mục tiêu không chứng minh các file đã có code hoặc đã chạy được.
- Phân biệt implementation hiện có, file khung và tên file mục tiêu. Giữ converter/Parser hiện có; không tự yêu cầu thay toàn bộ nội bộ khi adapter đáp ứng được hợp đồng.
- Các module nội bộ phải chuyển đầu ra về contract HCI trong SRS; cây Parser hoặc response dịch vụ không tự là ComparisonReport.
- Owner được ghi theo phạm vi đã nêu trong tài liệu gốc. Người tổng hợp một D-ID không mặc nhiên là người đã xác nhận mọi phương án hoặc đã hoàn thành code.
- Mỗi task có người chủ trì và bên nhận/reviewer. Người kiểm thử không thay trách nhiệm tự kiểm tra của owner.
- Thay contract cần bên cung cấp và bên nhận review mẫu, cập nhật schema, fixture và các tài liệu bị ảnh hưởng.
- LightRAG Server riêng qua HTTP là phương án B tạm chọn; release, model, API và vòng đời còn chờ D-04/D-05/D-13.
- Lựa chọn tên/cấu trúc file hỗ trợ và giao diện nội bộ chưa được xác định: chưa quyết định; owner đề xuất theo phạm vi và bên nhận review khi ảnh hưởng hợp đồng.

## 2. Tổng quan module và phân công

Đường dẫn các module dưới đây tính từ backend/app/ theo cây mục tiêu trong Architecture.

| Module | Owner theo tài liệu hiện có | Phối hợp và review | Trạng thái đặc tả |
| --- | --- | --- | --- |
| api/ | Dương Đức Anh | Tùng Dương nhận API; Dũng/Nam review dữ liệu | Contract HCI; route demo ở backend/demo.py và handler ở backend/main.py |
| schemas/ | Dương Đức Anh | Các bên cung cấp và nhận dữ liệu | Schema/fixture và validation còn chờ D-01/D-02 |
| document_processing/ | Owner chung: chưa quyết định. Dũng phụ trách đầu vào/adapter; Đức Anh phụ trách linker | Nam nhận trước–sau; Tùng Dương dùng nguồn | Chi tiết ranh giới theo D-02/D-03 |
| context/ | Dương Đức Anh | Dũng review nguồn; Nam nhận context; Tùng Dương đọc bằng chứng | Chờ D-04, phối hợp D-05/D-09/D-13 |
| change_analysis/ | Vương Thành Nam | Đức Anh tích hợp/vận hành; Dũng review nguồn/nhãn; Tùng Dương nhận nội dung hiển thị | Chờ D-05/D-06 |
| evaluation/ | Vương Thành Nam — phần đánh giá kỹ thuật | Dũng review gold; Đức Anh/Tùng Dương cung cấp kết quả | Công cụ và phép đo chờ D-11; không xác nhận evaluator hoàn chỉnh |

| Thành phần ngoài các folder trên | Người phụ trách theo tài liệu | Căn cứ và giới hạn |
| --- | --- | --- |
| Backend API/Pipeline và bộ tổng hợp báo cáo | Dương Đức Anh | HCI-02/HCI-09; D-01/D-03/D-09 |
| backend/main.py và backend/app/config.py | Chưa quyết định owner riêng từng file | Đức Anh phụ trách backend/vận hành; tài liệu chưa giao riêng ownership hai file |
| frontend/ và nhận xét trong phiên | Lê Tùng Dương | HCI-10/HCI-11; D-07/D-08; cấu trúc file frontend chờ đề xuất |
| Dữ liệu, manifest và đáp án ban đầu | Bạch Công Dũng | HCI-03/HCI-06; D-10; Nam review phần phân tích/nhãn |
| Nghiên cứu, dùng thử và đánh giá người dùng | Bạch Công Dũng | HCI-14/HCI-15; D-12; Tùng Dương phối hợp thiết kế |
| Đóng gói môi trường và bản chạy | Dương Đức Anh — quyết định chính D-13 | Từng owner bàn giao dependency/cách chạy; Dũng + Đức Anh cùng biên soạn development-guide.md |
| Tổng hợp kế hoạch và báo cáo đánh giá chung | Bạch Công Dũng | Nam chủ trì kỹ thuật D-11; Dũng chủ trì người dùng D-12; Đức Anh chủ trì kiểm thử tích hợp |
| Biên soạn api-contract.md và development-guide.md | Dũng + Đức Anh | Phối hợp D-01/D-13; hai file chưa có trong gói |

## 3. Đặc tả từng module

### 3.1. api/

**Owner:** Dương Đức Anh, theo HCI-02/HCI-09 và D-01.

**Hiện trạng mã nền:** Route upload hiện ở backend/main.py; api/compare.py còn trống. File compare.py dưới đây là vị trí mục tiêu, không xác nhận đã có logic.

**Nhiệm vụ và ranh giới:** Nhận yêu cầu từ frontend, kiểm tra đầu vào, gọi Pipeline, trả báo cáo/nguồn hoặc lỗi. Luồng người dùng dùng request đồng bộ, không thêm API lưu nhận xét hoặc job/polling.

| File mục tiêu | Trách nhiệm |
| --- | --- |
| compare.py | API so sánh V1–S và tham chiếu; request/response và lỗi theo contract HCI sau khi D-01 được review |

**Đầu vào:** multipart doc_v1, doc_s, reference_files tùy chọn.

**Đầu ra:** ComparisonReport HCI và nguồn đọc được trong giao diện; HTTP status/error body và cơ chế truyền nguồn chờ D-01/D-02.

**Bên kết nối:** Frontend của Tùng Dương; Pipeline của Đức Anh; nguồn của Dũng và phân tích của Nam.

**File hỗ trợ:** Chưa quyết định; đề xuất cùng giao diện cần bên nhận sử dụng.

**Điều kiện bàn giao:** Có mẫu SUCCESS/PARTIAL/FAILED, lỗi đầu vào và nguồn; Tùng Dương dùng được fixture; không lấy đọc/parse thành công làm kết quả phân tích hoàn chỉnh.

**Quyết định liên quan:** D-01, D-02, D-09, D-13.

### 3.2. schemas/

**Owner:** Dương Đức Anh, theo D-01 và phần quản lý schema/fixture trong kế hoạch.

**Nhiệm vụ và ranh giới:** Hiện thực hợp đồng dữ liệu và kiểm tra tính nhất quán. SRS là baseline; không lấy response cũ hoặc dict Parser thay contract HCI.

| File mục tiêu | Trách nhiệm |
| --- | --- |
| contracts.py | DocumentIdentity, bằng chứng, AmendmentResult, ComparisonReport và các kiểu dữ liệu liên quan |

**Đầu vào:** SRS cùng mẫu nguồn/đầu ra được bên giao và bên nhận review.

**Đầu ra:** Schema và fixture có validator; kiểm tra document_id, source_ref, amendment_id và change_id.

**Bên kết nối:** Dũng ở nguồn; Nam ở phân tích; Tùng Dương ở báo cáo/phiên; Đức Anh ở backend.

**File hỗ trợ:** Chưa quyết định.

**Điều kiện bàn giao:** Fixture được các bên dùng được; biểu diễn đúng PRESENT/ABSENT/UNRESOLVED, QUOTED/DERIVED và cảnh báo theo SRS. Danh sách ca validation chi tiết chờ D-01/D-02.

**Quyết định liên quan:** D-01, D-02, D-06, D-08.

### 3.3. document_processing/

**Owner chung:** Chưa quyết định. Phân công chức năng hiện có: Dũng xử lý đầu vào và adapter nguồn theo D-02; Đức Anh xử lý chỉ dẫn/liên kết theo D-03.

**Nhiệm vụ và ranh giới:** PDF có lớp chữ → DOCX → Parser hiện có; DOCX đi thẳng vào Parser. Giữ cây/nguồn rồi trích chỉ dẫn S, xác định đích và chuẩn bị trước–sau cục bộ. Không diff toàn văn V1 với S.

| File mục tiêu | Phụ trách và trách nhiệm |
| --- | --- |
| pdf_to_docx.py | Dũng: chuyển đổi và kiểm tra chất lượng, giữ bản gốc và thông tin chuyển đổi |
| parser/legal_structure_parser.py | Dũng: giữ thứ tự, Điều/Khoản/Điểm, bảng, outside và vị trí nguồn |
| document_adapter.py | Dũng: đề xuất adapter/native contract và ánh xạ nguồn theo D-02; Đức Anh nhận dữ liệu |
| amendment_linker.py | Đức Anh: trích chỉ dẫn, đích, thao tác, trước–sau và thông tin hiệu lực/chuyển tiếp theo D-03 |

**Đầu vào:** V1/S/tham chiếu có vai trò và nguồn; DOCX hoặc PDF có lớp chữ theo phạm vi.

**Đầu ra:** Cây/nguồn chuẩn hóa và nội dung cục bộ có căn cứ; chỉ dẫn chưa xác định phải được giữ cùng cảnh báo. Parser native trả articles/outside/source_blocks/warnings/status/summary theo mô tả Architecture; contract bàn giao chờ D-02/D-03.

**Bên kết nối:** Dũng → Đức Anh ở đầu vào/nguồn; Đức Anh → Nam ở dữ liệu phân tích; nguồn cung cấp cho Tùng Dương qua báo cáo.

**File hỗ trợ:** Chưa quyết định; chưa bắt buộc tách Reader riêng khỏi Parser hiện có.

**Điều kiện bàn giao:** Có mẫu DOCX và PDF, bảng/outside, chỉ dẫn sửa cụm từ/toàn đơn vị, thêm/bãi bỏ và đích mơ hồ; bên nhận chạy được. Nguồn block:N không được ghi như trang PDF khi chưa có mapping đã kiểm chứng.

**Quyết định liên quan:** D-02, D-03, D-10.

### 3.4. context/

**Owner:** Dương Đức Anh — quyết định chính D-04/D-13 theo phạm vi retrieval và vận hành; phối hợp Nam về lựa chọn mô hình thuộc D-05.

**Nhiệm vụ và ranh giới:** Chuẩn bị ngữ cảnh, dùng phương án retrieval tạm chọn, kiểm tra nguồn và nhu cầu tham chiếu; không giao dịch vụ quyết định kết quả pháp lý hoặc tạo báo cáo hoàn chỉnh.

| File mục tiêu | Trách nhiệm |
| --- | --- |
| chunk_builder.py | Tạo đoạn đủ nghĩa, giữ vai trò/định danh/spans và tránh nội dung full_text lặp |
| source_registry.py | Nối đoạn/kết quả truy xuất về đúng tài liệu và nguyên văn |
| lightrag_client.py | Giao tiếp HTTP: nhập, theo dõi sẵn sàng, query, lỗi và dọn theo phương án còn chờ review |
| context_builder.py | Truy vấn theo chỉ dẫn, chọn/kiểm tra căn cứ, giữ nhu cầu tham chiếu và giới hạn |

**Đầu vào:** Nguồn/cây, chỉ dẫn và dữ liệu liên quan từ D-02/D-03.

**Đầu ra:** Ngữ cảnh/bằng chứng và thông tin thiếu/chưa rõ theo contract được review; score retrieval không phải significance và mô tả dịch vụ không phải quote.

**Bên kết nối:** Dũng cung cấp nguồn; Nam nhận context; Đức Anh điều phối Pipeline; Tùng Dương kiểm tra đọc bằng chứng.

**File hỗ trợ:** Chưa quyết định; payload, model/release, storage, query/chunking và cơ chế cách ly chưa chốt.

**Điều kiện bàn giao:** Thử nhập → sẵn sàng → query → ánh xạ quote → dọn; hai bộ không lẫn. Query rỗng/lỗi dịch vụ không tự chứng minh thiếu tài liệu hoặc không thay đổi. Không dọn nguồn khi tác vụ vẫn sử dụng.

**Quyết định liên quan:** D-04, D-05, D-09, D-13.

### 3.5. change_analysis/

**Owner:** Vương Thành Nam, theo HCI-08 và D-05/D-06; Nam có quyền quyết định chính D-05, phối hợp bên liên quan khi thay contract, nguồn lực hoặc môi trường chung.

**Nhiệm vụ và ranh giới:** So sánh chữ, phân tích nghĩa và chấm tác động theo schema HCI; nhận định và điểm nối bằng change_id.

| File mục tiêu | Trách nhiệm |
| --- | --- |
| text_diff.py | Vùng INSERT/DELETE/REPLACE khớp before_text/after_text; không dùng chuỗi rỗng thay phía chưa xác định |
| semantic_diff.py | Nhận định và aspects có căn cứ; giữ nhiều khía cạnh, giải thích và trạng thái chưa xác định |
| scorer.py | Mức tác động cùng lý do theo rubric được review; thiếu căn cứ không ép LOW |
| ai_adapter.py | Gọi mô hình và kiểm tra output; phương pháp, prompt, validation/fallback chờ D-05 |

**Đầu vào:** Nội dung trước–sau và context/bằng chứng từ Đức Anh, nguồn/nhãn phối hợp Dũng.

**Đầu ra:** Nhận định có giải thích và nguồn, TextChange, aspects và mức tác động theo SRS; nội bộ và cách chuyển đổi chờ fixture được review.

**Bên kết nối:** Đức Anh cung cấp/tổng hợp; Dũng review nguồn/nhãn; Tùng Dương hiển thị kết quả.

**File hỗ trợ:** Chưa quyết định.

**Điều kiện bàn giao:** Ca bốn nhóm, sửa diễn đạt, nhiều khía cạnh, thiếu căn cứ, ngoài phạm vi và lỗi AI. Kiểm tra đúng cấu trúc không thay kiểm tra đúng nội dung; không làm mất chỉ dẫn khi chưa tạo được nhận định.

**Quyết định liên quan:** D-05, D-06, D-11.

### 3.6. evaluation/

**Owner:** Vương Thành Nam — phần kỹ thuật, theo HCI-12 và D-11.

**Nhiệm vụ và ranh giới:** Xây dựng công cụ và phương pháp đánh giá kỹ thuật, chạy phép đo và phân tích lỗi; tách khỏi đánh giá người dùng do Dũng chủ trì. Tài liệu hiện có chưa xác nhận công cụ hoàn chỉnh hoặc kết quả đo.

| File mục tiêu | Trách nhiệm |
| --- | --- |
| evaluator.py | Công cụ đánh giá kỹ thuật theo D-11; giao diện, metric, matching và lệnh chạy chưa quyết định |

**Đầu vào:** Kết quả của phiên bản được đo, dữ liệu/nhãn có nguồn và được review theo D-10/D-11.

**Đầu ra:** Kết quả kỹ thuật, lỗi và giới hạn gắn phiên bản; cấu trúc báo cáo và đường dẫn kết quả chưa quyết định.

**Bên kết nối:** Dũng review gold; Đức Anh/Tùng Dương cung cấp kết quả; Nam phân tích lỗi thuộc phần mình.

**File hỗ trợ:** Chưa quyết định.

**Điều kiện bàn giao:** Có ca tính tay, quy tắc khớp SemanticChange/aspects, xử lý thiếu/sai aspect, nguồn sai, chưa xác định và không có mẫu; có lệnh chạy và cấu hình để kiểm tra lại. Chưa chốt ngưỡng hoặc công thức thay owner.

**Quyết định liên quan:** D-10, D-11; phối hợp D-12 khi dùng đáp án cho tác vụ người dùng.

## 4. Đầu vào–đầu ra và các điểm nối

| Điểm nối | Bên giao | Bên nhận | Nội dung cần review | Quyết định |
| --- | --- | --- | --- | --- |
| Đầu vào/Parser/adapter → backend/linker | Dũng | Đức Anh | Cây, source_blocks, ID, vai trò, bảng/outside, spans, cảnh báo | D-01/D-02/D-03 |
| Linker/context → phân tích | Đức Anh | Nam | Trước–sau trích/suy ra, chỉ dẫn/đích, ngữ cảnh và phần thiếu căn cứ | D-03/D-04/D-05 |
| Text Diff → Semantic Diff → Scorer | Nam | Nam; Đức Anh review đầu ra tích hợp | Nội dung/offset, nhận định, aspects, rubric, nguồn và lỗi | D-05/D-06 |
| Phân tích → bộ tổng hợp/Pipeline | Nam | Đức Anh | Kết quả chuyển sang contract HCI, nhiều khía cạnh và cảnh báo | D-01/D-05/D-06 |
| API/Pipeline → frontend | Đức Anh | Tùng Dương | Report/nguồn, trạng thái, lỗi, file bổ sung và dữ liệu giữa hai lượt; Tùng Dương quyết định cơ chế giữ/đọc bằng chứng theo D-07, phối hợp D-01/D-02 | D-01/D-07/D-08 |
| Nội dung phân tích → hiển thị | Nam | Tùng Dương | Câu giải thích, bằng chứng, mức tác động và phần chưa rõ | D-06/D-07 |
| Nhãn/đáp án → đánh giá kỹ thuật | Dũng; Nam review | Nam | Bộ căn cứ, split, nhãn và quy tắc đối chiếu | D-06/D-10/D-11 |
| Bản dùng thử và đáp án → đánh giá người dùng | Đức Anh/Nam/Tùng Dương theo phần việc | Dũng | Phiên bản, tác vụ, dữ liệu, kết quả kỹ thuật và giới hạn | D-11/D-12/D-13 |

Tên hàm, kiểu, return, mã lỗi và fixture cụ thể còn chờ owner đề xuất. Bảng là các điểm bàn giao trong tài liệu hiện có, không tự tạo public API mới.

## 5. Phối hợp triển khai bán song song

Theo [Workflow](workflow.md): owner đề xuất và tự kiểm tra; bên nhận chạy fixture; ghi quyết định rồi cập nhật đặc tả/schema/fixture và tích hợp. D-01/D-02 cần rõ trước ghép dữ liệu; có thể thử D-03/D-04/D-05/D-07 song song bằng mẫu. Không cần mọi quyết định hoàn tất trước khi làm phần độc lập.

## 6. Kiểm thử và điều kiện hoàn thành

Task hoàn thành khi có đầu ra, kiểm tra phù hợp, cách chạy, kết quả và giới hạn; bên nhận dùng được. Đức Anh chủ trì kiểm thử tích hợp; Nam chủ trì đánh giá kỹ thuật; Dũng chủ trì dùng thử và thu ý kiến; Tùng Dương kiểm tra giao diện/phiên. Kế hoạch chi tiết ở [Test Evaluation Plan](test_evaluation_plan.md); ca nghiệm thu AT-01–AT-13 theo SRS.

## 7. Trạng thái hoàn thiện

| Hạng mục | Trạng thái theo tài liệu nguồn | Phần chờ |
| --- | --- | --- |
| Contract HCI và ReviewRecord frontend | Có baseline trong SRS | Fixture hiện tại và các quyết định D-02/D-06/D-08 |
| Converter/Parser và API/Pipeline nền | Được mô tả đã có ở bộ code nền trước đó | Đã đối chiếu mã main tại 01b98ce, chưa chạy test trong đợt này; còn lệch contract HCI |
| Linker/context/phân tích/frontend/evaluation | Chưa có bản hoàn chỉnh được xác nhận | Owner đề xuất/hiện thực theo D-ID liên quan |
| LightRAG | Phương án B tạm chọn | D-04/D-05/D-09/D-13 |
| document_processing/ owner chung | Chưa quyết định | Dũng/Đức Anh đã có phạm vi chức năng riêng; cần làm rõ nếu nhóm muốn một owner folder |
| Kế hoạch đánh giá chung | Đã có bản khung, đang hoàn thiện | Dũng tổng hợp; Nam phần kỹ thuật; Dũng phần người dùng; Đức Anh kiểm thử tích hợp |

Đủ đặc tả, đã hiện thực và đã tích hợp/kiểm tra là các trạng thái khác nhau. Không chuyển các D-ID đang chờ owner thành đã chốt chỉ bằng việc bổ sung tài liệu này.
