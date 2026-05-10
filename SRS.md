# Software Requirements Specification (SRS) - PyWarehouse

## 1. Giới thiệu
Hệ thống PyWarehouse được thiết kế để quản lý kho hàng cho các cửa hàng vừa và nhỏ, giúp theo dõi hàng hóa, giá vốn, giá bán và tình trạng tồn kho.

## 2. Yêu cầu Chức năng (Functional Requirements)

### FR1: Quản lý Sản phẩm
* **Thêm sản phẩm**: Nhập mới SKU, Tên, Số lượng, Giá nhập, Giá bán, Ngày nhập.
* **Sửa sản phẩm**: Thay đổi thông tin sản phẩm dựa trên SKU.
* **Xóa sản phẩm**: Gỡ bỏ sản phẩm khỏi hệ thống.
* **Tìm kiếm**: Tìm kiếm nhanh theo SKU hoặc Tên sản phẩm.

### FR2: Thống kê & Báo cáo
* **Tính tổng vốn**: Tổng giá trị hàng trong kho (Số lượng * Giá nhập).
* **Cảnh báo tồn kho**: Hiển thị màu sắc khác biệt cho sản phẩm dưới ngưỡng Min Stock.
* **Tính lợi nhuận**: Tính lợi nhuận gộp dự kiến dựa trên giá nhập và giá bán.

### FR3: Giao diện (GUI)
* **Cửa sổ chính**: Hiển thị danh sách sản phẩm dạng bảng (Treeview).
* **Cửa sổ phụ**: Form nhập liệu riêng cho chức năng Thêm và Sửa.
* **Tính thẩm mỹ**: Có icon, màu sắc nút bấm và hỗ trợ tự động co giãn cửa sổ.

### FR4: Xử lý file
* **Import CSV**: Đọc dữ liệu từ file CSV mẫu.
* **Export CSV**: Xuất dữ liệu hiện tại ra file CSV.

## 3. Yêu cầu Phi chức năng (Non-Functional Requirements)
* **Kiến trúc**: Tuân thủ mô hình MVC.
* **Hiệu năng**: Sử dụng Numpy/Pandas để xử lý dữ liệu nhanh chóng.
* **Độ tin cậy**: Kiểm tra dữ liệu đầu vào (Input Validation) và thông báo lỗi qua Messagebox.
