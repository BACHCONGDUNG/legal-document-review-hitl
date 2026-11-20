# Module Owner Decisions — HCI

**Học phần và nhóm:** 2627I_INT2041_1 — Nhóm 6
**Nhóm trưởng:** Bạch Công Dũng
**Phiên bản:** Bản chia hai phần quyết định
**Trạng thái:** Đã xác nhận trách nhiệm quyết định và phối hợp tài liệu; phương án kỹ thuật cụ thể vẫn chờ owner đề xuất và review
**Liên quan:** [SRS](srs.md), [Architecture](architecture.md), [Implementation Plan](implementation-plan-hci.md), [Data Guide](data-annotation-guide-hci.md), [User Research](user-research.md)

**Mục đích và baseline dùng chung**

Đây là nơi duy nhất theo dõi lựa chọn còn mở. Mỗi D-ID có một owner tổng hợp đề xuất, bên nhận/reviewer và đầu ra cần kiểm chứng. Owner được ghi theo phân công HCI đang có; việc có tên trong quyết định không xác nhận người đó đã nhận hoặc thực hiện một phương án cụ thể. Chưa đặt hạn ngày thay nhóm: mục “trước khi” là điểm phụ thuộc để owner ước lượng và nhóm gắn vào lịch học.

Bản tài liệu đồng bộ dùng baseline sau để các bên cùng trao đổi:

- Sinh viên Luật là người dùng chính; bài toán V1–S cùng tham chiếu đã cung cấp; không bắt buộc dựng V2.
- HCI tập trung hiểu, kiểm chứng, nhận xét và kiểm tra lại; chất lượng AI và usability là hai phép đánh giá khác nhau.
- POST `/api/compare` nhận multipart `doc_v1`, `doc_s` và `reference_files` tùy chọn. `ComparisonReport` gồm `comparison_id`, `base_document`, `amendment_document`, `reference_documents`, `status`, `results`, `warnings` và `errors`. Mỗi phần tử `results` là một `AmendmentResult`.
- Schema, validator và fixture dùng tám nhóm field_group theo SRS. ReviewRecord là dữ liệu riêng của frontend HCI.
- Giữ converter và Parser hiện có, qua adapter; PDF → DOCX → Parser trước mắt. Nguồn block:N/DOCX chuyển đổi không được tự coi là trang PDF.
- Tạm chọn B cho retrieval: LightRAG Server riêng được gọi HTTP. Có thể cùng máy localhost; chưa chọn model, release/API, prompt, chunk, ngưỡng hoặc cam kết offline.
- Nhận xét lưu trong phiên frontend, không tự thành gold/nhãn huấn luyện. Giữ request đồng bộ, không bổ sung account/kho lịch sử/job người dùng ở đợt này.
- Giữ tên thực tế backend/app/ và test/. Tên tài liệu có hậu tố -hci phải được dẫn đúng.

Baseline thống nhất tài liệu không thay nghiệm thu code hoặc review của owner. Đề xuất thay yêu cầu/contract phải nêu rõ phần bị ảnh hưởng và được bên giao/bên nhận kiểm tra trước khi cập nhật nguồn sở hữu.

**Cách đọc và phạm vi quyết định**

Giữ nguyên mã D-01–D-13, phạm vi, owner, bên review và đầu ra tối thiểu của tài liệu HCI. Nam quyết định chính D-05; Đức Anh quyết định chính D-04/D-13; Tùng Dương quyết định cơ chế giữ/đọc bằng chứng thuộc D-07. Dũng + Đức Anh cùng biên soạn api-contract.md và development-guide.md theo D-01/D-13.

Mỗi quyết định có hai phương án nền do người soạn đề xuất theo phạm vi hiện tại. Đây là điểm bắt đầu trao đổi, không phải hai lựa chọn duy nhất, không phải kết quả thử nghiệm và không thay lựa chọn owner. Hai phương án tập trung một hướng triển khai chính; các chi tiết còn lại vẫn phải được điền ở các trường nhỏ bên dưới. Phương án nào làm thay đổi yêu cầu/contract phải được review trước khi áp dụng.

**Phân quyền trong từng quyết định:** “Phần owner tự quyết định” áp dụng cho lựa chọn nội bộ trong baseline, không thay contract, phạm vi hay nguồn lực chung. “Phần cần nhiều bên thống nhất” chỉ yêu cầu các bên thực sự bị ảnh hưởng xác nhận; không mặc định mọi quyết định đều cần cả nhóm duyệt. Owner vẫn tự kiểm tra và bên nhận vẫn review đầu ra. Hai phần xác định quyền và trách nhiệm, không xác nhận phương án đã được chọn hoặc đã chốt.

**Trạng thái phương án kỹ thuật hiện tại:** CHỜ OWNER ĐỀ XUẤT. Có phương án nền trong tài liệu không đồng nghĩa owner đã đề xuất, đã chọn hoặc đã chốt.

Tài liệu có đúng hai phần chính. **Phần A** ghi quyền lựa chọn nội bộ và hai phương án nền của owner; **phần B** ghi hợp đồng/điều kiện phải thống nhất với các bên liên quan. Giữ mã D-01–D-13 ở cả hai phần để đối chiếu cùng một quyết định; không tạo mã quyết định mới. Trạng thái và kết luận phải được đọc theo đúng phạm vi A hoặc B, không coi chốt nội bộ là đã chốt toàn bộ D-ID.

Vấn đề cần chốt ở phần A được giữ làm bối cảnh chung của D-ID, không mở rộng quyền cá nhân sang các nội dung phải thống nhất ở phần B. Phương án nền có ảnh hưởng đầu vào/đầu ra, nguồn lực hoặc bên sử dụng chỉ được áp dụng sau khi phần B tương ứng được xác nhận.

## A. Quyết định thuộc phạm vi owner

Owner lựa chọn cách hiện thực trong baseline và tự kiểm tra. Hai phương án nền dưới mỗi D-ID được giữ nguyên để cân nhắc; không tự chốt thay owner. Các điều kiện có nhiều bên cùng quyết định nằm ở phần B cùng mã.

### D-01 — Contract API schema và báo cáo — Phần A

**Trạng thái:** Đã chốt hợp đồng API cho bản nền HCI. Còn bước kiểm tra và bàn giao.

**Chủ trì:** Dương Đức Anh

**Phần owner tự quyết định:** Đức Anh chọn cách tổ chức router, schema/validator và adapter nội bộ, miễn giữ đúng baseline và hợp đồng đã thống nhất.

**Quyết định tích hợp:** Dùng API, schema, validator và fixture nêu trong SRS.

**Việc tiếp theo:** Đức Anh phối hợp Dũng và Tùng Dương kiểm tra upload, báo cáo, lỗi HTTP và lỗi trong báo cáo. Các thay đổi sau baseline được review theo phần B.

### D-02 — Đầu vào Parser adapter và truy nguồn — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Bạch Công Dũng

**Phần owner tự quyết định:** Dũng chọn cách đọc/chuyển đổi, xử lý cây và hiện thực adapter trong phần đầu vào; giữ dữ liệu, nguồn và giới hạn đã cam kết.

**Vấn đề cần chốt:** Đầu ra native/adapter; quy ước ID, block/spans, bảng/outside/quotation; mapping DOCX chuyển đổi → PDF có thể bảo đảm đến đâu? Quy ước Unicode offsets?

**Hai phương án nền để cân nhắc:**

1. **Adapter tạo biểu diễn bàn giao chuẩn hóa.** Giữ Parser hiện có; adapter tạo đối tượng gồm định danh/vai trò, danh sách khối nguồn có thứ tự, cấu trúc Điều/Khoản/Điểm tham chiếu tới khối và cảnh báo. Bên nhận ít phụ thuộc dict native; cần kiểm tra không mất bảng, outside, span hoặc nội dung trích dẫn.
2. **Giữ cây native và cung cấp lớp truy cập nguồn ổn định.** Bàn giao cây Parser được kiểm tra cùng các thao tác đọc đơn vị/khối/đoạn nguồn theo contract cố định. Giảm chuyển đổi dữ liệu, nhưng cần kiểm soát thay đổi native và không để bên nhận tự đoán đường dẫn trường. Fixture lưu snapshot có thể đọc/kiểm tra lại.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-02 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

### D-03 — Chỉ dẫn vị trí đích và nội dung trước sau — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Dương Đức Anh

**Phần owner tự quyết định:** Đức Anh chọn thuật toán trích chỉ dẫn, tìm ứng viên đích và dựng nội dung cục bộ trong phạm vi đã giao.

**Vấn đề cần chốt:** Phương pháp trích chỉ dẫn, tìm văn bản/đích, dựng before/after, hiệu lực và nhận diện căn cứ cần thiết; xử lý mơ hồ ra sao?

**Hai phương án nền để cân nhắc:**

1. **Liên kết theo chỉ dẫn và cấu trúc pháp lý.** Nhận diện số hiệu, Điều/Khoản/Điểm và thao tác bằng quy tắc; áp chỉ dẫn vào đơn vị đã parse. Ưu tiên khả năng truy nguyên; gặp chỉ dẫn mơ hồ thì giữ ứng viên/UNRESOLVED thay vì đoán.
2. **Liên kết cấu trúc kết hợp đối chiếu nội dung.** Dùng quy tắc xác định phạm vi, sau đó đối chiếu cụm từ/nội dung để chọn giữa các ứng viên khi đánh số hoặc bố cục khó. Có thể xử lý thêm ca khó nhưng cần tiêu chí chấp nhận đã thử trên mẫu; không ép liên kết khi nhiều ứng viên còn hợp lý.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-03 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

### D-04 — Retrieval ngữ cảnh và vòng đời LightRAG — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Dương Đức Anh — quyền quyết định chính

**Phần owner tự quyết định:** Đức Anh quyết định chính cách hiện thực client, chunk/query và điều phối truy xuất trong phương án tạm chọn, đáp ứng contract và ngân sách đã thống nhất.

**Vấn đề cần chốt:** Release/API LightRAG; cách nhập/chia đoạn/query; registry; đợi index; cách ly và dọn dữ liệu; context đủ nghĩa và ngân sách truy xuất?

**Hai phương án nền để cân nhắc:**

1. **Chunk theo đơn vị cấu trúc và truy xuất trong một lượt.** Tạo chunk theo Điều/Khoản/Điểm có câu dẫn cần thiết; giữ registry nguồn; nhập bộ tài liệu một lần theo comparison, đợi sẵn sàng rồi query từng chỉ dẫn. Luồng đơn giản hơn để kiểm tra; phải thử giới hạn đơn vị quá dài và mất ngữ cảnh giữa đơn vị.
2. **Chunk theo cấu trúc kết hợp cửa sổ ngữ cảnh có giới hạn.** Giữ đoạn cấu trúc làm lõi, bổ sung đoạn lân cận/dẫn chiếu khi có căn cứ; query bổ sung chỉ trong ngân sách đã định. Linh hoạt hơn với ngữ cảnh phân tán nhưng tăng lượng xử lý và yêu cầu kiểm tra mapping/trùng lặp. Cả hai phương án phải kiểm chứng cách ly và dọn dữ liệu trên API/release thực tế.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-04 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

### D-05 — Mô hình prompt validation và fallback — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Vương Thành Nam — quyền quyết định chính

**Phần owner tự quyết định:** Nam quyết định chính phương pháp phân tích, prompt, kiểm tra nội bộ/fallback và lựa chọn LLM/embedding trong phạm vi, giao diện và nguồn lực đã thống nhất. Review không biến mọi chỉnh prompt nội bộ thành việc cả nhóm phải duyệt.

**Vấn đề cần chốt:** LLM/embedding cho các vai trò, nơi chạy local/ngoài, prompt, kiểm tra đầu ra, fallback; dùng retrieval thế nào trong phân tích?

**Hai phương án nền để cân nhắc:**

1. **Một lượt phân tích với đầu ra có cấu trúc.** Một lời gọi tạo nhận định/aspects/giải thích theo contract; code kiểm tra schema, quote và điều kiện cơ bản trước khi nhận. Ít lời gọi hơn nhưng cần đánh giá kỹ lỗi suy luận; phản hồi hợp lệ về cấu trúc không được coi là đúng nghiệp vụ.
2. **Tách bước tạo nhận định và bước kiểm tra.** Tạo nhận định trước rồi kiểm tra lại từng kết luận với nguồn bằng bước kiểm tra riêng; có thể dùng cùng mô hình hoặc mô hình khác nếu thử nghiệm hỗ trợ. Dễ phân tích lỗi từng bước, nhưng tăng thời gian/chi phí và không bảo đảm hết lỗi. Nam chọn model/embedding, nơi chạy và fallback sau thử mẫu.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-05 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

### D-06 — Bốn nhóm chia nhận định và rubric — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Vương Thành Nam

**Phần owner tự quyết định:** Nam chọn cách hiện thực phân nhóm, tổ chức nhận định/aspects và áp rubric bên trong module sau khi định nghĩa nghiệp vụ đã thống nhất.

**Vấn đề cần chốt:** Ranh giới tám nhóm phân tích, chia/gộp nhận định trong semantic_diff.changes, giá trị/đơn vị, rubric pilot và ca ngoài phạm vi

**Hai phương án nền để cân nhắc:**

1. **Tách theo từng nhận định pháp lý độc lập.** Mỗi nhận định kiểm chứng độc lập thành một nhận định trong semantic_diff.changes; khía cạnh liên quan đặt trong aspects. Dễ gắn bằng chứng/nhận xét và đối chiếu đáp án; cần quy tắc chống tách vụn, trùng hoặc làm mất quan hệ điều kiện.
2. **Nhóm các khía cạnh gắn chặt trong cùng nhận định.** Một nhận định trong semantic_diff.changes giữ các thay đổi cùng chủ thể/hành vi/điều kiện cần đọc chung; các nghĩa vụ độc lập vẫn tách. Giữ ngữ cảnh dễ đọc hơn nhưng cần tiêu chí nhóm rõ để không che một khía cạnh sai hoặc bỏ sót. Cả hai dùng tám nhóm hiện có và rubric được review, không tự thêm nhãn.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-06 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

### D-07 — Tương tác frontend và cách đọc bằng chứng — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Lê Tùng Dương

**Phần owner tự quyết định:** Tùng Dương quyết định chính thiết kế tương tác, bố cục, tổ chức frontend và lựa chọn cơ chế đọc/giữ bằng chứng trong baseline; chủ động chỉnh các chi tiết không đổi hợp đồng hay yêu cầu chung.

**Vấn đề cần chốt:** Stack frontend, luồng/màn hình, evidence display, bàn phím, lỗi, lọc/đếm và ReviewRecord; cấu trúc mã frontend? Tùng Dương quyết định cơ chế giữ/đọc bằng chứng sau khi backend dọn file; các phương án nền được liệt kê ngay dưới đây.

**Hai phương án nền để cân nhắc:**

1. **Giữ khối nguồn trong phiên và xem bằng chứng cạnh nhận định.** Backend trả các khối nguồn cần thiết cùng báo cáo; frontend tra theo document_id/source_ref, mở nội dung trong vùng bằng chứng cạnh mục đang rà soát. Có thể đọc rộng quanh đoạn trích và không cần file tạm backend; cần kiểm soát dung lượng/khả năng điều hướng.
2. **Giữ trích đoạn có ngữ cảnh trong phiên và mở chi tiết theo mục.** Backend trả trích đoạn cùng phần ngữ cảnh đã xác định, gắn đúng nguồn; frontend mở vùng chi tiết khi chọn bằng chứng. Nhẹ hơn và tập trung tác vụ, nhưng phải kiểm tra đoạn cắt có đủ để người dùng kiểm chứng. Tùng Dương chọn cách hiển thị, phối hợp D-01/D-02 để giữ đúng contract.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-07 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

### D-08 — Đối chiếu nhận xét giữa các lượt — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Lê Tùng Dương

**Phần owner tự quyết định:** Tùng Dương chọn cách tổ chức state, lưu/khôi phục nhận xét trong phiên và hiện thực đối chiếu khi dữ liệu cùng quy tắc đã rõ.

**Vấn đề cần chốt:** Nhận diện cùng mục và dữ liệu cần so sánh giữa hai lượt; giữ REVIEWED khi nào, RECHECK_REQUIRED và nhận xét không ghép được thế nào?

**Hai phương án nền để cân nhắc:**

1. **Nhận diện chắc chắn rồi so sánh đầy đủ nội dung.** Ghép bằng tổ hợp chỉ dẫn/đích/nguồn ổn định; chỉ giữ REVIEWED khi chứng minh nội dung phục vụ kiểm chứng không đổi. Giảm thao tác kiểm tra lại không cần thiết nhưng thuật toán và fixture phải bao quát đổi giải thích/bằng chứng/mức độ; không ghép chỉ theo ID hoặc số Điều.
2. **Đối chiếu thận trọng và yêu cầu kiểm tra lại.** Chỉ gắn những cặp xác định chắc chắn; các mục cũ nhận diện được đều yêu cầu kiểm tra lại, nhận xét cũ giữ riêng; mục không ghép chắc chắn ở danh sách chưa đối chiếu. Dễ kiểm chứng ở bản đầu nhưng người dùng phải rà lại nhiều hơn. Không tự gắn nhận xét theo chuỗi gần giống.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-08 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

### D-09 — Giới hạn vận hành deadline và cleanup — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Dương Đức Anh

**Phần owner tự quyết định:** Đức Anh chọn cách hiện thực kiểm tra giới hạn, deadline, retry và cleanup bên trong backend theo ràng buộc đã thống nhất.

**Vấn đề cần chốt:** Dung lượng/số file, đồng thời, deadline/timeout/retry; dọn tài nguyên khi blocking/tác vụ Server còn chạy; giới hạn ingress?

**Hai phương án nền để cân nhắc:**

1. **Một lượt xử lý đồng thời với deadline chung.** Giữ giới hạn một comparison đang xử lý; đo và cấu hình ngân sách toàn request, kiểm tra deadline giữa các bước. Dễ kiểm soát tài nguyên bản đầu; phải thông báo bận rõ ràng và không coi deadline là hủy được thư viện blocking.
2. **Số lượt đồng thời hữu hạn và ngân sách theo bước.** Giới hạn số comparison đang chạy cùng ngân sách từng bước/dịch vụ trong deadline chung. Có thể phục vụ thêm lượt nhưng cần kiểm chứng tài nguyên, cách ly, contention và cleanup. Vẫn request đồng bộ, không bổ sung job/queue hay xóa tài nguyên khi tác vụ còn dùng.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-09 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

### D-10 — Dữ liệu gold split và mẫu tác vụ — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Bạch Công Dũng

**Phần owner tự quyết định:** Dũng tổ chức thu thập, manifest, đóng gói và quản lý phiên bản dữ liệu theo tiêu chí nguồn/split đã thống nhất.

**Vấn đề cần chốt:** Bộ V1–S/tham chiếu, manifest, split theo nguồn, hồ sơ gold HCI và nhãn context; mẫu đúng/sai kiểm soát cho HCI

**Hai phương án nền để cân nhắc:**

1. **Một bộ nguồn quản lý tập trung bằng manifest.** Mỗi mẫu chỉ rõ file, hash, vai trò, lineage, tham chiếu và nhãn; fixture kỹ thuật/tương tác tham chiếu về bộ nguồn chung. Ít bản sao hơn, cần quản lý đường dẫn/phiên bản để mẫu không vô tình đổi.
2. **Đóng gói mẫu thành các bộ có phiên bản.** Mỗi mẫu có hồ sơ nguồn, bộ căn cứ, gold và review; manifest chung quản lý split/lineage. Bên nhận dễ chạy lại riêng nhưng có thể tăng trùng lặp; phải giữ cùng lineage trong một split và tách rõ gợi ý sai kiểm soát, V2/gold với đầu vào hệ thống.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-10 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

### D-11 — Matching metric và kiểm chứng phép đo — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Vương Thành Nam

**Phần owner tự quyết định:** Nam chọn cách hiện thực công cụ đo, tổ chức script và phân tích lỗi theo quy tắc đánh giá đã được thống nhất.

**Vấn đề cần chốt:** Matching SemanticChange/aspects, metric, ca null/không mẫu, lỗi nguồn/linker/retrieval; ngưỡng nào có căn cứ?

**Hai phương án nền để cân nhắc:**

1. **Matching theo nguồn và nội dung với tiêu chí cố định.** Dùng chỉ dẫn/đích/nguồn tạo cặp ứng viên; nhận cặp khi đạt các tiêu chí nội dung/aspects đã chốt, không tính trùng. Dễ tái lập hơn nhưng cần nêu rõ trường hợp không khớp hoặc diễn đạt khác và cách xử lý chia/gộp.
2. **Tạo cặp ứng viên rồi review đối chiếu có rubric.** Dùng nguồn/đích và nội dung để đề xuất cặp; người review xử lý diễn đạt khác hoặc chia/gộp theo rubric cố định, lưu quyết định trước khi tổng hợp số đo. Phù hợp bộ nhỏ nhưng tốn công và cần kiểm tra độ nhất quán. Cả hai phải tính sai/bỏ sót, không coi trùng ID hay một aspect là đủ đúng.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-11 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

### D-12 — Tác vụ người dùng và đánh giá cải tiến — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Bạch Công Dũng

**Phần owner tự quyết định:** Dũng chủ trì lựa chọn và tổ chức buổi dùng thử, điều phối người tham gia, thu phản hồi và tổng hợp vấn đề trong kế hoạch đã thống nhất.

**Vấn đề cần chốt:** Tác vụ, người tham gia, tiêu chí chấm, SUS/phản hồi, thiết kế so sánh giao diện, kế hoạch cải tiến/kiểm tra lại

**Hai phương án nền để cân nhắc:**

1. **Dùng thử theo tác vụ và cải tiến theo vấn đề.** Người tham gia thực hiện tác vụ tìm thay đổi, kiểm chứng, đọc cảnh báo và ghi nhận xét; ghi độ đúng/thời gian/lỗi, thu SUS/phản hồi rồi sửa và kiểm tra lại tác vụ bị ảnh hưởng. Dễ tổ chức hơn nhưng không tự chứng minh giao diện tốt hơn một phương án khác.
2. **So sánh hai cách trình bày trên tác vụ tương đương.** So sánh giao diện cơ bản với giao diện có giải thích/bằng chứng trên cùng đầu ra cố định; cân đối thứ tự và dùng tác vụ tương đương để hạn chế hiệu ứng học, thu kết quả/SUS/phản hồi. Có căn cứ so sánh rõ hơn nhưng cần chuẩn bị thêm và công bố giới hạn mẫu nhỏ; chưa chốt số người hoặc kết quả.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-12 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

### D-13 — Môi trường cấu hình và khả năng chạy lại — Phần A

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Dương Đức Anh — quyền quyết định chính

**Phần owner tự quyết định:** Đức Anh quyết định chính cách đóng gói, khởi động, kiểm tra sẵn sàng và cấu hình vận hành trong phạm vi đã thống nhất.

**Vấn đề cần chốt:** Cách cài/chạy LightRAG riêng, pin dependency/model/config; Python env hay container, storage, xác thực, log; khởi động và kiểm tra sẵn sàng

**Hai phương án nền để cân nhắc:**

1. **Hai môi trường Python riêng cho backend và LightRAG.** Pin dependency và hướng dẫn khởi động/kiểm tra từng môi trường; backend gọi Server HTTP. Dễ bám bộ code Python hiện có, nhưng cần kiểm tra cài sạch và khác biệt máy/hệ điều hành.
2. **Đóng gói các dịch vụ bằng container.** Tách backend và LightRAG thành dịch vụ với cấu hình/version được cố định, kèm kiểm tra sẵn sàng và hướng dẫn storage/cleanup. Dễ mô tả môi trường chạy thống nhất hơn, nhưng tăng công đóng gói và phải kiểm chứng model, dung lượng/tài nguyên cùng khả năng chạy trên máy dùng thử.

**Phương án owner đề xuất:** [Chọn, điều chỉnh hoặc đề xuất phương án khác.]

**Lý do và đánh đổi:** [Điền lý do, chi phí/giới hạn và ví dụ kiểm chứng.]

**Kết luận hiện có:** Chưa chốt phương án kỹ thuật; giữ baseline và trách nhiệm đã xác nhận. Hai phương án nền chưa là quyết định của owner.

**Phần phối hợp liên quan:** Xem D-13 ở phần B; không dùng lựa chọn nội bộ để tự đổi contract hoặc điều kiện chung.

## B. Quyết định cần nhiều bên thống nhất

Bên cung cấp và bên nhận thống nhất hợp đồng/fixture và những ràng buộc ảnh hưởng lẫn nhau. Chỉ cần các bên thực sự bị ảnh hưởng xác nhận; không mặc định cả nhóm duyệt mọi chi tiết. Lựa chọn hiện thực và hai phương án nền được dẫn theo cùng D-ID ở phần A.

### D-01 — Contract API schema và báo cáo — Phần B

**Trạng thái:** Đã chốt hợp đồng API cho bản nền HCI. Còn bước kiểm tra và bàn giao.

**Chủ trì:** Dương Đức Anh

**Bên cần thống nhất hoặc review:** Dũng + Đức Anh cùng biên soạn api-contract.md; Tùng Dương nhận API; Nam review dữ liệu

**Phần cần nhiều bên thống nhất:** Đức Anh, Dũng, Tùng Dương và Nam theo phần sử dụng thống nhất request/response, tên/kiểu/ý nghĩa trường, lỗi HTTP, fixture bàn giao và các thay đổi đối với hợp đồng API. Dũng + Đức Anh cùng biên soạn api-contract.md; đổi nguồn phối hợp D-02/D-07.

**Đầu vào cần thống nhất:** V1/S/tham chiếu, baseline SRS, report nền và dữ liệu module cần tổng hợp.

**Đầu ra cần thống nhất:** Request/response HCI, schema/validator, lỗi HTTP và fixture nguồn/báo cáo; giao diện nội bộ cần bên giao/nhận xác nhận.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Một bộ request/response thành công, PARTIAL, FAILED, lỗi đầu vào; bảng delta với code; schema/fixture validate được khi triển khai

**Trước khi và nơi cập nhật sau chốt:** Trước nối frontend và báo cáo HCI; SRS, api-contract.md, schema/fixtures

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-01 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-02 — Đầu vào Parser adapter và truy nguồn — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Bạch Công Dũng

**Bên cần thống nhất hoặc review:** Đức Anh nhận adapter; Nam/Tùng Dương dùng nguồn

**Phần cần nhiều bên thống nhất:** Dũng và Đức Anh thống nhất output bàn giao, ID, block/spans, bảng/outside, null/lỗi. Nam/Tùng Dương review phần nguồn họ sử dụng; mapping PDF và chuyển Unicode offsets phải được xác nhận với bên hiển thị/nhận dữ liệu.

**Đầu vào cần thống nhất:** File DOCX/PDF có lớp chữ, vai trò tài liệu, cây và source_blocks hiện có, thông tin chuyển đổi.

**Đầu ra cần thống nhất:** Nguồn cùng cấu trúc nội dung để Đức Anh dùng cho linker/context; định danh, block/spans, bảng/outside, cảnh báo và giới hạn mapping.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Một DOCX và một PDF: nguồn gốc/chuyển đổi, cây, contract bàn giao, quote truy đúng vị trí và giới hạn; ca reference không có Điều

**Trước khi và nơi cập nhật sau chốt:** Trước linker/context và hiển thị nguồn; SRS, Architecture, Data Guide, fixture nguồn

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-02 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-03 — Chỉ dẫn vị trí đích và nội dung trước sau — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Dương Đức Anh

**Bên cần thống nhất hoặc review:** Dũng review chỉ dẫn/đích; Nam nhận trước–sau

**Phần cần nhiều bên thống nhất:** Đức Anh và Nam thống nhất cấu trúc trước–sau, chỉ dẫn/đích, căn cứ trích/suy ra, hiệu lực và cảnh báo. Dũng review nghiệp vụ/nguồn; thay output từ Parser/adapter cần phối hợp D-02.

**Đầu vào cần thống nhất:** Cây/nguồn V1, nội dung S và tham chiếu cần thiết; hợp đồng nguồn D-02.

**Đầu ra cần thống nhất:** Các chỉ dẫn có đích/thao tác/phạm vi, trước–sau cục bộ, căn cứ tạo nội dung, hiệu lực và phần chưa xác định để Nam nhận.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Ví dụ sửa đơn vị/cụm từ, bổ sung/bãi bỏ, S sửa nhiều văn bản và đích mơ hồ; expected/actual và nguồn

**Trước khi và nơi cập nhật sau chốt:** Trước phân tích trên dữ liệu thật; Architecture, fixture linker, API khi ảnh hưởng

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-03 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-04 — Retrieval ngữ cảnh và vòng đời LightRAG — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Dương Đức Anh — quyền quyết định chính

**Bên cần thống nhất hoặc review:** Dũng review nguồn; Nam nhận context; Tùng Dương kiểm tra khả năng đọc bằng chứng

**Phần cần nhiều bên thống nhất:** Đức Anh thống nhất với Dũng về nguồn/mapping, với Nam về ngữ cảnh và bằng chứng bàn giao, với Tùng Dương về dữ liệu đọc nguồn. Model/embedding phối hợp Nam theo D-05; thay tài nguyên chung, cách ly hoặc vòng đời phải thống nhất với các bên bị ảnh hưởng và D-09/D-13.

**Đầu vào cần thống nhất:** Cây/khối nguồn đã chuẩn hóa, chỉ dẫn/đích và yêu cầu ngữ cảnh; cấu hình mô hình phối hợp D-05.

**Đầu ra cần thống nhất:** Ngữ cảnh có nguyên văn/vị trí nguồn, tình trạng căn cứ và tham chiếu; trạng thái nhập/query/lỗi/cleanup để Pipeline sử dụng.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Parser → nhập → xác nhận sẵn sàng → query → ánh xạ quote → dọn; hai bộ không lẫn; ghi request/response thực tế đã loại bí mật, thời gian và giới hạn

**Trước khi và nơi cập nhật sau chốt:** Trước tích hợp retrieval; Architecture, API contract phần nội bộ, Development Guide

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-04 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-05 — Mô hình prompt validation và fallback — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Vương Thành Nam — quyền quyết định chính

**Bên cần thống nhất hoặc review:** Đức Anh vận hành/client; Dũng review nguồn; thay contract vẫn phối hợp bên nhận

**Phần cần nhiều bên thống nhất:** Nam và Đức Anh thống nhất giao diện AI Adapter, cấu hình vận hành chung, dependency và output/lỗi; Dũng review nguồn, bên nhận review thay đổi contract. Phương án phát sinh chi phí, gửi dữ liệu ra ngoài hoặc thay yêu cầu tài nguyên phải phối hợp người chịu ảnh hưởng; không tự đổi ràng buộc chung chỉ vì được quyền chọn mô hình.

**Đầu vào cần thống nhất:** Nội dung trước–sau, chỉ dẫn, ngữ cảnh/bằng chứng và cấu trúc kết quả phân tích cần trả.

**Đầu ra cần thống nhất:** Kết quả gọi mô hình có cấu trúc, nguồn kiểm tra được, trạng thái lỗi/chưa rõ và cấu hình đủ tái lập để module phân tích sử dụng.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** So sánh trên cùng mẫu, cấu hình/mô hình/phiên bản, output đúng/sai/chưa rõ, token/chi phí nếu đo được; giới hạn và quyền truy cập

**Trước khi và nơi cập nhật sau chốt:** Trước chọn cấu hình phân tích và công bố nhu cầu mạng; Architecture, config, Development Guide

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-05 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-06 — Bốn nhóm chia nhận định và rubric — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Vương Thành Nam

**Bên cần thống nhất hoặc review:** Dũng review nhãn; Đức Anh/Tùng Dương nhận report

**Phần cần nhiều bên thống nhất:** Nam và Dũng thống nhất ranh giới nhãn, cách chia/gộp, rubric và ví dụ chuẩn; Đức Anh/Tùng Dương review cấu trúc kết quả họ nhận. Không tự đổi tám nhóm trong SRS, đơn vị đếm, gold hoặc nội dung giao diện bằng một lựa chọn nội bộ.

**Đầu vào cần thống nhất:** Bốn mã HCI trong SRS, chỉ dẫn và nội dung trước–sau, bằng chứng, ví dụ/nhãn pilot.

**Đầu ra cần thống nhất:** Quy tắc chia/gộp nhận định trong semantic_diff.changes, chọn aspects/nhóm và chấm mức tác động, cùng fixture ranh giới và ngoài phạm vi.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Ví dụ ranh giới, lý do gán nhãn, câu giải thích/evidence, ca không được ép mã; reviewer và phiên bản

**Trước khi và nơi cập nhật sau chốt:** Trước khóa gold hoặc dùng Scorer; SRS nếu đổi contract, Data Guide, fixtures

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-06 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-07 — Tương tác frontend và cách đọc bằng chứng — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Lê Tùng Dương

**Bên cần thống nhất hoặc review:** Dũng đối chiếu nghiên cứu; Đức Anh/Nam cung cấp dữ liệu

**Phần cần nhiều bên thống nhất:** Tùng Dương và Đức Anh thống nhất dữ liệu API/nguồn, lỗi và trạng thái; Dũng phối hợp provenance/đáp án và căn cứ người dùng; Nam review cách trình bày nhận định/bằng chứng. Cơ chế Tùng Dương chọn nếu cần đổi payload, endpoint, vòng đời hoặc giới hạn tài nguyên phải được bên cung cấp/nhận thống nhất trước hiện thực.

**Đầu vào cần thống nhất:** RQ/BG, kịch bản/tác vụ, fixture ComparisonReport/nguồn và dữ liệu nhận xét trong phiên.

**Đầu ra cần thống nhất:** Prototype, luồng/màn hình, trạng thái UI/ReviewRecord, cơ chế giữ/đọc bằng chứng sau cleanup và fixture tương tác.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Prototype theo tác vụ, fixture API dùng được, bảng trạng thái UI, cách đọc nguồn và kiểm thử tương tác

**Trước khi và nơi cập nhật sau chốt:** Trước triển khai luồng UI chính; thiết kế tương tác, Architecture, SRS khi đổi hành vi

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-07 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-08 — Đối chiếu nhận xét giữa các lượt — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Lê Tùng Dương

**Bên cần thống nhất hoặc review:** Đức Anh cung cấp ID/nguồn; Dũng/Nam review ca thay đổi

**Phần cần nhiều bên thống nhất:** Tùng Dương và Đức Anh thống nhất dữ liệu nhận diện, nội dung dùng để so sánh và contract báo cáo giữa hai lượt. Dũng/Nam review fixture thêm/đổi/tách/gộp/mất mục, giữ nhận xét và yêu cầu kiểm tra lại; thay quy tắc trạng thái SRS phải được các bên xác nhận.

**Đầu vào cần thống nhất:** Báo cáo cũ/mới, nội dung/nguồn liên quan, ReviewRecord và quan hệ chỉ dẫn/đích.

**Đầu ra cần thống nhất:** Quan hệ mục cũ–mới, trạng thái REVIEWED/UNREVIEWED/RECHECK_REQUIRED, previous_record và danh sách nhận xét không ghép được.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Hai report và ReviewRecord trước/sau; ca thêm mục, nội dung đổi, tách/gộp, mục mất, PARTIAL và request thất bại

**Trước khi và nơi cập nhật sau chốt:** Trước luồng bổ sung/phân tích lại; SRS nếu cần đổi, Architecture, fixture phiên

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-08 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-09 — Giới hạn vận hành deadline và cleanup — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Dương Đức Anh

**Bên cần thống nhất hoặc review:** Các owner module cung cấp số đo; Tùng Dương hiển thị giới hạn

**Phần cần nhiều bên thống nhất:** Đức Anh cùng các owner thống nhất giới hạn cần đo, ngân sách bước và khả năng dừng tác vụ; Tùng Dương thống nhất thông báo/cách tiếp tục ở UI. Dũng phối hợp nguồn lực và tác vụ dùng thử; không biến default code thành giới hạn nghiệm thu hoặc tự đổi hành vi timeout phía frontend.

**Đầu vào cần thống nhất:** Kích thước/số file, số đo từng module/dịch vụ và môi trường dự kiến chạy.

**Đầu ra cần thống nhất:** Cấu hình giới hạn, hành vi vượt giới hạn/lỗi/timeout, quy tắc retry và dọn tài nguyên, cùng ca kiểm chứng.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Đo trên mẫu/môi trường, ca vượt giới hạn/lỗi/timeout, vị trí cấu hình và phần không thể hủy cứng; không coi mặc định code là benchmark

**Trước khi và nơi cập nhật sau chốt:** Trước tích hợp thật và dùng thử; SRS yêu cầu vận hành, API Contract, config, Development Guide

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-09 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-10 — Dữ liệu gold split và mẫu tác vụ — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Bạch Công Dũng

**Bên cần thống nhất hoặc review:** Nam review nhãn/đáp án; Đức Anh/Tùng Dương dùng fixture

**Phần cần nhiều bên thống nhất:** Dũng và Nam thống nhất nhãn, đáp án, lineage/split, phạm vi đủ/thiếu căn cứ và review gold. Đức Anh/Tùng Dương review fixture cần sử dụng; mẫu người dùng/gợi ý sai kiểm soát phối hợp D-12, không tự thay dữ liệu đánh giá đã cố định.

**Đầu vào cần thống nhất:** V1/S/tham chiếu có nguồn, lineage, chất lượng chuyển đổi và phạm vi bốn nhóm HCI.

**Đầu ra cần thống nhất:** Manifest, mẫu/gold đã review, split, fixture đủ/thiếu căn cứ và dữ liệu tác vụ tách khỏi index/phép đo AI.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Danh sách file/hash/vai trò/lineage, mẫu bốn nhóm và thiếu căn cứ, đáp án/reviewer; tách V2/gold/gợi ý sai khỏi index và đo AI

**Trước khi và nơi cập nhật sau chốt:** Trước khóa dữ liệu/đánh giá; Data Guide, data/manifest và fixture

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-10 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-11 — Matching metric và kiểm chứng phép đo — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Vương Thành Nam

**Bên cần thống nhất hoặc review:** Dũng review gold; Đức Anh/Tùng Dương cung cấp kết quả

**Phần cần nhiều bên thống nhất:** Nam và Dũng thống nhất gold, đơn vị đánh giá, matching/aspects, công thức, cách xử lý chưa xác định và ngưỡng có căn cứ; Đức Anh/Tùng Dương phối hợp dữ liệu đầu ra và khả năng tái lập. Những thay đổi làm đổi cách diễn giải hoặc so sánh số liệu phải được bên dùng kết quả review trước đo.

**Đầu vào cần thống nhất:** Dự đoán và gold theo SemanticChange/aspects trên cùng bộ căn cứ, cùng quy tắc nhãn đã review.

**Đầu ra cần thống nhất:** Quy tắc đối chiếu, công thức/cách tổng hợp, ca tính tay, cách xử lý null/không mẫu, ngưỡng có căn cứ và lệnh/cấu hình đo.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Ca tính tay có TP/FP/FN, sai/thiếu aspect, nguồn sai và phần chưa xác định; lệnh đo/config; tiêu chí cố định trước test

**Trước khi và nơi cập nhật sau chốt:** Trước chạy đánh giá kỹ thuật; test_evaluation_plan.md phần kỹ thuật, evaluator/fixtures

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-11 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-12 — Tác vụ người dùng và đánh giá cải tiến — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Bạch Công Dũng

**Bên cần thống nhất hoặc review:** Tùng Dương thiết kế; Nam chuẩn bị đáp án; Đức Anh bàn giao bản chạy

**Phần cần nhiều bên thống nhất:** Dũng phối hợp Tùng Dương về tác vụ/giao diện, Nam về đáp án và gợi ý sai kiểm soát, Đức Anh về phiên bản/môi trường sẵn sàng. Thiết kế so sánh, cách chấm và cải tiến ảnh hưởng nhiều module cần các bên liên quan thống nhất trước thực hiện.

**Đầu vào cần thống nhất:** RQ/BG/AT, bản chạy ổn định, dữ liệu/đáp án, mẫu đúng/sai kiểm soát và nhóm người dùng mục tiêu.

**Đầu ra cần thống nhất:** Kế hoạch tác vụ/người tham gia/cách chấm, SUS/phản hồi, vấn đề/cải tiến và minh chứng kiểm tra lại gắn phiên bản.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Kế hoạch nối với BG/RQ/AT, đáp án và gợi ý sai kiểm soát, biểu mẫu/phiên bản, lịch/nguồn lực thực tế; phân biệt hai người nghiên cứu ban đầu với người dùng thử

**Trước khi và nơi cập nhật sau chốt:** Trước tuyển/dùng thử và thu số liệu; test_evaluation_plan.md phần usability, User Research chỉ khi có dữ liệu mới

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-12 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

### D-13 — Môi trường cấu hình và khả năng chạy lại — Phần B

**Trạng thái:** CHỜ OWNER ĐỀ XUẤT.

**Chủ trì:** Dương Đức Anh — quyền quyết định chính

**Bên cần thống nhất hoặc review:** Dũng + Đức Anh cùng biên soạn development-guide.md; mỗi owner bàn giao dependency/lệnh; Dũng xác nhận máy dùng thử

**Phần cần nhiều bên thống nhất:** Đức Anh nhận dependency/lệnh từ các owner, phối hợp Nam về model/embedding D-05 và Dũng về máy dùng thử/nguồn lực. Dũng + Đức Anh cùng biên soạn development-guide.md; đổi môi trường chung, chi phí, storage hoặc vòng đời ảnh hưởng bên khác phải được thống nhất.

**Đầu vào cần thống nhất:** Dependency/lệnh của từng module, cấu hình đã kiểm chứng, model/embedding theo D-05 và máy dùng thử.

**Đầu ra cần thống nhất:** Hướng dẫn cài/chạy, cấu hình mẫu không bí mật, phiên bản cố định, kiểm tra sẵn sàng và điều kiện Internet/tài nguyên.

**Chi tiết hợp đồng cần điền khi có điểm nối:**

- Bên giao → bên nhận: [Điền cặp chức năng và người liên quan.]
- Giao diện gọi và cách trao đổi: [Tên hàm/API, tham số, kiểu trả về hoặc cách bàn giao dữ liệu.]
- Trường dữ liệu và ý nghĩa: [Tên/kiểu, bắt buộc/tùy chọn, ID, nguồn và offset khi liên quan.]
- Null, rỗng, cảnh báo và lỗi: [Phân biệt chưa biết, không tồn tại, chưa chạy và thất bại.]
- Fixture và expected output: [Đường dẫn, phiên bản, căn cứ đáp án và bên nhận đã review.]

**Đầu ra tối thiểu để review:** Hướng dẫn cài sạch và chạy lại trên máy khác, cấu hình mẫu không bí mật, một lệnh/nhóm lệnh kiểm tra; khai báo phần cần Internet và nguồn phải tải trước

**Trước khi và nơi cập nhật sau chốt:** Trước bàn giao chạy thật; development-guide.md, requirements/config/deploy; README chỉ tóm tắt

**Xác nhận còn cần:** [Người/bên cần xác nhận, kết quả chạy lại và phần còn mở.]

**Tài liệu schema fixture hoặc code cần cập nhật:** [Điền đầu ra bị ảnh hưởng sau khi chốt.]

**Quyết định liên quan hoặc thay thế:** [Điền D-ID và phạm vi nếu có.]

**Lựa chọn hiện thực liên quan:** Xem D-13 ở phần A; xác nhận ở đây chỉ áp dụng cho nội dung phối hợp đã được các bên thống nhất.

Không cần mọi D-ID hoàn tất mới làm module. D-01/D-02 cần đủ rõ trước ghép dữ liệu; có thể thử riêng D-03/D-04/D-05/D-07 bằng fixture. D-06/D-10 và D-11/D-12 cần rõ trước khóa gold hoặc đánh giá. D-04 chọn cấu hình dịch vụ trong phép thử; D-13 đóng gói cấu hình đã kiểm chứng, không duy trì hai cấu hình trái nhau.

Các lựa chọn về phạm vi toàn file, tên trường/API, model, endpoint và ngưỡng chưa được chốt chỉ bằng việc ghi phương án nền. Trường hợp một D-ID không bàn giao dữ liệu runtime, phần hợp đồng được áp dụng cho bộ mẫu, cấu hình hoặc tài liệu bàn giao tương ứng; không bắt tạo API không cần thiết.

**Mẫu owner trả lời**

Owner điền các trường lựa chọn nội bộ ở phần A và cùng bên liên quan hoàn thiện phần B theo cùng D-ID; có thể thêm trường con khi cần. Mẫu dưới đây dùng khi tổng hợp đề xuất, không tạo một bản quyết định song song. Hai phương án nền là đề xuất tham khảo, không điền hộ lựa chọn hoặc xác nhận của owner.

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
Kết luận được chốt; người xác nhận:
File schema/fixture/tài liệu đã cập nhật:
```

**Quy tắc cập nhật**

1. Owner chọn phương pháp nội bộ trong baseline, tự kiểm tra và ghi đề xuất. Không cần họp cả nhóm cho mọi chi tiết thư viện.
2. Bên nhận/reviewer kiểm tra ví dụ và chạy lại phần bàn giao. Mỗi task vẫn có một owner; người kiểm thử không thay tự kiểm tra.
3. Đổi contract phải có schema và fixture cùng các module bị ảnh hưởng. Dũng tổng hợp thay đổi phạm vi/phân công/mốc; Đức Anh điều phối contract và tích hợp.
4. Chỉ chuyển ĐÃ CHỐT khi có quyết định được xác nhận, minh chứng và tài liệu sở hữu đã cập nhật. Dòng đề xuất không tự thành quyết định cả nhóm.
5. Giữ lịch sử phương án/căn cứ khi điều chỉnh; không ghi đè gold, kết quả nghiên cứu hoặc số đo để làm đẹp tiến độ.
6. Các file chuyên trách chỉ giữ yêu cầu/thiết kế đã thống nhất và dẫn D-ID còn mở; không sao chép nhiều bảng trạng thái khác nhau.

**Tài liệu cần hoàn thiện sau đề xuất**

- `api-contract.md`: Dũng + Đức Anh cùng biên soạn theo D-01; D-02 về nguồn, D-04 về dịch vụ, D-07 về cơ chế đọc bằng chứng, D-09 về giới hạn/lỗi. Chưa có trong gói.
- `development-guide.md`: Dũng + Đức Anh cùng biên soạn theo D-13; Đức Anh quyết định chính về triển khai/vận hành. Chưa có trong gói.
- [test_evaluation_plan.md](test_evaluation_plan.md): đã có bản khung, đang hoàn thiện; D-11 phần kỹ thuật, D-12 phần usability.

api-contract.md và development-guide.md chưa có; kế hoạch kiểm thử/đánh giá đã có bản khung, đang hoàn thiện. Không ghi thông số chưa được owner quyết định hoặc coi bản khung là kế hoạch đã hoàn tất.
