# Kiểm chứng schema HCI
Mốc HCI đã kiểm tra là fb49c9b. Bộ Schema có 51 test gồm 49 đạt và 2 expected failures. Hai giới hạn là chưa ép duy nhất change_id xuyên chỉ dẫn và chưa kiểm tra đầy đủ khả năng tái dựng text từ diff.
Báo cáo cấp S cần kiểu dữ liệu, mapping ID, validator và fixture riêng theo SRS mục 1.8. Kết quả kiểm tra cục bộ hiện tại áp dụng cho hợp đồng ComparisonReport.
Lệnh chạy lại từ repo root.
    python -m unittest discover -s test/schema_suite -p "test_*.py" -v
Gắn kết quả mới với commit và minh chứng của lượt chạy.
