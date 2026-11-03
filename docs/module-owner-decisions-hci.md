# Module Owner Decisions — HCI

**Học phần và nhóm:** 2627I_INT2041_1 — Nhóm 6  
**Nhóm trưởng:** Bạch Công Dũng  
**Phiên bản:** HCI 1.0.0  
**Ngày cập nhật:** 03/11/2026  
**Trạng thái:** Danh sách cần owner đề xuất; chưa có quyết định kỹ thuật nào được ghi nhận là owner đã chốt  
**Liên quan:** [SRS](srs.md), [Architecture](architecture.md), [Implementation Plan](implementation-plan-hci.md), [Data Guide](data-annotation-guide-hci.md), [User Research](user-research.md)

## 1. Mục đích và baseline dùng chung

Đây là nơi duy nhất theo dõi lựa chọn còn mở. Mỗi D-ID có một owner tổng hợp đề xuất, bên nhận/reviewer và đầu ra cần kiểm chứng. Owner được ghi theo phân công HCI đang có; việc có tên ở bảng không xác nhận người đó đã nhận hoặc thực hiện một phương án cụ thể. Chưa đặt hạn ngày thay nhóm: cột “trước khi” là điểm phụ thuộc để owner ước lượng và nhóm gắn vào lịch học.

Bản tài liệu đồng bộ dùng baseline sau để các bên cùng trao đổi:

- Sinh viên Luật là người dùng chính; bài toán V1–S cùng tham chiếu đã cung cấp; không bắt buộc dựng V2.
- HCI tập trung hiểu, kiểm chứng, nhận xét và kiểm tra lại; chất lượng AI và usability là hai phép đánh giá khác nhau.
- Contract HCI theo SRS: upload base_file/amendment_file/reference_files; báo cáo documents/items; ReviewItem và ReviewRecord tách biệt; bốn field_group TIME_LIMIT, QUANTITATIVE, CONDITIONS_EXCEPTIONS, SUBJECT_RIGHTS_DUTIES.
- Các module có thể dùng cấu trúc xử lý nội bộ, nhưng phải xuất đúng contract HCI trước khi tích hợp. Bản code nền trong ZIP còn lệch contract, chưa được sửa trong gói docs này.
- Giữ converter và Parser hiện có, qua adapter; PDF → DOCX → Parser trước mắt. Nguồn block:N/DOCX chuyển đổi không được tự coi là trang PDF.
- Tạm chọn B cho retrieval: LightRAG Server riêng được gọi HTTP. Có thể cùng máy localhost; chưa chọn model, release/API, prompt, chunk, ngưỡng hoặc cam kết offline.
- Nhận xét lưu trong phiên frontend, không tự thành gold/nhãn huấn luyện. Giữ request đồng bộ, không bổ sung account/kho lịch sử/job người dùng ở đợt này.
- Giữ tên thực tế backend/app/ và test/. Tên tài liệu có hậu tố -hci phải được dẫn đúng.

Baseline thống nhất tài liệu không thay nghiệm thu code hoặc review của owner. Đề xuất thay yêu cầu/contract phải nêu rõ phần bị ảnh hưởng và được bên giao/bên nhận kiểm tra trước khi cập nhật nguồn sở hữu.

## 2. Danh sách cần chốt

**Trạng thái ban đầu của toàn bộ D-01 đến D-13: CHỜ OWNER ĐỀ XUẤT.** Chưa có quyết định cuối, ngày chốt, mô hình hoặc ngưỡng được điền thay. Bảng mô tả câu hỏi và minh chứng cần có, không phải đáp án kỹ thuật.

| ID | Owner tổng hợp | Người phối hợp/review | Cần đề xuất điều gì? | Đầu ra tối thiểu để review | Trước khi / nơi cập nhật sau chốt |
| --- | --- | --- | --- | --- | --- |
| D-01 | Dương Đức Anh | Tùng Dương nhận API; Nam/Dũng review dữ liệu | Hiện thực schema HCI, fixture, HTTP status/error body; chuyển doc_v1/doc_s và khung báo cáo hiện tại sang contract HCI thế nào? Có cần alias tạm và cơ chế trả nguồn nào? | Một bộ request/response thành công, PARTIAL, FAILED, lỗi đầu vào; bảng delta với code; schema/fixture validate được khi triển khai | Trước nối frontend và báo cáo HCI; SRS, api-contract.md, schema/fixtures |
| D-02 | Bạch Công Dũng | Đức Anh nhận adapter; Nam/Tùng Dương dùng nguồn | Đầu ra native/adapter; quy ước ID, block/spans, bảng/outside/quotation; mapping DOCX chuyển đổi → PDF có thể bảo đảm đến đâu? Quy ước Unicode offsets? | Một DOCX và một PDF: nguồn gốc/chuyển đổi, cây, contract bàn giao, quote truy đúng vị trí và giới hạn; ca reference không có Điều | Trước linker/context và hiển thị nguồn; SRS, Architecture, Data Guide, fixture nguồn |
| D-03 | Dương Đức Anh | Dũng review chỉ dẫn/đích; Nam nhận trước–sau | Phương pháp trích chỉ dẫn, tìm văn bản/đích, dựng before/after, hiệu lực và nhận diện căn cứ cần thiết; xử lý mơ hồ ra sao? | Ví dụ sửa đơn vị/cụm từ, bổ sung/bãi bỏ, S sửa nhiều văn bản và đích mơ hồ; expected/actual và nguồn | Trước phân tích trên dữ liệu thật; Architecture, fixture linker, API khi ảnh hưởng |
| D-04 | Dương Đức Anh | Dũng review nguồn; Nam nhận context; Tùng Dương kiểm tra khả năng đọc bằng chứng | Release/API LightRAG; cách nhập/chia đoạn/query; registry; đợi index; cách ly và dọn dữ liệu; context đủ nghĩa và ngân sách truy xuất? | Parser → nhập → xác nhận sẵn sàng → query → ánh xạ quote → dọn; hai bộ không lẫn; ghi request/response thực tế đã loại bí mật, thời gian và giới hạn | Trước tích hợp retrieval; Architecture, API contract phần nội bộ, Development Guide |
| D-05 | Vương Thành Nam | Đức Anh vận hành/client; Dũng review nguồn | LLM/embedding cho các vai trò, nơi chạy local/ngoài, prompt, kiểm tra đầu ra, fallback; dùng retrieval thế nào trong phân tích? | So sánh trên cùng mẫu, cấu hình/mô hình/phiên bản, output đúng/sai/chưa rõ, token/chi phí nếu đo được; giới hạn và quyền truy cập | Trước chọn cấu hình phân tích và công bố nhu cầu mạng; Architecture, config, Development Guide |
| D-06 | Vương Thành Nam | Dũng review nhãn; Đức Anh/Tùng Dương nhận report | Ranh giới bốn mã HCI, chia/gộp ReviewItem, giá trị/đơn vị, rubric pilot và ca ngoài phạm vi | Ví dụ ranh giới, lý do gán nhãn, câu giải thích/evidence, ca không được ép mã; reviewer và phiên bản | Trước khóa gold hoặc dùng Scorer; SRS nếu đổi contract, Data Guide, fixtures |
| D-07 | Lê Tùng Dương | Dũng đối chiếu nghiên cứu; Đức Anh/Nam cung cấp dữ liệu | Stack frontend, luồng/màn hình, evidence display, bàn phím, lỗi, lọc/đếm và ReviewRecord; cấu trúc mã frontend? | Prototype theo tác vụ, fixture API dùng được, bảng trạng thái UI, cách đọc nguồn và kiểm thử tương tác | Trước triển khai luồng UI chính; thiết kế tương tác, Architecture, SRS khi đổi hành vi |
| D-08 | Lê Tùng Dương | Đức Anh cung cấp ID/nguồn; Dũng/Nam review ca thay đổi | Nhận diện cùng mục và dữ liệu cần so sánh giữa hai lượt; giữ REVIEWED khi nào, RECHECK_REQUIRED và nhận xét không ghép được thế nào? | Hai report và ReviewRecord trước/sau; ca thêm mục, nội dung đổi, tách/gộp, mục mất, PARTIAL và request thất bại | Trước luồng bổ sung/phân tích lại; SRS nếu cần đổi, Architecture, fixture phiên |
| D-09 | Dương Đức Anh | Các owner module cung cấp số đo; Tùng Dương hiển thị giới hạn | Dung lượng/số file, đồng thời, deadline/timeout/retry; dọn tài nguyên khi blocking/tác vụ Server còn chạy; giới hạn ingress? | Đo trên mẫu/môi trường, ca vượt giới hạn/lỗi/timeout, vị trí cấu hình và phần không thể hủy cứng; không coi mặc định code là benchmark | Trước tích hợp thật và dùng thử; SRS yêu cầu vận hành, API Contract, config, Development Guide |
| D-10 | Bạch Công Dũng | Nam review nhãn/đáp án; Đức Anh/Tùng Dương dùng fixture | Bộ V1–S/tham chiếu, manifest, split theo nguồn, hồ sơ gold HCI và nhãn context; mẫu đúng/sai kiểm soát cho HCI | Danh sách file/hash/vai trò/lineage, mẫu bốn nhóm và thiếu căn cứ, đáp án/reviewer; tách V2/gold/gợi ý sai khỏi index và đo AI | Trước khóa dữ liệu/đánh giá; Data Guide, data/manifest và fixture |
| D-11 | Vương Thành Nam | Dũng review gold; Đức Anh/Tùng Dương cung cấp kết quả | Matching ReviewItem/aspects, metric, ca null/không mẫu, lỗi nguồn/linker/retrieval; ngưỡng nào có căn cứ? | Ca tính tay có TP/FP/FN, sai/thiếu aspect, nguồn sai và phần chưa xác định; lệnh đo/config; tiêu chí cố định trước test | Trước chạy đánh giá kỹ thuật; test-evaluation-plan.md phần kỹ thuật, evaluator/fixtures |
| D-12 | Bạch Công Dũng | Tùng Dương thiết kế; Nam chuẩn bị đáp án; Đức Anh bàn giao bản chạy | Tác vụ, người tham gia, tiêu chí chấm, SUS/phản hồi, thiết kế so sánh giao diện, kế hoạch cải tiến/kiểm tra lại | Kế hoạch nối với BG/RQ/AT, đáp án và gợi ý sai kiểm soát, biểu mẫu/phiên bản, lịch/nguồn lực thực tế; phân biệt hai người nghiên cứu ban đầu với người dùng thử | Trước tuyển/dùng thử và thu số liệu; test-evaluation-plan.md phần usability, User Research chỉ khi có dữ liệu mới |
| D-13 | Dương Đức Anh | Mỗi owner bàn giao dependency/lệnh chạy; Dũng xác nhận máy dùng thử | Cách cài/chạy LightRAG riêng, pin dependency/model/config; Python env hay container, storage, xác thực, log; khởi động và kiểm tra sẵn sàng | Hướng dẫn cài sạch và chạy lại trên máy khác, cấu hình mẫu không bí mật, một lệnh/nhóm lệnh kiểm tra; khai báo phần cần Internet và nguồn phải tải trước | Trước bàn giao chạy thật; development-guide.md, requirements/config/deploy; README chỉ tóm tắt |

Không cần mọi D-ID xong mới làm module. Có thể thử D-03/D-04/D-05/D-07 song song bằng fixture. D-01/D-02 phải đủ rõ trước ghép dữ liệu; D-06/D-10 và D-11/D-12 phải đủ rõ trước đánh giá độc lập hoặc thu dữ liệu người dùng. D-04 chọn release/API trong phép thử, D-13 đóng gói lại cấu hình đã kiểm chứng; hai owner công việc này là cùng Đức Anh nên không tạo hai bản cấu hình riêng.

## 3. Mẫu owner trả lời

Mỗi owner bổ sung một mục theo mẫu dưới đây cho D-ID của mình; chưa điền phương án giả hoặc xác nhận hộ.

```text
ID:
Trạng thái: CHỜ OWNER ĐỀ XUẤT / ĐÃ ĐỀ XUẤT / ĐANG THỬ / ĐÃ CHỐT / CẦN ĐIỀU CHỈNH
Owner:
Phương án đề xuất:
Lựa chọn khác và lý do chọn:
Phần giữ nguyên baseline / thay đổi yêu cầu hoặc contract:
Đầu vào–đầu ra và ví dụ:
Code/commit, phiên bản thư viện hoặc mô hình:
Kiểm tra đã chạy; expected/actual:
Thời gian, tài nguyên, chi phí đã đo (nếu chưa đo thì ghi chưa đo):
Giới hạn, trường hợp lỗi và cách xử lý:
Bên nhận/reviewer; kết quả chạy lại:
Thời gian dự kiến và phụ thuộc:
Kết luận được chốt; người/ngày xác nhận:
File schema/fixture/tài liệu đã cập nhật:
```

## 4. Quy tắc cập nhật

1. Owner chọn phương pháp nội bộ trong baseline, tự kiểm tra và ghi đề xuất. Không cần họp cả nhóm cho mọi chi tiết thư viện.
2. Bên nhận/reviewer kiểm tra ví dụ và chạy lại phần bàn giao. Mỗi task vẫn có một owner; người kiểm thử không thay tự kiểm tra.
3. Đổi contract phải có schema và fixture cùng các module bị ảnh hưởng. Dũng tổng hợp thay đổi phạm vi/phân công/mốc; Đức Anh điều phối contract và tích hợp.
4. Chỉ chuyển ĐÃ CHỐT khi có quyết định được xác nhận, minh chứng và tài liệu sở hữu đã cập nhật. Dòng đề xuất không tự thành quyết định cả nhóm.
5. Giữ lịch sử phương án/căn cứ khi điều chỉnh; không ghi đè gold, kết quả nghiên cứu hoặc số đo để làm đẹp tiến độ.
6. Các file chuyên trách chỉ giữ yêu cầu/thiết kế đã thống nhất và dẫn D-ID còn mở; không sao chép nhiều bảng trạng thái khác nhau.

## 5. Tài liệu cần hoàn thiện sau đề xuất

- `api-contract.md`: D-01 tổng hợp; D-02 về nguồn, D-04 về giao tiếp dịch vụ, D-09 về giới hạn/lỗi. Chưa có trong gói.
- `development-guide.md`: D-13 tổng hợp yêu cầu/lệnh của các module; chưa có trong gói.
- `test-evaluation-plan.md`: D-11 phần kỹ thuật, D-12 phần usability; một tài liệu phân hai phần, chưa có trong gói.

Chưa tạo các file này ở dạng trống hoặc điền thông số chưa được owner quyết định. Đợt hiện tại bàn giao sáu tài liệu cũ đã đồng bộ, register này và changes-hci.md.
