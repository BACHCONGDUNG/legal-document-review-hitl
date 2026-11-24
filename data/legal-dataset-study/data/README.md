# legal-dataset-study

Thư mục khảo sát nguồn văn bản pháp luật, lọc ứng viên dân sự từ metadata và tải từng văn bản HTML để kiểm tra, chuẩn hóa dữ liệu.

## Cấu trúc thư mục

```text
legal-dataset-study/
├── .venv/                         Môi trường Python cục bộ, không đưa lên Git
├── download_metadata.py           Tải metadata, xuất CSV và gọi bộ lọc ứng viên
├── civil_metadata_rules.py        Bổ sung quy tắc lọc dữ liệu dân sự từ metadata
├── open_document.py               Tải HTML thuộc ứng viên, kiểm tra trùng tại đích
└── data/
    ├── README.md                 Hướng dẫn sử dụng thư mục
    ├── metadata.csv              Metadata gốc xuất từ dataset
    ├── thong_ke_linh_vuc.csv      Thống kê số văn bản theo linh_vuc
    ├── ung_vien_dan_su.csv        Danh sách ứng viên sau các lượt lọc metadata
    ├── ung_vien_dan_su_luot2_evidence.csv
    │                             Quy tắc và giá trị metadata làm căn cứ theo ID
    ├── ung_vien_dan_su_luot2_report.json
    │                             Thống kê kết quả, vai trò cột và nguồn tham khảo
    ├── vbpl-111436.html           HTML mẫu trích từ PDF nguồn
    ├── vbpl-<id>.html             HTML tạo khi tải văn bản mới
    └── vbpl-<id>.source.json      Dataset, revision, ID và hash của HTML tải mới
```

## Nguồn dữ liệu

Nguồn chính: [th1nhng0/vietnamese-legal-documents](https://huggingface.co/datasets/th1nhng0/vietnamese-legal-documents).

Các script tải dữ liệu cố định revision `8977887f17be2defae4c5171d55562e1cde7d695`.

| Thành phần dataset | Nội dung | Sử dụng trong thư mục |
| --- | --- | --- |
| `metadata` | Thông tin mô tả từng văn bản | Xuất thành `data/metadata.csv`, dùng để khảo sát và lọc ứng viên |
| `content` | Toàn văn trong trường `content_html` | Đọc streaming, tìm theo `id` rồi lưu thành HTML |
| `relationships` | Quan hệ giữa các văn bản | Chưa được các script trong thư mục xử lý |

[vohuutridung/vietnamese-legal-documents](https://huggingface.co/datasets/vohuutridung/vietnamese-legal-documents) là nguồn tham khảo bổ sung, chưa được tích hợp vào các script hiện tại.

`metadata.csv` có 171.556 dòng và 17 cột trong snapshot đi kèm. File được xuất từ metadata của dataset, không chứa toàn văn. Có metadata trên máy không đồng nghĩa đã tải toàn bộ nội dung văn bản.

## Chức năng các script

| File | Chức năng |
| --- | --- |
| `download_metadata.py` | Tải phần metadata, xuất `metadata.csv`, thống kê lĩnh vực và cập nhật danh sách ứng viên qua bộ quy tắc lọc |
| `civil_metadata_rules.py` | Bổ sung việc lọc ứng viên dân sự ngoài cách chỉ tìm từ “dân sự” trong `title` và `linh_vuc`; kết hợp thêm các cột metadata phù hợp, lưu căn cứ cho từng ID |
| `open_document.py` | Chỉ nhận ID trong CSV ứng viên; kiểm tra HTML/PDF/DOCX đã có ở thư mục đích và thư mục con, tải những văn bản còn thiếu, kiểm tra có chữ rồi lưu HTML kèm nguồn |

## Chuẩn bị môi trường

Mở PowerShell tại thư mục gốc repo, sau đó chuyển vào thư mục nghiên cứu:

```powershell
Set-Location .\data\legal-dataset-study
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install datasets pandas
```

Mỗi máy tạo `.venv` riêng; không sao chép môi trường từ máy khác. Nếu môi trường đã chạy được thì không cần tạo lại. Các lệnh dưới đây chạy tại `legal-dataset-study`, trừ khi có ghi chú khác.

## Tải hoặc xem metadata

Các CSV đi kèm có thể sử dụng ngay. Chỉ chạy lệnh sau khi cần tải lại metadata:

```powershell
.\.venv\Scripts\python.exe -u .\download_metadata.py
```

Script xuất ba CSV chính và các file bằng chứng/thống kê của bộ lọc. Lệnh chưa tải toàn văn. Hugging Face có thể lưu cache ngoài thư mục dự án.

Xem danh sách ứng viên và tra một văn bản:

```powershell
Import-Csv .\data\ung_vien_dan_su.csv -Encoding UTF8 | Select-Object -First 10 id, so_ky_hieu, title
Import-Csv .\data\metadata.csv -Encoding UTF8 | Where-Object { $_.id -eq '15289' } | Format-List id, so_ky_hieu, title
```

## Lọc ứng viên dân sự từ metadata

- Lượt 1: tìm từ “dân sự” trong `title` hoặc `linh_vuc`.
- Lượt 2: mở rộng theo chủ đề và các cột metadata phù hợp bằng `civil_metadata_rules.py`.

`title`, `linh_vuc`, `nganh` và `thong_tin_ap_dung` có thể cung cấp dấu hiệu chủ đề. `co_quan_ban_hanh` và `loai_van_ban` chỉ hỗ trợ kết hợp ngữ cảnh hoặc ưu tiên duyệt. Cột trống không được tự bổ sung giá trị. Số hiệu, ngày tháng, hiệu lực, người ký và phạm vi lãnh thổ không được dùng để quyết định văn bản thuộc dân sự.

Xem quy tắc, kiểm tra dự kiến và cập nhật kết quả:

```powershell
.\.venv\Scripts\python.exe .\civil_metadata_rules.py --describe-rules
.\.venv\Scripts\python.exe .\civil_metadata_rules.py --dry-run
.\.venv\Scripts\python.exe .\civil_metadata_rules.py
```

`--dry-run` không ghi file. Chạy cập nhật nhiều lần không nhân bản ID. Script giữ các ứng viên đã có, bổ sung dòng mới và không sửa `metadata.csv`. Có thể chỉ định `--metadata`, `--candidates`, `--evidence`, `--report` để thử trên bản sao.

| File kết quả | Cách sử dụng |
| --- | --- |
| `ung_vien_dan_su.csv` | Danh sách để lựa chọn văn bản cần tải; giữ nguyên 17 cột metadata |
| `ung_vien_dan_su_luot2_evidence.csv` | Nối với danh sách qua `id`; xem nhóm đề xuất, ưu tiên, mã quy tắc, cờ cần duyệt và giá trị metadata làm căn cứ |
| `ung_vien_dan_su_luot2_report.json` | Xem số lượng, độ đầy đủ/vai trò các cột, phiên bản quy tắc và nguồn tham khảo |

Snapshot đi kèm có 506 ứng viên từ lượt 1 và 4.093 ứng viên sau lượt 2. Các số lượng có thể thay đổi khi cập nhật dữ liệu hoặc quy tắc; xem report của lần chạy tương ứng.

Danh sách này chưa phải tập văn bản dân sự đã xác nhận. Nhóm liên quan/hỗ trợ và trường hợp dễ nhầm được đánh dấu để đọc toàn văn. Ngược lại, một văn bản không được chọn qua metadata cũng chưa có nghĩa đã được xác định ngoài phạm vi.

## Tải HTML từ danh sách ứng viên

`open_document.py` nhận ID qua dòng lệnh, không cần sửa mã nguồn. Phải chọn `--id` hoặc `--all-candidates`; không truyền lựa chọn thì chương trình chỉ báo cách dùng, không tự tải.

Kiểm tra dự kiến trước, rồi tải một văn bản chưa có:

```powershell
.\.venv\Scripts\python.exe -u .\open_document.py --id 15289 --output-dir .\data --dry-run
.\.venv\Scripts\python.exe -u .\open_document.py --id 15289 --output-dir .\data
```

Tải một số ID cụ thể hoặc thử tối đa 10 văn bản chưa có trong toàn bộ danh sách:

```powershell
.\.venv\Scripts\python.exe -u .\open_document.py --id 15289 26735 --output-dir .\data
.\.venv\Scripts\python.exe -u .\open_document.py --all-candidates --limit 10 --output-dir .\data --dry-run
.\.venv\Scripts\python.exe -u .\open_document.py --all-candidates --limit 10 --output-dir .\data --report .\data\tai_html.json
```

`--limit` giới hạn số văn bản chưa có sẽ được thử tải, không tính các file đã bỏ qua. HTML rỗng hoặc lỗi nguồn có thể làm số file tải thành công nhỏ hơn giới hạn. Không dùng `--all-candidates` không giới hạn nếu chưa chủ động muốn duyệt cả danh sách.

### Kiểm tra điều kiện và chống trùng

1. Mọi ID được yêu cầu phải nằm trong `ung_vien_dan_su.csv`. Nếu có ID ngoài danh sách, lệnh dừng trước khi tải bất kỳ ID nào.
2. Kiểm tra thư mục `--output-dir` và các thư mục con. File ở vị trí khác không được tính là đã có ở đích này.
3. Nhận diện HTML theo tên `vbpl-<id>.html` và bản ghi `.source.json`. Với PDF/DOCX, dùng `data/manifest.csv` theo dataset/revision/ID nếu có; tên file theo ID hoặc số hiệu cũng được coi là dấu hiệu có thể trùng.
4. File đã có được bỏ qua, không ghi đè. Nếu chưa xác nhận nguồn/phiên bản thì báo `skipped_unverified`; nếu rỗng, hỏng hoặc xung đột nguồn thì báo cần kiểm tra và giữ nguyên file.
5. Chỉ những ID còn thiếu mới được tìm trong `content` của snapshot đã cố định. Một lô dùng chung một lượt đọc streaming; kết thúc khi đã gặp đủ ID hoặc hết nguồn.
6. HTML có body rỗng, chỉ có script/style hoặc ảnh không có chữ sẽ không được lưu thành kết quả thành công.

Ví dụ kiểm tra văn bản đã có trong các ca nguồn:

```powershell
.\.venv\Scripts\python.exe .\open_document.py --id 15289 26735 --output-dir ..\raw --dry-run
```

### Đầu ra và tham số

Mỗi văn bản mới tạo `vbpl-<id>.html` và `vbpl-<id>.source.json` trong thư mục đích. Bản ghi nguồn chứa dataset, revision, ID, số hiệu, tiêu đề, thời điểm tải và SHA-256. Không tự cập nhật `data/manifest.csv` hoặc gán vai trò S/V1 cho một văn bản vừa tải.

| Tham số | Ý nghĩa |
| --- | --- |
| `--id ID [ID ...]` | Chọn một hoặc nhiều ID thuộc ứng viên |
| `--all-candidates` | Xét các ID theo thứ tự CSV ứng viên |
| `--limit N` | Giới hạn số văn bản chưa có sẽ được thử tải |
| `--output-dir PATH` | Vị trí lưu và kiểm tra trùng; mặc định là thư mục `data` bên cạnh script |
| `--candidates PATH` | CSV ứng viên khác; mặc định `data/ung_vien_dan_su.csv` bên cạnh script |
| `--manifest PATH`, `--manifest-root PATH` | Manifest dùng nhận diện file có sẵn và gốc tính các `local_path` tương đối; mặc định dùng manifest/gốc repo |
| `--dry-run` | Chỉ kiểm tra, không gọi mạng hoặc ghi HTML; chỉ lưu báo cáo nếu có `--report` |
| `--report PATH` | Lưu báo cáo JSON mới; không ghi đè báo cáo đã có |
| `--open` | Mở các HTML vừa tải thành công; mặc định không tự mở trình duyệt |

Streaming cần mạng và có thể đọc qua nhiều bản ghi trước khi gặp ID cần tìm. File HTML có chữ vẫn cần đối chiếu nguồn để xác nhận toàn văn đủ và đúng phiên bản. Script chưa tự chuyển sang DOCX hoặc thực hiện lượt phân loại nội dung.

### HTML mẫu 111436

`data/vbpl-111436.html` là bản đọc trích từ lớp chữ của PDF văn bản hợp nhất `25/VBHN-BTC`, không phải HTML nguyên bản có toàn văn của dataset. File có các phần tương ứng 20 trang PDF.

```powershell
Invoke-Item .\data\vbpl-111436.html
```

Nguồn đối chiếu: [thông tin văn bản](https://vbpl-bientap-gateway.moj.gov.vn/api/qtdc/public/doc/111436) và [PDF nguồn](https://vbpl-bientap-gateway.moj.gov.vn/api/qtdc/public/doc/minio/buckets/vbpl/111436/25-VBHN-BTC_25-VBHN-BTC.pdf/download).

HTML nguồn đã kiểm tra của ID này có `body` rỗng. Bộ tải giữ nguyên mẫu đang có và báo `skipped_unverified` nếu chưa có bản ghi nguồn cùng dataset/revision. Khi tải vào một thư mục trống, HTML nguồn rỗng sẽ bị từ chối. Muốn có nội dung cần đối chiếu PDF/nguồn khác và ghi rõ việc chuyển đổi.

## Chuyển HTML sang DOCX

Bộ chuyển đổi nằm tại `backend/app/document_processing/html_to_docx.py`. Sau khi tải HTML, có thể gọi riêng từ thư mục nghiên cứu:

```powershell
.\.venv\Scripts\python.exe -m pip install python-docx lxml
.\.venv\Scripts\python.exe ..\..\backend\app\document_processing\html_to_docx.py .\data\vbpl-15289.html --document-number "100/2006/NĐ-CP" --output-dir ..\raw\case_moi
```

Ví dụ trên tạo `data/raw/case_moi/100_2006_NĐ-CP.docx` và report chuyển đổi. Thay thư mục, ID và số hiệu theo văn bản thực tế. Bộ chuyển đổi tự nhận diện số ký hiệu nếu HTML có thông tin phù hợp; `--document-number` dùng giá trị từ metadata đã đối chiếu khi HTML thiếu số của chính văn bản. Dấu `/` được đổi thành `_` trong tên file; đầu ra đã tồn tại sẽ không bị ghi đè.

DOCX là sản phẩm chuyển đổi, cần kiểm tra với HTML/nguồn chính thức trước khi dùng cho Parser. Mẫu kiểm thử converter nằm trong `data/test_html_to_docx`; PDF dùng bộ chuyển đổi riêng `backend/app/document_processing/pdf_to_docx.py`.

## Hướng phát triển lượt lọc 3

Lượt 3 chưa được triển khai. Giả định đầu vào là danh sách ứng viên sau lượt 2 cùng toàn văn đã tải và có thể đọc được. Hướng xử lý tiếp theo:

1. Đọc nội dung cụ thể, ưu tiên phạm vi điều chỉnh, đối tượng áp dụng và các quy định về quan hệ nhân thân/tài sản.
2. Đề xuất nhóm phù hợp phạm vi dân sự, liên quan/hỗ trợ, ngoài phạm vi hoặc chưa đủ căn cứ; kiểm tra lại các trường hợp metadata gây nhầm.
3. Ghi nguyên văn làm bằng chứng, vị trí Điều/Khoản/Điểm hoặc block, nguồn và phiên bản văn bản cho từng nhận định.
4. Rà soát thủ công một tập mẫu để đánh giá và điều chỉnh cách phân loại trước khi mở rộng.

Kết quả lọc theo nội dung nên được lưu riêng, nối qua ID và thông tin nguồn, không sửa metadata gốc hoặc ghi đè bằng chứng lượt 2. Việc chọn các cặp S–V1, xác minh phiên bản và nạp kho truy xuất là bước tiếp theo sau khi dữ liệu được duyệt.

## Quy ước khi bổ sung dữ liệu

- Đọc ID dưới dạng chuỗi và giữ kèm tên dataset, revision, số hiệu, nguồn đối chiếu.
- Không ghép hai nguồn chỉ vì ID giống nhau; cần đối chiếu định danh và phiên bản văn bản.
- Giữ HTML nguồn để đối chiếu với DOCX; phân biệt tài liệu nguyên bản và bản chuyển đổi.
- Các ca nguồn phục vụ dự án đặt trong `data/raw/<case_id>/`, cập nhật nguồn và thông tin file trong `data/manifest.csv`.
- Đáp án phân loại/trước–sau đã duyệt cần lưu riêng với nguồn dùng cho truy xuất.

## Kiểm thử bộ lọc và bộ tải

Chạy tại thư mục gốc repo bằng môi trường Python đang sử dụng:

```powershell
py -B -m unittest discover -s test\data_suite -v
```

## Lỗi thường gặp

| Hiện tượng | Kiểm tra |
| --- | --- |
| Không tìm thấy `metadata.csv` | Chạy script tải metadata tại `legal-dataset-study`; kiểm tra file nằm trong thư mục con `data` |
| Môi trường `.venv` không chạy sau khi chuyển máy/thư mục | Tạo lại môi trường tại vị trí hiện tại và cài thư viện |
| Tải toàn văn bị ngắt | Chạy lại cùng lựa chọn và thư mục đích; file hoàn tất có bản ghi nguồn sẽ được bỏ qua, ID còn thiếu được thử lại |
| Cảnh báo WinError 10038 sau khi báo `downloaded` | Chạy lại cùng ID và đích để kiểm tra hash; file hoàn tất sẽ được bỏ qua. Nếu lỗi trước khi lưu thành công thì kiểm tra mạng và thử lại |
| `existing_invalid` / `existing_identity_conflict` | Kiểm tra file cũ, hash, dataset và revision; bộ tải không tự sửa hoặc ghi đè |
| `empty_or_invalid_html` | Nguồn không có chữ đọc được; đối chiếu HTML/PDF chính thức thay vì tạo DOCX trắng |
| Không nhận diện được số ký hiệu khi chuyển DOCX | Đối chiếu metadata và truyền `--document-number`; không lấy số của văn bản được viện dẫn |
| Bộ lọc báo ứng viên không khớp metadata | Kiểm tra dataset, revision và giá trị gốc; không ghép hoặc ghi đè trước khi làm rõ |
