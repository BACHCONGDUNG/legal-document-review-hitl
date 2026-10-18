# Hướng dẫn dữ liệu và gán nhãn

**Học phần và nhóm:** 2627I_INT2041_1 Nhóm 6  
**Dự án:** Legal Document Change Detection  
**Phiên bản:** HCI 1.1.0  
**Trạng thái:** Bản đề xuất để nhóm review  
**Ngày cập nhật:** 17/10/2026  
**Tài liệu liên quan:** [BRD](brd-hci.md),[SRS](srs-hci.md), [Architecture HCI](architecture-hci.md)

## 1. Phạm vi dữ liệu và đầu ra gán nhãn

Tài liệu hướng dẫn chuẩn bị mẫu V1–S, lập đáp án tham chiếu có bằng chứng và chuẩn bị dữ liệu kiểm thử tương tác. Phạm vi nghiệp vụ theo BRD HCI. Dữ liệu phân tích dùng chung bộ 8 mã và quy tắc gán nhãn PoCS; HCI bổ sung cách chọn mẫu ưu tiên và dữ liệu kiểm thử tương tác. Không định nghĩa lại schema API, tác vụ usability hoặc công thức chỉ số đánh giá.



Mỗi mẫu xác định rõ V1, S và bộ tài liệu tham chiếu thực sự cung cấp. Gán nhãn từng chỉ dẫn liên quan và từng nhận định thay đổi có thể kiểm tra riêng; không gán một bản ghi cho mọi Điều không thay đổi và không bắt buộc dựng V2 đầy đủ.

| Đầu ra | Nội dung cần có |
| --- | --- |
| Bộ đầu vào | File nguồn, vai trò, nguồn tải và trạng thái nền V1 |
| Nhãn tham chiếu | Chỉ dẫn, đích, nội dung trước–sau, nhóm thay đổi, giải thích, bằng chứng, mức tác động và phần chưa xác định |
| Hồ sơ review | Người gán/review, bất đồng, quyết định, phiên bản nhãn và giới hạn |
| Mẫu kiểm thử tương tác | Bộ kết quả trước/sau bổ sung tài liệu, quan hệ giữa các mục và trạng thái rà soát mong đợi |

Đáp án được lập từ nguồn đã kiểm tra, độc lập với dự đoán AI. Nhận xét AGREE/DISAGREE/INSUFFICIENT_BASIS của người dùng không thay thế nhãn đúng của hệ thống. Kết quả phỏng vấn, dữ liệu người tham gia và SUS không lưu chung như nhãn pháp lý.

## 2. Chọn nguồn và tổ chức bộ mẫu

### 2.1. Tiêu chí nhận mẫu

- V1 và S có quan hệ sửa đổi được xác định từ nội dung; V1 phù hợp trạng thái trước lần sửa đang xét. Chưa kiểm tra được các sửa đổi trước có liên quan thì ghi giới hạn, không mặc định nền đã đầy đủ.
- DOCX hoặc PDF có lớp chữ đọc được; không OCR. File scan, hỏng, mật khẩu hoặc sai cặp có thể giữ riêng làm ca lỗi, không coi là mẫu hợp lệ.
- S sửa nhiều văn bản thì giữ đầy đủ S; ghi APPLIES/OTHER_DOCUMENT/UNRESOLVED theo từng chỉ dẫn. Không nhập các yêu cầu sửa văn bản khác vào V1 được chọn.
- Ghi nguồn tải từ VBPL/cổng thông tin nhà nước khi có; đối chiếu số hiệu, tên và nội dung. Không tự tạo URL hoặc xác nhận hiệu lực chỉ từ tên file/ngày tải.
- Mẫu đủ và thiếu tham chiếu phải xác định đúng căn cứ có mặt. Tài liệu chỉ dùng để người gán nhãn kiểm tra được ghi riêng, không giả định hệ thống đã được nhận.

Khi chuyển `.doc` sang DOCX hoặc chuẩn bị DOCX từ PDF, giữ bản gốc và nhật ký chuyển đổi. Kiểm tra chữ, phủ định, số liệu, đơn vị, cấu trúc và bảng; không sao chép vị trí nguồn giữa hai định dạng khi chưa kiểm tra. Bản đầu đọc PDF trực tiếp theo thiết kế, không bắt buộc chuyển PDF sang DOCX.

### 2.2. Hồ sơ tối thiểu mỗi mẫu

Thư mục đề xuất, không xác nhận đã có dữ liệu:

```text
data/
  raw/                         # Bản nguồn giữ nguyên
  samples/HCI-001/
    <base_key>_v1.docx
    <amendment_key>_amendment.docx
    references/
    README.md                  # Nguồn, vai trò, bộ căn cứ và giới hạn
    gold.json                  # Nhãn phân tích theo cấu trúc chung PoCS
    review.md                  # Bất đồng và phiên bản nhãn
  interaction-fixtures/        # Kết quả mẫu và trạng thái tương tác mong đợi
  manifest.csv
```

PDF giữ đuôi .pdf. Văn bản gốc và S thường có số hiệu khác nhau, không buộc dùng chung base_key. Tài liệu dùng chung có thể tham chiếu đường dẫn/hash thay vì sao chép.

| Nhóm metadata | Trường cần ghi |
| --- | --- |
| Nhận diện | sample_id, lineage_id, document_id, role, local_path |
| Nguồn và nội dung | original_filename, source_url nếu có, downloaded_at, sha256, document_number/title, content_state_note |
| Chuẩn bị | origin: SOURCE / CONVERTED / DERIVED_REAL / SYNTHETIC; parent_files và preparation_log |
| Nhãn | annotator, reviewer, review_status, label_version, guideline_version, split, limitations |

Metadata quản lý không tự trở thành trường API. source_refs phải khớp đúng file và quy ước Reader. V2 dựng nội bộ ghi DERIVED_REAL và để ngoài đầu vào mẫu trừ khi chủ định cung cấp; không lấy bản dựng tự động làm đáp án đã xác nhận.

Các biến thể cùng văn bản nền/chuỗi sửa đổi giữ chung lineage_id và cùng tập dữ liệu. Không để bản PDF/DOCX hoặc mẫu đủ/thiếu tham chiếu cùng nguồn lọt sang cả tập phát triển và test. Mẫu giả định ghi SYNTHETIC, tách kết quả báo cáo với mẫu thực tế.

## 3. Quy tắc gán nhãn

### 3.1. Chỉ dẫn, nội dung và bằng chứng

1. Rà toàn bộ S, liệt kê chỉ dẫn và văn bản đích; sau đó xác định phần áp dụng V1. Theo chỉ dẫn nguồn, không ghép hai văn bản theo số Điều tương ứng.
2. Lấy đúng nội dung trước và nội dung sửa đổi, đọc thông tin tổng quát V1 cùng định nghĩa, điều kiện, ngoại lệ cần thiết. Giữ nguồn hiệu lực/chuyển tiếp liên quan theo EffectInfo, không tự xác minh hiệu lực thực tế.
3. Chia thành các SemanticChange có thể kiểm tra riêng. Một AmendmentItem có thể có nhiều changes; nhiều khía cạnh của cùng một quy định là các ChangeAspect trong một change. Hai nghĩa vụ độc lập được tách riêng dù cùng Điều hoặc cùng câu.
4. Ghi kết luận, khía cạnh và mức tác động trong phạm vi bằng chứng; giữ chỉ dẫn và lý do khi không tạo được nhận định.

| Trường hợp | Quy tắc |
| --- | --- |
| Thay toàn bộ Điều/Khoản/Điểm | AMEND; lấy đúng đơn vị cũ và nội dung thay thế; after_basis = QUOTED nếu nguyên văn trong S |
| Thay/bổ sung cụm từ trong đơn vị có sẵn | Thường là AMEND; nội dung cục bộ dựng từ chỉ dẫn dùng DERIVED, giữ nguồn V1 và S |
| Bổ sung đơn vị mới | ADD, before_text = null vì đơn vị mới chưa tồn tại; ghi vị trí chèn và nguồn nội dung mới |
| Bãi bỏ | REPEAL, after_basis = ABSENT; giữ chỉ dẫn và nội dung bị bãi bỏ |
| Chưa tìm được hoặc chưa rõ một phía | Giữ null ở nội dung chưa biết, needs_review = true và lý do; dùng UNRESOLVED ở trường trạng thái có hỗ trợ, không coi là ABSENT để suy ra thêm/xóa |
| Đổi số/gộp–tách | Theo nội dung chỉ dẫn, giữ quan hệ đích nếu xác định được; chưa rõ thì cảnh báo, không ép một–một |
| Thuộc văn bản khác | OTHER_DOCUMENT, nằm ngoài tổng mục rà soát V1 |

Gán operation theo hành vi được chỉ dẫn và đơn vị bị tác động, không chỉ từ khóa “bổ sung”. Nội dung nguyên văn đặt trong EvidenceRef.quote với document_id và source_refs; old_quote/new_quote giữ trích dẫn tương ứng theo cấu trúc chung; diễn giải đặt ở diff_details/interpretation. Không tự tạo số trang hoặc số đoạn. Nội dung DERIVED không được ghi thành trích nguyên văn hoặc bản hợp nhất chính thức.

### 3.2. Bộ 8 nhóm chung và phạm vi ưu tiên HCI

Mã và cấu trúc theo SRS PoCS 1.3.0; bảng này hướng dẫn chọn nhóm ở ca giao nhau.

| Trường hợp | Nhóm sử dụng | Quy tắc phân biệt |
| --- | --- | --- |
| Thêm một tổ chức vào đối tượng chịu nghĩa vụ | SUBJECT_OBJECT | Chủ thể phải làm; khác với cơ quan có quyền xử lý |
| “Có thể” thành “phải”, bỏ hoặc thêm nghĩa vụ | RIGHTS_DUTIES_ACTIONS | Ghi cả hành vi và tính chất bắt buộc/cho phép/cấm |
| Thêm trường hợp miễn, điều kiện kích hoạt nghĩa vụ | CONDITIONS_EXCEPTIONS | Nếu chỉ đổi số trong ngưỡng đã có thì ưu tiên TIME_QUANTITY |
| Hạn nộp, ngưỡng phút gián đoạn, tỷ lệ/số lượng | TIME_QUANTITY | Giữ đơn vị, mốc tính và dấu “quá/từ/đến”; hiệu lực thuộc nhóm khác |
| Cơ quan tiếp nhận/quyết định, phương thức báo cáo, giấy tờ | PROCEDURE_AUTHORITY | Đổi cơ quan có thẩm quyền không ghi thêm SUBJECT_OBJECT trùng |
| Tăng mức phạt hoặc đổi hình thức xử lý | CONSEQUENCES_SANCTIONS | Giá trị phạt ghi ở nhóm này, không nhân bản vào TIME_QUANTITY |
| Đổi thuật ngữ định nghĩa hoặc đích dẫn chiếu | DEFINITIONS_REFERENCES | Phân tích trực tiếp nội dung có trong bộ tài liệu được cung cấp; thiếu đích thì không suy diễn tác động |
| Địa bàn/lĩnh vực áp dụng, ngày hiệu lực, chuyển tiếp | SCOPE_EFFECT_TRANSITION | Mở rộng nhóm người chịu nghĩa vụ cụ thể ưu tiên SUBJECT_OBJECT; thời hạn thực hiện ưu tiên TIME_QUANTITY |

Một biến đổi chỉ có một nhóm; các biến đổi khác nhau của cùng quy định có thể thuộc nhiều nhóm. Không cố điền đủ 8 nhóm cho mỗi thay đổi. Định nghĩa thuật ngữ thay đổi được ghi nhóm định nghĩa; tác động tới các Điều khác chỉ ghi khi có đủ căn cứ trong phạm vi và tránh suy luận lan truyền không được kiểm chứng.

HCI ưu tiên chọn mẫu theo bốn hướng có thể kiểm chứng, nhưng không thay bộ mã gán nhãn:

| Hướng ưu tiên HCI | Mã nhãn dùng chung | Điều cần thể hiện |
| --- | --- | --- |
| Thời hạn | TIME_QUANTITY | Hạn thực hiện, mốc tính, đơn vị và ngoại lệ |
| Giá trị định lượng | TIME_QUANTITY | Số tiền, tỷ lệ, số lượng, ngưỡng; phân biệt ngưỡng thời gian với hạn thực hiện |
| Điều kiện, ngoại lệ | CONDITIONS_EXCEPTIONS | Điều kiện được thêm/bỏ/sửa và quy định bị chi phối |
| Chủ thể, quyền và nghĩa vụ | SUBJECT_OBJECT; RIGHTS_DUTIES_ACTIONS | Tách thay đổi ai chịu quy định khỏi thay đổi được làm/phải làm/bị cấm |

Bốn hướng trên là tiêu chí chọn và trình bày mẫu, không phải bốn lớp loại trừ nhau. Ví dụ mức phạt có giá trị số vẫn dùng CONSEQUENCES_SANCTIONS theo quy tắc chung. Ghi hướng ưu tiên trong hồ sơ mẫu nếu cần; không tạo field_group mới hoặc chuyển tất cả trường hợp định lượng thành TIME_QUANTITY.

Các nhóm còn lại vẫn được giữ khi có bằng chứng. Mẫu đổi dẫn chiếu đặc biệt hữu ích để thử luồng thiếu tài liệu/bổ sung tài liệu. Phần ngoài phạm vi chức năng của bản HCI phải được ghi rõ khi tạo kết quả trình diễn, không xóa nhãn nguồn hoặc đổi thành false/LOW. Các chỉ số cần nêu rõ đánh giá tập con ưu tiên hay toàn bộ bộ mẫu.

### 3.3. Kết luận và mức tác động

- `is_meaningful_change = true`: có căn cứ nội dung quy định đổi trong phạm vi phân tích; ghi khía cạnh và bằng chứng.
- `false`: có căn cứ nội dung tương đương dù khác câu chữ; aspects = [] và phải giải thích.
- `null`: chưa đủ căn cứ kết luận; needs_review = true và có review_reason. Một khía cạnh đã rõ không làm phần chưa rõ tự trở thành chắc chắn.
- Giá trị/nhận định chưa xác định khác phía không tồn tại. Dữ liệu rỗng tự nó không chứng minh không có thay đổi.

category tóm tắt SemanticChange; giữ nguyên tất cả aspects. Chỉ chọn trong các field_group đã xác định có đổi nghĩa của thay đổi đó. Quy tắc pilot đề xuất: CONSEQUENCES_SANCTIONS → RIGHTS_DUTIES_ACTIONS → SUBJECT_OBJECT → CONDITIONS_EXCEPTIONS → PROCEDURE_AUTHORITY → TIME_QUANTITY → SCOPE_EFFECT_TRANSITION → DEFINITIONS_REFERENCES. Thứ tự này là quy ước trình bày của dự án, không phải thứ tự mức tác động pháp lý.

Ví dụ có SUBJECT_OBJECT và TIME_QUANTITY thì category = SUBJECT_OBJECT; reason vẫn giải thích cả việc mở rộng chủ thể và thay ngưỡng. Trường hợp đổi nội dung quyền/nghĩa vụ và chủ thể thì ưu tiên RIGHTS_DUTIES_ACTIONS. Chưa có nhóm được xác định đủ căn cứ thì category = null và cảnh báo; chỉ đổi diễn đạt thì WORDING_ONLY. Thứ tự ưu tiên phải được nhóm review qua pilot, ghi phiên bản trước sử dụng chung.

**Mức tác động significance**

Các mức dưới đây kế thừa rubric PoCS để gán nhãn thử nghiệm; cần review chuyên môn khi có điều kiện. Chấm tác động trực tiếp thể hiện trong bộ tài liệu được cung cấp, không suy đoán vụ việc/thiệt hại thực tế hoặc coi loại văn bản là mức độ.

| Mức | Quy tắc pilot | Ví dụ và ranh giới |
| --- | --- | --- |
| LOW | Đã xác định chỉ đổi diễn đạt/hình thức, không đổi nghĩa | “chậm nhất vào ngày” thành “không muộn hơn ngày”, mọi điều kiện giữ nguyên |
| MEDIUM | Đổi nghĩa về cách thực hiện có phạm vi hẹp; giữ nguyên nghĩa vụ cốt lõi, nhóm chủ thể và điều kiện quan trọng | Thay một phương thức báo cáo bằng phương thức khác đã xác định tương đương về yêu cầu; thiếu căn cứ tương đương thì review |
| HIGH | Có căn cứ thay đổi đáng kể chủ thể, nội dung nghĩa vụ/quyền, điều kiện hoặc ngưỡng/thời hạn của quy định | Mở rộng bên chịu nghĩa vụ; hạ ngưỡng kích hoạt báo cáo sự cố. Không tự thành CRITICAL chỉ vì có số liệu |
| CRITICAL | Đảo chiều bắt buộc/cho phép/cấm hoặc loại bỏ toàn bộ một nghĩa vụ/quyền cốt lõi, có bằng chứng rõ và được reviewer xác nhận theo ví dụ ranh giới | Từ bắt buộc báo cáo sự cố thành không phải báo cáo bất kỳ sự cố nào. Chỉ bỏ một phương thức báo cáo không đủ tiêu chí này |
| null | Thiếu căn cứ phân biệt mức hoặc chưa giải quyết mơ hồ có ảnh hưởng chấm điểm | Thiếu văn bản dẫn chiếu, thiếu nội dung sau sửa đổi, hoặc chưa xác định phần bị tác động |

MEDIUM/HIGH phân biệt bằng việc đổi cách thực hiện hạn chế hay đổi phạm vi/điều kiện/nội dung nghĩa vụ đáng kể. HIGH/CRITICAL phân biệt bằng sửa đặc điểm quan trọng hay đảo chiều/loại bỏ toàn bộ nội dung cốt lõi theo rubric. Khó phân biệt phải đưa review, không chọn mức theo cảm giác hay tỷ lệ số chữ đổi.

Chỉ đổi nghĩa đã xác định không gán LOW theo rubric hiện tại. Thêm/xóa Điều đánh giá nội dung, không tự CRITICAL. Một SemanticChange có một mức significance; không cộng điểm theo số aspects. is_critical = true khi và chỉ khi significance đã xác định CRITICAL; is_critical = false với mức đã xác định khác CRITICAL, và null khi significance chưa rõ. reason nêu quy tắc được áp dụng và bằng chứng hỗ trợ, không chỉ lặp lại mức.


### 3.4. Mẫu thiếu căn cứ

ReferenceRequirement dùng AVAILABLE khi có đúng tài liệu và tìm được nội dung; MISSING khi chưa được cung cấp; UNRESOLVED khi có file nhưng chưa xác định đúng phiên bản/vị trí/nội dung cần dùng. Đổi dẫn chiếu A → B có thể cần nội dung cả hai phía nếu chưa có trong đầu vào; không yêu cầu mọi văn bản nêu ở phần căn cứ khi chúng không cần cho nhận định.

Mẫu thiếu tham chiếu có thể có nhãn xác định cho phần thay đổi trực tiếp và null cho tác động chưa đủ căn cứ. Đáp án phải phù hợp bộ tài liệu hệ thống được nhận. Không dùng thông tin chỉ có ở mẫu đầy đủ để bắt mẫu thiếu kết luận chắc chắn. Thiếu căn cứ cần thiết dẫn đến PARTIAL theo SRS; nhận xét người dùng vẫn là trạng thái độc lập.

## 4. Review, bất đồng và phiên bản nhãn

Mỗi mẫu có người gán và người review khác. Nam điều phối nhãn phân tích; Dũng phối hợp nguồn/nghiệp vụ; Đức Anh kiểm tra khả năng đóng gói theo SRS; Tùng Dương kiểm tra dữ liệu tương tác. Vai trò review được ghi theo từng mẫu, không mặc định người tạo dữ liệu đã tự review độc lập. Nhãn ngữ nghĩa/mức tác động cần được người có kiến thức luật kiểm tra nếu tiếp cận được; ghi rõ giới hạn khi chưa có.

Checklist chính:

- Đúng V1–S, trạng thái nền, bộ tham chiếu, nguồn và hash.
- Các chỉ dẫn có kết quả hoặc lý do chưa xác định; đúng đích và phần thuộc văn bản khác.
- Đúng bộ 8 nhóm và phạm vi ưu tiên của mẫu; không trùng biến đổi, không bỏ chủ thể/đơn vị/điều kiện/ngoại lệ cần thiết.
- Trích dẫn khớp file; phân biệt QUOTED/DERIVED/ABSENT/UNRESOLVED.
- Nhãn tác động và mức độ có căn cứ; mẫu thiếu tài liệu không dùng bằng chứng ẩn.
- Có phiên bản, reviewer, quyết định và ca tương tác liên quan nếu có.

Khi bất đồng, giữ các phương án cùng nguồn và lý do. Hai người đối chiếu theo hướng dẫn; chưa thống nhất thì mời người thứ ba hoặc tham vấn chuyên môn. Không lấy đa số làm chứng nhận pháp lý.

Trạng thái hồ sơ: DRAFT → IN_REVIEW → ACCEPTED, hoặc UNRESOLVED nếu chưa giải quyết. Đây là trạng thái review nhãn, khác needs_review của AI và review_status của người dùng. Nhãn ACCEPTED có thể yêu cầu hệ thống trả “chưa đủ căn cứ” ở một mẫu thiếu tài liệu; khác với người gán nhãn chưa thống nhất đáp án.

Lưu label_version, guideline_version, người/thời điểm review, file/hash và thay đổi nhãn. Sửa bộ đầu vào hoặc quy tắc thì rà lại phần ảnh hưởng. Không âm thầm loại mẫu khó hoặc sửa đáp án theo dự đoán để tăng điểm. Chỉ dùng nhãn đã review và validate cấu trúc cho tập đánh giá xác định; mẫu bất đồng phải báo riêng theo kế hoạch đánh giá. Không tự đặt quy mô hoặc chỉ số đạt ở tài liệu này.

## 5. Ví dụ ngắn và mẫu kiểm thử tương tác

### 5.1. Ví dụ nhãn phân tích

Các ví dụ dưới đây là giả định, chưa xác nhận đã có file chạy được. Mức tác động chỉ được chốt khi có đủ ngữ cảnh và review; không sao chép số đoạn minh họa thành source_refs thật.

| Mẫu | Nội dung trước → sau | Nhãn và điều cần giữ |
| --- | --- | --- |
| EX-01 | “Chậm nhất ngày 12” → “Không muộn hơn ngày 12”, mọi điều kiện giữ nguyên | false, aspects = [], category = WORDING_ONLY, LOW nếu xác định tương đương |
| EX-02 | Hạn nộp từ 30 → 15 ngày | TIME_QUANTITY; giữ mốc tính và hoạt động; không tự chốt HIGH |
| EX-03 | Thêm đơn vị cung cấp dịch vụ vào chủ thể báo cáo; ngưỡng sự cố từ quá 30 → quá 15 phút | Một SemanticChange với SUBJECT_OBJECT và TIME_QUANTITY; nêu rõ đây là ngưỡng sự cố, không phải hạn nộp |
| EX-04 | “Có thể nộp” → “Phải nộp” | RIGHTS_DUTIES_ACTIONS; kiểm tra điều kiện/ngoại lệ trước khi chấm mức |
| EX-05 | Bổ sung ngoại lệ cho quyền chuyển hạn | CONDITIONS_EXCEPTIONS; giữ quy định gốc làm ngữ cảnh |
| EX-06 | Dẫn chiếu bảng A → B nhưng chưa cung cấp B | DEFINITIONS_REFERENCES cho đổi đích đã rõ; giữ ReferenceRequirement, PARTIAL; mức tác động chưa rõ để null, không kết luận mức thu tăng/giảm |
| EX-07 | Ngày hiệu lực được nêu cùng ngoại lệ cho một khoản | EffectInfo đúng phạm vi; chỉ gán SCOPE_EFFECT_TRANSITION khi có thay đổi trước–sau được chứng minh |

Gold giữ AmendmentItem, SemanticDiffResult (gồm SemanticChange và ChangeAspect), ScoringResult và EvidenceRef theo cấu trúc chung PoCS. amendment_id nối kết quả với chỉ dẫn; change_id nối nhận định với ScoringResult. ID gold không cần trùng ID dự đoán; quy tắc đối chiếu để tính chỉ số thuộc kế hoạch đánh giá.

Khi tạo ReviewItem cho giao diện HCI, lưu ánh xạ tới amendment_id/change_id trong fixture. Mục chưa tạo được SemanticChange vẫn phải truy được về chỉ dẫn và lý do chưa xác định. Không giả định item_id của hai lượt phân tích là khóa ổn định.

### 5.2. Bộ mẫu trước và sau bổ sung tài liệu

Chuẩn bị bộ kết quả hai lượt có cùng lineage_id, mỗi lượt ghi bộ file được cung cấp và đáp án riêng. Trong hồ sơ fixture, ghi quan hệ giữa các mục theo nguồn và nội dung, không chỉ theo ID hoặc số Điều. Đây là đáp án kiểm thử kỹ thuật, không được cung cấp như đáp án ẩn cho thuật toán nhận diện mục.

| Ca | Kết quả mẫu | Trạng thái tương tác mong đợi |
| --- | --- | --- |
| IF-01 | Lượt đầu thiếu B, lượt sau thêm đúng B và giải thích/bằng chứng thay đổi | Báo cáo mới có comparison_id mới; mục cũ đã kiểm tra chuyển RECHECK_REQUIRED; decision hiện tại null, nhận xét cũ giữ riêng |
| IF-02 | Cùng mục, nội dung phục vụ kiểm chứng không đổi sau bổ sung | Có thể giữ REVIEWED khi xác minh được cả quan hệ mục và nội dung không đổi; chấp nhận phương án thận trọng yêu cầu kiểm tra lại theo SRS |
| IF-03 | Phân tích lại tạo thêm mục | Mục mới UNREVIEWED, không kế thừa decision từ vị trí dòng cũ |
| IF-04 | Một mục chia thành hai hoặc nhiều mục gộp lại, chưa ghép chắc chắn | Không tự chuyển xác nhận; giữ nhận xét cũ trong danh sách chưa đối chiếu được; mục hiện tại chưa có nhận xét là UNREVIEWED |
| IF-05 | Mục cũ không còn xuất hiện | Giữ nhận xét cũ riêng, không tính vào tổng mục hiện tại và không coi là xác nhận không thay đổi |
| IF-06 | Lượt phân tích lại thất bại/timeout | Giữ báo cáo và nhận xét trước, không tự gửi lặp |
| IF-07 | Lưu INSUFFICIENT_BASIS | review_status = REVIEWED; needs_review của AI không tự đổi theo thao tác này |

Fixture phải bao gồm trước thao tác, thao tác và đầu ra mong đợi. ReviewRecord giữ cấu trúc và các trạng thái tương tác của SRS HCI; ánh xạ item_id về nhãn nguồn được ghi riêng trong fixture. before_status nếu giao diện cần chỉ được suy ra từ thao tác, nội dung và lý do đã kiểm tra, không suy ra từ null đơn lẻ. Không yêu cầu dùng tài liệu pháp luật khác nhau để kiểm tra mọi thao tác frontend: có thể dùng response cố định có nguồn để cô lập lỗi trạng thái.

### 5.3. Dữ liệu cho tác vụ kiểm chứng AI

Khi chuẩn bị đầu ra đúng/sai hoặc chưa đủ căn cứ để thử khả năng kiểm chứng, lưu riêng phiên bản đầu ra trình cho người tham gia, đáp án có bằng chứng và lỗi được cài nếu có. Ví dụ lỗi có thể là bỏ sót ngoại lệ hoặc diễn giải sai ngưỡng; đáp án phải chỉ được nguồn bác bỏ cụ thể.

Không sửa file pháp luật thật hoặc gold để hợp thức hóa gợi ý sai; đầu ra sai có chủ đích được ghi nhãn là fixture thử nghiệm, không trộn vào tập đo chất lượng AI thực tế. Phản hồi người tham gia được lưu riêng và đối chiếu với đáp án tác vụ, không tự coi mọi bất đồng với AI là đúng. Cách tổ chức tác vụ, chấm điểm và giải thích lại tình huống sau thử nghiệm được quản lý trong kế hoạch usability.

### 5.4. Các điểm nhóm cần chốt trước khi khóa dữ liệu

- Xác nhận dùng bộ 8 mã chung và cách chọn tập con ưu tiên HCI; giữ các mẫu dẫn chiếu, gộp/tách và thiếu căn cứ cần cho tương tác.
- Thống nhất ánh xạ gold chung sang ReviewItem, vị trí lưu category/is_critical và cách hiển thị các khía cạnh; cập nhật SRS/Architecture tương ứng trước tích hợp.
- Review thứ tự ưu tiên category và ví dụ ranh giới significance qua pilot. Chưa có người chuyên môn kiểm tra thì ghi rõ giới hạn của nhãn.

Bản 1.1.0 giữ cấu trúc 5 phần. So với 1.0.0, thay 4 mã HCI bằng 8 mã chung, khôi phục category/WORDING_ONLY/is_critical và nhãn theo SemanticChange; giữ nguyên mục tiêu kiểm chứng, dữ liệu thiếu căn cứ và các ca tương tác HCI. Các quyết định còn mở không được coi là đã được toàn nhóm phê duyệt.
