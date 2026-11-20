# WORKFLOW — Quy trình làm việc, Git và kiểm thử chéo

**Học phần và nhóm:** 2627I_INT2041_1 — Nhóm 6 (HCI)

**Dự án:** Hệ thống hỗ trợ đối chiếu thay đổi văn bản pháp luật với AI có giải thích và có sự kiểm chứng của người dùng

**Phiên bản:** Bản hoàn thiện quy trình HCI

**Trạng thái:** Quy trình phối hợp áp dụng cho nhóm HCI; không xác nhận cấu hình GitHub hoặc trạng thái hoàn thành của module

## 1. Mục đích và phạm vi

Tài liệu quy định cách thành viên phối hợp từ lúc chốt lựa chọn đến khi code được kiểm tra và tích hợp. Quy trình chung: **chốt → code song song → tự kiểm tra → kiểm thử lẫn nhau → sửa lỗi → tích hợp**.

| Tài liệu | Vai trò |
| --- | --- |
| module-owner-decisions-hci.md | Câu hỏi cần chốt, phương án, người tham gia và kết luận lựa chọn/hợp đồng |
| module.md | Phân công, nhiệm vụ, file chính và điểm nối của module sau khi quyết định liên quan được chốt |
| workflow.md | Cách nhận việc, code song song, dùng Git, kiểm thử chéo và đưa kết quả vào nhánh chung |

Quy trình và quy tắc Git dưới đây là cách phối hợp của nhóm. Việc ghi quy tắc không tự xác nhận GitHub đã bật branch protection hoặc CI. Yêu cầu phần mềm theo [SRS](srs.md); trách nhiệm và điểm bàn giao theo [Module](module.md), [Implementation Plan HCI](implementation-plan-hci.md) và [Module Owner Decisions](module-owner-decisions-hci.md). Khi đổi hợp đồng hoặc phân công, cập nhật tài liệu và bên bị ảnh hưởng trước tích hợp.

Theo phân công HCI: Dũng phụ trách đầu vào/Parser/adapter nguồn, dữ liệu/docs, nghiên cứu và đánh giá người dùng; Đức Anh phụ trách backend/API/Pipeline, linker, context và tích hợp/vận hành; Nam phụ trách Text Diff, Semantic Diff, AI Adapter, Scorer và đánh giá kỹ thuật; Tùng Dương phụ trách thiết kế tương tác, frontend và nhận xét trong phiên. Nam quyết định chính D-05; Đức Anh quyết định chính D-04/D-13; Tùng Dương quyết định cơ chế giữ/đọc bằng chứng theo D-07. Dũng + Đức Anh cùng biên soạn api-contract.md và development-guide.md theo D-01/D-13. Quyền lựa chọn phương pháp không thay việc phối hợp khi đổi contract hoặc môi trường chung.

## 2. Quy trình làm việc

### 2.1. Nhận task và chốt trước khi code

Mỗi task có một người chịu trách nhiệm chính. Ghi task trong issue hoặc một nơi theo dõi chung mà nhóm thống nhất; không bắt buộc tạo thêm file tài liệu riêng.

Thông tin tối thiểu của task:

- Người làm chính và người review bên kết nối.
- Chức năng/file sẽ sửa, phạm vi được phép thay đổi.
- Đầu ra cần bàn giao và điều kiện được coi là xong.
- Quyết định/hợp đồng phụ thuộc; đang chờ ai hoặc điều gì nếu có.
- Nhánh nguồn để tạo branch và nhánh đích của PR.

Trước một task phụ thuộc, bên cung cấp và bên nhận thống nhất:

1. Input/output: tên trường, kiểu, ý nghĩa, ID, nguồn/offset và trường bắt buộc/tùy chọn.
2. Tên hàm hoặc giao diện gọi; giá trị null, danh sách rỗng, lỗi và cảnh báo.
3. Một bộ input/output mẫu cùng kết quả mong đợi đã được hai bên review.
4. Phiên bản hợp đồng hoặc commit làm căn cứ, để hai bên không code theo hai bản khác nhau.

Ghi lựa chọn trong module-owner-decisions-hci.md; cập nhật module.md và schema liên quan khi đã chốt. Nếu mới có đề xuất, không tự coi đó là hợp đồng chung. Chỉ cần chốt các quyết định liên quan trực tiếp đến task để bắt đầu phần độc lập; không cần chờ toàn bộ dự án xong quyết định. D-01/D-02 cần đủ rõ trước ghép dữ liệu; có thể thử riêng D-03/D-04/D-05/D-07 bằng fixture. D-06/D-10 và D-11/D-12 phải rõ trước khóa nhãn hoặc đánh giá. LightRAG HTTP vẫn là phương án tạm chọn theo tài liệu HCI; không xem đề xuất hoặc file khung là tích hợp đã hoàn thành.

### 2.2. Code song song bằng dữ liệu mẫu

- Bên cung cấp hiện thực để trả đúng hợp đồng đã chốt.
- Bên nhận sử dụng fixture/mock cùng hợp đồng để code ngay, không đợi bên cung cấp hoàn thiện toàn module.
- JSON có thể dùng lưu mẫu; các module trong cùng backend có thể gọi hàm với object/dict. Không bắt mọi điểm nối ghi file hoặc gọi HTTP.
- Mock phải có nhãn rõ, nằm ở phần phát triển/kiểm thử phù hợp. Không dùng kết quả mock để tuyên bố đã tích hợp với module thật.
- Khi giao AI assistant làm task, cung cấp cùng phiên bản quyết định, đặc tả module và dữ liệu mẫu. Không để AI tự thêm trường/đổi contract để code chạy được.

Ví dụ: Đức Anh và Nam chốt dữ liệu trước/sau cục bộ, chỉ dẫn/đích, ID, nguồn và cảnh báo. Nam triển khai phân tích với fixture đó trong khi Đức Anh hoàn thiện linker/context. Dũng đồng thời bàn giao nguồn/adapter theo hợp đồng với Đức Anh; Tùng Dương làm giao diện bằng fixture báo cáo. Chỉ có cây Parser chưa đủ thay cho đầu vào phân tích; mẫu phải bao phủ đúng điểm nối đang sử dụng.

### 2.3. Tự kiểm tra trước khi bàn giao

Người làm tự đọc diff và kiểm tra phần mình trước khi đề nghị bên khác review. Cần có lệnh chạy, dữ liệu mẫu, kết quả thực tế và giới hạn còn lại. Phần chưa hiện thực phải báo rõ; không trả thành công giả hoặc dùng mảng rỗng để che lỗi.

### 2.4. Kiểm thử chéo và tích hợp

Khi có output thật, hai owner chạy theo mục 4. Sau khi sửa lỗi và đạt điều kiện bàn giao, mở/hoàn thiện PR vào nhánh chung. Có thể mở draft PR sớm để cùng review nhưng chưa merge như phần đã hoàn thành.

Không đợi mọi module xong mới thử ghép: tích hợp từng điểm nối có dữ liệu thật và chạy lại phần bị ảnh hưởng. Đức Anh điều phối tích hợp/API và kiểm tra toàn luồng; owner sửa phần mình. Nam phụ trách đánh giá kỹ thuật, Dũng chủ trì đánh giá người dùng sau khi có bản chạy đủ điều kiện.

### 2.5. Khi cần thay đổi hoặc bị chặn

| Tình huống | Cách xử lý |
| --- | --- |
| Đổi thuật toán nội bộ, không ảnh hưởng contract/dependency chung | Người phụ trách chủ động triển khai, tự kiểm tra và báo trong PR |
| Đổi trường, kiểu, ý nghĩa, nguồn/offset hoặc giao diện công khai | Báo bên cung cấp/nhận; thống nhất decision trước, rồi cập nhật schema, mẫu và code phụ thuộc |
| Đổi dependency/cấu hình ảnh hưởng môi trường chung | Phối hợp Đức Anh và owner liên quan trước tích hợp; cấu hình mô hình thuộc D-05 do Nam quyết định chính, ảnh hưởng phạm vi/nguồn lực cần trao đổi với Dũng |
| Chưa có output thật | Tiếp tục phần độc lập bằng fixture/mock; ghi đang chờ gì, chưa đánh dấu đã tích hợp |
| Hợp đồng chưa rõ | Đưa ví dụ cụ thể vào decision, không để hai bên tự chọn cách hiểu riêng |
| Cần sửa file thuộc người khác | Thống nhất phạm vi với owner hoặc mở PR để owner review; không tự sửa hợp đồng ngầm |

## 3. Giới hạn thay đổi và quy định Git

### 3.1. Phạm vi được tự sửa

- Giữ folder chính và file bắt buộc theo cấu trúc đã chốt; không tự xóa, đổi tên hoặc chuyển vị trí.
- Được sửa implementation và thêm file hỗ trợ trong phần việc mình, theo nhiệm vụ đã giao. Không tạo module/folder chính mới hoặc buộc module khác import helper nội bộ khi chưa thống nhất.
- Không tự đổi schema chung, kết quả của người khác hoặc nội dung quyết định đã chốt. Mọi thay đổi ảnh hưởng bên nhận cần phối hợp theo mục 2.5.
- Không ghi đè implementation bằng file khung. Khi lấy code từ branch khác, kiểm tra hợp đồng và dependency trước, không mặc định code đó đã tương thích.

### 3.2. Nhánh chung và việc tạo branch

Nhánh tích hợp chung là `main`. Tạo nhánh công việc từ `main` đã cập nhật và mở PR về `main`. Nếu một task cần dựa trên thay đổi chưa merge của người khác, ghi rõ nhánh/commit phụ thuộc và thứ tự tích hợp; không tự biến nhánh công việc thành nhánh chung mới. Cấu trúc mục tiêu theo Architecture HCI, không ghi đè implementation bằng cây thư mục khung.

- Tạo branch từ nhánh tích hợp đã cập nhật, theo một task/phạm vi cụ thể.
- Không tự lập nhánh chung mới hoặc tạo branch không rõ mục đích. Thành viên tạo branch công việc theo quy ước cho task đã nhận; không cần xin lại quyền bắt đầu từng buổi làm việc.
- Không tạo branch mới chỉ vì đổi máy hoặc bắt đầu buổi làm việc mới. Task đang làm tiếp tục dùng branch hiện có.
- Branch cũ chỉ đóng/đổi tên sau khi phối hợp người liên quan; không viết lại lịch sử cũ chỉ để đổi cách đặt tên.
- Không code trực tiếp trên nhánh chung, không push trực tiếp hoặc force push vào nhánh chung. Đưa thay đổi vào bằng PR.

### 3.3. Đặt tên branch

Mẫu: `ten_owner/module` — tên owner và module/chức năng viết thường, không dấu; phần module dùng tên thống nhất trong nhóm.

Ví dụ: `dung/document_processing`, `ducanh/backend`, `nam/change_analysis`, `tungduong/frontend`. Branch tài liệu có thể dùng `dung/docs`. Giữ nhánh đang làm cho cùng phạm vi; không đổi tên chỉ để khớp ví dụ.

Không thêm prefix loại thay đổi như feat/ hoặc fix/ trước tên owner. Loại thay đổi được ghi trong commit theo mục 3.4; docs có thể là phạm vi công việc trong ten_owner/docs.

Một branch không gom các task không liên quan. Không tự đổi cấu trúc chính dưới danh nghĩa refactor.

### 3.4. Commit

Mẫu: `type(scope): mô tả ngắn`, ví dụ `fix(text-diff): correct replacement offsets` hoặc `docs(decision): chot hop dong text diff`.

| Loại (type) | Khi dùng | Ví dụ commit |
| --- | --- | --- |
| feat | Thêm chức năng | feat(parser): preserve source spans |
| fix | Sửa lỗi | fix(text-diff): correct replacement offsets |
| docs | Sửa tài liệu | docs(decision): update module assignments |
| test | Bổ sung kiểm thử | test(semantic-diff): add input fixtures |
| refactor | Tổ chức lại code trong phạm vi đã thống nhất | refactor(ai-adapter): separate response parsing |

- Commit theo một thay đổi có mục đích rõ; thông điệp cho biết thay gì, không chỉ ghi “sửa”, “update”, “done”.
- Có thể commit công việc đang làm trên branch task nếu ghi rõ chưa hoàn thiện; không coi commit đã push là đã nghiệm thu/merge.
- Trước commit, kiểm tra branch, git status và phần staged. Chỉ stage các file thuộc task; không dùng git add . một cách máy móc.
- Không commit khóa/API token, .env chứa bí mật, môi trường ảo, cache hoặc file tạm. Dữ liệu mẫu đưa vào repo phải đúng phạm vi và nguồn được thống nhất.
- Không tự viết lại commit người khác hoặc force push branch dùng chung. Nếu cần xử lý lịch sử branch cá nhân đã có người phụ thuộc, trao đổi trước.

### 3.5. PR, review, merge và xung đột

PR ghi tối thiểu: task/phạm vi, file/chức năng đổi, contract/version sử dụng, dữ liệu và lệnh kiểm tra, kết quả, phần chưa xong và bên bị ảnh hưởng.

- Người nhận đầu ra review cách module cung cấp dữ liệu; owner phần liên quan review thay đổi trong phạm vi của mình. Nếu cùng một người làm hai chức năng nối nhau, nhờ một thành viên khác review phần tích hợp; không tự gọi đó là kiểm thử chéo độc lập.
- Đức Anh điều phối tích hợp và thực hiện merge vào main, hoặc phối hợp người được Dũng giao thực hiện. Dũng điều phối chung và thay đổi phạm vi/phân công; người làm không tự merge trước khi reviewer cần thiết xác nhận.
- Chỉ merge khi các kiểm tra phù hợp đã đạt, không còn lỗi chặn và contract/schema/mẫu khớp nhau. Thay đổi cần nhiều PR phải ghi thứ tự tích hợp.
- Khi có conflict, phối hợp owner file liên quan; không chọn toàn bộ ours/theirs chỉ để hết lỗi. Sau giải quyết, đọc diff và chạy lại kiểm tra bị ảnh hưởng.
- Cấu hình bảo vệ nhánh/CI có thể thực thi các quy tắc sau khi được thiết lập. Khi chưa có, vẫn phải có bằng chứng review/test trong PR; không khẳng định cấu hình đã bật.

## 4. Kiểm thử lẫn nhau giữa hai module

### 4.1. Chia trách nhiệm

Với điểm nối A → B:

| Người | Việc phải làm |
| --- | --- |
| Owner A — bên cung cấp | Tự kiểm tra A; tạo output thật theo contract; kiểm tra B có đọc đúng ý nghĩa dữ liệu và giả định của A không |
| Owner B — bên nhận | Kiểm tra output A có đúng trường, giá trị, nguồn và đủ để B dùng; chạy B bằng cả fixture và output thật |
| Hai owner | Cùng thống nhất expected output, tái hiện lỗi, xác định bên sửa và xác nhận kiểm tra lại |
| Thành viên khác | Review phụ hoặc nghiệp vụ theo phạm vi; hỗ trợ xử lý bất đồng, không thay việc hai owner tự kiểm tra |

Đức Anh điều phối kiểm thử tích hợp; Nam chủ trì đánh giá kỹ thuật theo D-11; Dũng chủ trì đánh giá người dùng theo D-12; Tùng Dương kiểm tra giao diện và trạng thái phiên. Thiết kế đánh giá, matching và phép đo theo [Kế hoạch kiểm thử và đánh giá](test_evaluation_plan.md).

Công cụ đánh giá kỹ thuật thuộc Nam theo HCI-12/D-11 và cây evaluation/evaluator.py trong Architecture; không xác nhận công cụ đã hoàn thiện. Kiểm tra module/điểm nối vẫn là trách nhiệm owner và bên nhận. Test, fixture và script kiểm tra đặt theo cấu trúc test/ của HCI; kiểm thử chéo phải có kết quả và cách tái hiện.

### 4.2. Những cặp cần kiểm tra

| Điểm nối | Hai bên kiểm tra chính |
| --- | --- |
| Nguồn/Parser/adapter → backend/linker | Dũng ↔ Đức Anh |
| Linker/context → Text Diff/Semantic Diff/Scorer | Đức Anh ↔ Nam |
| Kết quả phân tích → Pipeline/API | Nam ↔ Đức Anh |
| Báo cáo/nguồn → frontend/nhận xét | Đức Anh ↔ Tùng Dương |
| Nội dung giải thích/aspects → hiển thị | Nam ↔ Tùng Dương |
| Nhãn/đáp án và rubric | Dũng ↔ Nam |
| Prototype/tác vụ và phản hồi người dùng | Dũng ↔ Tùng Dương |
| LightRAG/context và nguồn | Đức Anh ↔ Dũng về nguồn; Đức Anh ↔ Nam về ngữ cảnh sử dụng |
| Bản chạy dùng thử | Đức Anh/Nam/Tùng Dương bàn giao cho Dũng |

Các điểm nối có thể nằm cùng folder hoặc qua bước chuẩn hóa. Input/output và yêu cầu nguồn theo D-01/D-02/D-03/D-04/D-05/D-06; dữ liệu frontend/phiên theo D-07/D-08. Text Diff → Semantic Diff → Scorer cùng Nam vẫn phải được kiểm tra; Đức Anh review khi nhận kết quả tích hợp. Với các chức năng cùng một owner, có thành viên khác review phần liên quan trước khi gọi đó là kiểm thử chéo.

### 4.3. Trình tự kiểm thử một điểm nối

1. Xác nhận hai bên đang dùng cùng contract và bộ mẫu đã review.
2. Chạy A với input đã thống nhất; lưu output thật gắn với commit, không dùng output giả thay thế.
3. B kiểm tra cấu trúc lẫn ý nghĩa: ID, nội dung, nguồn, offset, null/rỗng, lỗi/cảnh báo liên quan.
4. Chạy B với output đó; A review cách B đọc và sử dụng các trường.
5. Đối chiếu với expected output độc lập; thêm ca lỗi vào kiểm tra tự động phù hợp nếu phát hiện lỗi cần ngăn tái diễn.
6. Hai bên ghi kết quả, phần phải sửa, kiểm tra lại sau sửa; chỉ xác nhận đạt khi output thật đã dùng được đúng hợp đồng.

Các ca tối thiểu tùy điểm nối: bình thường, không có kết quả hợp lệ, thiếu/chưa xác định dữ liệu, lỗi bước trước, lệch ID/nguồn/offset và giới hạn đầu vào liên quan. Không bắt mọi cặp chạy ca không liên quan.

Đáp án không chỉ sao chép từ output của A. Ví dụ số Điều/Khoản/Điểm phải đối chiếu mẫu nguồn; hai module cùng dùng sai một trường vẫn có thể chạy thông nhau nhưng không đúng nghiệp vụ.

### 4.4. Ghi nhận và xử lý lỗi

Mỗi lỗi nên có mẫu ngắn:

```text
Điểm nối:
Contract/version và commit hai bên:
Input tái hiện:
Output thực tế:
Kết quả mong đợi và căn cứ:
Bước/lệnh tái hiện:
Bên chịu trách nhiệm sửa:
Trạng thái và kết quả chạy lại:
```

Phân biệt: A trả sai contract → A sửa; A đúng nhưng B dùng sai → B sửa; contract mâu thuẫn/thiếu quy tắc → hai bên thống nhất lại decision, rồi cập nhật mẫu và code. Nếu bất đồng kỹ thuật liên module chưa giải quyết, Đức Anh phối hợp owner và mời người phù hợp review; vấn đề phạm vi/phân công do Dũng điều phối; không âm thầm sửa expected output để test đạt.

### 4.5. Bàn giao dùng thử và xử lý góp ý

Chỉ bàn giao dùng thử khi có phiên bản, cấu hình, dữ liệu/đáp án đã review, kết quả kiểm tra trọng tâm và giới hạn; không còn lỗi chặn tác vụ. Dũng phải chạy lại được bản bàn giao. Kế hoạch tác vụ, cách chấm và thu phản hồi được chuẩn bị trước khi dùng thử.

Dũng tổng hợp vấn đề từ người dùng, ưu tiên và giao owner sửa; Đức Anh xử lý phối hợp backend/tích hợp, Nam sửa phần phân tích, Tùng Dương sửa giao diện/phiên, Dũng sửa nguồn/đầu vào thuộc phần mình. Sau sửa, kiểm tra hoặc thử lại tác vụ bị ảnh hưởng; giữ minh chứng và phiên bản trước/sau. Nhận xét trong sản phẩm không tự thành nhãn chuẩn hoặc kết quả nghiên cứu.

## 5. Checklist xác nhận hoàn thành

### Trước khi bắt đầu task phụ thuộc

- [ ] Có người làm chính, bên review và phạm vi file/chức năng rõ ràng.
- [ ] Quyết định liên quan đã chốt hoặc phần chưa chốt được tách khỏi phạm vi đang code.
- [ ] Hai bên có cùng contract và input/output mẫu đã review.
- [ ] Nhánh nguồn/nhánh đích PR được xác định.

### Trước khi merge

- [ ] Người làm đã tự kiểm tra, đọc diff và ghi lệnh/kết quả.
- [ ] Output thật đã được bên nhận kiểm tra và chạy qua điểm nối liên quan.
- [ ] Cách sử dụng dữ liệu đã được bên cung cấp review.
- [ ] Lỗi đã sửa được kiểm tra lại; giới hạn còn lại được ghi rõ, không có lỗi chặn bị che đi.
- [ ] Contract, schema, fixture và tài liệu bị ảnh hưởng nhất quán.
- [ ] Reviewer cần thiết xác nhận; Đức Anh hoặc người được giao thực hiện tích hợp.

Phân biệt **đã code**, **đã tự kiểm tra**, **đã kiểm thử chéo**, **đã merge** và **đã chạy toàn luồng**. Chỉ báo trạng thái đã có bằng chứng; merge một điểm nối không tự xác nhận toàn bộ hệ thống đã hoàn thành.
