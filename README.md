# 📦PyWarehouse - Phần Mềm Quản Lý Kho Hàng (Kiến Trúc MVC)

![Python](https://img.shields.io/badge/python-3.14-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/Pandas-3.0.2-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-2.4.4-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Windows](https://img.shields.io/badge/dành_cho-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Version](https://img.shields.io/badge/phiên_bản_hiện_tại-v1.0.0-7303fc?style=for-the-badge)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg?style=for-the-badge)
#

PyWarehouse là một ứng dụng Python chuyên dụng dành cho các cửa hàng vừa và nhỏ, giúp quản lý thông tin hàng hóa, theo dõi tồn kho, tính toán lợi nhuận dự kiến và đưa ra các cảnh báo nhập hàng một cách trực quan và khoa học.

Dự án được xây dựng dựa trên kiến trúc **MVC (Model-View-Controller)** chuẩn mực, sử dụng thư viện mạnh mẽ như **Pandas** và **Numpy** để xử lý dữ liệu.

## 🚀 Tính năng nổi bật
1. **Kiến trúc MVC**: Tách biệt hoàn toàn Logic dữ liệu, Giao diện và Bộ điều phối, giúp mã nguồn dễ bảo trì và mở rộng.
2. **Quản lý Sản phẩm chuyên sâu**: Thêm, Sửa, Xoá, và Tìm kiếm nhanh chóng theo SKU hoặc Tên.
3. **Phân tích Dữ liệu thông minh**:
   - Sử dụng **Pandas/Numpy** tính toán Tổng vốn và Lợi nhuận tức thời.
   - Thống kê lợi nhuận trung bình theo từng nhóm sản phẩm (Phân loại).
4. **Cảnh báo Tồn kho**: Tự động dán nhãn màu đỏ cho các mặt hàng có số lượng dưới ngưỡng tối thiểu (Min Stock).
5. **Giao diện hiện đại**: Xây dựng bằng Tkinter, hỗ trợ **Auto-resize** linh hoạt khi thay đổi kích thước cửa sổ.
6. **Xử lý tệp tin**: Nhập (Import) và Xuất (Export) dữ liệu hàng loạt qua định dạng CSV chuẩn Excel.
7. **Đa luồng (Multi-threading)**: Tác vụ Import file lớn được xử lý ngầm, không gây treo giao diện người dùng.

## 📁 Cấu trúc Dự án
```text
PyWarehouse/
├── assets/                  # Tài nguyên (Icon, ảnh ứng dụng)
├── controllers/             # Layer Controller: Điều phối luồng dữ liệu (dieu_khien_gui.py)
├── data/                    # Nơi lưu trữ cơ sở dữ liệu (kho_hang.csv) và logs
├── models/                  # Layer Model: Xử lý logic nghiệp vụ và tính toán (kho_hang.py)
├── templates/               # Mẫu file CSV để người dùng nhập liệu (mau_kho_hang.csv)
├── utils/                   # Tiện ích bổ trợ (logger.py)
├── views/                   # Layer View: Xây dựng giao diện người dùng (giao_dien_gui.py)
├── tests/                   # Bộ kiểm thử tự động (test_kho_hang.py)
├── main.py                  # Điểm khởi chạy (Entry Point) của ứng dụng
├── README.md                # Hướng dẫn sử dụng và giới thiệu tổng quan
├── CONVENTIONS.md           # Quy chuẩn viết mã và tài liệu
├── SRS.md                   # Đặc tả yêu cầu hệ thống
└── SAD.md                   # Tài liệu thiết kế kiến trúc phần mềm
```

## 🛠️ Hướng dẫn cài đặt

Thực hiện các bước sau để thiết lập môi trường chạy mã nguồn trên máy tính của bạn:

### 1. Tải mã nguồn (Clone Repository)
Mở terminal (hoặc Git Bash) và chạy lệnh:
```bash
git clone https://github.com/UHL-FIT/ltpt-btl-20261-nhom-10.git
cd ltpt-btl-20261-nhom-10
```

### 2. Khởi tạo môi trường ảo (Virtual Environment)
Để tránh xung đột thư viện giữa các dự án, bạn nên sử dụng môi trường ảo.
- **Cách 1 (Tự động trên Windows)**: Chạy file script được cung cấp sẵn:
  ```bash
  .\setup_env.bat
  ```
- **Cách 2 (Thủ công)**:
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  ```

### 3. Khởi chạy ứng dụng
Sau khi đã kích hoạt môi trường ảo, chạy lệnh:
```bash
python main.py
```

### 4. Chạy kiểm thử (Unit Tests)
Để đảm bảo logic tính toán của Model vẫn hoạt động đúng sau khi bạn sửa code, hãy chạy:
```bash
.\run_tests.bat
```

### 5. Đóng gói ứng dụng thành file .exe
Nếu bạn muốn chia sẻ ứng dụng cho người khác mà không cần cài đặt Python, hãy chạy:
```bash
.\build.bat
```
Kết quả sẽ nằm trong thư mục `dist/`.

## 👥 Tác giả
* **Nhóm 10 (TT02A) - PyWarehouse**
* Thành viên: Vũ Tuấn Hưng (Trưởng Nhóm), Nguyễn Mạnh Hưng, Lương Quốc Khánh, Tạ Minh Thành
* Trường Đại học Hạ Long (UHL).

## Khác
[![Star History Chart](https://api.star-history.com/chart?repos=ltpt-btl-20261-nhom-10/ltpt-btl-20261-nhom-10&type=date&legend=top-left)](https://www.star-history.com/?repos=Nhom10%2FPyWarehouse&type=date&legend=top-left)

***Revision 1.4***