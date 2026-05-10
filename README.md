# PyWarehouse - Phần Mềm Quản Lý Kho Hàng (MVC)

PyWarehouse là một ứng dụng Python chuyên dụng giúp quản lý hàng hóa trong kho, theo dõi số lượng tồn kho, tính toán lợi nhuận và đưa ra các cảnh báo nhập hàng một cách trực quan, sử dụng kiến trúc MVC.

## Tính năng nổi bật
1. **Kiến trúc MVC chuẩn**: Tách biệt rõ ràng giữa Dữ liệu (Model), Giao diện (View) và Điều khiển (Controller).
2. **Quản lý Hàng hóa**: Thêm, Sửa, Xoá, và Tìm kiếm sản phẩm theo Mã SKU hoặc Tên sản phẩm.
3. **Xử lý Dữ liệu mạnh mẽ**: Sử dụng Pandas và Numpy để tính toán giá trị kho, lợi nhuận gộp và thống kê hàng tồn.
4. **Cảnh báo Thông minh**: Tự động cảnh báo các sản phẩm có số lượng dưới ngưỡng tối thiểu (Min Stock).
5. **Giao diện thân thiện**: Xây dựng bằng Tkinter với khả năng tự động co giãn (Auto-resize) và icon trực quan.
6. **Nhập/Xuất Dữ liệu**: Hỗ trợ Import và Export qua file `.csv` hàng loạt.

## Cấu trúc Dự án
```
PyWarehouse/
├── assets/                  # Icon và tài nguyên ảnh
├── controllers/             # Logic điều khiển (dieu_khien_gui.py, dieu_khien_cli.py)
├── data/                    # Cơ sở dữ liệu CSV (kho_hang.csv)
├── models/                  # Xử lý dữ liệu với Pandas/Numpy (kho_hang.py)
├── templates/               # Mẫu CSV để nhập liệu (mau_kho_hang.csv)
├── utils/                   # Tiện ích ghi log (logger.py)
├── views/                   # Giao diện người dùng (giao_dien_gui.py, giao_dien_cli.py)
├── main.py                  # Điểm khởi chạy ứng dụng
├── requirements.txt         # Các thư viện cần thiết (pandas, numpy, tkinter)
├── README.md                # Hướng dẫn sử dụng tổng quan
├── CONVENTIONS.md           # Quy chuẩn viết code
├── SRS.md                   # Đặc tả yêu cầu hệ thống
└── SAD.md                   # Tài liệu thiết kế kiến trúc
```

## Hướng dẫn cài đặt

1. **Cài đặt môi trường**: Chạy file `setup_env.bat` để tạo môi trường ảo và cài đặt thư viện.
2. **Chạy ứng dụng**: 
   - Mở terminal, kích hoạt môi trường ảo: `.venv\Scripts\activate`
   - Chạy lệnh: `python main.py`
3. **Đóng gói**: Chạy `build.bat` để tạo file `.exe`.

## Tác giả
* **Nhóm phát triển PyWarehouse**
* Dự án cuối kỳ môn Lập trình Python.
