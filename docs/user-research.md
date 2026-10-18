# Nghiên cứu người dùng

**Học phần và nhóm:** 2627I_INT2041_1 Nhóm 6  
**Đề tài:** Hệ thống hỗ trợ đối chiếu thay đổi văn bản pháp luật với AI có giải thích và có sự kiểm chứng của người dùng  
**Thành viên:** Bạch Công Dũng, Dương Đức Anh, Lê Tùng Dương, Vương Thành Nam  
**Phiên bản:** 0.3  
**Ngày cập nhật:** 15/10/2026  
**Cơ sở cập nhật:** Kết quả trao đổi với hai sinh viên vừa vào năm 3.

## 1. Mục đích và ranh giới tài liệu

Tài liệu tổng hợp cách người dùng đối chiếu văn bản pháp luật, nhu cầu thông tin và những điểm nhóm cần lưu ý khi thiết kế sản phẩm. Nội dung dành cho các thành viên cùng hiểu người dùng và có căn cứ xây dựng luồng tương tác.

Kết quả dưới đây dựa trên phần trả lời do người thực hiện trao đổi tổng hợp. Thông tư 33/2019/TT-BTC và hai Luật 64/2025/QH15, 87/2025/QH15 được dùng để kiểm tra cách hiểu nghiệp vụ và thuật ngữ. Các văn bản này không phải dữ liệu phỏng vấn.

Trong phạm vi dự án, S nêu các nội dung sửa đổi và vị trí bị tác động trong V1. Người đọc theo chỉ dẫn đó để tìm nội dung gốc và đối chiếu. Nhu cầu cần tìm hiểu là thông tin giúp họ phân tích phần thay đổi và kiểm chứng kết quả; không mặc định việc số Điều trong S khác số Điều đích là một khó khăn của người dùng.

Phạm vi chức năng và kỹ thuật theo báo cáo HCI, BRD, SRS và Architecture. Tài liệu này chỉ tổng hợp kết quả tìm hiểu và định hướng thiết kế rút ra.

## 2. Những điều đã tìm hiểu

Bốn câu hỏi dưới đây đã có thông tin trả lời trong bản cập nhật. Nội dung được diễn đạt lại từ ghi chép tổng hợp, không phải lời trích nguyên văn. Chưa có dữ liệu tách riêng từng người nên không xác định mức độ đồng thuận hoặc khác biệt giữa hai người.

| Mã | Câu hỏi nghiên cứu | Kết quả tìm hiểu hiện tại |
| --- | --- | --- |
| RQ-01 | Người dùng đang đối chiếu V1 và S theo những bước nào? Bước nào khiến họ phải tìm lại hoặc đọc lại? | Đọc S để xác định vị trí bị sửa, quay lại V1, đối chiếu nội dung trước–sau rồi suy ra nhận xét. Ghi chép chưa xác định bước nào tốn thời gian hoặc gây lỗi nhiều nhất. |
| RQ-02 | Để giải thích một thay đổi cụ thể, họ cần đọc thêm ngữ cảnh nào và khi nào thấy đủ căn cứ? | Theo trả lời hiện có, họ cần nắm mục đích chính của V1 và xem phần bị sửa ở dạng so sánh. Chưa có căn cứ kết luận hai phần này luôn đủ cho mọi tình huống pháp lý. |
| RQ-03 | Khi một dẫn chiếu chuyển sang văn bản khác, họ tìm tài liệu gì và làm sao biết đã chọn đúng? | Tìm bằng tên hoặc số hiệu văn bản được dẫn chiếu, sau đó đọc trực tiếp phần liên quan để áp dụng vào việc đối chiếu V1. Ghi chép chưa làm rõ cách kiểm tra phiên bản hoặc hiệu lực. |
| RQ-04 | Họ dựa vào đâu để chấp nhận, bác bỏ hoặc tạm hoãn kết luận từ gợi ý AI? | Đối chiếu kết quả AI với kết quả tự phân tích. Chưa nêu được tiêu chí cụ thể hơn để xử lý khi hai kết quả khác nhau hoặc khi chính người dùng chưa chắc chắn. |

Những câu trả lời này cho thấy cách tiếp cận hiện tại và nhu cầu thông tin ban đầu. Chúng chưa chứng minh hiệu quả của giao diện dự kiến hoặc độ tin cậy của AI.

## 3. Ghi nhận và phân tích bằng chứng

### 3.1. Kết quả từ trao đổi với người dùng

| Phát hiện | Căn cứ | Ý nghĩa đối với sản phẩm |
| --- | --- | --- |
| Người dùng bắt đầu từ chỉ dẫn sửa đổi rồi tìm lại nội dung gốc | RQ-01 | Mỗi mục kết quả nên nối chỉ dẫn trong S với đúng vị trí đích trong V1 và cho phép đọc hai phần liên quan cạnh nhau. |
| Người dùng muốn nắm ý chính của V1 và tập trung phần sửa | RQ-02 | Cung cấp thông tin tổng quát ngắn, ưu tiên nội dung trước–sau; cho phép đọc thêm ngữ cảnh liên quan khi cần. |
| Tên hoặc số hiệu là đầu mối tìm tài liệu tham chiếu | RQ-03 | Khi yêu cầu bổ sung tài liệu, hiển thị tên/số hiệu và vị trí cần đọc nếu xác định được. |
| Kết quả tự phân tích là điểm đối chiếu với AI | RQ-04 | Giữ nội dung nguồn dễ truy cập và tách nhận xét người dùng khỏi gợi ý AI; không coi thao tác đồng ý là bằng chứng AI đã đúng. |
| Tiêu chí kiểm chứng AI còn chưa rõ | RQ-04 | Cần trình bày nhận định cụ thể, căn cứ và giới hạn để hỗ trợ đối chiếu; chưa thể khẳng định một cách hiển thị nào đã hiệu quả. |

### 3.2. Nhu cầu và định hướng thiết kế rút ra

| Nhu cầu | Căn cứ từ trao đổi | Định hướng thiết kế |
| --- | --- | --- |
| Xem nội dung gốc và nội dung sửa đổi tại phần đang xét | RQ-01 | Từ mỗi chỉ dẫn trong S, cho phép xem ngay phần V1 tương ứng và nội dung mới. Không buộc người dùng tự tìm lại giữa các màn hình. |
| Nắm ý chính của V1 rồi tập trung phân tích phần sửa | RQ-02 | Hiển thị thông tin tổng quát ngắn và phần so sánh cục bộ; giữ khả năng mở ngữ cảnh khi cần. |
| Đọc nội dung dẫn chiếu có liên quan | RQ-03 | Nêu rõ tài liệu và phần cần đọc nếu xác định được; cho phép bổ sung khi nội dung đó chưa có. |
| Đối chiếu kết quả tự phân tích với gợi ý AI | RQ-04 | Tách rõ nội dung nguồn, giải thích AI và nhận xét người dùng; giữ bằng chứng dễ truy cập. |

Các lựa chọn giao diện trong bảng là đề xuất của nhóm dựa trên câu trả lời hiện có, chưa phải giải pháp đã được người dùng thử và xác nhận. Việc hiển thị liên kết chưa chắc chắn, cảnh báo thiếu căn cứ và phạm vi xử lý vẫn theo yêu cầu sản phẩm; chưa có bằng chứng từ hai cuộc trao đổi để kết luận người dùng đang nhầm những trạng thái đó.

## 4. Persona và scenario tạm thời

### 4.1. Persona tổng hợp ban đầu

Người dùng đại diện là sinh viên vừa vào năm 3, cần tìm hiểu thay đổi trong văn bản pháp luật. Cách làm được ghi nhận là đọc S, xác định phần bị sửa, quay lại V1 và đối chiếu để đưa ra nhận xét. Họ cần nắm mục đích chính của V1 và nội dung trước–sau tại phần sửa; khi có dẫn chiếu, họ tìm tài liệu theo tên hoặc số hiệu rồi đọc phần liên quan.

Đối với AI, họ dùng kết quả tự phân tích làm căn cứ đối chiếu nhưng chưa nêu được bộ tiêu chí kiểm chứng rõ ràng. Sản phẩm cần hỗ trợ đọc nguồn và tự hình thành nhận xét, đồng thời làm rõ điều chưa đủ căn cứ. Chưa có dữ liệu về công cụ thường dùng, tần suất đối chiếu hoặc hành vi sử dụng giao diện; persona này chỉ tổng hợp đặc điểm đã ghi nhận và vẫn ở mức ban đầu.

### 4.2. Scenario sử dụng dự kiến

Sinh viên cần tìm hiểu một quy định đã được sửa đổi để phục vụ học tập. Họ đọc S để biết phần nào bị sửa, tìm nội dung tương ứng trong V1, nắm mục đích chính của văn bản và đối chiếu phần trước–sau để hình thành nhận xét. Khi việc diễn giải cần nội dung từ một văn bản được dẫn chiếu, họ tìm văn bản đó theo tên hoặc số hiệu rồi đọc phần liên quan.

Khi dùng sản phẩm, sinh viên cần xem được nội dung đối chiếu và gợi ý AI để so với nhận xét của mình. Nếu thiếu căn cứ, hệ thống cần chỉ rõ nội dung còn thiếu, giữ phần kết quả đã có và hỗ trợ bổ sung tài liệu. Scenario này diễn đạt lại tác vụ từ kết quả trao đổi và phạm vi dự án; chưa phải hành vi đã quan sát trên giao diện.

## 5. Trạng thái hiện tại và đầu ra bàn giao

Đã có thông tin trao đổi ban đầu từ hai sinh viên vừa vào năm 3, tập trung vào cách đối chiếu, nhu cầu ngữ cảnh, tìm tài liệu dẫn chiếu và kiểm tra gợi ý AI. Các văn bản mẫu và luật liên quan đã được dùng để rà soát cách mô tả nghiệp vụ, không dùng để bổ sung các phát hiện người dùng chưa cung cấp.

Các thành viên có thể dùng bảng tại mục 3.2 làm đầu vào thiết kế giao diện và kiểm tra sự phù hợp của dữ liệu trả về. Phần schema, thuật toán và tiêu chí mức tác động tiếp tục được quản lý trong tài liệu đặc tả tương ứng.

Những nội dung chưa có kết quả gồm: bước nào gây khó khăn nhất; cách xác minh phiên bản tài liệu; cách hiểu các nhãn chưa chắc chắn; hành vi khi kết quả phân tích lại thay đổi; và hiệu quả thực tế của các thao tác kiểm chứng. Không xem các nội dung này là nhu cầu đã được xác nhận hoặc vấn đề đã xảy ra với cả hai người. Các giả định về chuyển đổi tài liệu gây mất thời gian, nhầm trạng thái hoặc hiệu quả của việc đặt bằng chứng cạnh AI chưa có dữ liệu đủ để kết luận.

Bản hiện tại là tổng hợp định tính ban đầu, chưa phải báo cáo thử nghiệm usability hoặc đánh giá độ chính xác AI. Không suy rộng kết quả của hai người thành đặc điểm chung của toàn bộ sinh viên Luật.
