# Software Architecture Document (SAD) - PyWarehouse

## 1. Mô hình Kiến trúc
PyWarehouse áp dụng kiến trúc **MVC (Model-View-Controller)**:

*   **Model (`models/kho_hang.py`)**: 
    *   Quản lý DataFrame của Pandas.
    *   Thực hiện các phép toán mảng bằng Numpy để tính toán thống kê.
    *   Đọc/Ghi trực tiếp vào file `data/kho_hang.csv`.
*   **View (`views/giao_dien_gui.py`)**:
    *   Xây dựng giao diện bằng CustomTkinter + Tkinter (ttk).
    *   Quản lý các Widget: Treeview, CTkEntry, CTkButton, CTkLabel, CTkOptionMenu.
    *   Xử lý việc hiển thị thông tin và nhận tương tác từ người dùng.
*   **Controller (`controllers/dieu_khien_gui.py`)**:
    *   Trung gian kết nối Model và View.
    *   Kiểm tra tính hợp lệ của dữ liệu (Validation).
    *   Xử lý đa luồng (Threading) khi thực hiện các tác vụ nặng như Import dữ liệu lớn.
    *   Quản lý bộ lọc dữ liệu: cập nhật danh sách phân loại động và áp dụng bộ lọc đồng thời.

## 2. Luồng xử lý chính
1. Người dùng tương tác với **View** (ví dụ: nhấn nút Thêm).
2. **View** gửi dữ liệu đến **Controller**.
3. **Controller** kiểm tra dữ liệu, sau đó gọi hàm tương ứng trong **Model**.
4. **Model** cập nhật dữ liệu vào CSV và trả về kết quả cho **Controller**.
5. **Controller** yêu cầu **View** cập nhật lại bảng hiển thị.

## 3. Luồng lọc dữ liệu (v1.2)
1. Người dùng thay đổi dropdown **Phân loại** hoặc **Tồn kho**, hoặc gõ từ khóa tìm kiếm.
2. **Controller** lấy toàn bộ dữ liệu từ **Model** (DataFrame).
3. Áp dụng lần lượt 3 bộ lọc (stacking): Tìm kiếm → Phân loại → Tồn kho.
4. Kết quả được hiển thị lên **Treeview**.

## 4. Công nghệ sử dụng
*   **Ngôn ngữ**: Python 3.9+
*   **Thư viện**: Pandas, Numpy, CustomTkinter, Tkinter (ttk), Logging, Threading.
