# SRS — Đặc tả yêu cầu phần mềm

**Học phần và nhóm:** 2627I_INT2041_1 Nhóm 6
**Dự án:** Legal Document Change Detection
**Phiên bản:** HCI 1.1.0
**Tài liệu nền:** [BRD](brd.md), [Nghiên cứu người dùng](user-research.md)

## 1. Phạm vi đặc tả

SRS quy định chức năng có thể kiểm tra, dữ liệu bàn giao cho giao diện, trạng thái rà soát và xử lý lỗi. Bài toán, người dùng, giá trị, phạm vi nghiệp vụ và tiêu chí mức tác động theo BRD; kết quả trao đổi người dùng theo User Research. Kiến trúc module, thư viện và thiết kế màn hình được quản lý trong tài liệu tương ứng.

Bản đầu xử lý một cặp V1–S và tài liệu tham chiếu do người dùng cung cấp. Mỗi lượt phân tích dùng request đồng bộ; nhận xét được quản lý trong phiên ở frontend. Bốn nhóm phân tích theo BRD là thời hạn; giá trị định lượng; điều kiện/ngoại lệ; chủ thể và quyền/nghĩa vụ.

Tên trường và mã trạng thái trong SRS này là hợp đồng đầu ra HCI. Module nội bộ có thể dùng cấu trúc xử lý riêng nhưng phải chuyển kết quả sang contract HCI trước khi trả cho giao diện. Khi đổi hợp đồng, bên cung cấp và bên nhận phải cập nhật cùng fixture và ca kiểm thử.

### 1.1. Baseline và hiện trạng

POST `/api/compare` nhận multipart `doc_v1`, `doc_s` và `reference_files` tùy chọn. `ComparisonReport` gồm `comparison_id`, `base_document`, `amendment_document`, `reference_documents`, `status`, `results`, `warnings` và `errors`. Mỗi phần tử `results` là một `AmendmentResult`.

`backend.demo:app` gắn runner xử lý DOCX bằng quy tắc cục bộ và cung cấp giao diện. Client LightRAG HTTP đã có kiểm thử mô phỏng. Nhận xét trong phiên, đọc thêm nguồn và kiểm tra lại thuộc phần mở rộng HCI.

## 2. Yêu cầu chức năng

| Mã | Chức năng | Điều kiện kiểm tra |
| --- | --- | --- |
| FR-01 | Chọn và kiểm tra đầu vào | Có hai vị trí chọn V1/S và phần thêm tài liệu tham chiếu. Nhận DOCX và PDF có lớp chữ; thiếu file chính, sai định dạng, file hỏng/mật khẩu hoặc không đọc được phải báo đúng file và hướng xử lý. Backend kiểm tra lại đầu vào, không chỉ dựa vào frontend. |
| FR-02 | Đọc nội dung và truy nguồn | Giữ thứ tự nội dung, ranh giới Khoản/Điểm và bảng đọc được; giữ định danh tài liệu, đoạn/bảng DOCX hoặc trang PDF. Không đọc được không được trả văn bản rỗng như thành công. |
| FR-03 | Trích chỉ dẫn và xác định vị trí đích | Theo chỉ dẫn trong S để xác định văn bản và Điều/Khoản/Điểm/cụm từ bị tác động. Phân biệt phần thuộc V1, thuộc văn bản khác và chưa xác định. Bổ sung, bãi bỏ, đổi số và gộp/tách phải giữ chỉ dẫn; thiếu căn cứ thì báo chưa chắc chắn, không tự kết luận thêm/xóa. |
| FR-04 | Chuẩn bị nội dung đối chiếu | Cung cấp nội dung gốc, nội dung mới hoặc chỉ dẫn tương ứng; phân biệt trích từ nguồn với nội dung suy ra cục bộ. Text Diff chỉ chạy khi đủ căn cứ; vị trí tô sáng khớp chuỗi được trả về. |
| FR-05 | Phân tích và giải thích | Với nhóm trong phạm vi, trả nhận định trước–sau, các khía cạnh thay đổi, bằng chứng và trạng thái đủ/chưa đủ căn cứ. Giữ chủ thể, đơn vị, điều kiện và ngoại lệ liên quan; không chỉ trả tên nhóm hoặc bản tóm tắt chung. |
| FR-06 | Mức tác động | Trả mức và lý do theo hướng dẫn nhãn. Chưa đủ căn cứ thì trả null và lý do; không dùng LOW thay cho chưa xác định. Mức tác động độc lập với trạng thái người dùng đã kiểm tra. |
| FR-07 | Xem kết quả và bằng chứng | Hiển thị thông tin tổng quát V1, các chỉ dẫn và thay đổi liên quan, nội dung đối chiếu, nguồn, mức tác động, cảnh báo và phạm vi xử lý. Chọn bằng chứng phải đọc được đoạn trích cùng tài liệu/vị trí trong giao diện; chưa bắt buộc nhúng trình xem file hoặc mở đúng trang file gốc. |
| FR-08 | Ghi nhận nhận xét | Người dùng chọn đồng ý/không đồng ý/chưa đủ căn cứ, thêm hoặc sửa ghi chú, lưu và xóa nhận xét trong phiên. Không ghi đè đầu ra AI hoặc tự huấn luyện lại mô hình. |
| FR-09 | Tổng hợp và lọc rà soát | Hiển thị số mục chưa kiểm tra/đã kiểm tra/cần kiểm tra lại. Lọc được theo trạng thái rà soát, nhận xét, cảnh báo và mức tác động. Tổng số và chi tiết phải dùng cùng đơn vị đếm. |
| FR-10 | Yêu cầu tài liệu còn thiếu | Trả tên/số hiệu nếu xác định được, phần cần đọc, lý do và mục bị ảnh hưởng. Giữ kết quả xác định được; tài liệu có file nhưng không tìm được nội dung cần thiết vẫn phải báo chưa giải quyết. |
| FR-11 | Bổ sung và phân tích lại | Gửi lại V1/S cùng bộ tham chiếu hiện có và tài liệu bổ sung. Không tự gửi lại khi timeout. Khi thành công, chỉ rõ mục cập nhật, đối chiếu nhận xét theo quy tắc mục 4; khi thất bại giữ báo cáo và nhận xét trước đó. |
| FR-12 | Thông tin hiệu lực và chuyển tiếp | Giữ nội dung, phạm vi và bằng chứng xác định được trong S; chưa rõ thì cảnh báo. Không coi trích ngày hiệu lực là xác minh hiệu lực thực tế. |

Yêu cầu bổ sung của phương án B: kết quả truy xuất phải ánh xạ được về nguồn V1/S/tham chiếu của đúng lần so sánh. Dịch vụ lỗi hoặc truy xuất rỗng không tự chứng minh tài liệu thiếu hay không có thay đổi. Đây là yêu cầu của FR-02/05/10/11, không thay các chức năng kiểm chứng của HCI.

## 3. Dữ liệu đầu vào và báo cáo

### 3.1. Đầu vào mỗi lượt

POST `/api/compare` nhận multipart `doc_v1`, `doc_s` và `reference_files` tùy chọn. `ComparisonReport` gồm `comparison_id`, `base_document`, `amendment_document`, `reference_documents`, `status`, `results`, `warnings` và `errors`. Mỗi phần tử `results` là một `AmendmentResult`.

### 3.2. Hợp đồng đầu ra

Nguồn chuẩn là [contracts.py](../backend/app/schemas/contracts.py), [validator](../backend/app/schemas/report_validation.py) và [fixture báo cáo](../test/fixtures/reports/common_contract.json). Mỗi `AmendmentResult` giữ chỉ dẫn `amendment`, ngữ cảnh, `text_diff`, `semantic_diff`, `scoring` và cảnh báo/lỗi theo schema. `semantic_diff.changes` chứa từng nhận định và các `aspects`. `scoring` nối với nhận định bằng `change_id` trong chỉ dẫn tương ứng.

### 3.3. Nhóm phân tích và bằng chứng

Tám nhóm `field_group` là SUBJECT_OBJECT, RIGHTS_DUTIES_ACTIONS, CONDITIONS_EXCEPTIONS, TIME_QUANTITY, PROCEDURE_AUTHORITY, CONSEQUENCES_SANCTIONS, DEFINITIONS_REFERENCES và SCOPE_EFFECT_TRANSITION. `category`, `significance`, `is_critical`, `needs_review` và `review_reason` tuân theo validator. Một thay đổi chỉ về diễn đạt dùng `WORDING_ONLY` và `LOW`; mức chưa xác định giữ `significance` và `is_critical` ở null cùng lý do review. Giao diện demo đọc trích dẫn và vị trí từ bằng chứng trong báo cáo. Cơ chế mở thêm nguồn sau khi dọn file thuộc D-07.

### 3.4. Dữ liệu nhận xét trong phiên

Frontend quản lý `ReviewRecord` gồm:

| Trường | Quy định |
| --- | --- |
| comparison_id, amendment_id, change_id (nếu rà soát theo nhận định) | Khóa dự kiến gắn với đúng kết quả đang hiển thị; D-08 chốt đơn vị nhận xét |
| decision | AGREE / DISAGREE / INSUFFICIENT_BASIS hoặc null |
| note | Chuỗi ghi chú; mặc định rỗng |
| review_status | UNREVIEWED / REVIEWED / RECHECK_REQUIRED |
| previous_record | Bản nhận xét và comparison_id trước đó khi cần giữ để kiểm tra lại; null nếu không có |

Khóa nhận xét dự kiến gắn với báo cáo và mục đang hiển thị. Khi phân tích lại, D-08 quyết định cách đối chiếu và đánh dấu nhận xét cần xem lại.

### 3.5. Trách nhiệm dữ liệu

Pipeline tổng hợp kết quả theo schema HCI và kiểm tra bằng validator. D-06 tiếp tục review ví dụ, cách chia/gộp nhận định và rubric. D-07 và D-08 phụ trách nguồn mở rộng và nhận xét trong phiên.

## 4. Trạng thái và vòng đời nhận xét

### 4.1. Thao tác trong phiên

| Sự kiện | Trạng thái yêu cầu |
| --- | --- |
| Kết quả lần đầu | UNREVIEWED, decision = null, note rỗng |
| Chỉ sửa ghi chú | Giữ UNREVIEWED nếu chưa lưu một nhận xét có decision |
| Lưu nhận xét | Bắt buộc chọn một decision; chuyển REVIEWED, lưu note |
| Chọn “Chưa đủ căn cứ” rồi lưu | REVIEWED + INSUFFICIENT_BASIS; vẫn có thể needs_review = true từ AI |
| Sửa nhận xét đã lưu | Chỉ cập nhật khi người dùng lưu; hủy sửa giữ bản trước |
| Xóa nhận xét | Xác nhận xóa; về UNREVIEWED, xóa decision/note; không xóa kết quả AI |
| Chuyển bộ V1/S khác hoặc bắt đầu phiên mới | Cảnh báo nếu mất nhận xét; chỉ đặt lại khi người dùng xác nhận |

Đang gửi request thì ngăn gửi lặp và hiển thị đang xử lý; không hiển thị phần trăm tiến độ không có dữ liệu thật. Người dùng vẫn đọc được kết quả cũ khi phân tích lại, nhưng tạm khóa lưu/sửa nhận xét cho tới khi request kết thúc để tránh gắn nhầm phiên bản.

### 4.2. Sau khi bổ sung tài liệu

- Lượt mới trả SUCCESS hoặc PARTIAL có kết quả dùng được nhận comparison_id mới và được đối chiếu. Giữ bản nhận xét cũ trong phiên; FAILED/timeout không thay báo cáo và nhận xét đang có.
- Chỉ chuyển tiếp REVIEWED khi xác định được cùng mục và toàn bộ nội dung phục vụ kiểm chứng không đổi: chỉ dẫn/đích, nội dung trước–sau, giải thích/khía cạnh, bằng chứng, mức tác động và cảnh báo. So sánh nội dung nguồn, không chỉ document_id hoặc vị trí trong danh sách.
- Nếu cùng mục nhưng nội dung liên quan đổi, chuyển RECHECK_REQUIRED, decision hiện tại = null; giữ nhận xét cũ riêng trong previous_record để người dùng đọc và quyết định lại.
- Mục mới là UNREVIEWED. Không ghép chắc chắn được sau chia/gộp hoặc thay đổi định danh thì không chuyển xác nhận cũ; giữ nhận xét cũ trong danh sách “Nhận xét chưa đối chiếu được”, nêu rõ chúng thuộc báo cáo trước.
- Mục cũ không còn xuất hiện không được âm thầm xóa nhận xét hoặc hiểu thành người dùng đã xác nhận không thay đổi. Chỉ đưa vào danh sách nhận xét cũ; không cộng vào tổng mục hiện tại.
- Khi người dùng lưu nhận xét cho mục RECHECK_REQUIRED, chuyển REVIEWED cho phiên bản mới. Request mới thất bại/timeout giữ nguyên báo cáo và nhận xét trước đó.

Cơ chế nhận diện cùng mục và so sánh phiên bản cần được backend/frontend thống nhất bằng fixture. Khi chưa triển khai được đối chiếu đáng tin cậy, dùng phương án an toàn: mọi mục đã kiểm tra mà nhận diện được được yêu cầu kiểm tra lại; mục không ghép được giữ nhận xét cũ riêng. Không tự giữ xác nhận chỉ dựa trên số Điều.

## 5. Kết quả xử lý và lỗi

### 5.1. Trạng thái báo cáo

| status | Điều kiện |
| --- | --- |
| SUCCESS | Hoàn tất các bước trong phạm vi; có thể còn bất định cần người dùng kiểm tra, phải nêu lý do |
| PARTIAL | Có kết quả dùng được nhưng có phần chưa xử lý hoặc bị giới hạn vì thiếu căn cứ; liệt kê rõ mục bị ảnh hưởng |
| FAILED | Không tạo được kết quả dùng được; báo lý do, không đưa danh sách rỗng như kết luận không thay đổi |

Thiếu tài liệu cần thiết để phân tích tác động → PARTIAL. Không chắc một liên kết nhưng đã giữ chỉ dẫn và trạng thái chưa xác định không tự đồng nghĩa request thất bại; nếu vì thế không phân tích được một phần yêu cầu thì PARTIAL. SUCCESS không có nghĩa AI chắc chắn đúng.

### 5.2. Lỗi API và báo cáo

Route `POST /api/compare` dùng xử lý lỗi trong [backend/main.py](../backend/main.py). Lỗi upload hoặc vận hành có thể trả HTTP ngoài 2xx. Một request HTTP 200 vẫn có thể chứa `report.status = FAILED`; UI đọc trạng thái, lỗi và cảnh báo trong báo cáo trước khi hiển thị kết luận. `backend.main:app` mặc định trả HTTP 501 và `ANALYSIS_NOT_CONFIGURED` khi đầu vào hợp lệ và runner chưa được gắn. Giao diện demo dùng `backend.demo:app`.

## 6. Yêu cầu sử dụng và vận hành

- Trạng thái, loại thay đổi và cảnh báo phải có chữ/ký hiệu dễ hiểu, không chỉ dùng màu. Các thao tác chính dùng được bằng bàn phím và có nhãn nhận diện.
- Không bắt người dùng đọc lỗi kỹ thuật nội bộ. Mỗi lỗi có hướng tiếp tục: chọn lại file, bổ sung căn cứ, thử lại hoặc xem kết quả còn dùng được.
- Nhận xét tồn tại khi điều hướng/lọc trong cùng phiên; không cam kết giữ sau đóng tab/tải lại. Thông báo rõ giới hạn trước khi người dùng bắt đầu lưu nhận xét.
- File tạm và dữ liệu chỉ mục phục vụ từng comparison phải được dọn sau khi mọi tác vụ sử dụng đã kết thúc, kể cả lỗi. Nội dung nguồn cần cho báo cáo phải tới frontend trước khi dọn. Không xóa nguồn khi converter/Server còn chạy chỉ vì HTTP hết thời gian. Frontend giữ dữ liệu/file cần gửi lại trong phiên; không yêu cầu tài khoản hoặc kho lịch sử.
- Backend nghiệp vụ giữ request đồng bộ và không có job/polling cho người dùng. Nếu Server nhập dữ liệu nền, client theo dõi hoàn tất nội bộ trong deadline; cách làm cụ thể ở D-04/D-09. Không mặc định nhập xong là index sẵn sàng hoặc comparison_id tự cách ly dữ liệu.
- HTTP localhost không bắt buộc Internet; chưa chọn mô hình/embedding nên chưa cam kết offline toàn hệ thống. LLM/embedding, nơi chạy và chi phí là quyết định D-05/D-13; không đổi phạm vi HCI vì mặc định framework.
- Không ghi toàn văn tài liệu/ghi chú vào log; log phục vụ chẩn đoán có comparison_id, bước, mã lỗi và thời gian. Không trả đường dẫn nội bộ hoặc khóa API cho frontend.
- Nếu dùng API AI ngoài, khóa đặt ở backend; nội dung gửi ra ngoài và cấu hình mô hình phải được nhóm chốt, ghi rõ trong hướng dẫn vận hành. Cấu hình phải đủ để tái lập thử nghiệm.
- Dung lượng/số file/timeout được công bố và kiểm tra cả hai phía. Chưa cam kết tốc độ bằng số trước khi đo trên mẫu và môi trường cụ thể; ghi nhận thời gian xử lý theo kích thước đầu vào.
- Không âm thầm cắt nội dung hoặc bỏ chỉ dẫn. Khi vượt khả năng xử lý, nêu phần bị ảnh hưởng và trạng thái tương ứng.

## 7. Ca nghiệm thu trọng tâm

Mỗi ca dùng fixture có đáp án, nguồn và đầu ra mong đợi. Đây là kiểm tra yêu cầu phần mềm; đánh giá với người dùng và chất lượng AI thực hiện theo kế hoạch đánh giá riêng.

| Ca | Nội dung | Điều kiện đạt |
| --- | --- | --- |
| AT-01 | DOCX/PDF text; sai định dạng, scan, thiếu file | Nhận đầu vào hợp lệ; lỗi chỉ rõ file; không trả kết quả giả |
| AT-02 | S có nhiều chỉ dẫn và sửa nhiều văn bản | Giữ chỉ dẫn, đúng đích và phạm vi; không coi phần V1 không được nhắc tới là bị xóa |
| AT-03 | Thêm/bãi bỏ và nội dung chưa xác định | Phân biệt ABSENT với UNRESOLVED; diff không tô sai vì dữ liệu thiếu |
| AT-04 | Bốn nhóm thay đổi và sửa diễn đạt | Giữ các khía cạnh/bằng chứng; phân biệt time limit với ngày hiệu lực; trường hợp chưa xác định không bị ép false/LOW |
| AT-05 | Đổi số/gộp–tách hoặc đích mơ hồ | Giữ nguồn và cảnh báo; không ép ghép một–một |
| AT-06 | Đọc bằng chứng và cảnh báo | Đúng file, đúng trích dẫn/vị trí; cảnh báo có nhãn chữ và không bị mất khi lọc |
| AT-07 | Lưu/sửa/xóa và lọc nhận xét | Ba decision hoạt động; trạng thái rà soát độc lập AI; đếm mục nhất quán |
| AT-08 | Thiếu rồi thêm tài liệu tham chiếu | Kết quả ban đầu PARTIAL; lượt mới có ID mới; thay đổi được nhận diện và nhận xét bị ảnh hưởng cần kiểm tra lại |
| AT-09 | Chia/gộp mục giữa hai lượt, không ghép chắc chắn | Không gắn nhầm nhận xét; nhận xét cũ vẫn đọc được và không nằm trong tổng mục hiện tại |
| AT-10 | Lỗi AI, timeout hoặc phân tích lại thất bại | Giữ nguồn/kết quả có ích; giữ báo cáo và nhận xét cũ; không tự gửi lặp |
| AT-11 | Nội dung ngoài phạm vi, hiệu lực/chuyển tiếp | Báo rõ phạm vi và bằng chứng; không hiển thị như kết luận không thay đổi |
| AT-12 | Truy xuất ngữ cảnh, index chưa sẵn sàng và lỗi dịch vụ | Đợi hoàn tất có giới hạn; nguồn đối chiếu được; lỗi không thành kết luận thiếu tài liệu hoặc không đổi |
| AT-13 | Hai bộ tài liệu và kết thúc xử lý | Không tìm lẫn nguồn; dọn đúng bộ khi tác vụ kết thúc, không làm hỏng bộ khác |

Trước tích hợp, nhóm cần chốt fixture JSON, quy tắc nhận diện mục qua các lần chạy, rubric mức tác động, các giới hạn cấu hình và tên file tài liệu trong kho mã. Không đổi trường bàn giao mà không cập nhật bên nhận. Phương pháp đo, ngưỡng chất lượng kỹ thuật, tác vụ usability và SUS được quản lý ở kế hoạch đánh giá, không lặp lại BRD trong SRS.

## 8. Các lựa chọn chờ module owner

Danh sách duy nhất để theo dõi là [Module Owner Decisions](module-owner-decisions-hci.md): D-01/D-02 cho contract và nguồn, D-03/D-04 cho linker/context/LightRAG, D-05/D-06 cho phân tích và nhãn, D-07/D-08 cho frontend/đối chiếu lượt, D-09/D-13 cho vận hành, D-10/D-11/D-12 cho dữ liệu và đánh giá. Đó là việc cần đề xuất và review, không phải các lựa chọn đã được owner xác nhận.
