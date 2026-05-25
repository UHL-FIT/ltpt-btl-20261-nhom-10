# Software Architecture Document (SAD) - PyWarehouse

## 1. Mô hình Kiến trúc
PyWarehouse áp dụng kiến trúc **MVC (Model-View-Controller)** kết hợp **REST API**:

*   **Model (`models/kho_hang.py`)**: 
    *   Truy vấn trực tiếp qua SQLite (`data/kho_hang.db`).
    *   Tự động nạp dữ liệu cũ từ CSV sang SQLite khi chạy lần đầu.
    *   Thực hiện các phép toán mảng bằng Numpy để tính toán thống kê.
*   **View (`views/giao_dien_gui.py`)**:
    *   Xây dựng giao diện bằng CustomTkinter + Tkinter (ttk).
    *   Tích hợp vẽ biểu đồ trực quan hóa dữ liệu bằng Matplotlib (`FigureCanvasTkAgg`).
*   **Controller (`controllers/dieu_khien_gui.py`)**:
    *   Trung gian kết nối Model và View.
    *   Kiểm tra tính hợp lệ của dữ liệu (Validation).
    *   Xử lý đa luồng (Threading): Import dữ liệu và chạy Flask REST API Server ở chế độ daemon thread.
*   **REST API (`api_server.py`)**:
    *   Cung cấp các API endpoint dạng JSON cho phép hệ thống khác truy vấn và quản lý kho hàng từ xa.

## 2. Luồng xử lý chính
1. Người dùng tương tác với **View** (ví dụ: nhấn nút Thêm).
2. **View** gửi dữ liệu đến **Controller**.
3. **Controller** kiểm tra dữ liệu, sau đó gọi hàm tương ứng trong **Model**.
4. **Model** cập nhật dữ liệu vào SQLite và trả về kết quả cho **Controller**.
5. **Controller** yêu cầu **View** cập nhật lại bảng hiển thị và dashboard.

## 3. Luồng lọc dữ liệu (v1.4)
1. Người dùng thay đổi dropdown **Phân loại** hoặc **Tồn kho**, hoặc gõ từ khóa tìm kiếm.
2. **Controller** lấy toàn bộ dữ liệu từ **Model** (DataFrame từ SQLite).
3. Áp dụng lần lượt 3 bộ lọc (stacking): Tìm kiếm → Phân loại → Tồn kho.
4. Kết quả được hiển thị lên **Treeview** (các sản phẩm sắp hết hàng < 10 được tô màu đỏ).

## 4. Công nghệ sử dụng
*   **Ngôn ngữ**: Python 3.10+
*   **Thư viện**: Pandas, Numpy, CustomTkinter, sqlite3, Flask, Matplotlib, Logging, Threading.
