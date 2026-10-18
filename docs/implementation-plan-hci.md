# Kế hoạch triển khai dự án HCI

**Học phần và nhóm:** 2627I_INT2041_1 Nhóm 6  
**Đề tài:** Hệ thống hỗ trợ đối chiếu thay đổi văn bản pháp luật với AI có giải thích và có sự kiểm chứng của người dùng  
**Nhóm trưởng:** Bạch Công Dũng  
**Thành viên:** Bạch Công Dũng, Dương Đức Anh, Lê Tùng Dương, Vương Thành Nam  
**Phiên bản:** HCI 1.1.0  
**Ngày cập nhật:** 17/10/2026  
**Thời gian:** Tuần 6–14 của học phần; hoàn thành nội bộ cuối tuần 13, tuần 14 dành cho dự phòng và bàn giao theo lịch học phần.  
**Tài liệu liên quan:** [BRD](brd.md), [SRS](srs.md), [Architecture](architecture.md), [Nghiên cứu người dùng](user-research.md), [Hướng dẫn dữ liệu và gán nhãn](data-annotation-guide.md).

Kế hoạch xác định người chịu trách nhiệm, thứ tự triển khai, đầu ra và điểm bàn giao. Mỗi thành viên dùng tài liệu chuyên trách để triển khai yêu cầu; các mốc dưới đây là kế hoạch, không xác nhận chức năng đã hoàn thành.

## 1. Phân công thành viên

### 1.1. Bạch Công Dũng

**Phụ trách nền tảng tài liệu, dữ liệu và xử lý đầu vào; tổ chức nghiên cứu và đánh giá sản phẩm với người dùng.**

Giai đoạn chuẩn bị:

- Hoàn thiện tài liệu tổng quát, kế hoạch, phân công; tổng hợp nghiên cứu người dùng, persona, kịch bản và tác vụ làm căn cứ thiết kế.
- Thu thập V1, S và tài liệu tham chiếu; kiểm tra quan hệ sửa đổi, trạng thái nền, nguồn và chất lượng file; quản lý manifest và hướng dẫn nhãn.
- Xây dựng module nhận DOCX/PDF có lớp chữ, chuyển PDF sang DOCX và kiểm tra chất lượng chuyển đổi. Giữ bản gốc, liên hệ giữa file gốc và file chuyển đổi; báo rõ phần không bảo đảm chất lượng.
- Đọc DOCX, giữ thứ tự đoạn/bảng và vị trí nguồn; tách Điều/Khoản/Điểm của V1. Với S và tài liệu tham chiếu, bàn giao nội dung đọc được cùng vị trí nguồn cho bước xử lý tiếp theo.
- Chuẩn bị mẫu và đáp án tham chiếu ban đầu, phối hợp Nam review phần ngữ nghĩa/mức tác động; chuẩn bị tác vụ và đáp án kiểm chứng.
- Bàn giao mã nguồn xử lý đầu vào, dữ liệu mẫu, hướng dẫn chạy, hợp đồng đầu ra và giới hạn để các thành viên sử dụng độc lập.

Sau khi sản phẩm vượt qua kiểm thử kỹ thuật: hoàn thiện tác vụ theo bản chạy thật; tổ chức dùng thử, thu thập ý kiến và kết quả tác vụ; tổng hợp số liệu, phân tích vấn đề, đề xuất cải tiến và hoàn thiện báo cáo đánh giá. Trong giai đoạn phát triển, Dũng duy trì điều phối và sửa lỗi thuộc dữ liệu/module đầu vào đã bàn giao.

### 1.2. Dương Đức Anh

**Phụ trách backend, xử lý chỉ dẫn sửa đổi và tích hợp các module thành luồng phân tích hoàn chỉnh.**

- Xây dựng API, schema và Pipeline; tích hợp module chuẩn bị đầu vào, phân tích và frontend.
- Xử lý chỉ dẫn trong S, xác định văn bản/vị trí đích và thao tác sửa đổi; giữ quan hệ đổi số/gộp–tách và phần liên kết chưa chắc chắn.
- Chuẩn bị nội dung trước–sau cục bộ, ngữ cảnh, thông tin hiệu lực/chuyển tiếp và yêu cầu tài liệu tham chiếu cho phân tích.
- Tổng hợp báo cáo có bằng chứng, cảnh báo và phần chưa xác định; hiện thực bổ sung tài liệu/phân tích lại, cung cấp dữ liệu đối chiếu lượt chạy.
- Kiểm thử backend và tích hợp, quản lý cấu hình, tài nguyên/file tạm và đóng gói môi trường chạy.

### 1.3. Lê Tùng Dương

**Phụ trách thiết kế tương tác và frontend; xây dựng giao diện đối chiếu, kiểm chứng và quản lý nhận xét trong phiên.**

- Phát triển wireframe, prototype và luồng thao tác từ nghiên cứu, kịch bản và tác vụ đã thống nhất.
- Xây dựng giao diện chọn file, theo dõi xử lý, đối chiếu trước–sau, xem giải thích, truy nguồn, lọc và thông báo lỗi.
- Hiện thực nhận xét, ghi chú, tổng hợp trạng thái rà soát và quản lý dữ liệu trong phiên.
- Xử lý trạng thái sau phân tích lại: mục mới, mục cần kiểm tra lại và nhận xét cũ chưa đối chiếu được.
- Kiểm thử giao diện/tích hợp API; sửa vấn đề giao diện từ đánh giá người dùng và lưu minh chứng thay đổi thiết kế.

### 1.4. Vương Thành Nam

**Phụ trách so sánh và phân tích thay đổi; bảo đảm chất lượng diễn giải, bằng chứng và mức tác động.**

- Triển khai, tích hợp và hiệu chỉnh Text Diff, Semantic Diff, AI Adapter và Scorer trên dữ liệu trước–sau/ngữ cảnh được bàn giao.
- Tạo các khía cạnh, giải thích và mức tác động có căn cứ; giữ kết quả chưa xác định cùng lý do.
- Kiểm tra cấu trúc phản hồi AI, trích dẫn và tính phù hợp của giải thích với nguồn.
- Phối hợp Dũng review nhãn, đáp án và ca đúng/sai/thiếu căn cứ phục vụ kiểm thử, kiểm chứng AI.
- Xây dựng công cụ đánh giá kỹ thuật, chạy phép đo và phân tích lỗi; tổng hợp giới hạn, sửa lỗi thuộc module phụ trách.

## 2. Giai đoạn và mốc hoàn thành

### 2.1. Đầu ra và điều kiện hoàn thành

| Mốc | Trọng tâm và đầu ra | Điều kiện chuyển bước |
| --- | --- | --- |
| G1 — Chuẩn bị và bàn giao nền tảng | Tài liệu đủ triển khai; hợp đồng/fixture thống nhất; bộ nguồn, DOCX chuẩn hóa, cấu trúc V1 và module đầu vào; kịch bản/tác vụ ban đầu | Đức Anh chạy được đầu ra của Dũng; Nam có mẫu và đáp án thử phân tích; Tùng Dương có kịch bản và báo cáo mẫu để thiết kế |
| G2 — Phát triển song song và tích hợp | Backend, phân tích, prototype/frontend; luồng tải file → xem nguồn → ghi nhận xét; bổ sung tài liệu và phân tích lại | Có luồng chạy trên file thật; đầu ra chưa xử lý được có cảnh báo; các module bàn giao đúng hợp đồng |
| G3 — Kiểm thử kỹ thuật | Kết quả kiểm thử module, đầu-cuối và chất lượng phân tích; phiên bản ổn định, cấu hình, bộ mẫu và giới hạn | Các ca nghiệm thu trọng tâm đã có kết quả; không còn lỗi chặn tác vụ dùng thử; Dũng chạy lại được phiên bản bàn giao |
| G4 — Dùng thử và cải tiến | Dũng tổ chức thử nghiệm, thu thập ý kiến và tổng hợp vấn đề; chủ module sửa phần được giao | Có kết quả gắn với phiên bản; các cải tiến được kiểm tra lại, thử lại tác vụ bị ảnh hưởng khi cần; còn hạn chế thì ghi rõ |
| G5 — Hoàn thiện và bàn giao | Bản chạy cuối, hướng dẫn, dữ liệu mẫu, kết quả kiểm thử/đánh giá, báo cáo, slide và minh chứng đóng góp | Chạy được theo hướng dẫn; nội dung trình bày khớp phiên bản, số liệu và giới hạn công bố |

Sau khi thống nhất hợp đồng và fixture, các thành viên có thể phát triển bằng dữ liệu mẫu trong G1. Dũng tập trung chuẩn bị đầu vào và bàn giao ở G1; trong G2–G3 hỗ trợ phần mình sở hữu; ở G4 chủ trì đánh giá người dùng. Đức Anh điều phối kỹ thuật G2–G3; Tùng Dương và Nam tự kiểm tra phần phụ trách trước tích hợp.

### 2.2. Kế hoạch theo tuần

Tuần được tính theo lịch học phần. Hạn hoàn thành nội bộ là **cuối tuần 13**, bao gồm sản phẩm, đánh giá người dùng, cải tiến và hồ sơ bàn giao. **Tuần 14 là thời gian dự phòng**, không phải thời điểm bắt đầu đánh giá người dùng; lịch nộp và bảo vệ thực hiện theo thông báo của giảng viên.

| Tuần | Mốc | Công việc và người phụ trách | Đầu ra cần bàn giao |
| --- | --- | --- | --- |
| 6 | G1 | Dũng chốt tài liệu, bộ nguồn mẫu và triển khai chuyển đổi/Reader; Đức Anh chốt hợp đồng và fixture với các bên; Tùng Dương dựng prototype; Nam review nhãn và thử phương pháp phân tích trên fixture | Phạm vi triển khai, schema/fixture và bộ nguồn mẫu có thể dùng để phát triển song song |
| 7 | G1 | Dũng hoàn thiện chuyển đổi, Reader DOCX, cấu trúc V1 và đáp án ban đầu; Đức Anh kiểm tra tiếp nhận đầu ra; Nam review đáp án; Tùng Dương hoàn thiện prototype theo tác vụ | Cuối tuần 7: module đầu vào và dữ liệu bàn giao được; người nhận chạy được mẫu; prototype được review |
| 8 | G2 | Đức Anh triển khai chỉ dẫn S, liên kết đích và trước–sau cục bộ; Nam phát triển diff/AI/scorer; Tùng Dương phát triển frontend theo fixture; Dũng sửa lỗi đầu vào khi phát hiện | Đầu ra HCI-07 trên mẫu thật; các module có bản chạy ban đầu và bắt đầu nối luồng tích hợp |
| 9 | G2 | Đức Anh tích hợp API/Pipeline; Nam bàn giao phân tích có bằng chứng; Tùng Dương nối giao diện với API và trạng thái phiên | Cuối tuần 9: chạy đầu-cuối trên dữ liệu thật, gồm xem nguồn, nhận xét, thiếu tài liệu và phân tích lại |
| 10 | G3 | Đức Anh chủ trì kiểm thử tích hợp; Nam hoàn tất đánh giá kỹ thuật; từng chủ module sửa lỗi; Dũng nhận bản dùng thử, chốt tác vụ/chỉ số và sắp lịch người dùng | Cuối tuần 10: bản dùng thử ổn định, không còn lỗi chặn tác vụ; Dũng chạy lại được và sẵn sàng tổ chức đánh giá |
| 11 | G4 | Dũng tổ chức dùng thử, thu thập kết quả tác vụ và phản hồi; các chủ module hỗ trợ xử lý sự cố thuộc phần mình | Kết quả gắn với phiên bản, tổng hợp vấn đề và thứ tự ưu tiên cải tiến |
| 12 | G4 | Dũng phân công và theo dõi cải tiến; Đức Anh, Tùng Dương, Nam và Dũng sửa module tương ứng; Dũng tổ chức kiểm tra/thử lại tác vụ bị ảnh hưởng | Cuối tuần 12: bản cải tiến được kiểm tra lại, số liệu và minh chứng trước–sau, báo cáo đánh giá người dùng |
| 13 | G5 | Đức Anh đóng gói bản chạy; Tùng Dương và Nam hoàn tất minh chứng phần mình; Dũng tổng hợp báo cáo, hướng dẫn, dữ liệu, slide; cả nhóm chạy thử và tập trình bày | Cuối tuần 13: bộ sản phẩm bàn giao nội bộ hoàn chỉnh, đã bao gồm kết quả kiểm thử và đánh giá người dùng |
| 14 | Dự phòng và bàn giao | Cả nhóm xử lý lỗi còn lại theo chủ module, kiểm tra lại bản sửa và nộp/bảo vệ theo lịch học phần | Bản bàn giao chính thức, tài liệu và số liệu thống nhất với phiên bản cuối |

Cuối mỗi tuần, chủ task cập nhật đầu ra, vấn đề và khả năng đáp ứng hạn; Dũng tổng hợp tiến độ, Đức Anh rà soát phụ thuộc kỹ thuật. Nếu có nguy cơ trễ, nhóm ưu tiên luồng và tác vụ nghiệm thu chính, điều chỉnh phần mở rộng và ghi rõ thay đổi. Không đưa bản còn lỗi chặn tác vụ vào đánh giá người dùng chỉ để giữ lịch; mọi điều chỉnh phải bảo vệ thời gian đánh giá, cải tiến và kiểm tra lại trước bàn giao.

## 3. Danh mục công việc và phụ thuộc

Mỗi task có một người chủ trì. Phụ thuộc là điều kiện dùng đầu ra thật; fixture là dữ liệu đầu vào–đầu ra mẫu để phát triển trước khi phần phụ thuộc hoàn thành. Hạn trong bảng là thời điểm bàn giao và được bên nhận kiểm tra; công việc có thể bắt đầu sớm trên fixture. HCI-04 bàn giao mẫu Reader từ đầu tuần 7 để HCI-05 triển khai nối tiếp; HCI-09 và HCI-11 tích hợp dần trong tuần 8–9, không đợi đến hạn cuối mới nối module. Tài liệu và dữ liệu được duy trì khi có thay đổi sau lần bàn giao đầu tiên.

| Mã | Công việc | Chủ trì | Đầu ra | Phụ thuộc để hoàn thành | Mốc | Hạn hoàn thành |
| --- | --- | --- | --- | --- | --- | --- |
| HCI-01 | Tài liệu và kế hoạch | Dũng | Phạm vi, trách nhiệm và mốc bàn giao rõ | Chủ module review phần liên quan | G1 | Cuối tuần 6 |
| HCI-02 | Hợp đồng và fixture | Đức Anh | Mẫu dữ liệu đầu vào, phân tích, báo cáo, lỗi và nguồn | HCI-01; các bên cung cấp/nhận cùng thử | G1 | Cuối tuần 6 |
| HCI-03 | Nguồn dữ liệu và manifest | Dũng | Bộ V1–S/tham chiếu có nguồn và giới hạn | HCI-01 | G1 | Mẫu ban đầu cuối tuần 6; bộ bàn giao cuối tuần 7 |
| HCI-04 | Chuyển đổi và đọc tài liệu | Dũng | PDF → DOCX; Reader DOCX, nguồn và lỗi chuyển đổi | HCI-02, HCI-03 | G1 | Giữa tuần 7 |
| HCI-05 | Cấu trúc V1 | Dũng | Điều/Khoản/Điểm, bảng, nội dung ngoài Điều và cảnh báo | HCI-04 | G1 | Cuối tuần 7 |
| HCI-06 | Nhãn và đáp án ban đầu | Dũng | Nhãn được review, ca đủ/thiếu căn cứ và tác vụ ban đầu | HCI-03; Nam review phân tích, Dũng đối chiếu nguồn | G1 | Cuối tuần 7 |
| HCI-07 | Chỉ dẫn, liên kết và ngữ cảnh | Đức Anh | Đích, thao tác, trước–sau, ngữ cảnh, tham chiếu/hiệu lực | HCI-02, HCI-04, HCI-05 | G2 | Cuối tuần 8 |
| HCI-08 | Diff, AI Adapter và Scorer | Nam | Phân tích có bằng chứng, mức tác động và cảnh báo | HCI-02, HCI-07; dùng HCI-06 để kiểm tra | G2 | Giữa tuần 9 |
| HCI-09 | API, Pipeline và báo cáo | Đức Anh | Luồng backend, nguồn, lỗi và lượt phân tích lại | HCI-02, HCI-04, HCI-05, HCI-07, HCI-08 | G2 | Cuối tuần 9 |
| HCI-10 | Prototype và luồng thao tác | Tùng Dương | Prototype được review theo tác vụ | HCI-01, HCI-02; kịch bản từ Dũng | G1–G2 | Cuối tuần 7 |
| HCI-11 | Frontend và quản lý phiên | Tùng Dương | Giao diện, nhận xét, trạng thái sau phân tích lại | HCI-10; HCI-09 để tích hợp thật | G2 | Cuối tuần 9 |
| HCI-12 | Đánh giá kỹ thuật phân tích | Nam | Công cụ đo, kết quả, lỗi và giới hạn | HCI-06, HCI-08; quy tắc đo đã thống nhất | G2–G3 | Giữa tuần 10 |
| HCI-13 | Kiểm thử và bản dùng thử | Đức Anh | Kết quả đầu-cuối và gói chạy ổn định | HCI-09, HCI-11, HCI-12; chủ module sửa lỗi | G3 | Cuối tuần 10 |
| HCI-14 | Dùng thử và thu thập ý kiến | Dũng | Kết quả tác vụ, phản hồi và báo cáo vấn đề | HCI-06, HCI-13; tác vụ cập nhật theo bản chạy | G4 | Cuối tuần 11 |
| HCI-15 | Cải tiến và kiểm tra lại | Dũng | Danh sách cải tiến được giao, minh chứng sửa và kết quả kiểm tra lại | HCI-14; mỗi chủ module thực hiện phần được giao | G4 | Cuối tuần 12 |
| HCI-16 | Hoàn thiện sản phẩm bàn giao | Dũng | Bộ sản phẩm, báo cáo và minh chứng đóng góp | HCI-15; từng thành viên bàn giao phần mình, Đức Anh đóng gói bản chạy | G5 | Cuối tuần 13 |

## 4. Phối hợp và bàn giao

| Điểm phối hợp | Thành viên | Quyết định cần thống nhất | Minh chứng bàn giao |
| --- | --- | --- | --- |
| DOCX và vị trí nguồn | Dũng + Đức Anh | Hợp đồng đầu ra Reader; cách giữ đoạn/bảng, nhận diện file gốc/file chuyển đổi và truy nguồn; khi nào phải dừng vì chuyển đổi không bảo đảm | Cả PDF và DOCX đi qua cùng luồng DOCX; vị trí nguồn mở đúng; lỗi không trở thành nội dung rỗng thành công |
| Cấu trúc V1 và chỉ dẫn S | Dũng + Đức Anh | Dũng tách V1; Đức Anh xử lý chỉ dẫn S. Thống nhất cấu trúc lồng nhau, nhãn đặc biệt, phần chưa rõ và truy xuất nội dung | Một mẫu cấu trúc V1 cùng chỉ dẫn sửa đổi được Đức Anh dùng xác định đúng đích |
| Đầu vào ngữ nghĩa | Đức Anh + Nam | Phạm vi trước–sau, nội dung trích/suy ra, ngữ cảnh cần dùng, tham chiếu còn thiếu và cảnh báo | Nam chạy được fixture và mẫu thật; không phải suy đoán trường còn thiếu |
| Nhãn và đáp án | Dũng + Nam | Ranh giới nhận định/khía cạnh, bằng chứng, rubric và cách ghi chưa đủ căn cứ; ánh xạ nhãn sang kết quả trình bày | Bộ nhãn có review, ca ranh giới và đáp án phù hợp bộ căn cứ được cung cấp |
| Prototype và tác vụ | Dũng + Tùng Dương | Luồng kiểm chứng, nội dung cần đọc, cách mở nguồn và thao tác nhận xét | Prototype thực hiện được kịch bản; vấn đề review có người sửa |
| Báo cáo và trạng thái phiên | Đức Anh + Tùng Dương | Fixture API, truy nguồn, lỗi, định danh mục và đối chiếu lượt chạy; giữ nhận xét khi kết quả thay đổi/không ghép được | Ca thành công, thiếu tài liệu, phân tích lại và thất bại hiển thị đúng; không gắn nhầm nhận xét |
| Nội dung phân tích trên giao diện | Nam + Tùng Dương | Cách trình bày nhiều khía cạnh, câu giải thích, bằng chứng và phần chưa rõ | Một kết quả có nhiều khía cạnh/cảnh báo được hiển thị đủ, truy đúng nguồn |
| Bản dùng thử | Đức Anh + Nam + Tùng Dương bàn giao cho Dũng | Phiên bản, cấu hình, bộ mẫu, kết quả kỹ thuật và giới hạn; tách đầu ra thử nghiệm cố định với kết quả chạy thực tế | Dũng chạy lại được tác vụ; phiên bản và dữ liệu dùng thử được ghi nhận |

Chốt hợp đồng ở HCI-02 phải bao gồm cách chuẩn hóa DOCX, ranh giới xử lý cấu trúc và cách đưa nhãn phân tích lên giao diện. Các mô tả chưa thống nhất trong SRS, Architecture hoặc hướng dẫn dữ liệu phải được cập nhật trước khi tích hợp task liên quan; hợp đồng đã chốt và fixture là căn cứ thực hiện.

Thống nhất cụ thể cách truy bằng chứng từ PDF gốc sau chuyển đổi; không gán số trang PDF theo thứ tự đoạn DOCX hoặc sao chép vị trí giữa hai định dạng khi chưa xác minh. Phương pháp hiện thực thuộc chủ module, các trường dữ liệu chung do bên giao/bên nhận chốt với Đức Anh.

## 5. Điều kiện hoàn thành và quản lý thay đổi

**Hoàn thành task:** có đầu ra theo bảng công việc, ví dụ/kiểm tra phù hợp, hướng dẫn sử dụng và giới hạn; người nhận chạy được phần được bàn giao. Mỗi người tự viết mô tả, lệnh chạy và kết quả kiểm thử của module mình. Dũng tổng hợp tài liệu chung.

**Sẵn sàng dùng thử:** có bản chạy gắn commit/phiên bản, kết quả các ca nghiệm thu trọng tâm, dữ liệu/đáp án đã review và giới hạn đã biết; không còn lỗi chặn tác vụ. Phương pháp, chỉ số và quy mô thử nghiệm được xác định trong kế hoạch đánh giá trước khi thu thập kết quả. Nhận xét người dùng được lưu riêng với nhãn tham chiếu và kết quả AI.

**Xử lý vấn đề:** người phát hiện ghi đầu vào, phiên bản, kết quả mong đợi/thực tế và minh chứng. Dũng phân loại, theo dõi các vấn đề từ dùng thử; chủ module sửa lỗi của mình. Lỗi liên module do Đức Anh phối hợp xác định ranh giới; thay đổi thiết kế do Tùng Dương thực hiện, lỗi phân tích do Nam xử lý, lỗi nguồn/chuyển đổi/cấu trúc V1 do Dũng xử lý. Bản sửa được kiểm tra lại theo tác động, kết quả đánh giá ghi rõ phiên bản trước/sau.

**Thay đổi hợp đồng hoặc kế hoạch:** bên cung cấp và bên nhận thử trên một mẫu cụ thể, ghi quyết định, người sửa và ảnh hưởng. Đức Anh quản lý schema/fixture chung; Dũng cập nhật phạm vi, phân công và mốc với người liên quan. Đổi nội bộ do chủ module quyết định và kiểm tra; đổi giao diện bàn giao phải cập nhật tài liệu và bên nhận trước tích hợp. Quy tắc nhãn thay đổi phải rà lại mẫu chịu ảnh hưởng cùng Nam.

**Bàn giao cuối:** mã nguồn, cấu hình/dependency, hướng dẫn chạy, dữ liệu mẫu có nguồn, tài liệu thiết kế, kết quả kiểm thử/đánh giá, báo cáo, slide và minh chứng đóng góp thực tế. Đức Anh chuẩn bị gói chạy; Tùng Dương bàn giao thiết kế và minh chứng giao diện; Nam bàn giao phương pháp/kết quả kỹ thuật; Dũng tổng hợp dữ liệu, nghiên cứu người dùng và báo cáo chung. Bộ sản phẩm phải chạy lại được và truy được số liệu về đúng phiên bản.
