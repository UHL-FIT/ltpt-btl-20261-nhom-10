# Lịch Sử Phiên Bản
## v1.0 - Initial Release
* Xây dựng mã nguồn nền sử dụng cấu trúc MVC
* Tạo những tính năng cơ bản (Thêm/Sửa/Xóa/...)
## v1.1 - Bento Box
*Với phiên bản v1.1, tuy rằng đây chỉ là cập nhật nhỏ nhưng sẽ đem lại trải nghiệm sử dụng dễ chịu hơn*
* Cập nhật lại giao diện phù hợp hơn với màn hình độ phân giải lớn.
* Nâng cấp trải nghiệm với thiết kế giao diện mới, hiện đại hơn và dễ nhìn hơn.
* Hiện nay đã có thể dùng tính năng sắp xếp theo danh mục bằng cách nhấn vào. 

## v1.2 - Cargo Crate
*Phiên bản v1.3 tập trung vào bộ lọc dữ liệu nâng cao và hoàn thiện giao diện*
* **Bộ lọc Phân loại**: Dropdown lọc sản phẩm theo loại (Điện tử, Phụ kiện, ...) — danh sách được cập nhật tự động từ dữ liệu.
* **Bộ lọc Tồn kho**: Dropdown lọc theo tình trạng tồn kho (Sắp hết hàng / Còn hàng).
* **Lọc đồng thời (Stacking)**: Ba bộ lọc (Tìm kiếm + Phân loại + Tồn kho) hoạt động kết hợp cùng lúc.
* **Dọn dẹp mã nguồn**: Xóa file thừa, đồng bộ phiên bản, chỉnh sửa giao diện.

## v1.3 - Database Docking
*Phiên bản v1.3 nâng cấp hệ thống với SQLite Database, Flask REST API và biểu đồ Matplotlib*
* **SQLite Database Backend**: Chuyển đổi lưu trữ dữ liệu sang cơ sở dữ liệu SQLite (`kho_hang.db`) tăng tính tin cậy, tự động nạp dữ liệu cũ từ CSV sang SQLite khi chạy lần đầu.
* **Flask REST API**: Tích hợp API Server nội bộ chạy trên một luồng phụ (`http://127.0.0.1:5000`) cung cấp các endpoint JSON hữu ích (`GET/POST/DELETE`).
* **Matplotlib Visualization**: Thêm nút "Biểu Đồ" vẽ biểu đồ cột Top 5 tồn kho và biểu đồ tròn cơ cấu chủng loại trực quan.