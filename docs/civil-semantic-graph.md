# Trích thuộc tính DOCX và nối quy định dân sự

CLI chạy ngoại tuyến trên kho DOCX. Bộ trích ghi các cụm từ nhận diện được từ thân Điều, Khoản và Điểm. Mỗi bản ghi có ID văn bản, vị trí, khối nguồn và đoạn trích. Offset tính theo ký tự Python trong khối nguồn, với đầu trái tính và đầu phải không tính. Trường vắng căn cứ có giá trị `null` và trạng thái `NOT_FOUND`. Chủ thể, đối tượng và hoạt động là cụm được nhận diện. Bộ trích v1 chưa phân giải đồng tham chiếu qua nhiều khối hoặc tách toàn bộ các vai trò trong một câu.

Quy tắc nối trong đợt này áp dụng cho **mốc đăng ký biện pháp bảo đảm bằng quyền sử dụng đất**. A → B nghĩa là quy định A đặt mốc mà B dùng. CLI kiểm tra vị trí điều khoản và trích câu thể hiện vai trò ở cả hai phía trước khi tạo cạnh. Ứng viên ký quỹ bị loại do mốc phát sinh hiệu lực thuộc sự kiện khác. Khi thiếu điều kiện kiểm chứng, CLI xuất quyết định cần rà soát kèm nguồn hai đầu và lý do. Cạnh thể hiện liên hệ trong phạm vi đã ghi. Việc kiểm chứng tác động của một lần sửa cần chỉ dẫn cụ thể. [BRD §8.7](brd.md#87-hai-loại-quan-hệ-giữa-các-văn-bản) · [SRS §1.9](srs.md#19-đặc-tả-mục-tiêu-cho-nút-và-hai-loại-quan-hệ) · [Gán nhãn §4.8](data-annotation-guide-hci.md#48-thuộc-tính-và-hai-loại-quan-hệ-giữa-các-văn-bản) · [Kiểm thử RG](test_evaluation_plan.md#ca-kiểm-chứng-hai-loại-quan-hệ--27112026)

## Chạy lại

Từ gốc repo, dùng Python 3.11 trở lên. Chế độ kiểm chứng cài thêm `python-docx` theo `requirements-demo.txt` để dựng bản DOCX từ đoạn nguồn công khai đã chép. Chọn thư mục đầu ra mới cho mỗi lần chạy.

```sh
python -m backend.civil_semantic_cli --output-dir runtime/lightrag/civil-extraction
python -m backend.civil_semantic_cli --verify-cases --output-dir runtime/lightrag/civil-verification
python -m unittest test.context_suite.test_civil_semantic_graph test.context_suite.test_document_graph_pilot -v
```

`--corpus` chọn thư mục có DOCX, quét cả thư mục con. `--catalog` chọn danh mục ứng viên theo định dạng CSV của dự án. Dùng `--no-catalog` để trích đặc trưng theo ID tệp khi không có metadata; các quy tắc nối cần số hiệu đã phân giải.

| Đầu ra | Nội dung |
|---|---|
| `attributes.jsonl` | Một bản ghi cho mỗi đoạn có thuộc tính, với vị trí và giá trị kèm offset. |
| `nodes.json` | Một bản ghi mỗi tệp. Có hash, trạng thái đọc và trích, trạng thái đối chiếu danh mục và trạng thái quan hệ. |
| `relations.json` | Cạnh có nguồn hai đầu và các quyết định loại hoặc yêu cầu rà soát. |
| `statistics.json` | Số tệp đọc được, số tệp sinh ít nhất một giá trị có nguồn, số bản ghi và số lượng theo trạng thái. |
| `cases.json` | Ba ca nghiệm thu khi bật `--verify-cases`. |

## Kết quả nghiệm thu

Kho chính ở `main@21b09f3` có **2.096 DOCX**. Đọc được cả 2.096 tệp. **1.362 tệp đạt** theo tiêu chí có ít nhất một thuộc tính truy được về nguồn, với **60.458 bản ghi**. **734 tệp** có trạng thái `NO_GROUNDED_ATTRIBUTES`. Trong lượt có nguồn bổ sung, 2 tài liệu của kho có cạnh, 1.360 tệp đã trích được thuộc tính nhưng chưa tìm được cạnh trong phạm vi quy tắc. [Thống kê JSON](../data/semantic-relation-cases/results/statistics.json)

Danh mục trên `main` có Nghị định 99/2022/NĐ-CP ở bản ghi 159372 nhưng bỏ trống đường dẫn tải. Khi bật kiểm chứng, CLI đọc đoạn Điều 6 từ văn bản hợp nhất 2161/VBHN-BTP, dựng thành một DOCX trích đoạn và chạy qua cùng bộ phân tích. Trích đoạn có dấu nguồn riêng và nằm ngoài mẫu số kho. Đầu còn lại của các ca RG đọc trực tiếp từ DOCX Nghị định 21/2021 trong kho. [Dữ liệu nguồn](../data/semantic-relation-cases/sources.json) · [Văn bản hợp nhất](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/4/2161-vbhn-btp.pdf#page=6)

| Ca | Kết quả đã kiểm tra |
|---|---|
| RG-04 | Điểm a khoản 1 Điều 6 NĐ 99 xác định mốc đăng ký, khoản 2 Điều 23 NĐ 21 dùng mốc đó. Giữ thêm điều kiện hợp đồng bảo đảm đã có hiệu lực tại khoản 1 Điều 23. Kiểm tra số hiệu dẫn chiếu trên toàn DOCX NĐ 21 và đoạn NĐ 99 đã sử dụng. |
| RG-05 | Khoản 5 Điều 23 NĐ 21 cũng nói về hiệu lực đối kháng, nhưng mốc ký quỹ là gửi tài sản vào tài khoản phong tỏa. Lưu quyết định `REJECTED` với cả hai đoạn. |
| RG-06 | Chỉ dẫn tại điểm đ khoản 10 Điều 11 NĐ 18/2026 đổi tên Sở ở khoản 1 Điều 10 NĐ 99. Với riêng chỉ dẫn này, kết quả là `NO_IMPACT_SHOWN` đối với mốc tại Điều 6. NĐ 18 còn có một chỉ dẫn khác sửa chính Điều 6. |

Lượt chạy có nguồn bổ sung xuất hai cạnh. Cạnh thứ hai nối Điều 6 NĐ 99 với khoản 2 Điều 319 Bộ luật Dân sự trong phạm vi thế chấp quyền sử dụng đất. Kết quả là bằng chứng chạy của một quy tắc có phạm vi xác định. Chiều nghiệp vụ và chất lượng ngoài các ca này còn cần reviewer của nhóm kiểm tra trước khi dùng cho đánh giá độc lập. [Kết quả cạnh](../data/semantic-relation-cases/results/relations.json) · [Ba ca nghiệm thu](../data/semantic-relation-cases/results/cases.json)
