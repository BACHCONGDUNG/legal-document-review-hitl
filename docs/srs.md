# SRS — Đặc tả yêu cầu phần mềm

**Học phần và nhóm:** 2627I_INT2041_1 Nhóm 6  
**Dự án:** Legal Document Change Detection  
**Phiên bản:** HCI 1.0.0  
**Ngày cập nhật:** 15/10/2026  
**Tài liệu nền:** [BRD](brd.md), [Nghiên cứu người dùng](user-research.md)

## 1. Phạm vi đặc tả

SRS quy định chức năng có thể kiểm tra, dữ liệu bàn giao cho giao diện, trạng thái rà soát và xử lý lỗi. Bài toán, người dùng, giá trị, phạm vi nghiệp vụ và tiêu chí mức tác động theo BRD; kết quả trao đổi người dùng theo User Research. Kiến trúc module, thư viện và thiết kế màn hình được quản lý trong tài liệu tương ứng.

Bản đầu xử lý một cặp V1–S và tài liệu tham chiếu do người dùng cung cấp. Mỗi lượt phân tích dùng request đồng bộ; nhận xét được quản lý trong phiên ở frontend. Bốn nhóm phân tích theo BRD là thời hạn; giá trị định lượng; điều kiện/ngoại lệ; chủ thể và quyền/nghĩa vụ.

Tên trường và mã trạng thái trong SRS này là hợp đồng đầu ra HCI. Có thể tái sử dụng module PoCS thông qua bước chuyển đổi dữ liệu; không yêu cầu module nội bộ phải thay toàn bộ schema theo giao diện. Khi đổi hợp đồng, bên cung cấp và bên nhận phải cập nhật cùng fixture và ca kiểm thử.

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

## 3. Dữ liệu đầu vào và báo cáo

### 3.1. Đầu vào mỗi lượt

| Trường | Kiểu | Quy định |
| --- | --- | --- |
| base_file | File | Bắt buộc, vai trò V1 |
| amendment_file | File | Bắt buộc, vai trò S |
| reference_files | File[] | Có thể rỗng; mỗi tệp có định danh riêng |

Giới hạn dung lượng, số tệp và thời gian xử lý quản lý trong cấu hình/API contract, hiển thị trước khi gửi. Giữ lựa chọn file trong phiên để gửi lại; nếu trình duyệt đã mất quyền truy cập file thì yêu cầu chọn lại. Tên file không được dùng để tự xác nhận số hiệu, vai trò pháp lý hoặc hiệu lực.

### 3.2. Hợp đồng đầu ra tối thiểu

Các trường dưới đây là dữ liệu JSON; `null` nghĩa là chưa có giá trị theo quy tắc của từng trường. Mảng rỗng không được dùng để che lỗi hoặc bước chưa thực hiện.

| Đối tượng | Trường bắt buộc | Ý nghĩa |
| --- | --- | --- |
| DocumentIdentity | document_id, role, filename | role: BASE / AMENDMENT / REFERENCE; không trả đường dẫn nội bộ |
| EvidenceRef | document_id, source_refs, quote | Trích nguyên văn, gắn với đúng file và vị trí |
| ReferenceRequirement | reference_id, document_label, target_locator, reason, status, affected_item_ids | status: AVAILABLE / MISSING / UNRESOLVED; tên/vị trí chưa xác định cho phép null và phải giải thích |
| ProcessingIssue | code, message, affected_item_ids | Lỗi/cảnh báo dễ hiểu, chỉ ra phần bị ảnh hưởng; [] nếu ảnh hưởng toàn báo cáo |
| EffectInfo | text, applies_to, evidence, needs_review, review_reason | Nội dung hiệu lực/chuyển tiếp và căn cứ; phạm vi chưa rõ cho phép null |
| ComparisonReport | comparison_id, documents, status, general_context, general_context_evidence, items, reference_requirements, effect_info, warnings, errors | Một báo cáo của một lần phân tích; comparison_id mới mỗi lần |

`ComparisonReport.status`: SUCCESS / PARTIAL / FAILED theo mục 5. `general_context` là thông tin tổng quát V1; có thể null nếu chưa tạo được, kèm cảnh báo. Nhận xét người dùng không nằm trong đầu ra AI của backend.

### 3.3. Mục kết quả và các khía cạnh

Đơn vị người dùng rà soát là `ReviewItem`: một nhận định thay đổi cụ thể có thể kiểm tra riêng, gắn với chỉ dẫn sửa đổi. Nếu chưa tạo được nhận định vì liên kết/lỗi phân tích, vẫn trả một mục thể hiện chỉ dẫn và vấn đề. Không làm mất chỉ dẫn chỉ vì AI không trả kết quả.

| Trường ReviewItem | Kiểu/giá trị | Quy định |
| --- | --- | --- |
| item_id | string | Duy nhất trong báo cáo; dùng để ghi nhận và đếm mục rà soát |
| amendment_id | string | Nhiều mục có thể thuộc một chỉ dẫn sửa đổi |
| instruction | EvidenceRef | Chỉ dẫn từ S |
| target_document, target_locator | string hoặc null | Văn bản và vị trí bị tác động; chưa rõ phải cảnh báo |
| applicability | APPLIES / OTHER_DOCUMENT / UNRESOLVED | OTHER_DOCUMENT giữ trong danh sách phạm vi, không tính vào mục rà soát V1 |
| operation | AMEND / ADD / REPEAL / UNRESOLVED | Đổi số/gộp–tách được mô tả trong chỉ dẫn và giải thích, không ép thành thêm/xóa |
| before_text, after_text | string hoặc null | Nội dung cục bộ; phân biệt không tồn tại do thêm/bãi bỏ với chưa xác định |
| before_status | PRESENT / ABSENT / UNRESOLVED | ABSENT chỉ khi xác nhận không có nội dung cũ, chẳng hạn bổ sung mới |
| after_basis | QUOTED / DERIVED / ABSENT / UNRESOLVED | DERIVED là nội dung suy ra cục bộ, không phải trích nguyên văn hoặc V2 chính thức |
| text_changes | TextChange[] hoặc null | null khi chưa đủ căn cứ/chưa xử lý; [] khi đã so sánh nhưng không có khác biệt chữ |
| is_meaningful_change | boolean hoặc null | true: đổi nội dung; false: tương đương có căn cứ; null: chưa xác định |
| explanation | string hoặc null | Nhận định tổng thể; không tạo được thì null và ghi lý do |
| aspects | ChangeAspect[] | Giữ các khía cạnh đã xác định; [] không tự có nghĩa không đổi nghĩa |
| evidence | EvidenceRef[] | Nguồn hỗ trợ nhận định tổng thể và ngữ cảnh |
| significance | LOW / MEDIUM / HIGH / CRITICAL hoặc null | Có giá trị phải có significance_reason và bằng chứng; dùng rubric đã chốt |
| significance_reason | string hoặc null | null khi chưa chấm được, lý do thiếu ở review_reason |
| needs_review, review_reason | boolean, string | Bất định của hệ thống, độc lập với nhận xét người dùng; false thì lý do rỗng |

**ChangeAspect:** `aspect_id`, `field_group`, `old_value`, `new_value`, `interpretation`, `evidence`, `needs_review`, `review_reason`. Giá trị trước/sau cho phép null khi không tồn tại hoặc chưa xác định; diễn giải phải nói rõ trường hợp nào. Nội dung diễn giải không được đưa vào `EvidenceRef.quote` như trích nguyên văn.

| field_group HCI | Nhóm theo BRD |
| --- | --- |
| TIME_LIMIT | Thời hạn thực hiện; không dùng cho ngày hiệu lực văn bản |
| QUANTITATIVE | Giá trị định lượng, giữ đủ đơn vị và điều kiện |
| CONDITIONS_EXCEPTIONS | Điều kiện và ngoại lệ |
| SUBJECT_RIGHTS_DUTIES | Chủ thể và quyền/nghĩa vụ; diễn giải phải chỉ rõ thành phần thay đổi |

Một mục có nhiều khía cạnh, không ép về một nhãn chính rồi bỏ phần còn lại. Chỉ đổi diễn đạt có thể có aspects = []; vẫn giữ giải thích và bằng chứng. Nếu ngoài phạm vi hoặc chưa phân nhóm được thì giữ chỉ dẫn, dùng cảnh báo tương ứng và không khẳng định đã phân tích đầy đủ. Trường hợp chỉ đổi dẫn chiếu, nêu thay đổi trực tiếp và tài liệu thiếu; không ép thành một khía cạnh đổi nghĩa thuộc bốn nhóm khi chưa đủ căn cứ.

**TextChange:** `type` (INSERT / DELETE / REPLACE), `old_start`, `old_end`, `new_start`, `new_end`. Vị trí ký tự bắt đầu từ 0, khoảng [start, end), khớp chính xác before_text/after_text đã trả. Phía ABSENT được dùng chuỗi rỗng khi tính vị trí; phía UNRESOLVED không được thay bằng chuỗi rỗng để chạy diff.

**Quy tắc nguồn:** document_id + source_ref xác định nguồn duy nhất trong lượt phân tích. PDF hiển thị trang tính từ 1; DOCX dùng đoạn/bảng có chỉ số theo quy ước Reader đã thống nhất, không suy ra trang Word. Mỗi trích dẫn phải truy được nội dung tương ứng để giao diện hiển thị; có thể trả thêm danh sách SourceBlock (document_id, source_ref, text) hoặc cơ chế truy xuất tương đương trong cùng phiên. Khi nguồn chỉ định vị tới Điều hoặc trang, phải ghi đúng mức chính xác đó, không giả định đã định vị tới từng ký tự.

### 3.4. Dữ liệu nhận xét trong phiên

Frontend quản lý `ReviewRecord` gồm:

| Trường | Quy định |
| --- | --- |
| comparison_id, item_id | Gắn với đúng phiên bản kết quả đang hiển thị |
| decision | AGREE / DISAGREE / INSUFFICIENT_BASIS hoặc null |
| note | Chuỗi ghi chú; mặc định rỗng |
| review_status | UNREVIEWED / REVIEWED / RECHECK_REQUIRED |
| previous_record | Bản nhận xét và comparison_id trước đó khi cần giữ để kiểm tra lại; null nếu không có |

Không dùng số Điều hoặc thứ tự dòng làm khóa nhận xét. Không coi item_id của hai lần phân tích là cùng một mục chỉ vì chuỗi giống nhau. Mục chưa xác định liên quan V1 vẫn có thể được ghi nhận chưa đủ căn cứ; mục OTHER_DOCUMENT không nằm trong tổng số rà soát V1. Đếm theo ReviewItem, ghi rõ đây là số mục rà soát, không gọi là số Điều hoặc số chỉ dẫn.

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

- Lượt mới thành công nhận comparison_id mới. Giữ bản nhận xét cũ trong phiên để đối chiếu.
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

### 5.2. Mã lỗi và cảnh báo tối thiểu

| Mã | Trường hợp | Hành vi |
| --- | --- | --- |
| INVALID_INPUT | Thiếu file chính, định dạng/giới hạn không hợp lệ | Không chạy pipeline; chỉ rõ cần sửa gì |
| UNREADABLE_DOCUMENT | File hỏng/mật khẩu/không có chữ đọc được | Chỉ rõ file; file chính lỗi thì không tạo báo cáo hợp lệ; tham chiếu lỗi không che kết quả khác nếu vẫn phân tích được |
| STRUCTURE_UNRESOLVED | Không nhận diện cấu trúc cần thiết trong V1/S | FAILED nếu không thể tiếp tục; PARTIAL nếu chỉ ảnh hưởng một phần có thể chỉ ra |
| LINK_UNCERTAIN | Đích sửa đổi chưa rõ | Giữ chỉ dẫn, ứng viên nếu có và lý do; không tự chốt thêm/bãi bỏ |
| REFERENCE_MISSING | Thiếu tài liệu cần thiết | PARTIAL và ReferenceRequirement tương ứng |
| REFERENCE_UNRESOLVED | Có tệp nhưng chưa tìm/kiểm tra được nội dung cần thiết | Giữ yêu cầu bổ sung/làm rõ và cảnh báo phần bị giới hạn |
| ANALYSIS_UNRESOLVED | AI lỗi, phản hồi sai cấu trúc hoặc chưa đủ căn cứ | Giữ dữ liệu nguồn và nhận định đã xác định; phần chưa có trả null kèm lý do |
| OUT_OF_SCOPE | Loại nội dung chưa hỗ trợ | Giữ chỉ dẫn và thông tin phạm vi, không báo đã phân tích đầy đủ |
| TIMEOUT | Hết thời gian chờ | Báo chưa nhận được kết quả; cho chủ động thử lại, không tự gửi lại |

Có chỉ dẫn mà chưa phân tích được vẫn phải hiển thị chỉ dẫn. Chỉ thông báo không tìm thấy yêu cầu tác động V1 khi SUCCESS, đã xử lý hết S trong phạm vi và không còn đối tượng/phần chưa xác định. Text Diff rỗng hoặc aspects rỗng không đủ để kết luận này.

## 6. Yêu cầu sử dụng và vận hành

- Trạng thái, loại thay đổi và cảnh báo phải có chữ/ký hiệu dễ hiểu, không chỉ dùng màu. Các thao tác chính dùng được bằng bàn phím và có nhãn nhận diện.
- Không bắt người dùng đọc lỗi kỹ thuật nội bộ. Mỗi lỗi có hướng tiếp tục: chọn lại file, bổ sung căn cứ, thử lại hoặc xem kết quả còn dùng được.
- Nhận xét tồn tại khi điều hướng/lọc trong cùng phiên; không cam kết giữ sau đóng tab/tải lại. Thông báo rõ giới hạn trước khi người dùng bắt đầu lưu nhận xét.
- File tạm backend xóa sau request kể cả lỗi; nội dung nguồn cần cho báo cáo phải được trả về trước khi xóa. Frontend giữ dữ liệu/file cần gửi lại trong phiên, không yêu cầu tài khoản hoặc kho lịch sử.
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

Trước tích hợp, nhóm cần chốt fixture JSON, quy tắc nhận diện mục qua các lần chạy, rubric mức tác động, các giới hạn cấu hình và tên file tài liệu trong kho mã. Không đổi trường bàn giao mà không cập nhật bên nhận. Phương pháp đo, ngưỡng chất lượng kỹ thuật, tác vụ usability và SUS được quản lý ở kế hoạch đánh giá, không lặp lại BRD trong SRS.
