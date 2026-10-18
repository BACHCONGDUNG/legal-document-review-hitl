# BRD — Hệ thống hỗ trợ đối chiếu thay đổi văn bản pháp luật

**Dự án:** Legal Document Change Detection  
**Học phần và nhóm:** 2627I_INT2041_1 Nhóm 6  
**Thành viên:** Bạch Công Dũng, Dương Đức Anh, Lê Tùng Dương, Vương Thành Nam  
**Phiên bản tài liệu:** HCI 1.0.0  
**Ngày cập nhật:** 15/10/2026   
**Phạm vi phiên bản đầu:** Phân tích văn bản quy phạm pháp luật tiếng Việt ban đầu (V1) và văn bản sửa đổi (S), kèm tài liệu tham chiếu do người dùng cung cấp khi cần.

## 1. Mục đích tài liệu

BRD mô tả vấn đề nghiệp vụ, người sử dụng, giá trị mong đợi, phạm vi, yêu cầu nghiệp vụ và tiêu chí đánh giá của hệ thống. Tài liệu tập trung vào sinh viên Luật cần hiểu và kiểm chứng thay đổi phục vụ học tập hoặc nghiên cứu.

BRD là căn cứ để nhóm xây dựng yêu cầu phần mềm trong SRS và lựa chọn thiết kế trong Architecture. Các cấu trúc dữ liệu, endpoint API, thư viện, mô hình và thuật toán được quy định trong các tài liệu kỹ thuật tương ứng.

Căn cứ người dùng ban đầu là kết quả trao đổi với hai sinh viên vừa vào năm 3 và tra cứu trên mạng xã hội, được tổng hợp trong [Nghiên cứu người dùng](user-research.md). Người dùng mô tả cách đọc S, quay lại phần liên quan trong V1, đối chiếu trước–sau và tìm tài liệu dẫn chiếu theo tên/số hiệu. Họ dùng kết quả tự phân tích để đối chiếu AI nhưng chưa nêu tiêu chí kiểm chứng cụ thể. Các chức năng kiểm chứng, trạng thái rà soát và cảnh báo dưới đây là đề xuất của nhóm theo định hướng học phần; hiệu quả cần được đánh giá, không mặc định đã được hai người xác nhận.

## 2. Bối cảnh và vấn đề nghiệp vụ

Khi nghiên cứu hoặc thực hiện công việc pháp lý, người dùng cần đối chiếu yêu cầu trong văn bản sửa đổi với nội dung tương ứng của văn bản ban đầu. Họ cần biết những quy định nào được thêm, xóa hoặc sửa; sự thay đổi có ảnh hưởng đến nội dung quy định hay chỉ là thay đổi cách diễn đạt; và những nội dung nào cần được kiểm tra trước.

Ngoài cách làm đã ghi nhận, nhóm xác định các vấn đề thiết kế cần xử lý và kiểm tra qua thử nghiệm:

- Văn bản có thể dài và nhiều nội dung liên quan; cần hỗ trợ truy lại nguồn và xem ngữ cảnh để kiểm tra nhận định.
- Một thay đổi ngắn như từ phủ định, đối tượng áp dụng, thời hạn hoặc điều kiện có thể làm thay đổi đáng kể nội dung quy định.
- Hệ thống phải theo đúng chỉ dẫn sửa đổi trong S, thể hiện phần nội dung thay đổi và phân biệt trường hợp chỉ đổi cách diễn đạt hoặc số thứ tự.
- Chỉ liệt kê phần chữ thay đổi chưa đủ để người dùng hiểu nội dung pháp lý nào cần chú ý.
- Người dùng cần kiểm chứng kết quả bằng đoạn trích cũ, đoạn trích mới và vị trí trong tài liệu gốc.
- Một số thay đổi cần kiến thức hoặc văn bản liên quan ngoài hai tài liệu đầu vào để kết luận; hệ thống phải thể hiện sự chưa chắc chắn.

**Ví dụ giả định:** Nếu thời hạn đổi từ “30 ngày” thành “15 ngày”, người dùng cần nhận biết thời hạn được rút ngắn, xác định hoạt động, chủ thể, cách tính và điều kiện liên quan từ nguồn. Không suy ra dụng ý của cơ quan ban hành hoặc toàn bộ tác động pháp lý chỉ từ việc thay con số.

Hệ thống được xây dựng để hỗ trợ tìm kiếm, đối chiếu và ưu tiên rà soát các thay đổi. Người dùng tiếp tục chịu trách nhiệm kiểm tra văn bản nguồn và đưa ra kết luận cho công việc của mình.

## 3. Người dùng và các bên liên quan

### 3.1. Sinh viên Luật — nhóm người dùng chính

**Công việc cần hỗ trợ:** Đối chiếu văn bản gốc và chỉ dẫn sửa đổi để giải thích thay đổi phục vụ bài tập hoặc nghiên cứu, đồng thời kiểm tra nhận định bằng nguồn.

**Nhu cầu có căn cứ ban đầu từ trao đổi:**

1. Đọc S, tìm phần V1 bị tác động và xem nội dung trước–sau để hình thành nhận xét.
2. Nắm mục đích chính của V1, tập trung phần sửa và đọc thêm ngữ cảnh liên quan khi cần.
3. Tìm văn bản dẫn chiếu theo tên/số hiệu và đọc phần liên quan.
4. Đối chiếu gợi ý AI với kết quả tự phân tích.

**Nhu cầu hỗ trợ do nhóm đề xuất:** Truy cập bằng chứng thuận tiện; biết căn cứ còn thiếu; ghi nhận đồng ý, không đồng ý hoặc chưa đủ căn cứ; theo dõi phần đã kiểm tra và kiểm tra lại khi kết quả cập nhật. Các đề xuất này cần được đánh giá trong thiết kế tương tác và thử nghiệm usability.

**Giá trị mong đợi:** Người dùng mô tả đúng thay đổi cụ thể, chỉ ra bằng chứng, nhận ra giới hạn và quản lý được việc rà soát trong phiên. Chưa khẳng định giảm thời gian hoặc giảm lỗi trước khi đo.

### 3.2. Luật sư và người làm pháp chế — nhóm tham vấn nếu tiếp cận được

Nhóm có thể tham vấn người có chuyên môn về ví dụ, cách diễn giải, bằng chứng và nhãn mức tác động. Họ không phải nhóm người dùng chính của thử nghiệm HCI trong phiên bản này. Việc trao đổi với hai sinh viên không thay thế việc review chuyên môn pháp luật và không được coi là đại diện cho nhu cầu hành nghề.

### 3.3. Các bên liên quan khác

| Bên liên quan | Vai trò |
| --- | --- |
| Nhóm phát triển | Hiện thực yêu cầu, kiểm thử và ghi nhận giới hạn của hệ thống. |
| Giảng viên hướng dẫn | Góp ý phạm vi, cách đánh giá và mức độ phù hợp với mục tiêu môn học. |
| Người rà soát có chuyên môn pháp luật | Khi có điều kiện tham gia: góp ý ví dụ, hướng dẫn gán nhãn, tiêu chí mức độ và các trường hợp bất đồng. |
| Người gán nhãn và đánh giá | Lập đáp án tham chiếu theo hướng dẫn chung, đối chiếu kết quả và ghi nhận sai sót. |

Việc liệt kê vai trò không có nghĩa dự án đã tuyển được người tham gia tương ứng. Nhóm cần ghi nhận nguồn lực thực tế trong kế hoạch triển khai.

## 4. Mục tiêu nghiệp vụ

| Mã | Mục tiêu | Biểu hiện mong đợi ở người dùng |
| --- | --- | --- |
| BG-01 | Xác định nội dung bị sửa | Tìm đúng phần liên quan trong V1 từ chỉ dẫn trong S và phân biệt thêm, bãi bỏ, sửa nội dung. |
| BG-02 | Hiểu thay đổi cụ thể | Diễn đạt được nội dung trước–sau thuộc các nhóm ưu tiên, giữ đúng chủ thể, điều kiện và ngoại lệ có liên quan. |
| BG-03 | Kiểm chứng gợi ý AI | Chỉ ra nguồn hỗ trợ hoặc mâu thuẫn với nhận định; không chỉ lặp lại nhãn của AI. |
| BG-04 | Nhận biết giới hạn | Phân biệt liên kết không chắc chắn, thiếu căn cứ và phần chưa xử lý; biết khi nào chưa thể kết luận. |
| BG-05 | Ghi nhận và tiếp tục rà soát | Biết mục nào đã kiểm tra, nhận xét của mình là gì và mục nào cần xem lại trong phiên. |
| BG-06 | Bổ sung căn cứ và kiểm tra lại | Hiểu tài liệu cần bổ sung, cung cấp được tài liệu phù hợp và nhận biết kết quả thay đổi sau phân tích lại. |
| BG-07 | Ưu tiên kiểm tra có căn cứ | Hiểu mức tác động và lý do khi có, sử dụng để chọn mục xem trước mà không coi đó là kết luận pháp lý cuối cùng. |

## 5. Phạm vi nghiệp vụ

### 5.1. Đầu vào

- Bản đầu xử lý một cặp V1–S mỗi lượt; chưa tự động phân tích toàn bộ chuỗi nhiều văn bản sửa đổi theo thời gian. V1 cần phản ánh nội dung trước lần sửa đang xét; thiếu sửa đổi trước có liên quan phải được ghi rõ.
- Hai tài liệu chính: văn bản ban đầu (V1) và văn bản sửa đổi (S) có nội dung tác động đến V1. S không phải bản đầy đủ sau sửa đổi (V2).
- DOCX là định dạng chính; hỗ trợ PDF có lớp văn bản đọc được. Không hỗ trợ PDF scan/ảnh.
- Người dùng cung cấp tài liệu tham chiếu bổ sung khi việc phân tích cần nội dung ngoài V1 và S; có thể tải ngay từ đầu hoặc bổ sung theo yêu cầu cụ thể của hệ thống.
- Người dùng chịu trách nhiệm chọn đúng văn bản gốc, văn bản sửa đổi, phiên bản tài liệu tham chiếu và kiểm tra nguồn tài liệu.
- Hệ thống kiểm tra khả năng đọc và sự phù hợp của tài liệu với nội dung được dẫn chiếu trong giới hạn hỗ trợ; không mặc định xác minh được tính chính thức, tính đầy đủ hoặc hiệu lực pháp lý thực tế.

### 5.2. Đơn vị đối chiếu

Đơn vị phân tích là từng yêu cầu sửa đổi, bổ sung hoặc bãi bỏ trong S, liên kết với đúng văn bản và Điều/Khoản/Điểm hoặc cụm từ bị tác động trong V1. Số Điều trong S không phải số Điều đích trong V1.

Một Điều của S có thể chứa nhiều yêu cầu; một Điều của V1 có thể chịu nhiều thay đổi. Không ghép toàn bộ hai văn bản theo quy tắc một–một và không xem phần V1 không được nhắc đến trong S là bị xóa.

Phân tích tập trung vào phần thay đổi, sử dụng thông tin tổng quát của V1 về phạm vi, đối tượng và mục đích điều chỉnh cùng ngữ cảnh liên quan như định nghĩa, điều kiện, ngoại lệ. Không bắt buộc dựng V2 đầy đủ hoặc phân tích ngữ nghĩa từng đoạn không thay đổi.

### 5.3. Đầu ra

- Danh sách yêu cầu sửa đổi, bổ sung, bãi bỏ và vị trí bị tác động trong V1.
- Nội dung trước thay đổi, nội dung hoặc chỉ dẫn sửa đổi trong S và phần chữ khác biệt khi xác định được.
- Nhận định về thay đổi nội dung quy định, nhóm nội dung thay đổi, mức độ và lý do khi có đủ căn cứ.
- Bằng chứng và vị trí nguồn trong V1, S và tài liệu tham chiếu được sử dụng.
- Thông tin hiệu lực và chuyển tiếp được nêu trong S, kèm phạm vi áp dụng và căn cứ; phần chưa xác định phải được đánh dấu.
- Danh sách tài liệu/nội dung tham chiếu còn thiếu, cảnh báo và lỗi xử lý.
- Nhận xét, ghi chú và trạng thái rà soát do người dùng ghi nhận trong phiên, tách riêng khỏi đầu ra AI.

### 5.4. Phạm vi bao phủ

Hệ thống xử lý những yêu cầu trong S tác động đến V1 được chọn, cùng thông tin hiệu lực và chuyển tiếp liên quan. Yêu cầu sửa văn bản khác phải được phân biệt và ghi rõ nằm ngoài đối tượng phân tích.

Phần mở đầu, chữ ký và phụ lục không được so sánh toàn diện trong phiên bản đầu. Nội dung đọc được ở các phần này, bao gồm bảng được dẫn chiếu, có thể làm ngữ cảnh hoặc bằng chứng. Nội dung không xử lý được phải được báo rõ; không mặc định suy ra toàn bộ văn bản không thay đổi.

## 6. Tình huống sử dụng

### 6.1. UC-01 — Sinh viên tìm hiểu một thay đổi

**Mục đích:** Hiểu nội dung trước–sau và xác định bằng chứng liên quan.

**Điều kiện:** Người dùng có V1 và S phù hợp, đọc được.

1. Người dùng chọn V1, S và tài liệu tham chiếu nếu có.
2. Hệ thống trình bày thông tin tổng quát, danh sách chỉ dẫn tác động đến V1 và phạm vi xử lý.
3. Người dùng chọn một thay đổi, xem nội dung gốc, chỉ dẫn/nội dung sửa đổi và ngữ cảnh liên quan.
4. Người dùng đọc gợi ý phân tích, mở nguồn và diễn đạt thay đổi bằng lời của mình.

**Kết quả mong đợi:** Xác định đúng nội dung thay đổi và dẫn được nguồn. Nếu xử lý một phần thì biết phần còn thiếu; nếu thất bại thì có lý do rõ, không nhận danh sách rỗng như kết luận không thay đổi.

### 6.2. UC-02 — Kiểm chứng AI và ghi nhận nhận xét

**Mục đích:** Đối chiếu gợi ý với nguồn và quản lý kết quả rà soát trong phiên.

1. Người dùng xem nhận định cụ thể và bằng chứng của AI.
2. Người dùng đối chiếu với nội dung tự phân tích, đọc thêm ngữ cảnh khi cần.
3. Người dùng ghi nhận đồng ý, không đồng ý hoặc chưa đủ căn cứ, kèm ghi chú nếu muốn.
4. Hệ thống giữ nhận xét riêng với kết quả AI và thể hiện trạng thái rà soát.
5. Người dùng xem tổng hợp, lọc các mục chưa kiểm tra hoặc cần xem lại để tiếp tục.

**Kết quả mong đợi:** Người dùng biết mình đã kiểm tra những gì và có nhận xét nào. Không đồng ý không tự sửa đầu ra AI; đồng ý không có nghĩa kết quả đã được xác nhận đúng về pháp luật. Phản hồi không tự huấn luyện lại mô hình trong phiên bản đầu.

### 6.3. UC-03 — Bổ sung căn cứ và kiểm tra kết quả cập nhật

**Mục đích:** Tiếp tục phân tích khi thiếu tài liệu dẫn chiếu cần thiết.

1. Hệ thống trình bày kết quả đã có cùng tài liệu/phần nội dung còn thiếu, lý do và nhận định bị ảnh hưởng.
2. Người dùng tìm tài liệu theo tên/số hiệu, bổ sung và chủ động yêu cầu phân tích lại.
3. Hệ thống cho biết kết quả nào được cập nhật và còn thiếu căn cứ nào.
4. Người dùng kiểm tra lại phần cập nhật. Nhận xét cũ gắn với kết quả đã thay đổi được đánh dấu cần kiểm tra lại, không tự coi là xác nhận cho kết quả mới.

**Ngoại lệ:** Nếu không bổ sung hoặc tài liệu mới không đáp ứng, kết quả đã xác định vẫn được giữ cùng giới hạn. Liên kết chưa chắc chắn được trình bày với lý do; bản đầu không bắt buộc cho người dùng sửa trực tiếp liên kết.

## 7. Yêu cầu nghiệp vụ

Tất cả yêu cầu trong bảng là yêu cầu của phiên bản đầu trong phạm vi đã nêu. Mức độ tự động hóa thực tế phải được đánh giá bằng kiểm thử.

| Mã | Yêu cầu | Điều kiện đáp ứng từ góc nhìn người dùng |
| --- | --- | --- |
| BR-01 | Phân biệt vai trò tài liệu | Người dùng nhận diện rõ V1, S và tài liệu tham chiếu; S không được trình bày như bản V2 đầy đủ. |
| BR-02 | Liên kết yêu cầu sửa đổi với nội dung gốc | Báo cáo chỉ rõ văn bản và Điều/Khoản/Điểm bị tác động; liên kết chưa chắc chắn có cảnh báo. |
| BR-03 | Nhận biết thêm, xóa và sửa | Người dùng phân biệt được nội dung được bổ sung, bãi bỏ và sửa đổi. |
| BR-04 | Hiển thị khác biệt văn bản | Người dùng thấy đoạn chữ thay đổi trong tiêu đề hoặc nội dung, cùng ngữ cảnh của Điều. |
| BR-05 | Phân biệt thay đổi ý nghĩa và cách diễn đạt | Nhận định có lý do; thiếu căn cứ thì đánh dấu chưa chắc chắn, không suy ra không đổi nghĩa chỉ vì thiếu từ khóa. |
| BR-06 | Mô tả các nội dung quy định bị thay đổi | Khi có căn cứ trong đầu vào, báo cáo chỉ ra thay đổi liên quan đến bốn nhóm ưu tiên: thời hạn; giá trị định lượng; điều kiện/ngoại lệ; chủ thể và quyền/nghĩa vụ. |
| BR-07 | Giữ bằng chứng và vị trí nguồn | Người dùng đọc được bằng chứng trong V1, chỉ dẫn sửa đổi trong S và tài liệu tham chiếu nếu sử dụng; phân biệt nội dung nguồn với nội dung sau sửa đổi được suy ra. |
| BR-08 | Phân loại mức độ và giải thích | Mức độ được gắn với từng thay đổi được nhận diện, có lý do và theo tiêu chí chung; không chỉ dựa vào số chữ đổi. |
| BR-09 | Biểu diễn nhiều thay đổi trong cùng Điều | Một Điều có thể có nhiều nhận định riêng; không ép toàn bộ nội dung thành một thay đổi duy nhất. |
| BR-10 | Thể hiện nhu cầu kiểm tra của con người | Cảnh báo cho biết điều gì chưa chắc chắn và vì sao; người dùng vẫn xem được bằng chứng có sẵn. |
| BR-11 | Thể hiện trạng thái và phạm vi xử lý | Người dùng phân biệt kết quả xử lý đầy đủ, một phần và thất bại, đồng thời biết phần bị ảnh hưởng. |
| BR-12 | Dùng ngôn ngữ dễ hiểu | Giải thích tập trung vào nội dung cũ/mới và tác động trực tiếp được suy ra từ các tài liệu được cung cấp; tránh kết luận rộng hơn bằng chứng. |
| BR-13 | Bảo vệ nội dung tài liệu đầu vào | Nội dung không được công khai hoặc ghi toàn văn vào log vận hành; việc xử lý tệp tạm tuân theo chính sách được mô tả trong tài liệu kỹ thuật. |
| BR-14 | Bổ sung tài liệu tham chiếu | Hệ thống chỉ rõ căn cứ còn thiếu; người dùng có thể tải bổ sung. Thiếu tài liệu chỉ giới hạn nhận định bị ảnh hưởng, không che mất kết quả khác. |
| BR-15 | Thể hiện hiệu lực và chuyển tiếp | Báo cáo giữ nội dung, phạm vi áp dụng và nguồn của thông tin hiệu lực/chuyển tiếp trong S; chưa đủ căn cứ thì không tự áp một thời điểm cho mọi thay đổi. |
| BR-16 | Ghi nhận nhận xét trong phiên | Người dùng lưu đồng ý, không đồng ý hoặc chưa đủ căn cứ và ghi chú; kết quả AI không bị ghi đè. |
| BR-17 | Theo dõi trạng thái rà soát | Phân biệt chưa kiểm tra, đã kiểm tra và cần kiểm tra lại với nhận xét và trạng thái chắc chắn của AI. |
| BR-18 | Rà soát sau cập nhật | Nhận biết phần kết quả thay đổi sau bổ sung; xác nhận cũ không tự áp dụng cho nội dung đã đổi. |
| BR-19 | Xem tổng hợp việc kiểm tra | Xem và lọc các mục theo trạng thái để tiếp tục rà soát trong phiên. |


## 8. Quy tắc nghiệp vụ

### 8.1. Thay đổi văn bản và thay đổi ý nghĩa

Khác biệt về ký tự chưa đồng nghĩa với thay đổi nội dung quy định. Ngược lại, thay đổi ít ký tự vẫn có thể ảnh hưởng đáng kể đến quyền, nghĩa vụ hoặc điều kiện.

- **Thay đổi cách diễn đạt:** Có khác biệt câu chữ nhưng nội dung quy định được đánh giá là không thay đổi, với căn cứ đủ để giải thích.
- **Thay đổi ý nghĩa:** Có thay đổi nội dung quy định thể hiện trong văn bản gốc, văn bản sửa đổi và tài liệu tham chiếu được cung cấp, chẳng hạn chủ thể, quyền, nghĩa vụ, điều kiện hoặc thời hạn.
- **Chưa xác định:** Chưa đủ căn cứ để phân biệt hai trường hợp trên. Hệ thống phải ghi nhận nhu cầu kiểm tra thay vì mặc định là thay đổi cách diễn đạt.

### 8.2. Nhóm nội dung ưu tiên

| Nhóm | Nội dung người dùng cần hiểu và kiểm chứng |
| --- | --- |
| Thời hạn | Khoảng thời gian, mốc tính, hoạt động chịu thời hạn và điều kiện liên quan thay đổi thế nào? |
| Giá trị định lượng | Số tiền, tỷ lệ, số lượng hoặc ngưỡng cùng đơn vị và phạm vi áp dụng thay đổi thế nào? |
| Điều kiện và ngoại lệ | Trường hợp áp dụng, miễn trừ hoặc ngoại lệ được thêm, bỏ hay sửa thế nào? |
| Chủ thể và quyền/nghĩa vụ | Ai chịu tác động; quyền, yêu cầu bắt buộc hoặc hành vi bị cấm thay đổi thế nào? |

Một thay đổi có thể thuộc nhiều nhóm. Dẫn chiếu và định nghĩa là căn cứ cần đọc khi liên quan; thay đổi dẫn chiếu không tự chứng minh tác động thực chất. Bản HCI không cam kết hiểu toàn bộ ý nghĩa pháp lý; nội dung ngoài bốn nhóm được báo giới hạn và giữ nguồn để kiểm tra. Mã nhãn và ví dụ được quy định trong SRS/hướng dẫn gán nhãn tương ứng.

### 8.3. Mức tác động và trạng thái kiểm chứng

Mức tác động hỗ trợ ưu tiên rà soát theo tiêu chí thống nhất, có lý do và bằng chứng. Nếu sử dụng LOW, MEDIUM, HIGH, CRITICAL thì ranh giới và ví dụ được quản lý trong hướng dẫn gán nhãn; không tự gán mức cao nhất chỉ vì thêm/xóa Điều hoặc đổi thời hạn. Thiếu căn cứ thì để chưa xác định, không ép thành LOW.

Phân biệt ba loại thông tin:

- **Kết quả hệ thống:** nhận định, mức tác động và lý do còn chưa chắc chắn nếu có.
- **Nhận xét người dùng:** đồng ý, không đồng ý hoặc chưa đủ căn cứ; có thể kèm ghi chú.
- **Trạng thái rà soát:** chưa kiểm tra, đã kiểm tra hoặc cần kiểm tra lại. Mục đã kiểm tra vẫn có thể mang nhận xét chưa đủ căn cứ.

Mức tác động không tự xác định quy định áp dụng cho vụ việc, mức độ thiệt hại hoặc dụng ý của cơ quan ban hành. Tự động thay đổi kết quả không được làm mất dấu nhận xét cũ hay tạo hiểu nhầm rằng người dùng đã xác nhận nội dung mới.

### 8.4. Liên kết và bao phủ kết quả

- Mỗi yêu cầu sửa đổi liên quan đến V1 phải có kết quả hoặc lý do chưa xử lý; tránh bỏ sót và tính trùng.
- Liên kết dựa trên văn bản đích, Điều/Khoản/Điểm và nội dung; không ghép theo số Điều của S với số Điều của V1.
- Với tách/gộp hoặc vị trí đích mơ hồ, yêu cầu kiểm tra; không tự khẳng định thêm hoặc bãi bỏ chỉ vì không tìm thấy đoạn tương ứng.
- Không phân tích phần thay đổi tách rời ngữ cảnh giữ nguyên có ảnh hưởng đến cách hiểu.
- Khi chỉ một phần được xử lý, báo cáo chỉ rõ phần thiếu hoặc vấn đề gặp phải.

### 8.5. Kết luận không phát hiện thay đổi

Chỉ thông báo “Không tìm thấy yêu cầu sửa đổi đối với V1 trong S đã cung cấp” khi đã xử lý đầy đủ S trong phạm vi hỗ trợ, không còn nội dung chưa xác định và không tìm thấy yêu cầu liên quan. Kết luận này không khẳng định V1 chưa từng được sửa đổi bởi văn bản khác.

Có yêu cầu sửa đổi nhưng chưa xác định tác động thì vẫn phải hiển thị yêu cầu đó. Không dùng kết quả Text Diff rỗng, lỗi hoặc thiếu tài liệu làm căn cứ kết luận không có thay đổi.

### 8.6. Dẫn chiếu, hiệu lực và căn cứ phân tích

- Khi dẫn chiếu chuyển từ nội dung A sang B, phân biệt việc xác định đổi dẫn chiếu với việc xác định tác động thực chất. Phân tích tác động trước–sau cần nội dung A và B cùng ngữ cảnh áp dụng liên quan, nếu chưa có trong đầu vào.
- Người dùng cung cấp tài liệu còn thiếu; hệ thống không tự thu thập hoặc duy trì kho văn bản pháp luật. Chỉ kết luận trong phạm vi bằng chứng có sẵn.
- Ưu tiên dẫn chiếu trực tiếp liên quan đến thay đổi; nếu còn phụ thuộc chưa được giải quyết, ghi rõ giới hạn thay vì suy luận không có căn cứ.
- Thông tin hiệu lực và chuyển tiếp được trích từ S và gắn với thay đổi khi có căn cứ. Việc trích xuất không đồng nghĩa với xác minh hiệu lực pháp lý thực tế tại mọi thời điểm.

## 9. Yêu cầu đối với báo cáo và trải nghiệm sử dụng

Một báo cáo có ích cần trả lời được các câu hỏi sau:

1. Văn bản nào là V1, văn bản nào là S và tài liệu tham chiếu nào đã được sử dụng?
2. Những Điều nào thêm, xóa hoặc sửa?
3. Nội dung trước và sau khác nhau ở đâu?
4. Hệ thống nhận định nội dung quy định đã thay đổi như thế nào, dựa trên bằng chứng nào?
5. Tôi nên ưu tiên kiểm tra những thay đổi nào và vì sao?
6. Kết quả nào chưa chắc chắn hoặc chưa được xử lý đầy đủ?
7. Phạm vi nào nằm ngoài báo cáo?
8. Thông tin hiệu lực/chuyển tiếp nào liên quan và cần bổ sung tài liệu nào?
9. Tôi đã kiểm tra mục nào, ghi nhận nhận xét gì và mục nào cần kiểm tra lại sau cập nhật?

Kết quả cần hiển thị nội dung cũ/mới cạnh nhau hoặc theo cách đối chiếu rõ ràng; phần chữ thay đổi phải dễ nhận biết. Không chỉ dùng màu sắc để truyền đạt loại thay đổi, mức độ hoặc cảnh báo.

Tóm tắt báo cáo phải nhất quán với kết quả chi tiết. Không dùng tổng số Điều thay đổi thay thế cho tổng số thay đổi nội dung quy định mà không ghi rõ đơn vị đếm.

Phiên bản đầu không bắt buộc xuất báo cáo thành PDF/DOCX, quản lý tài khoản, lưu lịch sử dài hạn hoặc cung cấp chức năng cộng tác.

## 10. Tiêu chí thành công và nghiệm thu

### 10.1. Mức độ đáp ứng công việc người dùng

Đánh giá dự kiến với khoảng 5–10 sinh viên Luật phù hợp nhóm mục tiêu, dùng tác vụ và đáp án đã rà soát. Hai người đã trao đổi ban đầu là nguồn nghiên cứu nhu cầu; chưa được tính là đã tham gia thử nghiệm sản phẩm.

| Mục tiêu | Tác vụ đánh giá | Kết quả mong đợi |
| --- | --- | --- |
| BG-01, BG-02 | Tìm và giải thích thay đổi thuộc nhóm ưu tiên | Đúng nội dung trước–sau, chủ thể/điều kiện liên quan và vị trí nguồn. |
| BG-03 | Kiểm tra một gợi ý AI | Nêu được căn cứ đồng ý/bất đồng hoặc lý do chưa đủ căn cứ; nhận ra gợi ý sai trong tác vụ có đáp án kiểm soát. |
| BG-04 | Đọc cảnh báo hoặc báo cáo một phần | Hiểu giới hạn, không nhầm chưa xác định với không thay đổi hoặc tác động thấp. |
| BG-05 | Ghi nhận và tiếp tục rà soát | Tìm lại nhận xét và phân biệt mục đã/chưa kiểm tra. |
| BG-06 | Bổ sung tài liệu và phân tích lại | Chọn được tài liệu mẫu phù hợp, nhận ra phần cập nhật và kiểm tra lại nhận xét bị ảnh hưởng. |
| BG-07 | Xem một mức tác động có lý do | Hiểu lý do ưu tiên và giới hạn của mức tác động. |

Ghi nhận tỷ lệ hoàn thành đúng, thời gian, lỗi, khả năng phát hiện/chấp nhận gợi ý sai, SUS và phản hồi định tính. Mục tiêu là hỗ trợ thực hiện tác vụ đúng và kiểm chứng có căn cứ; không đặt mục tiêu tăng niềm tin hoặc tăng tỷ lệ đồng ý với AI bằng mọi giá.

Kế hoạch usability quy định chi tiết tác vụ, tiêu chí chấm và cách so sánh giao diện. Có thể so sánh giao diện đối chiếu cơ bản với giao diện thêm giải thích/bằng chứng trên cùng đầu ra cố định và tác vụ tương đương. Quy mô nhỏ được báo rõ, không khái quát cho mọi sinh viên Luật.

### 10.2. Chất lượng thành phần xử lý

Vẫn đánh giá khả năng liên kết chỉ dẫn, phát hiện thay đổi, độ phù hợp của giải thích và bằng chứng, cảnh báo thiếu căn cứ và mức tác động khi có nhãn đủ tin cậy. Chỉ số, ngưỡng và quy tắc đối chiếu được chốt trong SRS và kế hoạch đánh giá kỹ thuật của HCI.

Mỗi chỉ tiêu kỹ thuật phải gắn với bộ dữ liệu, phạm vi nhãn và điều kiện đo đã chốt. Báo cáo phân biệt chất lượng AI với hiệu quả của giao diện, không suy từ một kết quả sang kết quả còn lại.

### 10.3. Nguyên tắc đánh giá

- Có đáp án tác vụ, hướng dẫn nhãn và cách xử lý bất đồng; tìm nguồn review chuyên môn nếu tiếp cận được và công bố giới hạn nếu chưa có.
- Tách dữ liệu phát triển khỏi kiểm thử độc lập; tính cả phát hiện sai, bỏ sót và lỗi từ các bước đầu vào/liên kết.
- Công bố số mẫu, người tham gia, trường hợp thiếu căn cứ và chỉ số không tính được; không tự quy đổi kết quả chưa xác định thành kết quả đúng.
- Đánh giá quy trình sử dụng hoàn chỉnh, không chỉ mức hài lòng hoặc chất lượng mô hình.
- Kết quả nghiên cứu nhu cầu, giả định thiết kế và bằng chứng thử nghiệm được trình bày riêng; ghi nhận cải tiến sau đánh giá.

### 10.4. Điều kiện nghiệm thu chức năng

1. Có luồng chạy hoàn chỉnh: tải V1/S → xem thay đổi → đọc nguồn và giải thích → ghi nhận nhận xét → xem tổng hợp.
2. Có ví dụ đủ bốn nhóm ưu tiên, thay đổi cách diễn đạt và thiếu căn cứ; nội dung có nguồn/nhãn tham chiếu rõ.
3. Có tình huống chỉ dẫn tới Khoản/Điểm, S sửa nhiều văn bản, đổi số/gộp–tách chưa chắc chắn; không bắt buộc tự giải quyết mọi trường hợp nhưng phải báo giới hạn.
4. Bổ sung tài liệu và phân tích lại được; kết quả thay đổi được đánh dấu cần kiểm tra lại.
5. Nhận xét người dùng, trạng thái rà soát, mức tác động và sự chưa chắc chắn không bị nhập làm một.
6. Đầu vào lỗi hoặc báo cáo một phần không được trình bày như không có thay đổi.
7. Có kết quả kiểm thử kỹ thuật, đánh giá người dùng, hướng dẫn sử dụng và giới hạn thực tế.

## 11. Ngoài phạm vi phiên bản đầu

- OCR hoặc xử lý PDF scan/ảnh không có lớp văn bản đọc được.
- So sánh hợp đồng, văn bản tiếng nước ngoài hoặc cặp văn bản không có quan hệ gốc–sửa đổi.
- Tự tái dựng phiên bản đầy đủ từ văn bản chỉ liệt kê nội dung sửa đổi, bổ sung.
- Tự động giải quyết đầy đủ mọi trường hợp tách/gộp hoặc yêu cầu sửa đổi không xác định được vị trí đích.
- So sánh toàn diện phần mở đầu, chữ ký và phụ lục; các phần đọc được vẫn có thể cung cấp ngữ cảnh hoặc bằng chứng liên quan.
- Tự tải, cập nhật hoặc duy trì kho văn bản pháp luật dùng chung.
- Tự xác minh hiệu lực, tính chính thức, tính xác thực hoặc tính đầy đủ của văn bản đầu vào.
- Tự xác định quy định áp dụng cho một vụ việc cụ thể.
- Suy luận toàn bộ tác động từ các văn bản được dẫn chiếu nhưng chưa được cung cấp.
- Cung cấp ý kiến tư vấn pháp lý cuối cùng hoặc bảo đảm không bỏ sót mọi thay đổi.
- Quản lý tài khoản, lịch sử dài hạn, cơ sở dữ liệu nghiệp vụ hoặc chức năng cộng tác; nhận xét và ghi chú trong phiên thuộc phạm vi.
- Tự động huấn luyện lại mô hình từ phản hồi của người dùng hoặc sửa trực tiếp liên kết bằng giao diện.

## 12. Giả định và phụ thuộc

1. Người dùng cung cấp đúng V1, S và tài liệu tham chiếu cần thiết trong phạm vi hỗ trợ.
2. Tài liệu có nội dung đọc được và cấu trúc đủ để nhận diện các Điều; mức độ hỗ trợ bố cục cụ thể được kiểm chứng qua bộ mẫu.
3. Nhóm có các cặp tài liệu có nguồn và quyền sử dụng phù hợp cho phát triển, gán nhãn và đánh giá.
4. Có tiêu chí phân loại được thống nhất; sự tham gia của người có chuyên môn pháp luật là nguồn lực cần tìm kiếm và xác nhận.
5. Giới hạn kích thước, độ dài, số Điều và thời gian xử lý được công bố theo thiết kế và số đo thực tế. BRD không tự đặt một cam kết hiệu năng chưa đo.
6. Cần tìm người dùng phù hợp để đánh giá; việc họ có hiểu cảnh báo và kiểm chứng được hay không là nội dung phải kiểm tra, không phải giả định đã đúng.

## 13. Rủi ro và biện pháp xử lý

| Rủi ro | Ảnh hưởng nghiệp vụ | Biện pháp |
| --- | --- | --- |
| Chọn sai V1, S hoặc phiên bản tài liệu tham chiếu | Diễn giải nhầm thêm/xóa, hiểu sai chiều thay đổi | Hiển thị rõ vai trò của các tài liệu; hướng dẫn người dùng kiểm tra trước khi xử lý. |
| Nguồn không chính thức hoặc tài liệu thiếu | Báo cáo không phản ánh đúng nội dung cần nghiên cứu | Dữ liệu đánh giá có nguồn; người dùng kiểm tra đầu vào; không coi đọc thành công là xác minh pháp lý thành công. |
| Bố cục phức tạp, bảng hoặc nhiều trang | Mất chữ, đảo thứ tự, tách Điều sai | Kiểm thử tài liệu thực tế; giữ vị trí nguồn; báo lỗi hoặc giới hạn khi nhận diện được vấn đề. |
| Đánh lại số, tách/gộp hoặc liên kết sai vị trí đích | Nhận định sai về thêm/xóa hoặc sửa | Kiểm tra nhiều tín hiệu đối chiếu; cảnh báo mơ hồ; đưa các tình huống này vào bộ kiểm thử. |
| Thiếu định nghĩa hoặc ngữ cảnh dẫn chiếu | Giải thích vượt quá căn cứ | Chỉ rõ tài liệu/nội dung cần bổ sung; cho phép tải thêm; không khẳng định tác động chưa có bằng chứng. |
| Tiêu chí mức độ không thống nhất | Các thành viên gán nhãn khác nhau, chỉ số khó tin cậy | Hướng dẫn có ví dụ ranh giới; gán nhãn chéo; ghi nhận và giải quyết bất đồng. |
| Sai hoặc bỏ sót thay đổi | Người dùng bỏ qua nội dung quan trọng | Giữ bằng chứng, cảnh báo; đánh giá đầy đủ phát hiện sai/bỏ sót; báo cáo kết quả và giới hạn thực tế. |
| Ít dữ liệu hoặc ít mẫu CRITICAL | Khó kết luận chất lượng tổng quát | Công bố số mẫu và cách chọn; không diễn giải chỉ số trên tập nhỏ thành bảo đảm rộng. |
| Người dùng tin tuyệt đối vào kết quả | Sử dụng nhận định thiếu kiểm chứng | Nhắc rõ vai trò hỗ trợ, lý do và phần chưa xác định trong báo cáo. |
| Lộ nội dung tài liệu qua log hoặc tệp tạm | Ảnh hưởng tính riêng tư của dữ liệu | Không log toàn văn; kiểm soát truy cập và vòng đời tệp tạm theo thiết kế triển khai. |

## 14. Ví dụ nghiệp vụ để xây dựng bộ kiểm thử

**Toàn bộ ví dụ trong mục này là giả định, không trích dẫn quy định pháp luật hiện hành.** Nội dung cũ lấy từ V1; nội dung mới hoặc chỉ dẫn sửa đổi lấy từ S. Mức độ cụ thể chỉ được gán sau khi đối chiếu hướng dẫn gán nhãn đã chốt.

| Mã | Nội dung cũ → mới | Điều cần kiểm tra |
| --- | --- | --- |
| EX-01 | “Trong thời hạn 30 ngày” → “Trong thời hạn 15 ngày” | Nhận biết giảm thời hạn; xác định hoạt động và chủ thể liên quan từ ngữ cảnh; không chỉ báo thay số. |
| EX-02 | “Có thể cung cấp” → “Phải cung cấp” | Nhận biết khả năng chuyển từ lựa chọn sang nghĩa vụ; đọc đầy đủ điều kiện và ngoại lệ. |
| EX-03 | “Áp dụng đối với tổ chức” → “Áp dụng đối với tổ chức và cá nhân” | Nhận biết mở rộng đối tượng; giữ đúng bằng chứng. |
| EX-04 | Một câu được viết lại nhưng nội dung được người gán nhãn xác nhận tương đương | Phát hiện khác biệt chữ và giải thích căn cứ không đổi nội dung quy định. |
| EX-05 | Điều 5 cũ thành Điều 6 mới, nội dung giữ nguyên | Nhận diện chỉ dẫn đánh lại số trong S; không tự diễn giải thành bãi bỏ và bổ sung nội dung. |
| EX-06 | Một Điều cũ được phân thành hai Điều mới | Liên kết chỉ dẫn tách/gộp với Điều gốc; cảnh báo nếu chưa xác định đủ nội dung bị tác động. |
| EX-07 | Một đoạn không đọc được hoặc một giai đoạn xử lý bị lỗi | Báo phần bị ảnh hưởng; không kết luận toàn bộ không thay đổi. |
| EX-08 | Sửa một dẫn chiếu nhưng tài liệu được dẫn chiếu không có trong đầu vào | Chỉ ra thay đổi dẫn chiếu, yêu cầu tài liệu bổ sung và giới hạn kết luận; phân tích lại khi đủ nội dung trước/sau. |

## 15. Liên kết và thống nhất tài liệu

| Tài liệu | Trách nhiệm |
| --- | --- |
| BRD HCI | Người dùng, nhu cầu, giá trị, phạm vi và quy tắc nghiệp vụ của sản phẩm HCI. |
| [Nghiên cứu người dùng](user-research.md) | Kết quả trao đổi, căn cứ nhu cầu, persona/scenario và giới hạn nghiên cứu. |
| SRS HCI | Cụ thể hóa chức năng, dữ liệu, trạng thái kiểm chứng và điều kiện kiểm tra. |
| Architecture | Module, luồng xử lý và quyết định triển khai theo phạm vi đã chốt. |
| Thiết kế tương tác | Luồng thao tác, prototype, trạng thái giao diện và lý do thiết kế. |
| Kế hoạch đánh giá usability | Tác vụ, người tham gia, cách đo và phân tích kết quả sử dụng. |
| Hướng dẫn gán nhãn và kế hoạch đánh giá kỹ thuật | Tiêu chí nhãn/mức tác động, đáp án tham chiếu, phương pháp và chỉ số kỹ thuật. |
| README | Giới thiệu, hiện trạng, cách chạy và chỉ dẫn tài liệu. |

Bộ PoCS là nền tham khảo cho xử lý V1–S. Tài liệu HCI phải ghi rõ phần kế thừa và yêu cầu bổ sung; không mặc định rằng mọi chức năng, nhóm nhãn hoặc chỉ tiêu PoCS đều áp dụng nguyên vẹn. Tên file dẫn chiếu cần khớp cấu trúc kho mã khi nhóm đưa tài liệu vào dự án.
