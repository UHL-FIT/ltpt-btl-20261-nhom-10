# PyWarehouse - Codebase Context Summary

Tài liệu này tóm tắt toàn bộ cấu trúc và chức năng của dự án **PyWarehouse** tính đến phiên bản **v1.3.1** ("Database Docking").

---

## 🏗️ 1. KIẾN TRÚC HỆ THỐNG (MVC + REST API)

Dự án áp dụng mô hình **Model-View-Controller** mở rộng thêm **REST API**:

*   **Model (`models/kho_hang.py`)**: 
    *   Lưu trữ dữ liệu trong Cơ sở dữ liệu SQLite (`data/kho_hang.db`).
    *   Sử dụng **sqlite3** để truy vấn trực tiếp và **Pandas** để quản lý DataFrame.
    *   Sử dụng **Numpy** để tối ưu tính toán mảng (Tổng vốn, Lợi nhuận).
    *   Cung cấp các hàm CRUD: `them_san_pham`, `sua_san_pham`, `xoa_san_pham`.
    *   Tự động phát hiện và import dữ liệu CSV cũ (`data/kho_hang.csv`) sang SQLite khi khởi động lần đầu.
*   **View (`views/giao_dien_gui.py`)**:
    *   Giao diện hiện đại sử dụng thư viện **CustomTkinter**.
    *   Cửa sổ chính hiển thị bảng dữ liệu (Treeview), thanh công cụ và dashboard thống kê.
    *   Cửa sổ biểu đồ tích hợp **Matplotlib** vẽ thống kê chủng loại & số lượng tồn kho.
    *   Cửa sổ phụ (Popup) dùng cho việc nhập/sửa dữ liệu.
    *   Hỗ trợ đa ngôn ngữ (Tiếng Việt) và chế độ **Dark Mode**.
*   **Controller (`controllers/dieu_khien_gui.py`)**:
    *   Điều phối luồng dữ liệu giữa View và Model.
    *   Xử lý sự kiện (Event Handlers) cho các nút bấm và tích hợp sự kiện mở biểu đồ.
    *   Thực hiện **Input Validation** (kiểm tra lỗi dữ liệu đầu vào).
    *   Xử lý đa luồng (**Multi-threading**) cho tính năng Import CSV và khởi chạy **REST API Server** dưới dạng daemon thread.
*   **API Server (`api_server.py`)**:
    *   Expose các endpoint REST API bằng **Flask** hoạt động song song với giao diện đồ họa.
    *   Các endpoint chính: `GET/POST /api/products`, `DELETE /api/products/<sku>`, và `GET /api/stats`.

---

## 🌟 2. CÁC TÍNH NĂNG CHÍNH

### Quản lý Sản phẩm
*   Thêm mới sản phẩm với đầy đủ thông tin (SKU, Tên, Loại, SL, Giá).
*   Sửa thông tin sản phẩm (khóa mã SKU để đảm bảo định danh duy nhất).
*   Xóa một hoặc nhiều sản phẩm cùng lúc.

### Tìm kiếm & Lọc dữ liệu
*   **Tìm kiếm tức thời**: Bảng tự động lọc khi người dùng gõ phím vào ô tìm kiếm.
*   **Sắp xếp cột**: Click vào tiêu đề cột để sắp xếp Tăng/Giảm dần (Hỗ trợ cả chuỗi và con số).
*   **Lọc theo Phân loại**: Dropdown hiển thị danh sách phân loại động, tự cập nhật khi dữ liệu thay đổi.
*   **Lọc theo Tồn kho**: Dropdown lọc sản phẩm sắp hết hàng (< 10) hoặc còn hàng (≥ 10).
*   **Lọc đồng thời (Stacking)**: Ba bộ lọc (Tìm kiếm + Phân loại + Tồn kho) hoạt động kết hợp.

### Thống kê & Biểu đồ trực quan
*   Tự động tính **Tổng mặt hàng**, **Tổng vốn**, và số lượng **Cần nhập hàng** (nếu SL < 10).
*   Tô màu đỏ cảnh báo các dòng sản phẩm sắp hết hàng trong bảng.
*   **Trực quan hóa dữ liệu**: Hỗ trợ vẽ biểu đồ Matplotlib gồm biểu đồ cột Top 5 tồn kho lớn nhất và biểu đồ tròn cơ cấu ngành hàng ngay trong ứng dụng.

### REST API
*   API JSON chuẩn REST giúp các hệ thống khác có thể tích hợp và kiểm soát kho hàng từ xa.

### Import/Export
*   Hỗ trợ nhập dữ liệu hàng loạt từ file CSV bên ngoài vào SQLite.
*   Xuất toàn bộ cơ sở dữ liệu hiện tại ra file CSV chuẩn Excel.

### Giao diện
*   Hỗ trợ chế độ **Dark Mode** cho các thành phần CustomTkinter.
*   Giao diện hoàn toàn bằng **Tiếng Việt**.
*   Nút chuyển đổi giao diện: Hệ thống / Tối / Sáng.

---

## 🛠️ 3. CÔNG NGHỆ SỬ DỤNG
*   **Ngôn ngữ**: Python 3.10+
*   **Cơ sở dữ liệu**: SQLite (sqlite3).
*   **API Server**: Flask.
*   **Thống kê/Vẽ biểu đồ**: Pandas, Numpy, Matplotlib.
*   **Giao diện**: CustomTkinter, Tkinter (ttk).
*   **Đóng gói**: PyInstaller (tạo file .exe).
*   **Kiểm thử**: Unittest.

