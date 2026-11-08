# Hướng dẫn dữ liệu và gán nhãn

**Học phần và nhóm:** 2627I_INT2041_1 Nhóm 6
**Dự án:** Legal Document Change Detection
**Phiên bản:** HCI 1.2.0
**Trạng thái:** Bản đề xuất để nhóm review
**Tài liệu liên quan:** [BRD](brd.md), [SRS](srs.md), [Architecture HCI](architecture.md), [Owner Decisions](module-owner-decisions-hci.md)

## 1. Phạm vi dữ liệu và đầu ra gán nhãn

Tài liệu hướng dẫn chuẩn bị mẫu V1–S, lập đáp án tham chiếu có bằng chứng và chuẩn bị dữ liệu kiểm thử tương tác. Phạm vi nghiệp vụ theo BRD HCI. Baseline gold/fixture HCI dùng ReviewItem, ChangeAspect và bốn mã của SRS HCI. Đầu ra phân tích và nhãn phải được kiểm tra theo cùng hợp đồng trước khi đưa vào giao diện hoặc đánh giá. Không định nghĩa lại schema API, tác vụ usability hoặc công thức chỉ số đánh giá.


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

Khi chuyển `.doc` sang DOCX hoặc chuẩn bị DOCX từ PDF, giữ bản gốc và nhật ký chuyển đổi. Kiểm tra chữ, phủ định, số liệu, đơn vị, cấu trúc và bảng; không sao chép vị trí nguồn giữa hai định dạng khi chưa kiểm tra. Luồng đầu vào trước mắt dùng converter PDF → DOCX rồi Parser hiện có, DOCX đi thẳng vào Parser. Đọc PDF trực tiếp là phương án owner có thể đề xuất ở D-02, không phải implementation đã có.

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
    gold.json                  # Đáp án ReviewItem/ChangeAspect theo SRS HCI
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

Metadata quản lý không tự trở thành trường API. source_refs phải khớp đúng file và registry; Parser hiện dùng block:N, span Python [start,end) trên text block. Không đổi block thành số trang/paragraph bằng suy đoán. Với PDF chuyển đổi, chỉ gán trang PDF khi có mapping đã kiểm chứng (D-02). V2 dựng nội bộ ghi DERIVED_REAL và để ngoài đầu vào mẫu trừ khi chủ định cung cấp; không lấy bản dựng tự động làm đáp án đã xác nhận.

Các biến thể cùng văn bản nền/chuỗi sửa đổi giữ chung lineage_id và cùng tập dữ liệu. Không để bản PDF/DOCX hoặc mẫu đủ/thiếu tham chiếu cùng nguồn lọt sang cả tập phát triển và test. Mẫu giả định ghi SYNTHETIC, tách kết quả báo cáo với mẫu thực tế.

## 3. Quy tắc gán nhãn

### 3.1. Chỉ dẫn, nội dung và bằng chứng

1. Rà toàn bộ S, liệt kê chỉ dẫn và văn bản đích; sau đó xác định phần áp dụng V1. Theo chỉ dẫn nguồn, không ghép hai văn bản theo số Điều tương ứng.
2. Lấy đúng nội dung trước và nội dung sửa đổi, đọc thông tin tổng quát V1 cùng định nghĩa, điều kiện, ngoại lệ cần thiết. Giữ nguồn hiệu lực/chuyển tiếp liên quan theo EffectInfo, không tự xác minh hiệu lực thực tế.
3. Chia thành các ReviewItem có thể kiểm tra riêng, nối với chỉ dẫn qua amendment_id. Một chỉ dẫn có thể có nhiều item; các khía cạnh của cùng nhận định nằm trong aspects. Hai nghĩa vụ độc lập có thể tách item dù cùng Điều/câu; dùng fixture để review cách chia. Cách chia/gộp item và đối chiếu nhận định được review trên fixture theo D-06.
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

Gán operation theo hành vi được chỉ dẫn và đơn vị bị tác động, không chỉ từ khóa “bổ sung”. Nội dung nguyên văn đặt trong EvidenceRef.quote với document_id và source_refs; diễn giải tổng thể ở explanation, diễn giải từng khía cạnh ở interpretation theo SRS HCI. Chỉ dùng các trường đã định nghĩa trong SRS cho response HCI. Không tự tạo số trang hoặc số đoạn. Nội dung DERIVED không được ghi thành trích nguyên văn hoặc bản hợp nhất chính thức.

### 3.2. Bốn mã phân tích và ranh giới gán nhãn

SRS HCI sở hữu field_group đầu ra. Gold/fixture HCI và giao diện dùng cùng bốn mã dưới đây; một ReviewItem có thể có nhiều aspects. Mã nhãn được xác định theo nội dung và bằng chứng; mọi sửa nhãn phải có reviewer, lý do và phiên bản.

| Mã HCI | Cách chọn | Căn cứ cần giữ |
| --- | --- | --- |
| TIME_LIMIT | Hạn thực hiện một hành vi/nghĩa vụ | Mốc tính, đơn vị, chủ thể, hoạt động, điều kiện/ngoại lệ; không là ngày hiệu lực |
| QUANTITATIVE | Số tiền, tỷ lệ, số lượng hoặc ngưỡng trong phạm vi hỗ trợ | Đơn vị, toán tử quá/từ/đến, phạm vi; ngưỡng sự cố theo phút không tự là hạn nộp |
| CONDITIONS_EXCEPTIONS | Điều kiện áp dụng hoặc ngoại lệ được thêm/bỏ/sửa | Quy tắc bị chi phối, chủ thể/phạm vi và nguồn liên quan |
| SUBJECT_RIGHTS_DUTIES | Chủ thể, quyền, nghĩa vụ, hành vi được phép/bắt buộc/cấm | Nêu rõ thành phần thay đổi; không tự mở rộng mọi thay đổi thẩm quyền thành nhóm này |

Không ép mọi nội dung pháp lý vào bốn nhóm. Dẫn chiếu/định nghĩa/hiệu lực vẫn được giữ làm căn cứ hoặc thông tin phạm vi; khi ngoài phạm vi phân tích thì giữ chỉ dẫn, evidence và OUT_OF_SCOPE/UNRESOLVED, không báo không thay đổi. Số tiền phạt chỉ được phân tích theo QUANTITATIVE khi phạm vi và đáp án đã review hỗ trợ; không suy rộng từ giá trị số sang toàn bộ ý nghĩa chế tài.

| Ca ranh giới | Cách xử lý |
| --- | --- |
| Thời hạn và ngưỡng theo thời gian | Hạn thực hiện một hành vi dùng TIME_LIMIT; ngưỡng sự cố/điều kiện định lượng dùng QUANTITATIVE; giữ mốc tính và đơn vị |
| Chủ thể cùng quyền/nghĩa vụ | Dùng SUBJECT_RIGHTS_DUTIES, diễn giải rõ thành phần đổi và giữ các aspects độc lập khi cần |
| Điều kiện có số liệu | Xác định thay đổi là sửa giá trị/ngưỡng hay thêm/bỏ điều kiện; tránh gán trùng cùng biến đổi |
| Thẩm quyền, thủ tục, chế tài | Review theo nội dung và phạm vi; không tự ép vào nhóm chỉ vì có tên cơ quan hoặc con số |
| Dẫn chiếu, định nghĩa, hiệu lực | Giữ evidence, ReferenceRequirement và EffectInfo tương ứng; chỉ tạo aspect khi tác động trong phạm vi có căn cứ |

Nam chủ trì D-06 cùng Dũng review mẫu; Đức Anh và Tùng Dương kiểm tra kết quả dùng được. Lưu lý do/phiên bản khi sửa nhãn; không dùng field_group ngoài SRS như thể đã được chấp nhận. Quy tắc ca ranh giới còn chờ owner đề xuất trên mẫu; enum đầu ra thống nhất theo SRS hiện có.

### 3.3. Kết luận và mức tác động

- `is_meaningful_change = true`: có căn cứ nội dung quy định đổi trong phạm vi phân tích; ghi khía cạnh và bằng chứng.
- `false`: có căn cứ nội dung tương đương dù khác câu chữ; aspects = [] và phải giải thích.
- `null`: chưa đủ căn cứ kết luận; needs_review = true và có review_reason. Một khía cạnh đã rõ không làm phần chưa rõ tự trở thành chắc chắn.
- Giá trị/nhận định chưa xác định khác phía không tồn tại. Dữ liệu rỗng tự nó không chứng minh không có thay đổi.

Chỉ đổi diễn đạt dùng is_meaningful_change=false, aspects=[] và explanation/evidence. Mức tác động đặt tại significance/significance_reason của ReviewItem; review_reason giải thích bất định. Không tự thêm mã hoặc trường phân loại ngoài SRS để biểu diễn trường hợp này.

**Mức tác động significance**

Các mức dưới đây là rubric pilot tham khảo đã có, chưa là ngưỡng/tiêu chí được owner xác nhận cho bản tích hợp. Nam review D-06 với Dũng trên ví dụ ranh giới và ghi phiên bản; cần review chuyên môn khi có điều kiện. Chấm tác động trực tiếp thể hiện trong bộ tài liệu được cung cấp, không suy đoán vụ việc/thiệt hại thực tế hoặc coi loại văn bản là mức độ.

| Mức | Quy tắc pilot | Ví dụ và ranh giới |
| --- | --- | --- |
| LOW | Đã xác định chỉ đổi diễn đạt/hình thức, không đổi nghĩa | “chậm nhất vào ngày” thành “không muộn hơn ngày”, mọi điều kiện giữ nguyên |
| MEDIUM | Đổi nghĩa về cách thực hiện có phạm vi hẹp; giữ nguyên nghĩa vụ cốt lõi, nhóm chủ thể và điều kiện quan trọng | Thay một phương thức báo cáo bằng phương thức khác đã xác định tương đương về yêu cầu; thiếu căn cứ tương đương thì review |
| HIGH | Có căn cứ thay đổi đáng kể chủ thể, nội dung nghĩa vụ/quyền, điều kiện hoặc ngưỡng/thời hạn của quy định | Mở rộng bên chịu nghĩa vụ; hạ ngưỡng kích hoạt báo cáo sự cố. Không tự thành CRITICAL chỉ vì có số liệu |
| CRITICAL | Đảo chiều bắt buộc/cho phép/cấm hoặc loại bỏ toàn bộ một nghĩa vụ/quyền cốt lõi, có bằng chứng rõ và được reviewer xác nhận theo ví dụ ranh giới | Từ bắt buộc báo cáo sự cố thành không phải báo cáo bất kỳ sự cố nào. Chỉ bỏ một phương thức báo cáo không đủ tiêu chí này |
| null | Thiếu căn cứ phân biệt mức hoặc chưa giải quyết mơ hồ có ảnh hưởng chấm điểm | Thiếu văn bản dẫn chiếu, thiếu nội dung sau sửa đổi, hoặc chưa xác định phần bị tác động |

MEDIUM/HIGH phân biệt bằng việc đổi cách thực hiện hạn chế hay đổi phạm vi/điều kiện/nội dung nghĩa vụ đáng kể. HIGH/CRITICAL phân biệt bằng sửa đặc điểm quan trọng hay đảo chiều/loại bỏ toàn bộ nội dung cốt lõi theo rubric. Khó phân biệt phải đưa review, không chọn mức theo cảm giác hay tỷ lệ số chữ đổi.

Chỉ đổi nghĩa đã xác định không gán LOW theo rubric hiện tại. Thêm/xóa Điều đánh giá nội dung, không tự CRITICAL. Một ReviewItem có một mức significance; không cộng điểm theo số aspects. significance_reason nêu quy tắc và bằng chứng, không chỉ lặp mức. Khi chưa chấm được, significance/significance_reason để null và review_reason giải thích; không yêu cầu is_critical trong response HCI.


### 3.4. Mẫu thiếu căn cứ

ReferenceRequirement dùng AVAILABLE khi có đúng tài liệu và tìm được nội dung; MISSING khi chưa được cung cấp; UNRESOLVED khi có file nhưng chưa xác định đúng phiên bản/vị trí/nội dung cần dùng. Đổi dẫn chiếu A → B có thể cần nội dung cả hai phía nếu chưa có trong đầu vào; không yêu cầu mọi văn bản nêu ở phần căn cứ khi chúng không cần cho nhận định.

Mẫu thiếu tham chiếu có thể có nhãn xác định cho phần thay đổi trực tiếp và null cho tác động chưa đủ căn cứ. Đáp án phải phù hợp bộ tài liệu hệ thống được nhận. Không dùng thông tin chỉ có ở mẫu đầy đủ để bắt mẫu thiếu kết luận chắc chắn. Thiếu căn cứ cần thiết dẫn đến PARTIAL theo SRS; nhận xét người dùng vẫn là trạng thái độc lập.

## 4. Review, bất đồng và phiên bản nhãn

Mỗi mẫu có người gán và người review khác. Nam điều phối nhãn phân tích; Dũng phối hợp nguồn/nghiệp vụ; Đức Anh kiểm tra khả năng đóng gói theo SRS; Tùng Dương kiểm tra dữ liệu tương tác. Vai trò review được ghi theo từng mẫu, không mặc định người tạo dữ liệu đã tự review độc lập. Nhãn ngữ nghĩa/mức tác động cần được người có kiến thức luật kiểm tra nếu tiếp cận được; ghi rõ giới hạn khi chưa có.

Checklist chính:

- Đúng V1–S, trạng thái nền, bộ tham chiếu, nguồn và hash.
- Các chỉ dẫn có kết quả hoặc lý do chưa xác định; đúng đích và phần thuộc văn bản khác.
- Đúng bốn mã của SRS; ca ranh giới được review; không trùng biến đổi hoặc bỏ chủ thể/đơn vị/điều kiện/ngoại lệ cần thiết.
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
| EX-01 | “Chậm nhất ngày 12” → “Không muộn hơn ngày 12”, mọi điều kiện giữ nguyên | is_meaningful_change=false, aspects=[], explanation/evidence; LOW theo rubric pilot khi đã xác định tương đương |
| EX-02 | Hạn nộp từ 30 → 15 ngày | TIME_LIMIT; giữ mốc tính và hoạt động; không tự chốt HIGH |
| EX-03 | Thêm đơn vị cung cấp dịch vụ vào chủ thể báo cáo; ngưỡng sự cố từ quá 30 → quá 15 phút | Một ReviewItem nếu cùng quy định, aspects SUBJECT_RIGHTS_DUTIES và QUANTITATIVE; review chia item nếu là nghĩa vụ độc lập |
| EX-04 | “Có thể nộp” → “Phải nộp” | SUBJECT_RIGHTS_DUTIES; kiểm tra điều kiện/ngoại lệ trước khi chấm mức |
| EX-05 | Bổ sung ngoại lệ cho quyền chuyển hạn | CONDITIONS_EXCEPTIONS; giữ quy định gốc làm ngữ cảnh |
| EX-06 | Dẫn chiếu bảng A → B nhưng chưa cung cấp B | Giữ thay đổi trực tiếp trong chỉ dẫn/explanation, ReferenceRequirement và PARTIAL; tác động chưa rõ để null, không ép field_group hoặc kết luận mức thu tăng/giảm |
| EX-07 | Ngày hiệu lực được nêu cùng ngoại lệ cho một khoản | EffectInfo đúng phạm vi; không gán ngày hiệu lực thành TIME_LIMIT |

Gold HCI dùng ReviewItem/ChangeAspect/EvidenceRef theo SRS, kèm hồ sơ nguồn và trạng thái review nhãn. amendment_id nối về chỉ dẫn, item_id định danh trong báo cáo/fixture. Không cần ID gold trùng ID dự đoán; matching do D-11 chốt trước đo. Gold phải được đóng gói theo hợp đồng HCI; D-06/D-10 chốt ví dụ, cách chia item và kiểm tra nguồn trước khi khóa nhãn.

Mục chưa tạo được nhận định vẫn giữ instruction và lý do. Không coi item_id là khóa ổn định giữa hai lượt. Các fixture tương tác giữ report HCI và ReviewRecord riêng, không thay nhận xét người dùng bằng kết quả AI.

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

### 5.4. Căn cứ retrieval và việc chờ owner

Với mẫu đại diện, ghi nhu cầu context (định nghĩa/câu dẫn/ngoại lệ/dẫn chiếu), các đoạn nguyên văn chấp nhận được, document_id/source_ref/spans đã kiểm tra, lý do cần đọc, trạng thái căn cứ và người review. Không lấy ID chunk sinh bởi LightRAG hoặc mô tả graph làm gold. Có thể nhiều đoạn cần đọc cùng nhau hoặc các bằng chứng tương đương; hình thức hồ sơ và matching chờ D-10/D-11.

Chỉ đưa đúng bộ V1/S/tham chiếu đã cấp cho mẫu vào index. Không đưa V2 đối chiếu, gold, review nhãn, đầu ra gợi ý sai có chủ đích hoặc bộ test khác vào retrieval. Biến thể đủ/thiếu tham chiếu cùng nguồn giữ chung lineage_id/split; query rỗng không làm đổi đáp án nguồn đã review. Giữ gợi ý sai kiểm soát dùng cho usability tách khỏi dữ liệu đo AI thật.

Các lựa chọn cần owner trả lời nằm ở [Module Owner Decisions](module-owner-decisions-hci.md): D-02 cho nguồn, D-04 cho chunk/registry, D-06 cho chia item/nhãn/rubric, D-10 cho bộ mẫu/split/hồ sơ, D-11 cho matching/metric, D-12 cho tác vụ người dùng. Chưa chốt threshold, số mẫu cuối hoặc lịch thu thập chỉ vì tài liệu đã đồng bộ.

Bản HCI 1.2.0 thống nhất nhãn, ví dụ và dữ liệu tương tác theo bốn mã trong SRS. Không thay kết quả nguồn hoặc tự xác nhận rubric pilot đã được toàn nhóm nghiệm thu.
