# Software Architecture Document (SAD) - PyWarehouse

## 1. Mô hình Kiến trúc
PyWarehouse áp dụng kiến trúc **MVC (Model-View-Controller)**:

*   **Model (`models/kho_hang.py`)**: 
    *   Quản lý DataFrame của Pandas.
    *   Thực hiện các phép toán mảng bằng Numpy để tính toán thống kê.
    *   Đọc/Ghi trực tiếp vào file `data/kho_hang.csv`.
*   **View (`views/giao_dien_gui.py`)**:
    *   Xây dựng giao diện bằng Tkinter.
    *   Quản lý các Widget: Treeview, Entry, Button, Label.
    *   Xử lý việc hiển thị thông tin và nhận tương tác từ người dùng.
*   **Controller (`controllers/dieu_khien_gui.py`)**:
    *   Trung gian kết nối Model và View.
    *   Kiểm tra tính hợp lệ của dữ liệu (Validation).
    *   Xử lý đa luồng (Threading) khi thực hiện các tác vụ nặng như Import dữ liệu lớn.

## 2. Luồng xử lý chính
1. Người dùng tương tác với **View** (ví dụ: nhấn nút Thêm).
2. **View** gửi dữ liệu đến **Controller**.
3. **Controller** kiểm tra dữ liệu, sau đó gọi hàm tương ứng trong **Model**.
4. **Model** cập nhật dữ liệu vào CSV và trả về kết quả cho **Controller**.
5. **Controller** yêu cầu **View** cập nhật lại bảng hiển thị.

## 3. Công nghệ sử dụng
*   **Ngôn ngữ**: Python 3.9+
*   **Thư viện**: Pandas, Numpy, Tkinter, Logging, Threading.
