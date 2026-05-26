# 📦PyWarehouse - Phần Mềm Quản Lý Kho Hàng (Kiến Trúc MVC + DB & API)

![Python](https://img.shields.io/badge/python-3.10+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/Pandas-3.0.2-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-2.4.4-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Windows](https://img.shields.io/badge/dành_cho-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Version](https://img.shields.io/badge/phiên_bản_hiện_tại-v1.3.0-7303fc?style=for-the-badge)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg?style=for-the-badge)
#

PyWarehouse là một ứng dụng Python chuyên dụng dành cho các cửa hàng vừa và nhỏ, giúp quản lý thông tin hàng hóa, theo dõi tồn kho, tính toán lợi nhuận dự kiến và đưa ra các cảnh báo nhập hàng một cách trực quan và khoa học.

Dự án được xây dựng dựa trên kiến trúc **MVC (Model-View-Controller)** chuẩn mực, nâng cấp thêm hệ thống cơ sở dữ liệu **SQLite**, dịch vụ **REST API bằng Flask** chạy nền và vẽ biểu đồ phân tích trực quan bằng **Matplotlib**.

## 🚀 Tính năng nổi bật
1. **Kiến trúc MVC**: Tách biệt hoàn toàn Logic dữ liệu, Giao diện và Bộ điều phối, giúp mã nguồn dễ bảo trì và mở rộng.
2. **Cơ sở dữ liệu SQLite**: Chuyển đổi từ file CSV phẳng sang SQLite (`data/kho_hang.db`) để lưu trữ dữ liệu an toàn và thực hiện truy vấn nhanh chóng. Có tính năng tự động chuyển dữ liệu cũ từ CSV sang SQLite khi chạy lần đầu.
3. **REST API Service**: Máy chủ Flask chạy đa luồng ngầm song song hỗ trợ tích hợp dữ liệu với các ứng dụng khác (`http://127.0.0.1:5000/api/...`).
4. **Biểu đồ trực quan**: Bổ sung tính năng vẽ biểu đồ cột (Top 5 sản phẩm tồn kho) và biểu đồ tròn (cơ cấu chủng loại) tích hợp bằng thư viện **Matplotlib**.
5. **Cảnh báo Tồn kho**: Tự động dán nhãn màu đỏ cho các mặt hàng có số lượng dưới ngưỡng tối thiểu (Min Stock).
6. **Xử lý tệp tin**: Nhập (Import) và Xuất (Export) dữ liệu hàng loạt qua định dạng CSV chuẩn Excel.

## 📁 Cấu trúc Dự án
```text
PyWarehouse/
├── controllers/             # Layer Controller: Điều phối luồng dữ liệu (dieu_khien_gui.py)
├── data/                    # Nơi lưu trữ cơ sở dữ liệu (kho_hang.db) và logs
├── docs/                    # Thư mục chứa tài liệu đặc tả môn học và dự án (.md)
├── models/                  # Layer Model: Xử lý logic nghiệp vụ và SQL (kho_hang.py)
├── templates/               # Mẫu file CSV để người dùng nhập liệu (mau_kho_hang.csv)
├── utils/                   # Tiện ích bổ trợ (logger.py)
├── views/                   # Layer View: Xây dựng giao diện và Biểu đồ (giao_dien_gui.py)
├── tests/                   # Bộ kiểm thử tự động (test_kho_hang.py)
├── api_server.py            # API REST endpoints điều phối dữ liệu dạng JSON bằng Flask
├── main.py                  # Điểm khởi chạy (Entry Point) của ứng dụng
└── README.md                # Hướng dẫn sử dụng và giới thiệu tổng quan
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
Yêu cầu Python từ phiên bản **3.10** hoặc **3.11** trở lên.
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
*Lưu ý:* Khi ứng dụng chạy, một máy chủ REST API cục bộ sẽ tự động được khởi chạy song song tại địa chỉ `http://127.0.0.1:5000`.

### 4. Sử dụng REST API (Ví dụ)
Bạn có thể dùng trình duyệt web, Postman, hoặc lệnh `curl` để gọi API:
* **Lấy danh sách sản phẩm**: `GET http://127.0.0.1:5000/api/products`
* **Lấy thống kê tổng quan**: `GET http://127.0.0.1:5000/api/stats`

### 5. Chạy kiểm thử (Unit Tests)
Để đảm bảo logic tính toán của Model vẫn hoạt động đúng sau khi bạn sửa code, hãy chạy:
```bash
.\run_tests.bat
```

### 6. Đóng gói ứng dụng thành file .exe
Nếu bạn muốn đóng gói toàn bộ ứng dụng (bao gồm cả GUI, SQLite, Flask, Matplotlib) thành file chạy độc lập trên mọi máy Windows 10+:
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