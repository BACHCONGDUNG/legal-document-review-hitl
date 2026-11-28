-- Synthetic, reviewable examples. X and Y are distinct territories. Dates are fixture values.
PRAGMA foreign_keys = ON;
BEGIN;
INSERT INTO document VALUES
 ('A','demo-v1','1','Quy định sử dụng vỉa hè','A-MAU','Văn bản mẫu',NULL,NULL,'AVAILABLE_IN_PILOT',0),
 ('B','demo-v1','1','Quy định về sạp hàng di động','B-MAU','Văn bản mẫu',NULL,NULL,'AVAILABLE_IN_PILOT',0),
 ('C','demo-v1','1','Quy định về điểm bán hàng tại khu Y','C-MAU','Văn bản mẫu',NULL,NULL,'AVAILABLE_IN_PILOT',0);
INSERT INTO source_block VALUES
 ('A','block:1','Điều 1. Trong năm 2026, tại khu X, mọi tổ chức, cá nhân sử dụng vỉa hè để bán hàng chỉ được đặt thiết bị trong phần diện tích đã được đánh dấu.'),
 ('A','block:2','Điều 2. Mẫu sổ tiếp nhận được in trên giấy khổ A4.'),
 ('B','block:1','Điều 3. Trong năm 2026, tại khu X, người kinh doanh đặt sạp hàng di động trên vỉa hè phải bố trí sạp trong phần diện tích được phép bán hàng.'),
 ('C','block:1','Điều 1. Trong năm 2026, người kinh doanh đặt sạp trên vỉa hè tại khu Y phải sử dụng phần diện tích dành cho bán hàng.'),
 ('C','block:2','Điều 2. Tham khảo mẫu sổ tiếp nhận của văn bản A-MAU.');
INSERT INTO concept VALUES
 ('SIDEWALK_TRADING_AREA','Phần diện tích vỉa hè được sử dụng để bố trí thiết bị bán hàng.'),
 ('MOBILE_STALL','Sạp có thể di chuyển. Bản thân loại thiết bị chưa cho biết sạp đặt ở đâu.');
INSERT INTO facet VALUES
 ('A.1','A','block:1','Điều 1','SETS_CONDITION','SIDEWALK_TRADING_AREA','Mọi tổ chức, cá nhân','Sử dụng vỉa hè để bán hàng','Thiết bị bán hàng','Chỉ được','Trong phần diện tích đã đánh dấu',NULL,'*','SIDEWALK_TRADE','X','2026-01-01','2026-12-31',1),
 ('B.3','B','block:1','Điều 3','USES_CONDITION','SIDEWALK_TRADING_AREA','Người kinh doanh','Đặt sạp trên vỉa hè','Sạp hàng di động','Phải','Trong phần diện tích được phép bán hàng',NULL,'TRADER','SIDEWALK_TRADE','X','2026-01-01','2026-12-31',1),
 ('C.1','C','block:1','Điều 1','USES_CONDITION','SIDEWALK_TRADING_AREA','Người kinh doanh','Đặt sạp trên vỉa hè','Sạp hàng','Phải','Trong phần diện tích dành cho bán hàng',NULL,'TRADER','SIDEWALK_TRADE','Y','2026-01-01','2026-12-31',1);
INSERT INTO document_reference VALUES ('C.2-A','C','A','block:2','CITES');
COMMIT;
