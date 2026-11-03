# Tóm tắt thay đổi tài liệu HCI

**Ngày:** 03/11/2026  
**Nguồn đối chiếu:** thư mục docs trong ZIP HCI người dùng cung cấp  
**Phạm vi bàn giao:** tám file trong docs — sáu file có sẵn được đồng bộ, hai file mới. Không sửa code, dữ liệu, lịch sử Git hoặc README ở gốc.

## 1. Nội dung thống nhất

| Nội dung | Baseline làm việc thống nhất |
| --- | --- |
| Dự án | HCI, học phần 2627I_INT2041_1 Nhóm 6; nhóm trưởng Bạch Công Dũng, bốn thành viên theo kế hoạch HCI |
| Người dùng / mục tiêu | Sinh viên Luật; hiểu thay đổi, đọc bằng chứng, kiểm chứng AI và quản lý nhận xét; tách đánh giá AI khỏi usability |
| Bài toán | V1–S và tham chiếu do người dùng cung cấp; không bắt buộc dựng V2, không tự xác minh hiệu lực pháp luật |
| Contract | SRS HCI sở hữu base_file/amendment_file/reference_files; ComparisonReport có documents/items; ReviewItem và ReviewRecord riêng |
| Nhóm khía cạnh | Bốn mã theo SRS; gán nhãn theo nội dung, nguồn và ca ranh giới được review |
| Đầu vào / nguồn | PDF → DOCX → Parser hiện có; DOCX parse trực tiếp; block:N và spans theo nguồn thực; mapping trang PDF còn phải kiểm chứng |
| LightRAG | Tạm chọn B cho retrieval; client HTTP riêng; chưa chốt release/API/model/chunk/budget/lifecycle chi tiết |
| Nhận xét | Frontend giữ trong phiên; không tự huấn luyện/gold; reanalysis có kết quả dùng được phải đối chiếu, không áp xác nhận cũ lên nội dung đổi |
| Trạng thái | Tách SUCCESS/PARTIAL/FAILED, needs_review của AI, decision/review_status người dùng và trạng thái review nhãn |
| Tổ chức | backend/app/ và test/ theo ZIP; tài liệu dùng đúng tên file hiện có |
| Quyết định owner | Một register module-owner-decisions-hci.md, 13 D-ID đều CHỜ OWNER ĐỀ XUẤT |

Đây là baseline đồng bộ tài liệu theo phạm vi đã trao đổi, không phải xác nhận các owner đã review xong, code đã đáp ứng contract hoặc chức năng đã được nghiệm thu.

## 2. Thay đổi theo từng file

### docs/brd.md — HCI 1.0.0 → HCI 1.1.0

- Giữ nguyên người dùng sinh viên Luật, mục tiêu BG, yêu cầu BR, use case, phạm vi và tiêu chí nghiệm thu HCI.
- Làm rõ SRS sở hữu contract/bốn mã; các module nội bộ phải chuyển kết quả sang cùng hợp đồng và giữ bằng chứng.
- Đồng bộ tên/link các tài liệu và dẫn register quyết định.
- Đặt lựa chọn LightRAG ở Architecture, không biến thành nhu cầu người dùng được nghiên cứu xác nhận.
- Không thêm kết quả phỏng vấn, thử nghiệm, số đo hoặc thay thời hạn học phần.

### docs/srs.md — HCI 1.0.0 → HCI 1.1.0

- Giữ các chức năng FR-01–12, schema HCI và bốn field_group; ReviewItem là đơn vị rà soát của giao diện.
- Ghi rõ chênh lệch code nền: doc_v1/doc_s và khung báo cáo hiện tại chưa đáp ứng contract HCI, cần D-01 chuyển đổi.
- Làm rõ kiểu danh sách documents/items, phạm vi affected_item_ids và nguồn evidence đọc được sau dọn file; chi tiết truyền nguồn/fixture để owner đề xuất.
- Bổ sung quy tắc Parser native/adapter, block:N, Unicode offsets, DOCX chuyển đổi và mapping PDF chưa xác minh.
- Làm rõ ranh giới phân nhóm và dữ liệu nội bộ; response tuân theo các trường trong SRS.
- Bổ sung yêu cầu context/LightRAG, lỗi retrieval không tự là thiếu tài liệu, chờ index/cách ly/dọn dữ liệu.
- Làm rõ reanalysis SUCCESS hoặc PARTIAL có kết quả dùng được đều cần đối chiếu; FAILED/timeout giữ bản cũ.
- Bổ sung AT-12/13 cho truy xuất và cách ly/lifecycle; dẫn D-ID thay vì tự chốt endpoint/ngưỡng/mô hình.

### docs/architecture.md — HCI 1.0.0 → HCI 1.1.0

- Thay mô tả “không cần RAG” bằng phương án B tạm chọn cho truy xuất, giữ backend nghiệp vụ và session HCI.
- Đưa hiện trạng ZIP lên rõ ràng: Parser/converter và API/pipeline nền có code; phần HCI đầy đủ chưa có.
- Thống nhất cây backend/app/, test/ và trách nhiệm từng module dự kiến; không coi tên file trong cây là code đã tạo.
- Mô tả ranh giới Parser/adapter/linker/context/client/AI Adapter/tổng hợp HCI; quy trình nhập/query/ánh xạ/dọn index là thiết kế chờ kiểm chứng.
- Giữ luồng xem nguồn, ghi nhận nhận xét, reanalysis, các trạng thái và dữ liệu trong phiên.
- Tách HTTP localhost với Internet, request đồng bộ người dùng với theo dõi nhập nội bộ; không tuyên bố hủy cứng hoặc offline chưa đo.
- Quyết định cụ thể chuyển về register D-01–13; không chọn framework/model/threshold thay owner.

### docs/data-annotation-guide-hci.md — HCI 1.1.0 → HCI 1.2.0

- Sửa liên kết brd-hci.md/srs-hci.md/architecture-hci.md sang tên file thực tế.
- Thống nhất gold và fixture HCI theo bốn mã của SRS, giữ reviewer, bằng chứng và phiên bản khi điều chỉnh nhãn.
- Bổ sung ca ranh giới cần review: hạn thực hiện so với ngưỡng; chủ thể/quyền/nghĩa vụ; nội dung ngoài phạm vi giữ nguồn/cảnh báo.
- Đồng bộ hướng dẫn trường explanation/significance_reason/ReviewItem; không tự thêm mã hoặc trường ngoài SRS.
- Cập nhật các ví dụ EX-01–07 cho bốn mã, ReferenceRequirement và EffectInfo; vẫn là ví dụ giả định, không tạo dữ liệu thật.
- Giữ rubric cũ như pilot tham khảo, yêu cầu Nam/Dũng review thay vì coi đã chốt.
- Đồng bộ PDF → DOCX, block/spans; thêm căn cứ retrieval, cách ly và ngăn V2/gold/gợi ý sai rò vào index.
- Giữ các ca tương tác IF, nhận xét độc lập với gold, review nhãn và dữ liệu người dùng.

### docs/implementation-plan-hci.md — HCI 1.1.0 → HCI 1.2.0

- Giữ bốn thành viên và trách nhiệm HCI, lịch mục tiêu tuần 6–14 và mốc nội bộ tuần 13; không ghi các tuần cũ là hoàn thành.
- Sửa link Data Guide đúng tên -hci; thêm baseline và hiện trạng code so với contract.
- Bổ sung thứ tự tiếp nhận quyết định theo điểm bàn giao, khả năng làm bằng fixture song song và review bởi bên nhận.
- Dẫn 13 D-ID thay vì ghi phương án kỹ thuật hộ owner; không tự đặt hạn ngày khi chưa có ước lượng.
- Sửa minh chứng nguồn: đọc đúng block/quote và ghi rõ giới hạn mapping PDF.
- Ghi ba tài liệu API Contract/Development Guide/Evaluation Plan còn thiếu, owner cung cấp nội dung trước khi hoàn thiện.

### docs/user-research.md — giữ nghiên cứu phiên bản 0.3

- Giữ nguyên toàn bộ nội dung gốc, ngày ghi nhận và kết quả hai người ở mục 1–5, không sửa persona/kết quả để khớp công nghệ.
- Chỉ thêm mục 6 dẫn tài liệu và D-07/D-08/D-12, ghi rõ đây là đồng bộ biên tập, chưa có nghiên cứu hoặc thử nghiệm mới.
- Phân biệt lựa chọn LightRAG với nhu cầu người dùng đã được xác nhận.

### docs/module-owner-decisions-hci.md — file mới, HCI 1.0.0

- Tập trung baseline và 13 lựa chọn cần owner đề xuất.
- Mỗi D-ID có đúng một owner tổng hợp, bên phối hợp/review, câu hỏi, đầu ra kiểm tra và nơi cập nhật sau chốt.
- Ghi trạng thái ban đầu CHỜ OWNER ĐỀ XUẤT; chưa có model/release/endpoint/prompt/threshold hoặc ngày chốt được điền thay.
- Có mẫu owner trả lời, quy tắc thay contract và lưu minh chứng/lịch sử.

### docs/changes-hci.md — file mới

- Tóm tắt baseline, thay đổi cũ–mới từng file, phần còn mở và giới hạn phạm vi của gói.

## 3. Những việc còn để owner quyết định

Không chốt hộ release/API LightRAG; mô hình/embedding và nơi chạy; prompt/validation/fallback; chunking/registry; thuật toán linker; ngưỡng dung lượng/timeout/đồng thời; ca ranh giới nhãn/rubric; thiết kế UI/đối chiếu nhận xét; bộ dữ liệu cuối/split; metric/ngưỡng kỹ thuật; kế hoạch usability và môi trường cài đặt. Xem từng D-ID trong register để giao yêu cầu cụ thể.

Chưa tạo api-contract.md, development-guide.md, test-evaluation-plan.md vì thiếu đầu vào owner. Các tài liệu hiện có không dẫn chúng như file đã tồn tại. Chưa tạo schema hoặc fixture chạy được chỉ bằng việc ghi tên trong docs.

## 4. Ảnh hưởng ngoài docs — chưa sửa trong đợt này

- Code nền dùng doc_v1/doc_s và khung report chưa khớp SRS; cần chuyển theo contract sau D-01, không dùng việc sửa docs làm bằng chứng code đã đồng bộ.
- README ở gốc còn Group 4, mô tả người dùng ưu tiên khác BRD HCI, liên kết không có docs/ và tên file -hci chưa đúng; cây README ghi tests/ trong khi repo có test/. Chưa thay README vì đầu ra yêu cầu lần này là docs/.
- Chưa cài/chạy LightRAG thật hoặc chạy lại test code trong đợt sửa tài liệu; không công bố F1, SUS hoặc kết quả người dùng mới.
- Không sửa file pháp luật, gold, dữ liệu nghiên cứu gốc hoặc mã nguồn của dự án.


