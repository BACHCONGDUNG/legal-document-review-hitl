# Kế hoạch của Nam sau Text Diff

**Mốc xuất phát** là `nam/AI@debd848` ngày 24/11/2026. Đầu ra cần bàn giao là một lượt phân tích mà Đức Anh có thể chạy từ `AmendmentItem` đến `AmendmentResult`, truy lại được bằng chứng cho từng nhận định, nhận ra phần còn thiếu và đo được số thay đổi bị bỏ sót. Text Diff đã có bộ hồi quy. Kế hoạch dùng lõi so sánh từng đích đang chạy trên nhánh này.

**Căn cứ dự án** gồm [đặc tả đầu ra](../../srs.md), [phân công và điểm nối](../../module.md), [quyết định CN-06, CN-08 và LK-08–10](../../module-owner-decisions-hci.md), [ví dụ nhãn EX-01–13](../../data-annotation-guide-hci.md) và [kế hoạch đánh giá](../../test_evaluation_plan.md).

## Thứ tự và phụ thuộc

| Mốc | Nam có thể bắt đầu | Đầu vào cần từ nhóm | Bằng chứng hoàn thành |
|---|---|---|---|
| 1. Semantic Diff | Chạy rule hiện có với fixture, viết ca đổi nghĩa, đổi diễn đạt và thiếu nguồn | Đức Anh thống nhất điều kiện xác nhận đủ ngữ cảnh. Dũng review ví dụ nghiệp vụ | Cùng một ca chạy được ở hai trạng thái đủ và thiếu căn cứ |
| 2. Scorer | Dùng đầu ra mẫu của Semantic để viết test song song với mốc 1 | Dũng và reviewer duyệt ranh giới các mức trên ca pilot | Mỗi thay đổi có một kết quả chấm, có lý do hoặc yêu cầu review |
| 3. AI Adapter | Viết giao diện nội bộ và test phản hồi mô phỏng ngay khi thống nhất cấu trúc đầu ra Semantic | Thống nhất với Đức Anh và Dũng người phụ trách cấu hình, nhà cung cấp, dữ liệu được gửi và giới hạn lần gọi trước khi thử dịch vụ thật | Lượt thành công và lượt lỗi đều trả được phần báo cáo còn dùng được |
| 4. Đánh giá kỹ thuật | Viết phép đo bằng tập nhỏ tính tay từ ngày đầu | Dũng cung cấp nhãn đã review, Đức Anh chốt cách ghép và cấu hình chạy | Chạy lại được từ cùng commit, dữ liệu, nhãn và lệnh |

Các mốc là thứ tự bàn giao đề xuất. Hai tài liệu phân công đang ghi khác nhau về AI Adapter: LK-01 và Module giao Nam, CN-08 ghi Dũng và Đức Anh. Kế hoạch dùng phân công Nam đang nhận cho phần code và test. Cần xác nhận đầu mối dịch vụ thật trước khi kết nối.

## 1. Semantic Diff

**Điểm sửa chính** là `backend/app/change_analysis/semantic_diff.py`. Giữ tương thích với `detect_semantic_changes(item, text_diff, *, context_complete=False)`. Hàm trả `SemanticDiffResult` có cùng `amendment_id`. Hiện hàm nhận `text_diff` nhưng rule đọc hai chuỗi trước–sau. Bridge kiểm tra ID, còn demo gọi Semantic với giá trị mặc định của `context_complete`. Rule hiện nhận một mẫu thời hạn hẹp và một cặp cách diễn đạt tương đương.

- [x] **Lập đường cơ sở.** Chạy hàm thật bằng fixture `context_and_text_diff_to_semantic/deadline_reduction.json`. Ca hồi quy nằm trong `test/handoff_suite/test_fixture_consistency.py` để kiểm tra Text Diff, Semantic Diff, Scorer và validator cùng một lượt. Fixture mô tả “trong 30 ngày”. Nguồn V1 ở `block:3` cho biết cách tính ngày làm việc của Điều 2. Kết quả được ghi ở phần cuối kế hoạch.
- [ ] **Chốt điều kiện suy luận.** Kiểm tra yêu cầu áp dụng đúng đích, cùng đơn vị trước–sau, ID diff và nguồn của phần chữ đổi. Xác định với Đức Anh nơi kiểm tra các dẫn chiếu cần thiết trước khi truyền trạng thái đủ ngữ cảnh. Dùng cặp test có/mất căn cứ trên cùng đầu vào. Một lần retrieval trả về văn bản chỉ chứng minh đã lấy được nguồn đó.
- [ ] **Triển khai từng quy tắc có thể kiểm tra.** Bắt đầu với EX-01 đổi diễn đạt và ca thời hạn. Tiếp theo dùng EX-03 cho một nghĩa vụ đổi cả chủ thể lẫn ngưỡng, cùng một `change_id` có hai `aspects`. Tạo thêm một ca có hai nghĩa vụ độc lập, kỳ vọng hai `change_id` phân biệt. Với mỗi quy tắc, thêm một ca gần giống nhưng khác điều kiện để phát hiện kết luận quá rộng. Dùng các nhóm trong `GROUPS` của validator.
- [ ] **Giữ rõ phần biết và chưa biết.** `true` cần ít nhất một khía cạnh có bằng chứng. `false` dùng cho ca xác định chỉ đổi diễn đạt, với `aspects=[]`. Chưa thể kết luận thì dùng `null`, `needs_review=true` và lý do cụ thể. Với `DERIVED`, truy phần thay thế về chỉ dẫn S và phần giữ nguyên về V1. Nếu chưa hỗ trợ truy nguồn đó, trả kết quả cần review. Thử EX-12 để giữ thay đổi dẫn chiếu đã biết và ghi rõ bảng B còn thiếu.
- [ ] **Bàn giao.** Chạy qua `run_semantic_stage` và runner với một ca đủ nguồn, một ca thiếu nguồn. Kiểm tra ID, nguyên văn trích dẫn và cờ review ở từng cấp. Cho Scorer hai đầu ra thực tế này cùng đoạn nguồn để chạy lại.

## 2. Scorer

**Điểm sửa chính** là `backend/app/change_analysis/scorer.py`. Giữ `score_changes(semantic) -> list[ScoringResult]`. Hiện có thứ tự ưu tiên tám nhóm, nhánh `WORDING_ONLY/LOW` và một quy tắc `HIGH` hẹp cho thời hạn. Chốt rubric thử nghiệm bằng ví dụ trước khi mở rộng các nhánh chấm.

- [ ] **Khóa quan hệ đầu vào–đầu ra.** Trong `test/unit/change_analysis/test_scorer.py`, thử đầu vào có 0, 1 và 2 thay đổi. Mỗi `change_id` xuất hiện đúng một lần trong đầu ra. Với thay đổi nghĩa, `category` phải có trong các `field_group` đã xác định của thay đổi đó. Giữ mọi khía cạnh trong kết quả Semantic.
- [ ] **Lập bảng quyết định pilot.** Dùng EX-01 cho `WORDING_ONLY/LOW`, EX-06 cho `MEDIUM` khi hai cách thực hiện đã được xác nhận tương đương, EX-03 cho `HIGH`, EX-04 cho `CRITICAL` khi đủ căn cứ và reviewer đã xác nhận việc bỏ toàn bộ nghĩa vụ cốt lõi. Với mỗi ca, ghi đoạn nguồn, tiêu chí áp dụng và tình huống sát ranh giới. Thêm đối chứng EX-06 thiếu căn cứ tương đương và EX-04 chỉ bỏ một phương thức thực hiện.
- [ ] **Xử lý phần chưa kết luận.** Với fixture chung `semantic_to_scorer/deadline_reduction.json`, kỳ vọng `category=TIME_QUANTITY`, `significance=null`, `is_critical=null`, `needs_review=true`. Với mức đã xác định, cờ `is_critical` đúng duy nhất cho `CRITICAL`. Giữ lý do review từ Semantic và bổ sung căn cứ cho mức đã chấm.
- [ ] **Kiểm tra điểm nối thật.** Chạy đầu ra mốc 1 qua Scorer rồi `validate_report`. Thêm ca `is_meaningful_change=false` đi cùng cảnh báo cần review: validator hiện yêu cầu `WORDING_ONLY/LOW` cho mọi kết quả `false`, còn scorer hiện chỉ gán hai giá trị này khi cờ review tắt. Nếu đã xác định chỉ đổi diễn đạt, giữ nhãn và truyền cảnh báo. Nếu cảnh báo làm kết luận về nghĩa chưa chắc chắn, sửa kết luận Semantic thành `null`. Kiểm tra cả hai đường đi.

## 3. AI Adapter

**Điểm triển khai** là `backend/app/change_analysis/ai_adapter.py`, hiện trống. Giao diện nội bộ đề xuất nhận item, diff, bằng chứng đã kiểm tra và thời gian còn lại. Khi thành công, trả ứng viên `SemanticDiffResult` theo schema hiện có. Khi lỗi, trả nguyên nhân cho bên gọi để giữ kết quả từng phần. Chốt chữ ký với Đức Anh trước khi nối vào runner.

- [ ] **Chuẩn bị yêu cầu mẫu.** Gửi chỉ dẫn, đích, đoạn trước–sau, vùng chữ đổi và danh sách bằng chứng được phép viện dẫn cho item hiện tại. Dùng EX-05 làm ca quy tắc chưa xử lý nhưng có đủ nguồn. Cho phép thay hàm gọi dịch vụ bằng hàm mô phỏng trong test. Giữ chế độ chạy bằng rule làm mặc định.
- [ ] **Kiểm tra đầu ra trước khi nhận.** Dùng `validate_payload` cho kiểu dữ liệu. Đối chiếu `amendment_id`, các ID thay đổi/khía cạnh, nhóm cho phép, vai trò V1/S, nguồn được cấp cho item và nguyên văn từng quote. Tái sử dụng `validate_sources` ở nơi có kho tài liệu. Kiểm tra thêm trích dẫn có thực sự hỗ trợ khía cạnh đang được gán. Câu trích có thật vẫn có thể thuộc điều khoản khác.
- [ ] **Viết test độc lập với dịch vụ.** Trong `test/unit/change_analysis/test_ai_adapter.py`, thử phản hồi hợp lệ, JSON hỏng, sai ID, bịa trích dẫn, trích đúng chữ từ sai nguồn, timeout, thiếu cấu hình và hai item liên tiếp. Với ca lỗi, giữ Text Diff cùng bằng chứng hữu ích, ghi lý do review cho đúng item. Kiểm tra số lần gọi bằng 0 khi rule đã đủ căn cứ hoặc khi nguồn bắt buộc còn thiếu.
- [ ] **Tích hợp rồi mới đo dịch vụ thật.** Thử cơ chế dùng model khi rule chưa giải quyết được và nguồn đủ để suy luận. Dùng cùng một ca cho chế độ tắt/bật, lưu model/phiên bản, cấu hình, độ trễ, số lần gọi và chi phí nếu có. Báo cáo rõ test mô phỏng nào đã đạt và ca nào đã chạy với dịch vụ thật.

## 4. Đánh giá kỹ thuật chất lượng phân tích

Đề xuất đặt script ngoại tuyến tại `test/evaluation_suite/score_predictions.py`, kèm `test_metrics.py`. Dữ liệu đầu vào gồm báo cáo dự đoán, nhãn tham chiếu đã review và phiên bản bộ dữ liệu. Kết quả là bảng đếm, chỉ số, danh sách ca sai và các ca cần xem lại. Pipeline sản phẩm tiếp tục trả báo cáo theo hợp đồng hiện có.

- [ ] **Chốt đơn vị chấm với nhóm.** Một nhãn là một thay đổi của một quy định xác định. Đề xuất ghép theo văn bản/phiên bản, điều khoản, nội dung thay đổi và bằng chứng. ID do thuật toán sinh dùng để nối nội bộ. Lưu quyết định của reviewer đối với diễn đạt tương đương, ca chia/gộp và ca còn bất đồng. Cố định cách ghép trước đợt đo chính thức.
- [ ] **Tạo bộ mẫu nhỏ tính tay.** Với 3 thay đổi chuẩn và 3 dự đoán, trong đó 2 dự đoán đúng và 1 dự đoán lặp một thay đổi đã ghép, kỳ vọng TP=2, FP=1, FN=1 và F1=2/3. Thêm ca bỏ sót thay đổi trọng yếu, ca gold có thay đổi nhưng hệ thống trả chưa xác định, và ca mẫu số bằng 0. Ghi rõ số ca chưa xác định; với gold đã xác nhận, thay đổi bị bỏ sót vẫn tính FN đầu cuối. Với gold chưa thống nhất, ghi riêng số ca và lý do.
- [ ] **Chuẩn bị và khóa tập đánh giá.** Dũng cung cấp nguồn, phiên bản, nhãn và người review độc lập. Chia phát triển/kiểm thử theo văn bản hoặc chuỗi sửa đổi để các bản gần trùng nằm cùng phía. Các fixture dùng viết rule là dữ liệu phát triển. Giữ nhãn của tập kiểm thử ngoài prompt và chỉ mục truy xuất.
- [ ] **Đo theo cùng một bộ ca.** So sánh rule hiện tại với rule đã cải tiến, rồi với rule + model khi dịch vụ sẵn sàng. Chạy một lượt với đích và nguồn đã xác minh để đo riêng lõi Semantic/Scorer, một lượt qua Pipeline để đo lỗi đầu cuối. Khi đánh giá luồng chỉ S, cố định thêm snapshot kho. Ghi riêng lỗi chọn phiên bản, lỗi retrieval, hiểu sai nghĩa và chấm sai mức.
- [ ] **Xuất báo cáo.** Tính Precision = TP/(TP+FP), Recall = TP/(TP+FN), F1 = 2TP/(2TP+FP+FN). Critical Change Recall là số thay đổi trọng yếu chuẩn vừa được phát hiện vừa được nhận diện đúng là trọng yếu, chia cho tổng số thay đổi trọng yếu chuẩn theo quy ước đề xuất để nhóm duyệt. Khi mẫu số bằng 0, ghi “không tính được” cùng số mẫu. Báo thêm nhóm mức bị nhầm, số kết luận thiếu/sai bằng chứng, tỷ lệ cần review, độ trễ và chi phí khi có model. Lưu commit, cấu hình, phiên bản nhãn, lệnh chạy và ví dụ lỗi tiêu biểu. Change F1 ≥ 90% và Critical Change Recall ≥ 95% hiện là mốc dự tính.

## Kiểm tra tích hợp và bàn giao

Sau mỗi mốc, chạy từ gốc repo trong môi trường đã cài `requirements-demo.txt`. Các lệnh dưới đây dùng khi các test tương ứng đã có.

```bash
python -m unittest discover -s test/unit/change_analysis -v
python -m unittest discover -s test/handoff_suite -v
python -m unittest discover -s test/schema_suite -v
python -m unittest discover -s test/demo_suite -v
python -m unittest discover -s test/evaluation_suite -v
```

**Lượt đầu tiên** nên hoàn thành một cặp hồi quy trên `deadline_reduction`: lần một thiếu căn cứ về cách tính ngày, lần hai có `v1/block:3` và đủ điều kiện xác nhận ngữ cảnh. Đối chiếu nhận định, trích dẫn và mức `null` của Scorer. Cặp này cho cả ba bên một ví dụ để chốt hợp đồng trước khi cần tài khoản mô hình.

**Mốc mở rộng cấp S.** Sau khi Đức Anh và nhóm chốt hợp đồng báo cáo cấp S, dùng lại lõi trên từng đích đã xác minh. Bổ sung ca S sửa hai văn bản nhưng chỉ một đích đủ nguồn. Đối với tác động gián tiếp, thử một điều khoản B thực sự phụ thuộc phần V1 đã đổi và một điều khoản B chỉ liên quan chủ đề. Đầu ra cần nêu điều khoản B, liên kết về thay đổi gốc, giải thích, bằng chứng và phần chưa rõ. Đánh giá chất lượng nhận định gián tiếp riêng khi đã có nguồn và nhãn B được review.

## Kết quả lượt đầu

| Căn cứ đưa vào | Semantic Diff | Scorer |
|---|---|---|
| Có `v1/block:3` áp dụng đúng Điều 2 và bên gọi đã xác nhận đủ ngữ cảnh | `TIME_QUANTITY`. Thời hạn giảm từ 30 xuống 15 ngày làm việc. Bằng chứng gồm đoạn cũ, đoạn mới và quy tắc cách tính ngày. | Giữ `TIME_QUANTITY`, mức và cờ trọng yếu là `null`. Lý do yêu cầu kiểm tra theo rubric. |
| Thiếu đoạn nguồn, ngữ cảnh chưa được xác nhận hoặc quy tắc tính ngày thuộc Điều khác | Giữ trước–sau và Text Diff. Kết quả ngữ nghĩa là `null` kèm lý do review. | Mức và cờ trọng yếu là `null`. |

Ca hồi quy dùng fixture tổng hợp và kiểm tra cả nguồn trích dẫn lẫn hợp đồng báo cáo. Bên gọi truyền `context_complete=True` sau khi xác minh ngữ cảnh. Demo hiện vẫn dùng giá trị mặc định `False`.

```bash
python -m unittest test.handoff_suite.test_fixture_consistency.HandoffFixtureTests -k deadline -v
```
