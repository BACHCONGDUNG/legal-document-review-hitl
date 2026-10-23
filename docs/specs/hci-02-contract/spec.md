# HCI-02 — Hợp đồng dữ liệu và fixture

| Thuộc tính | Nội dung |
| --- | --- |
| Người phụ trách | Dương Đức Anh |
| Trạng thái | Draft — chờ review với các bên liên quan |
| Phạm vi | Hợp đồng dữ liệu phục vụ phát triển và tích hợp các module |
| Tài liệu căn cứ | SRS, Architecture và Implementation Plan |

## 1. Mục tiêu

Xác định hợp đồng dữ liệu giữa module đọc tài liệu, module xử lý chỉ dẫn sửa đổi, module phân tích và giao diện.

Cung cấp schema cùng dữ liệu mẫu để các thành viên có thể phát triển song song, kiểm tra dữ liệu bàn giao và tích hợp các module.

Trong tài liệu này:

- **V1:** Văn bản gốc cần được đối chiếu.
- **S:** Văn bản chứa chỉ dẫn sửa đổi V1; không phải bản V2 hoàn chỉnh.
- **Hợp đồng dữ liệu:** Quy định về cấu trúc, kiểu dữ liệu, ý nghĩa và ràng buộc của dữ liệu trao đổi giữa các thành phần.
- **Schema:** Định nghĩa có thể dùng để kiểm tra dữ liệu có tuân thủ hợp đồng hay không.
- **Fixture:** Dữ liệu mẫu có chủ đích, phục vụ phát triển và kiểm thử.

## 2. Tài liệu căn cứ

- [SRS](../../srs.md): Yêu cầu chức năng, dữ liệu và trạng thái.
- [Architecture](../../architecture.md): Kiến trúc và ranh giới trách nhiệm.
- [Implementation Plan](../../implementation-plan-hci.md): Phân công, phụ thuộc và điều kiện bàn giao.

Tên trường và mã trạng thái của hợp đồng đầu ra HCI tuân theo SRS mục 3.

Những quyết định bổ sung hoặc thay đổi hợp đồng phải được ghi nhận và review với bên cung cấp, bên nhận dữ liệu. Nếu thay đổi nội dung đã được quy định trong SRS, phải cập nhật tài liệu liên quan và fixture tương ứng.

## 3. Phạm vi

### 3.1. Trong phạm vi

| Đầu ra | Nội dung cần xác định |
| --- | --- |
| Hợp đồng đầu ra Reader/Parser | Cấu trúc văn bản, nội dung nguồn, định danh, vị trí nguồn và cảnh báo |
| Hợp đồng đầu vào phân tích | Chỉ dẫn, đích sửa đổi, nội dung trước–sau, ngữ cảnh, bằng chứng và phần chưa xác định |
| Hợp đồng đầu ra phân tích | Kết quả so sánh, giải thích, khía cạnh thay đổi, mức tác động và lỗi |
| Hợp đồng báo cáo | Dữ liệu theo SRS mục 3 và nội dung nguồn để giao diện hiển thị bằng chứng |
| Hợp đồng API | Đầu vào, đầu ra, cấu trúc lỗi và cách ánh xạ sang mã HTTP |
| Schema và fixture | Định nghĩa dữ liệu có thể kiểm tra cùng các mẫu phục vụ phát triển và kiểm thử |

Hợp đồng Reader/Parser cần xem xét đầu ra hiện có của module xử lý tài liệu. Không yêu cầu thay toàn bộ cấu trúc nội bộ nếu có thể chuyển đổi sang hợp đồng chung mà vẫn giữ đủ nội dung và vị trí nguồn.

### 3.2. Ngoài phạm vi

HCI-02 chưa hiện thực:

- Thuật toán trích chỉ dẫn và xác định đích sửa đổi.
- Thuật toán dựng nội dung trước–sau cục bộ.
- Text Diff, phân tích AI và chấm mức tác động.
- Toàn bộ API và Pipeline xử lý tài liệu thật.
- Giao diện và chức năng quản lý nhận xét người dùng.
- Database hoặc cơ chế lưu lịch sử dài hạn.

Các thành phần trên sẽ sử dụng hợp đồng được xác định trong task này.

## 4. Các điểm bàn giao dữ liệu

| Bên cung cấp | Bên nhận | Dữ liệu bàn giao |
| --- | --- | --- |
| Reader/Parser của Dũng | Backend của Đức Anh | Nội dung tài liệu, cấu trúc V1, nguồn và cảnh báo |
| Backend của Đức Anh | Module phân tích của Nam | Chỉ dẫn, đích sửa đổi, nội dung trước–sau, ngữ cảnh và bằng chứng |
| Module phân tích của Nam | Backend của Đức Anh | Kết quả so sánh, nhận định, khía cạnh, mức tác động và lỗi |
| Backend của Đức Anh | Frontend của Tùng Dương | Báo cáo, nội dung nguồn, yêu cầu tài liệu tham chiếu và lỗi |

## 5. Yêu cầu hợp đồng dữ liệu

### 5.1. Đầu vào mỗi lượt phân tích

API mục tiêu là `POST /api/compare`, nhận dữ liệu dạng `multipart/form-data`.

| Trường | Kiểu | Bắt buộc | Ý nghĩa |
| --- | --- | --- | --- |
| `base_file` | File | Có | Văn bản gốc V1 |
| `amendment_file` | File | Có | Văn bản sửa đổi S |
| `reference_files` | File[] | Không | Các tài liệu tham chiếu được cung cấp |

Giới hạn dung lượng, số tệp và thời gian xử lý cần được xác định trong hợp đồng API và cấu hình triển khai. Không tự đặt các giới hạn chưa được review như yêu cầu đã thống nhất.

### 5.2. Đầu ra Reader/Parser

Hợp đồng phải đủ thông tin để:

- Xác định tài liệu tương ứng với dữ liệu đã đọc.
- Giữ thứ tự các đoạn và bảng đọc được.
- Truy xuất Điều, Khoản và Điểm của V1.
- Giữ nội dung ngoài Điều khi cần lấy ngữ cảnh.
- Truy ngược nội dung về các khối nguồn.
- Giữ cảnh báo và phần chưa xác định.

Với S, dữ liệu đọc được phải giữ chỉ dẫn và nội dung trích dẫn để bước xử lý tiếp theo phân biệt chúng. Không mặc định mọi nhãn Điều trong nội dung trích dẫn đều là Điều cấp ngoài của S.

### 5.3. Đầu vào và đầu ra phân tích

Đầu vào phân tích phải thể hiện được:

- Chỉ dẫn sửa đổi và bằng chứng từ S.
- Văn bản, vị trí đích và trạng thái liên kết.
- Thao tác sửa đổi.
- Nội dung trước–sau và căn cứ hình thành nội dung đó.
- Ngữ cảnh, tài liệu tham chiếu và phần còn thiếu.
- Cảnh báo ảnh hưởng tới việc phân tích.

Đầu ra phân tích phải thể hiện được:

- Kết quả Text Diff khi đủ căn cứ.
- Nhận định tổng thể và các khía cạnh thay đổi.
- Bằng chứng hỗ trợ.
- Mức tác động và lý do khi đủ căn cứ.
- Phần chưa xác định, lỗi và giới hạn xử lý.

Cấu trúc chi tiết cần được Đức Anh và Nam review trên fixture trước khi tích hợp.

### 5.4. Báo cáo và nội dung nguồn

Hợp đồng báo cáo tuân theo các đối tượng được quy định trong SRS mục 3:

- `DocumentIdentity`
- `EvidenceRef`
- `ReferenceRequirement`
- `ProcessingIssue`
- `EffectInfo`
- `ComparisonReport`
- `ReviewItem`
- `ChangeAspect`
- `TextChange`

Response phải cung cấp đủ nội dung nguồn để giao diện đọc được bằng chứng sau khi backend đã dọn file tạm.

Tên trường và cấu trúc chứa các khối nguồn cần được thống nhất trong hợp đồng chi tiết và fixture.

### 5.5. Lỗi API

Hợp đồng phải phân biệt:

- Lỗi đầu vào khiến request bị từ chối trước khi chạy Pipeline.
- Báo cáo có kết quả dùng được nhưng bị giới hạn hoặc lỗi một phần.
- Trường hợp không tạo được kết quả dùng được.

Cấu trúc error body và mã HTTP phải được xác định rõ. Không dùng trực tiếp trạng thái báo cáo để thay thế mã HTTP.

## 6. Quy tắc và ràng buộc

### 6.1. Định danh và bằng chứng

1. Mỗi bằng chứng phải xác định đúng tài liệu, vị trí nguồn và đoạn trích nguyên văn.
2. Cặp `document_id` và `source_ref` phải xác định duy nhất một khối nguồn trong lượt phân tích.
3. Nội dung diễn giải không được đưa vào `quote` như trích nguyên văn.
4. Chỉ số đoạn hoặc bảng DOCX không được trình bày như số trang Word hoặc PDF.
5. Không suy ra vị trí trong PDF gốc từ thứ tự đoạn DOCX khi chưa có ánh xạ được kiểm chứng.

### 6.2. Nội dung trước–sau

1. Phải phân biệt nội dung chưa xác định với nội dung được xác nhận không tồn tại.
2. `before_status = UNRESOLVED` biểu thị chưa xác định được nội dung cũ.
3. `before_status = ABSENT` chỉ được sử dụng khi đã xác nhận không có nội dung cũ.
4. Nội dung mới suy ra cục bộ từ chỉ dẫn phải có `after_basis = DERIVED`.
5. Nội dung `DERIVED` không được trình bày như trích nguyên văn hoặc bản V2 chính thức.
6. Không thay nội dung chưa xác định bằng chuỗi rỗng để chạy Text Diff.
7. Vị trí trong `TextChange` phải khớp chính xác chuỗi trước–sau được trả về, theo quy ước của SRS.

### 6.3. Phân tích và trạng thái

1. Khi bước phân tích bị lỗi, phải giữ chỉ dẫn và dữ liệu nguồn đã xác định được.
2. Không dùng danh sách rỗng để che lỗi hoặc biểu thị một bước chưa thực hiện.
3. `SUCCESS`, `PARTIAL` và `FAILED` là trạng thái báo cáo.
4. Trạng thái báo cáo độc lập với trạng thái parser và mã HTTP.
5. Chưa đủ căn cứ chấm mức tác động thì trả `null` cùng lý do; không dùng `LOW` thay cho chưa xác định.
6. `SUCCESS` không có nghĩa kết quả AI chắc chắn đúng.
7. Chỉ dẫn thuộc văn bản khác phải được giữ thông tin phạm vi theo SRS, không ép thành thay đổi của V1.

### 6.4. Nhận xét và phân tích lại

1. Nhận xét người dùng do frontend quản lý trong phiên.
2. Nhận xét không thuộc đầu ra phân tích AI của backend.
3. Mỗi lượt phân tích mới có `comparison_id` mới.
4. Không mặc định hai mục ở hai lượt phân tích là cùng một mục chỉ vì có cùng `item_id`, số Điều hoặc vị trí trong danh sách.
5. Fixture phải hỗ trợ kiểm tra trường hợp mục thay đổi và nhận xét cũ không ghép được.
6. Nếu chưa thể đối chiếu đáng tin cậy, áp dụng phương án yêu cầu kiểm tra lại hoặc giữ nhận xét cũ riêng theo SRS mục 4.

## 7. Các trường hợp fixture bắt buộc

| Mã | Trường hợp | Kết quả mong đợi |
| --- | --- | --- |
| FX-01 | Đủ dữ liệu và hoàn tất phân tích trong phạm vi | Báo cáo `SUCCESS`, có kết quả và bằng chứng truy xuất được |
| FX-02 | Thiếu tài liệu tham chiếu cần thiết | Báo cáo `PARTIAL`, có yêu cầu tài liệu và danh sách mục bị ảnh hưởng |
| FX-03 | Một mục phân tích bị lỗi nhưng còn kết quả dùng được | Giữ chỉ dẫn, nguồn và các kết quả còn dùng được; nêu lỗi và phần bị ảnh hưởng |
| FX-04 | Không tạo được kết quả dùng được | Báo cáo `FAILED`, có lý do; không thể hiện thành không có thay đổi |
| FX-05 | File chính không hợp lệ | Lỗi request theo hợp đồng API; không chạy Pipeline |
| FX-06 | Phân tích lại làm thay đổi nội dung của mục nhận diện được | Có `comparison_id` mới; dữ liệu đủ để frontend yêu cầu kiểm tra lại |
| FX-07 | Phân tích lại không ghép chắc chắn được với mục cũ | Không tự chuyển xác nhận; hỗ trợ frontend giữ nhận xét cũ riêng |

Fixture có thể sử dụng nội dung giả lập ngắn, nhưng phải ghi rõ là dữ liệu minh họa.

Fixture giả lập không được trình bày như kết quả chạy trên văn bản thật hoặc như kết quả đánh giá chất lượng hệ thống.

## 8. Điều kiện nghiệm thu

- [ ] Có hợp đồng đầu ra Reader/Parser và quy tắc ánh xạ từ đầu ra hiện tại.
- [ ] Có hợp đồng đầu vào và đầu ra module phân tích.
- [ ] Có hợp đồng báo cáo và nội dung nguồn tuân theo SRS.
- [ ] Có hợp đồng lỗi API và cách ánh xạ mã HTTP.
- [ ] Schema kiểm tra được toàn bộ fixture hợp lệ.
- [ ] Có kiểm tra từ chối dữ liệu sai quan trọng, gồm mã trạng thái không hợp lệ và trường bắt buộc bị thiếu.
- [ ] Bằng chứng trong fixture truy được tới đúng tài liệu và nội dung nguồn.
- [ ] Dũng xác nhận đầu ra Reader/Parser có thể bàn giao theo hợp đồng.
- [ ] Nam xác nhận đầu vào đủ để phát triển module phân tích.
- [ ] Tùng Dương xác nhận báo cáo đủ để dựng giao diện và hiển thị các trạng thái.
- [ ] Những quyết định còn thiếu và giới hạn đã biết được ghi nhận rõ.

Việc viết xong schema chưa đủ để xác nhận HCI-02 hoàn thành. Hợp đồng và fixture phải được các bên liên quan kiểm tra khả năng sử dụng.

## 9. Các quyết định cần review

| Nội dung | Người phối hợp | Trạng thái |
| --- | --- | --- |
| Ánh xạ đầu ra parser hiện tại vào hợp đồng chung | Đức Anh và Dũng | Chưa review |
| Định danh tài liệu, vị trí nguồn và cảnh báo | Đức Anh và Dũng | Chưa review |
| Cấu trúc đầu vào trước–sau và đầu ra phân tích | Đức Anh và Nam | Chưa review |
| Cấu trúc báo cáo và dữ liệu nguồn cho giao diện | Đức Anh và Tùng Dương | Chưa review |
| Dữ liệu hỗ trợ đối chiếu mục giữa các lượt phân tích | Đức Anh và Tùng Dương | Chưa review |
| Mã HTTP, error body và giới hạn đầu vào | Đức Anh đề xuất, review với các bên liên quan | Chưa review |

## 10. Quản lý thay đổi

Khi thay đổi hợp đồng:

1. Ghi rõ vấn đề và nội dung đề xuất thay đổi.
2. Xác định bên cung cấp và bên nhận bị ảnh hưởng.
3. Thử thay đổi trên một fixture hoặc mẫu cụ thể.
4. Cập nhật schema, fixture và tài liệu liên quan.
5. Kiểm tra lại các trường hợp bị ảnh hưởng.
6. Ghi nhận kết quả review trước khi coi thay đổi là hợp đồng đã thống nhất.

Thay đổi hợp đồng đã được quy định trong SRS phải đi kèm cập nhật SRS. Không thay đổi tên trường hoặc ý nghĩa dữ liệu bàn giao mà không thông báo cho bên nhận.