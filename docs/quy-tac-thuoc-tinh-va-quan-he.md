# Thuộc tính nút và quy tắc nối văn bản

Bộ quy tắc v1 lưu mỗi phiên bản văn bản thành một nút. Mỗi thuộc tính nghiệp vụ thuộc về một quy định cụ thể và có đoạn trích nguồn. Đồ thị giữ được nhiều cạnh có hướng giữa cùng hai nút. [Dữ liệu và quy tắc chạy được](../data/legal-dataset-study/semantic-graph/)

## Thuộc tính cần lưu

| Cấp | Trường | Cách gán |
|---|---|---|
| Văn bản | ID, số hiệu, tên, loại văn bản, cơ quan ban hành, nguồn, phiên bản, snapshot kho | Mỗi phiên bản có ID riêng. Khi ghép với pilot dùng ID nguồn như `dataset:56666` trong cùng snapshot. |
| Tình trạng nguồn | Tình trạng toàn văn và cờ đã xác minh phiên bản pháp lý | Ghi riêng hai giá trị. Có bản DOCX chỉ xác nhận tệp có mặt. |
| Quy định | ID thuộc tính, Điều/Khoản/Điểm, ID khối, nguyên văn | Tách mỗi mệnh đề có điều kiện áp dụng khác nhau thành một bản ghi. Nếu cần nhiều đoạn để hiểu một quy định, chỉ gán vai trò sau khi rà đủ căn cứ; mẫu v1 lưu một đoạn chính cho mỗi bản ghi. |
| Nội dung | Chủ thể, hành vi, đối tượng, tính chất quy phạm, điều kiện, ngoại lệ | Ví dụ “người kinh doanh”, “đặt sạp”, “sạp di động”, “phải”, “trong diện tích được phép”. Giữ câu nguồn song song với giá trị chuẩn hóa. |
| Phạm vi | Nhóm chủ thể, loại sử dụng, địa bàn, ngày đầu và cuối kỳ áp dụng đang xét | Chuẩn hóa về cùng tập mã. Hai mã cụ thể khác nhau chỉ được dùng như hai nhóm loại trừ nhau. Với phạm vi lồng nhau, tách về cùng đơn vị trước khi nối. Hai đầu ngày tính cả ngày biên. |
| Vai trò | Quy định đặt ra điều gì hoặc sử dụng điều gì, mã khái niệm chung | Ví dụ A *đặt điều kiện* về diện tích vỉa hè để bán hàng, B *sử dụng điều kiện* ấy khi quy định cách đặt sạp. Lưu vai trò ở cả hai đầu. |
| Rà soát | Đã kiểm tra điều kiện và ngoại lệ cho phạm vi đã mã hóa | Thiếu điều kiện, có ngoại lệ chưa phân giải hoặc chưa xác định được thời gian thì giữ để rà soát. `NULL` biểu thị chưa biết. Dấu `*` chỉ dùng khi nguồn khẳng định bao phủ toàn bộ giá trị của chiều đó. |

## Hai loại cạnh có hướng

**Quan hệ văn bản.** Nếu A nhắc B, lưu cạnh từ A đến B cùng khối nguồn trong A. Nhãn mặc định là `CITES` cho lời nhắc đã nhận diện. Chỉ dùng `BASIS`, `AMENDS`, `SUPPLEMENTS`, `REPEALS` khi ngữ cảnh thể hiện căn cứ, sửa, bổ sung hoặc bãi bỏ. Phân giải số hiệu và phiên bản trước khi ghi vào bảng cạnh đã nối. Pilot hiện có danh sách đích mơ hồ cần rà soát.

**Quan hệ ngữ nghĩa.** Quy ước của bộ mẫu là A → B (`MAY_AFFECT`) khi A đặt quy định mà một hoạt động cụ thể trong B sử dụng. Có thể lần từ A sang B khi quy định ở A thay đổi. Bốn quy tắc trong [rules.sql](../data/legal-dataset-study/semantic-graph/rules.sql) là:

| Quy tắc | Vai trò ở A | Vai trò ở B |
|---|---|---|
| Điều kiện áp dụng | Đặt điều kiện | Hoạt động cần đáp ứng điều kiện |
| Định nghĩa | Xác định nghĩa của một khái niệm | Quy định sử dụng khái niệm theo chính nghĩa đó |
| Thủ tục | Đặt các bước của thủ tục | Yêu cầu thực hiện thủ tục đó |
| Ngưỡng hoặc thời hạn | Đặt giá trị hoặc giới hạn | Dùng chính giới hạn đó để xác định hành vi hoặc nghĩa vụ |

Hai vai trò phải bổ sung nhau, cùng khái niệm và cùng snapshot. Hai phía phải giao nhau về nhóm chủ thể, loại sử dụng, địa bàn và thời gian. Người gán phải kiểm tra ngoại lệ và nghĩa của từng vai trò theo nguồn. Cùng từ khóa, cùng mức số hoặc cùng nhắc đến một thủ tục có thể giúp tìm ứng viên. Chỉ gán vai trò sử dụng khi có căn cứ rằng quy định B thực sự cần điều kiện, định nghĩa, thủ tục hoặc ngưỡng được mô tả ở A. Từ điển và bản gán thuộc tính trong ví dụ được chuẩn bị trước. Truy vấn SQL tự nối các bản gán đủ điều kiện.

Để có B → A, cần thêm một cặp quy định mà B đóng vai trò đặt quy tắc và A sử dụng nó. Khi A hoặc B sửa, kiểm tra lại các cạnh gắn với điều khoản hoặc căn cứ đã thay đổi. Có thể tra cả cạnh đến và đi. Chỉ kết luận tác động thực tế sau khi đối chiếu nội dung trước/sau với quy định ở đầu kia. Ví dụ sửa khổ giấy ở Điều 2 của A không cho phép kết luận sạp của B bị ảnh hưởng.

## Ví dụ đã lưu

Các văn bản A, B, C và địa bàn X, Y trong ví dụ đều là giả định. A quy định phạm vi được phép sử dụng vỉa hè để bán hàng ở X. B quy định người đặt sạp ở X phải sử dụng đúng diện tích được phép. Hai văn bản không nêu tên nhau. C có quy định đặt sạp tại Y và nhắc A khi nói về mẫu sổ.

| Cặp | Kết quả | Căn cứ |
|---|---|---|
| A → B | Cạnh ngữ nghĩa `MAY_AFFECT` | Điều 1 của A đặt điều kiện mà Điều 3 của B sử dụng tại X trong cùng kỳ. |
| B → A | Chưa có cạnh | Trong ví dụ, A không sử dụng quy định nào do B đặt ra. |
| C → A | Cạnh văn bản `CITES` | Điều 2 của C nhắc số hiệu A-MAU. |
| A → C | Loại ứng viên ngữ nghĩa | Cùng khái niệm nhưng quy định ở C áp dụng tại Y. |

## Đọc và dùng lại

Mở [cơ sở dữ liệu SQLite](../data/legal-dataset-study/semantic-graph/sidewalk.sqlite3) hoặc [đồ thị JSON có nguyên văn từng cạnh](../data/legal-dataset-study/semantic-graph/sidewalk.graph.json). Trong SQLite, bảng `document` giữ nút, `facet` giữ thuộc tính, `source_block` giữ nguyên văn và `document_reference` giữ tham chiếu đã phân giải. View `semantic_pair` cho biết cặp nào đủ căn cứ, khác phạm vi hoặc cần review. View `graph_edge` trả hai loại cạnh.

Từ thư mục `data/legal-dataset-study/semantic-graph`, có thể dựng lại trên một tệp SQLite mới và xuất JSON:

```sh
sqlite3 -bail demo.sqlite3 '.read rules.sql' '.read sidewalk.sql'
sqlite3 -header -column demo.sqlite3 'SELECT family, relation, source_id, target_id FROM graph_edge'
sqlite3 -bail demo.sqlite3 '.read export.sql' > demo.graph.json
```

Khi dùng với dữ liệu thật, nhập nút và khối từ đúng phiên bản DOCX, dùng ID của pilot ở hai đầu, thêm các bản gán đã rà soát rồi xuất lại. JSON giữ `nodes`, `edges`, `source_id`, `target_id`, `relation` và `evidence` theo cách tổ chức của đồ thị văn bản trong dự án. Đây là dữ liệu đồ thị cục bộ. Đồng bộ vào LightRAG hoặc hiển thị trong web demo là điểm tích hợp riêng. [Đặc tả nguồn trên main](https://github.com/BACHCONGDUNG/legal-document-review-hitl/blob/21b09f3/docs/srs.md#19-đặc-tả-mục-tiêu-cho-nút-và-hai-loại-quan-hệ)
