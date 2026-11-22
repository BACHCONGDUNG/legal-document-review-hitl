# Nền HCI và phạm vi thiết kế
## Mốc mã nguồn
Mốc bắt đầu Phiên 1 là fb49c9b. Bộ tài liệu ngày 22/11/2026 mở rộng thiết kế. Đợt cập nhật này chỉ thay đổi tài liệu.
## Bản demo đã kiểm tra
Ứng dụng backend.demo:app nhận doc_v1, doc_s, reference_files và trả ComparisonReport.results. Có Parser/adapter, linker hẹp, Text Diff, context, Semantic Diff/Scorer bằng quy tắc và giao diện. LightRAG/model mặc định tắt. backend.main:app mặc định chưa gắn runner.
Kết quả kiểm tra trên bản tải từ fb49c9b gồm 111 test đạt, 2 expected failures và 2 test dịch vụ thật được bỏ qua. Kết quả áp dụng tại mốc đó. Chưa chạy đánh giá chất lượng pháp lý hoặc PDF xuyên luồng.
## Phần cần triển khai và xác nhận
Luồng chỉ S, kho dân sự bền vững, chọn đúng phiên bản, nhiều đích, tác động gián tiếp và báo cáo cấp S cần hợp đồng/fixture mới và kiểm tra trên HCI. Thiết kế index/query song song Text Diff cần đối chiếu code HCI trước khi ghi hoàn thành. Báo cáo cục bộ dùng v1/s/ref_* cần mapping sang kho và từng đích.
## Phân công
Dũng chuẩn bị nguồn/metadata, đầu vào/adapter, review dữ liệu và nghiên cứu người dùng. Đức Anh phụ trách linker, schema, context/LightRAG, Pipeline/API và tích hợp. Nam phụ trách phân tích, AI Adapter và đánh giá kỹ thuật. Tùng Dương phụ trách tương tác và frontend.
Nhận xét người dùng là chức năng mở rộng theo SRS. Nghiên cứu ngắn hạn tập trung vào lựa chọn giữ nhận xét, định danh và kiểm tra lại.
