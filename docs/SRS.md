# Software Requirements Specification (SRS) - PyWarehouse

## 1. Giới thiệu
Hệ thống PyWarehouse được thiết kế để quản lý kho hàng cho các cửa hàng vừa và nhỏ, giúp theo dõi hàng hóa, giá vốn, giá bán và tình trạng tồn kho.

## 2. Yêu cầu Chức năng (Functional Requirements)

### FR1: Quản lý Sản phẩm
* **Thêm sản phẩm**: Nhập mới SKU, Tên, Phân loại, Số lượng, Giá nhập, Giá bán, Ngày nhập.
* **Sửa sản phẩm**: Thay đổi thông tin sản phẩm dựa trên SKU.
* **Xóa sản phẩm**: Gỡ bỏ sản phẩm khỏi hệ thống.
* **Tìm kiếm**: Tìm kiếm nhanh theo SKU hoặc Tên sản phẩm.

### FR2: Lọc dữ liệu
* **Lọc theo Phân loại**: Dropdown hiển thị danh sách loại sản phẩm, cập nhật tự động từ dữ liệu.
* **Lọc theo Tồn kho**: Dropdown lọc sản phẩm sắp hết hàng (< 10) hoặc còn hàng (≥ 10).
* **Lọc đồng thời**: Ba bộ lọc (Tìm kiếm + Phân loại + Tồn kho) hoạt động kết hợp cùng lúc.

### FR3: Thống kê & Biểu đồ trực quan
* **Tính tổng vốn**: Tổng giá trị hàng trong kho (Số lượng * Giá nhập).
* **Cảnh báo tồn kho**: Hiển thị màu sắc khác biệt cho sản phẩm dưới ngưỡng Min Stock.
* **Vẽ biểu đồ**: Nút vẽ biểu đồ cột Top 5 sản phẩm tồn kho và biểu đồ tròn cơ cấu chủng loại bằng Matplotlib.

### FR4: Giao diện (GUI)
* **Cửa sổ chính**: Hiển thị danh sách sản phẩm dạng bảng (Treeview).
* **Cửa sổ phụ**: Form nhập liệu riêng cho chức năng Thêm và Sửa.
* **Chế độ Sáng/Tối**: Hỗ trợ chuyển đổi giữa giao diện Sáng, Tối và Hệ thống.

### FR5: REST API
* **GET /api/products**: Lấy toàn bộ danh sách sản phẩm dưới dạng JSON.
* **POST /api/products**: Thêm mới sản phẩm từ JSON body.
* **DELETE /api/products/<sku>**: Xóa sản phẩm qua API.
* **GET /api/stats**: Lấy số liệu thống kê tổng quát của kho hàng.

### FR6: Xử lý lưu trữ & File
* **SQLite Database**: Lưu trữ dữ liệu lâu dài trong cơ sở dữ liệu SQLite thay vì file phẳng.
* **Tự động chuyển đổi**: Tự động import dữ liệu từ file CSV cũ sang SQLite khi chạy ứng dụng lần đầu.
* **Import/Export CSV**: Nhập/xuất dữ liệu từ/ra file CSV bên ngoài để lưu trữ dự phòng.

## 3. Yêu cầu Phi chức năng (Non-Functional Requirements)
* **Kiến trúc**: Tuân thủ mô hình MVC kết hợp REST API.
* **Khả năng tương thích**: Chạy độc lập trên Windows 10+ không cần cài đặt Python (sau khi đóng gói .exe).
* **Độ tin cậy**: Kiểm tra dữ liệu đầu vào (Input Validation) và ghi nhật ký hoạt động qua logging.
* **Bảo mật mạng**: REST API server chỉ lắng nghe cục bộ (localhost/127.0.0.1) trên cổng 5000.
