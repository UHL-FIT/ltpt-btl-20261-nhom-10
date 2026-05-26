# PyWarehouse - Tài Liệu Tham Khảo Thuyết Trình

Tài liệu này giúp bạn trả lời nhanh các câu hỏi (Q1 - Q13) từ file yêu cầu dự án.

---

## 🟢 PHẦN 1: ÁNH XẠ CÂU HỎI VÀO MÃ NGUỒN

| Câu hỏi | Nội dung câu hỏi | Vị trí trong Code | Giải thích nhanh cho giảng viên |
|:---:|:---|:---|:---|
| **[Q1]** | Chức năng Thêm xử lý ở đâu? | `controllers/dieu_khien_gui.py` (Dòng 111) | Hàm `hanh_dong_them()` bắt sự kiện từ nút bấm, kiểm tra dữ liệu và gọi Model. |
| **[Q2]** | Muốn thêm dữ liệu mới phải sửa file nào? | Cả 3 lớp MVC | **Model**: Thêm cột hoặc sửa câu lệnh SQL. **View**: Thêm ô nhập/nút. **Controller**: Validate dữ liệu và liên kết chúng. |
| **[Q3]** | Thay đổi màu sắc/icon nút ở đâu? | `views/giao_dien_gui.py` (Dòng 35-50, 127) | Sửa tham số `fg_color` (màu nền), `hover_color` hoặc text (emoji/icon) của các nút. |
| **[Q4]** | Pandas/Numpy tính toán như thế nào? | `models/kho_hang.py` (Dòng 42, 58, 153) | Đọc bằng `pd.read_sql_query` từ SQLite và dùng `np.multiply` trên các giá trị mảng. |
| **[Q5]** | Tại sao dùng Numpy thay vì Python thuần? | `models/kho_hang.py` (Dòng 58) | Sử dụng tính chất Vectorization (xử lý đồng loạt) nhanh hơn vòng lặp `for` thuần nhiều lần. |
| **[Q6]** | Layout Manager nào đảm bảo Auto-resize? | `views/giao_dien_gui.py` (Dòng 26, 27) | Bố cục sử dụng `.grid()` và cấu hình trọng số co giãn bằng `columnconfigure(0, weight=1)` và `rowconfigure(1, weight=1)`. |
| **[Q7]** | Logic Validation (kiểm tra rỗng) đặt ở đâu? | `controllers/dieu_khien_gui.py` (Dòng 116-130) | Đặt ở Controller để chặn lỗi sớm trước khi gửi yêu cầu xuống tầng cơ sở dữ liệu (Model). |
| **[Q8]** | Tùy chỉnh Widget Table hiển thị màu nền? | `controllers/dieu_khien_gui.py` (Dòng 89-100) | Sử dụng tag `"nguy_hiem"` khi insert dòng và cấu hình `tree.tag_configure` sang nền màu đỏ nhạt (#ffcccc). |
| **[Q9]** | Nếu dùng Custom Tkinter thì phải viết lại gì? | Chỉ viết lại lớp **View** | Không cần viết lại logic của Model hay Controller vì cấu trúc MVC tách biệt hoàn toàn giao diện khỏi nghiệp vụ. |
| **[Q10]** | Nếu không dùng Thread cho file lớn thì sao? | Giao diện bị đơ (Not Responding) | Do UI chạy đơn luồng (Single Thread), nếu chạy tác vụ I/O lớn trên luồng chính sẽ gây treo giao diện. |
| **[Q11]** | Cách dùng Thread cho Import CSV? | `controllers/dieu_khien_gui.py` (Dòng 190-201) | Dùng `threading.Thread(target=worker)` và cập nhật lại giao diện bằng `root.after()`. |
| **[Q13]** | Xử lý ngoại lệ (Exception Handling) ở đâu? | `models/kho_hang.py` (Toàn bộ file) | Dùng cấu trúc `try...except` bao quanh mọi hoạt động kết nối SQLite và nhập/xuất file CSV để tránh crash app. |

---

## 🔵 PHẦN 2: CÁC VỊ TRÍ LOGIC QUAN TRỌNG KHÁC

### 1. MODEL (`models/kho_hang.py`)
*   **Dòng 23**: Hàm `khoi_tao_csv()` tạo bảng SQLite và tự động import dữ liệu cũ từ file CSV sang DB nếu phát hiện.
*   **Dòng 153**: Hàm `thong_ke_kho()` thực hiện tính lợi nhuận trung bình nhóm bằng `groupby()` của Pandas dựa trên dữ liệu lấy từ SQLite.

### 2. VIEW (`views/giao_dien_gui.py`)
*   **Dòng 49**: **[NEW]** Bổ sung nút bấm `"📊 Biểu Đồ"`.
*   **Dòng 194**: **[NEW]** Hàm `hien_thi_bieu_do()` nhúng biểu đồ cột và tròn bằng **Matplotlib** (`FigureCanvasTkAgg`) trực quan ngay trên giao diện CustomTkinter.

### 3. CONTROLLER (`controllers/dieu_khien_gui.py`)
*   **Dòng 226**: **[NEW]** Hàm `hanh_dong_bieu_do()` bắt sự kiện khi nhấn nút để hiển thị màn hình biểu đồ.
*   **Dòng 254**: **[NEW]** Khởi chạy Flask REST API server ngầm trên một **Thread phụ** độc lập (`api_server.run_server`).

### 4. REST API SERVER (`api_server.py`)
*   Toàn bộ file định nghĩa các route API JSON (`/api/products`, `/api/stats`) cho Flask.

---
**Ghi chú**: Lưu trữ tài liệu tham khảo này tại `/docs/DOCS_REFERENCE.md`.
