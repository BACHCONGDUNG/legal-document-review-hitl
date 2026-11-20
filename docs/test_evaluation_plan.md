# Kế hoạch kiểm thử và đánh giá

**Học phần và nhóm:** 2627I_INT2041_1 — Nhóm 6

**Phiên bản:** Bản khung bổ sung

**Trạng thái:** Tập hợp yêu cầu kiểm chứng đã có trong tài liệu HCI; phương pháp, fixture, metric/ngưỡng và cách tổ chức chi tiết còn chờ owner đề xuất.

## 1. Mục đích và phạm vi

Tài liệu tập hợp kiểm thử chức năng, kiểm tra module/điểm nối/toàn luồng, đánh giá kỹ thuật và đánh giá người dùng. Căn cứ là [SRS](srs.md) mục 7, [BRD](brd.md) mục 10, [Implementation Plan HCI](implementation-plan-hci.md), [Data Guide](data-annotation-guide-hci.md), [User Research](user-research.md) và [Module Owner Decisions](module-owner-decisions-hci.md).

Bài toán dùng V1, S và tham chiếu được cung cấp. S chứa chỉ dẫn sửa đổi; không bắt buộc dựng V2 đầy đủ. Kết quả phải có nguồn, giữ giới hạn, không coi truy xuất rỗng/lỗi AI là không thay đổi.

Nam chủ trì đánh giá kỹ thuật theo D-11/HCI-12; Dũng chủ trì đánh giá người dùng theo D-12/HCI-14; Đức Anh chủ trì kiểm thử tích hợp theo HCI-13. Dũng tổng hợp kế hoạch và báo cáo đánh giá chung; Nam phụ trách phần kỹ thuật, Dũng phụ trách phần người dùng, Đức Anh chủ trì kiểm thử tích hợp. Công cụ evaluator trong cây Architecture vẫn là mục tiêu của phần kỹ thuật, chưa xác nhận đã hoàn thiện.

## 2. Quan hệ với các tài liệu khác

| Tài liệu | Nội dung sở hữu | Cách phối hợp |
| --- | --- | --- |
| module-owner-decisions-hci.md | Danh sách duy nhất các lựa chọn, owner, đề xuất và kết luận | D-11 phần kỹ thuật; D-12 phần người dùng; các D-ID khác cung cấp contract/phương án cần kiểm chứng |
| module.md | Trách nhiệm, file mục tiêu, input/output, điểm nối và bàn giao | Owner cung cấp lệnh/kết quả/giới hạn; bên nhận chạy lại |
| workflow.md | Quy trình phối hợp, tự kiểm tra, review, tích hợp và quy định Git | Không thay trách nhiệm đánh giá kỹ thuật/người dùng bằng review code |
| SRS | FR-01–FR-12, contract HCI, trạng thái và AT-01–AT-13 | Fixture và kết quả mong đợi phải phản ánh đúng yêu cầu |
| Data Guide | Nguồn, gold/nhãn, bằng chứng, review và split | Tách nhãn pháp lý với dữ liệu nghiên cứu và nhận xét người dùng |
| User Research và BRD | Nhu cầu, RQ/BG, dự kiến tác vụ và giới hạn nghiên cứu | Định hướng thử nghiệm, không coi giả định thiết kế là kết quả đã quan sát |

Tên thống nhất là test_evaluation_plan.md; đã có bản khung, đang hoàn thiện. Nội dung được bổ sung theo quyết định của owner và contract/fixture đã review, không tự xác nhận các phép đo hoặc test đã chạy.

## 3. Cách hoàn thiện theo tiến độ

| Giai đoạn theo kế hoạch HCI | Nội dung cần chuẩn bị/kiểm tra | Điều kiện chuyển bước |
| --- | --- | --- |
| G1 — Nền tảng và fixture | Nguồn/đáp án, contract và dữ liệu mẫu cho các bên | D-01/D-02 đủ rõ để ghép dữ liệu; người nhận chạy được mẫu |
| G2 — Phát triển và tích hợp | Kiểm tra từng module/điểm nối, luồng file thật và cảnh báo | Đầu ra đúng contract; phần chưa làm hoặc thiếu căn cứ được thể hiện |
| G3 — Kiểm thử kỹ thuật | Kiểm tra AT trọng tâm, chất lượng phân tích và phiên bản dùng thử | Có kết quả/giới hạn; không còn lỗi chặn tác vụ; Dũng chạy lại được |
| G4 — Dùng thử và cải tiến | Thu kết quả tác vụ, ý kiến, phân loại vấn đề và kiểm tra lại | Kết quả gắn phiên bản; owner sửa phần mình; tác vụ bị ảnh hưởng được kiểm tra/thử lại |
| G5 — Bàn giao | Đối chiếu bản chạy, báo cáo, slide, dữ liệu và minh chứng | Chạy lại được; số liệu và giới hạn khớp phiên bản |

Lịch tuần 6–14 là lịch mục tiêu trong kế hoạch gốc, không xác nhận tiến độ thực tế. Không suy tuần đã hoàn thành. D-03/D-04/D-05/D-07 có thể thử riêng bằng fixture; D-06/D-10 và D-11/D-12 cần rõ trước đánh giá độc lập hoặc thu dữ liệu người dùng.

## 4. Trách nhiệm và điều phối

| Phạm vi | Chủ trì theo tài liệu HCI | Phối hợp/review |
| --- | --- | --- |
| Chuyển đổi, Parser và nguồn/adapter | Dũng | Đức Anh nhận dữ liệu; Nam/Tùng Dương dùng nguồn; D-02 |
| Linker, context, dịch vụ retrieval và backend | Đức Anh | Dũng review chỉ dẫn/nguồn; Nam nhận trước–sau/context; D-01/D-03/D-04 |
| Text Diff, Semantic Diff, AI Adapter và Scorer | Nam | Đức Anh cung cấp/tổng hợp; Dũng review nhãn; Tùng Dương kiểm tra hiển thị; D-05/D-06 |
| Frontend, nhận xét và đối chiếu lượt | Tùng Dương | Đức Anh cung cấp report/ID/nguồn; Dũng/Nam review; D-07/D-08 |
| Kiểm thử tích hợp và bản dùng thử | Đức Anh | Chủ module sửa lỗi; Dũng tiếp nhận bản chạy; HCI-13 |
| Nhãn/dữ liệu và đáp án tác vụ | Dũng | Nam review; Đức Anh/Tùng Dương dùng fixture; D-10 |
| Đánh giá kỹ thuật và công cụ đo | Nam | Dũng review gold; Đức Anh/Tùng Dương cung cấp kết quả; D-11 |
| Đánh giá người dùng và cải tiến | Dũng | Tùng Dương thiết kế; Nam chuẩn bị đáp án; Đức Anh bàn giao bản chạy; D-12 |
| Môi trường tái lập và đóng gói | Đức Anh | Mỗi owner cung cấp dependency/lệnh; Dũng xác nhận máy dùng thử; D-13 |
| Sở hữu/tổng hợp kế hoạch chung | Chưa quyết định | D-11/D-12 đã có chủ trì riêng |

Người gán và người review nhãn, người thực hiện từng ca, người tham gia thử nghiệm và lịch thực tế còn cần điền theo mẫu đã chốt. Không xem vai trò phối hợp là đã hoàn thành review.

## 5. Phân biệt các loại kiểm chứng

| Loại | Nội dung theo tài liệu HCI | Bằng chứng cần bàn giao |
| --- | --- | --- |
| Module | Kiểm tra đầu vào/nguồn, thuật toán, output và lỗi của phần được giao | Ví dụ, expected/actual, cấu hình/lệnh và giới hạn |
| Điểm nối | Kiểm tra contract và khả năng bên nhận dùng dữ liệu | Fixture được hai bên thử, schema và dữ liệu nguồn |
| Toàn luồng | File thật → báo cáo/nguồn → nhận xét, bổ sung và phân tích lại | Phiên bản chạy, AT tương ứng, lỗi và kết quả kiểm tra lại |
| Kỹ thuật phân tích | Liên kết, nhận định/aspects, bằng chứng, mức tác động và phần chưa xác định | Phép đo theo D-11, gold đã review, ca tính tay và phân tích lỗi |
| Người dùng | Tìm/hiểu thay đổi, kiểm chứng AI, nhận biết giới hạn, lưu và tiếp tục rà soát | Kết quả tác vụ, thời gian, lỗi, SUS/phản hồi theo D-12 và phiên bản |

Chất lượng AI và hiệu quả giao diện là hai phép đánh giá khác nhau. Không suy từ mức hài lòng thành độ đúng pháp lý, hoặc từ output đúng thành người dùng hiểu đúng. Kiểm tra schema/quote cũng không tự chứng minh diễn giải AI đúng.

## 6. Danh mục kiểm tra ban đầu

Giữ mã AT hiện có trong SRS; không tạo thêm danh mục yêu cầu thay thế. Bảng chỉ tập hợp phạm vi và bên liên quan; chưa xác nhận test đã chạy hoặc đã đạt.

| Mã nguồn | Phạm vi kiểm tra | Yêu cầu cốt lõi | Bên liên quan theo chức năng |
| --- | --- | --- | --- |
| AT-01 | Đầu vào DOCX/PDF text và lỗi | Định dạng/scan/thiếu file báo đúng; không trả thành công giả | Dũng, Đức Anh, Tùng Dương |
| AT-02 | S nhiều chỉ dẫn/nhiều văn bản | Giữ chỉ dẫn, đúng đích/phạm vi; không coi phần không nhắc đến bị xóa | Dũng, Đức Anh |
| AT-03 | Bổ sung/bãi bỏ/chưa rõ | ABSENT khác UNRESOLVED; Text Diff không tô từ dữ liệu thiếu | Đức Anh, Nam |
| AT-04 | Bốn nhóm và sửa diễn đạt | Đủ aspects/nguồn; không ép false/LOW khi chưa rõ | Nam, Dũng |
| AT-05 | Đổi số/gộp–tách/đích mơ hồ | Giữ nguồn/cảnh báo; không ép ghép cấu trúc một–một | Đức Anh, Nam |
| AT-06 | Đọc bằng chứng/cảnh báo | Đúng file/quote/vị trí; cảnh báo có chữ và không mất khi lọc | Dũng, Đức Anh, Tùng Dương |
| AT-07 | Nhận xét và lọc/đếm | Ba decision, trạng thái độc lập với AI, đếm cùng đơn vị | Tùng Dương, Đức Anh |
| AT-08 | Thiếu rồi bổ sung tham chiếu | PARTIAL ban đầu, ID lượt mới, nhận xét bị ảnh hưởng cần kiểm tra lại | Đức Anh, Tùng Dương, Nam |
| AT-09 | Chia/gộp mục giữa hai lượt | Không gắn nhầm; nhận xét cũ giữ riêng, không đếm vào mục hiện tại | Tùng Dương, Đức Anh; Dũng/Nam review |
| AT-10 | Lỗi AI/timeout/phân tích lại lỗi | Giữ nguồn/kết quả có ích và báo cáo/nhận xét cũ; không gửi lặp | Nam, Đức Anh, Tùng Dương |
| AT-11 | Ngoài phạm vi/hiệu lực | Giữ phạm vi và căn cứ; không hiển thị thành không thay đổi | Đức Anh, Nam; Dũng review |
| AT-12 | Retrieval/index/dịch vụ lỗi | Đợi có giới hạn, nguồn đối chiếu được; lỗi không tự là thiếu tài liệu | Đức Anh, Nam; Dũng review nguồn |
| AT-13 | Hai bộ tài liệu và cleanup | Không lẫn nguồn; dọn đúng bộ khi tác vụ kết thúc | Đức Anh; Dũng/Nam/Tùng Dương phối hợp phần bị ảnh hưởng |

Tại mỗi điểm nối, người nhận đầu ra chạy kiểm tra và thông báo kết quả; owner cung cấp vẫn phải tự kiểm tra và phối hợp review cách sử dụng dữ liệu. Ghi tên người chạy/bên review theo ca cụ thể khi triển khai. Nơi lưu kết quả chung còn chờ thống nhất; không thay trách nhiệm hai bên bằng việc báo đã chạy.

Các tác vụ người dùng theo BG-01–BG-07 ở BRD gồm tìm/giải thích thay đổi, kiểm chứng gợi ý AI, hiểu cảnh báo, ghi nhận/tiếp tục rà soát, bổ sung tài liệu và hiểu mức tác động. D-12 cần biến các mục tiêu này thành tác vụ, đáp án, biểu mẫu và tiêu chí cụ thể.

## 7. Mẫu hoàn thiện từng ca kiểm tra

Các thông tin cần tập hợp từ yêu cầu bàn giao trong D-ID và kế hoạch HCI:

- AT/FR/BG hoặc D-ID được kiểm tra; module/điểm nối và mục đích.
- Người thực hiện, bên nhận/reviewer; phần chưa quyết định được ghi rõ.
- File/fixture, nguồn, bộ tham chiếu thực sự cung cấp và đáp án đã review.
- Phiên bản code, cấu hình, dependency/model khi có và lệnh/bước chạy.
- Expected/actual; nguồn xác nhận; phần chưa xử lý hoặc chưa đủ căn cứ.
- Lỗi/giới hạn, người sửa và kết quả kiểm tra lại theo phạm vi ảnh hưởng.

Với tác vụ người dùng, bổ sung nhóm người tham gia, tác vụ/câu hỏi, cách chấm, thời gian/lỗi/phản hồi và phiên bản giao diện. Mẫu biểu chính thức chờ D-11/D-12, không tự thêm kết quả, thông số hoặc xác nhận review.

## 8. Dữ liệu nhãn và đánh giá chất lượng

### 8.1. Chuẩn bị dữ liệu

Dũng chủ trì D-10; Nam review đáp án/nhãn. Giữ manifest, nguồn/hash, vai trò, lineage, bộ tham chiếu và giới hạn theo Data Guide. Các biến thể cùng nguồn/chuỗi sửa đổi ở cùng split; mẫu giả định/biến đổi có đánh dấu và không đại diện tự động cho mẫu thực tế.

Gold dùng các nhận định và ChangeAspect theo tám nhóm phân tích trong SRS. Dữ liệu nhận xét HCI, V2 đối chiếu và gợi ý sai có kiểm soát được lưu riêng khỏi đầu vào đánh giá AI theo D-10.

Nghiên cứu hiện có mới tổng hợp trao đổi với hai sinh viên vừa vào năm 3; chưa là thử nghiệm sản phẩm. Những khoảng trống về bước khó nhất, cách kiểm tra phiên bản, hiểu cảnh báo và hành vi sau phân tích lại vẫn giữ đúng giới hạn trong User Research.

### 8.2. Phép đo cần đề xuất và chốt

| Phạm vi | Căn cứ đã có | Nội dung chưa quyết định | Chủ trì đề xuất |
| --- | --- | --- | --- |
| Chất lượng kỹ thuật | BRD mục 10.2; D-11 | Metric/công thức, matching SemanticChange/aspects, ca thiếu/sai aspect, nguồn sai, null/không mẫu và ngưỡng | Nam; Dũng review gold |
| Nhãn/mức tác động | SRS/Data Guide; D-06 | Rubric pilot, ca ranh giới, chia/gộp item, dữ liệu/đáp án cuối | Nam; Dũng review |
| Đúng tác vụ người dùng | BRD BG-01–BG-07; D-12 | Tác vụ, đáp án, cách chấm hoàn thành đúng và lỗi diễn giải | Dũng; Nam/Tùng Dương phối hợp |
| Thời gian và phản hồi | BRD mục 10.1; D-12 | Cách ghi thời gian, SUS, biểu mẫu/phản hồi và cách tổng hợp | Dũng |
| Kiểm chứng gợi ý AI | BG-03/BG-04; D-10/D-12 | Mẫu gợi ý sai kiểm soát, tiêu chí nhận ra sai hoặc thiếu căn cứ | Dũng; Nam chuẩn bị đáp án |
| Giới hạn vận hành | D-09/D-13 | Dung lượng, đồng thời, deadline, retry, số đo tài nguyên và môi trường | Đức Anh; owner cung cấp số đo |

Chưa đặt số ngưỡng chất lượng kỹ thuật hoặc quy tắc matching thay Nam. Không áp đặt một kiểu ghép đánh giá trước D-11. Ghép dự đoán–gold để đo khác với ghép nhận xét qua các lượt ở D-08 và khác liên kết cấu trúc ở D-03.

BRD dự kiến khoảng 5–10 sinh viên Luật; đây là quy mô dự kiến, không xác nhận đã tuyển hoặc dùng thử. Hai người trao đổi ban đầu chưa được tính như đã thử sản phẩm. Quy mô, điều kiện người tham gia và cách thực hiện phải được Dũng hoàn thiện theo D-12 trước thu kết quả.

### 8.3. So sánh phương pháp

D-05 yêu cầu so sánh trên cùng mẫu, giữ cấu hình/model/output và giới hạn. Phương án so sánh cụ thể chưa quyết định; không tự đặt một baseline kỹ thuật mới.

BRD cho phép so sánh giao diện đối chiếu cơ bản với giao diện có thêm giải thích/bằng chứng trên cùng đầu ra cố định và tác vụ tương đương. Đây là phương án có thể thực hiện, chưa là thiết kế thử nghiệm đã chốt. D-12 xác định cách so sánh và tiêu chí, tách đầu ra thử nghiệm cố định với kết quả chạy thật.

Báo cáo số mẫu, giới hạn, trường hợp thiếu căn cứ và chỉ số không tính được. Không khái quát mẫu nhỏ cho toàn bộ sinh viên Luật hoặc lấy tăng đồng ý/tin tưởng AI làm mục tiêu thay độ đúng và khả năng kiểm chứng.

## 9. Điều kiện bàn giao và báo cáo

Bản dùng thử cần commit/phiên bản, kết quả AT trọng tâm, dữ liệu/đáp án đã review, giới hạn và cấu hình; không còn lỗi chặn tác vụ, Dũng chạy lại được. Phương pháp, quy tắc và tiêu chí được cố định trước thu kết quả. Nhãn/dữ liệu nghiên cứu và nhận xét trong sản phẩm được quản lý riêng.

Nam bàn giao phương pháp, công cụ và kết quả kỹ thuật; Dũng tổng hợp báo cáo đánh giá người dùng và vấn đề; Tùng Dương giữ minh chứng thiết kế/cải tiến; Đức Anh chuẩn bị bản chạy và môi trường. Mỗi owner tự cung cấp mô tả/lệnh/kết quả/giới hạn của phần mình.

Dũng tổng hợp báo cáo đánh giá chung từ phần kỹ thuật của Nam, phần người dùng do Dũng chủ trì và kết quả kiểm thử tích hợp do Đức Anh điều phối. Tên file, vị trí và định dạng báo cáo/kết quả: **chưa quyết định**; không tạo định dạng runtime mới thay nhóm. Sau cải tiến, kiểm tra/thử lại tác vụ bị ảnh hưởng và nêu đúng phiên bản trước/sau.

## 10. Việc cần bổ sung sau đề xuất owner

| Việc cần bổ sung | Người chủ trì có căn cứ | Phụ thuộc |
| --- | --- | --- |
| Owner tổng hợp kế hoạch và báo cáo đánh giá chung | Dũng | D-11 và D-12 có chủ trì riêng; cần phân biệt với Dũng tổng hợp báo cáo dự án |
| Contract API/schema và fixture | Đức Anh phụ trách schema; Dũng + Đức Anh cùng biên soạn api-contract.md | D-01, phối hợp D-02/D-06/D-07/D-08 |
| Native/adapter, nguồn, Unicode và mapping PDF | Dũng | D-02; Đức Anh/Tùng Dương nhận |
| Chỉ dẫn/đích và trước–sau | Đức Anh | D-03, nguồn từ D-02 |
| Retrieval và vòng đời | Đức Anh | D-04, phối hợp D-05/D-09/D-13 |
| AI/prompt/validation/fallback và rubric | Nam | D-05/D-06; Dũng review nguồn/nhãn |
| Giao diện, cơ chế giữ/đọc bằng chứng và đối chiếu nhận xét | Tùng Dương | D-07/D-08; API từ Đức Anh, nguồn từ Dũng theo D-01/D-02 |
| Dữ liệu/gold, mẫu tác vụ và split | Dũng | D-10; Nam review |
| Metric, matching, ca tính tay và ngưỡng kỹ thuật | Nam | D-11; dữ liệu/nhãn đã review |
| Người tham gia, tác vụ, đáp án, SUS/phản hồi | Dũng | D-12; phối hợp Nam/Tùng Dương, bản chạy từ Đức Anh |
| Môi trường, tài nguyên và khả năng chạy lại | Đức Anh quyết định chính D-13; Dũng + Đức Anh cùng biên soạn development-guide.md | D-09/D-13; số đo/lệnh của owner |
| Người chạy/reviewer từng ca và nơi lưu kết quả | Người nhận đầu ra chạy và thông báo; owner cung cấp tự kiểm tra và phối hợp review | Ghi tên theo ca; nơi lưu kết quả chung còn chờ thống nhất |


Tất cả D-01–D-13 vẫn giữ trạng thái chờ owner như register nguồn, trừ khi có đề xuất và xác nhận thực tế. Việc bổ sung kế hoạch này không tự xác nhận đã có API contract, development guide, công cụ đo hoặc kết quả người dùng.
