# YÊU CẦU DỰ ÁN: XÂY DỰNG ỨNG DỤNG QUẢN LÝ KHO HÀNG (KIẾN TRÚC MVC)

Dự án yêu cầu xây dựng ứng dụng quản lý kho hàng hoàn chỉnh theo mô hình **MVC**, sử dụng **Tkinter** làm giao diện và **Pandas/Numpy** để xử lý dữ liệu chuyên sâu.

---

## I. MODEL (File: `model.py`)
Đảm nhận vai trò lưu trữ và xử lý logic dữ liệu.

### 1. Yêu cầu lưu trữ
- Sử dụng tệp **CSV** làm cơ sở dữ liệu chính.
- Các trường thông tin cần quản lý:
    - **Mã SKU**: Định danh duy nhất.
    - **Tên sản phẩm**: Tên chi tiết.
    - **Số lượng tồn kho**: Số lượng hiện có.
    - **Giá nhập**: Đơn giá mua vào.
    - **Giá bán**: Đơn giá bán ra.
    - **Ngày nhập**: Ngày đưa sản phẩm vào kho.

### 2. Xử lý dữ liệu với Pandas & Numpy
- Sử dụng **Pandas** để load và quản lý DataFrame từ tệp CSV.
- Sử dụng **Numpy** để tối ưu các phép toán thống kê và xử lý mảng.
- **Nhiệm vụ thống kê:**
    - Tính tổng giá trị hàng tồn kho (Số lượng * Giá nhập).
    - Cảnh báo sản phẩm sắp hết hàng (Dựa trên ngưỡng **Min Stock** cố định).
    - Tính lợi nhuận gộp trung bình theo từng nhóm/loại sản phẩm.

> **[Q4]** Trong model, nhóm đã sử dụng thư viện pandas và numpy để tính toán thống kê (ví dụ: điểm trung bình/lợi nhuận) như thế nào? Hãy mô tả dòng code cụ thể đã dùng để load dữ liệu từ CSV vào DataFrame của pandas.
> 
> **[Q5]** Nếu nhóm dùng numpy để xử lý mảng, hãy nêu một ví dụ về một hàm numpy được nhóm sử dụng và giải thích tại sao không dùng Python thuần mà phải dùng numpy cho tác vụ đó.

---

## II. VIEW (File: `view.py`)
Đảm nhận giao diện đồ họa người dùng (GUI).

### 1. Cấu trúc Windows
- **01 Main Window**:
    - Bảng dữ liệu (`Treeview`) hiển thị danh sách sản phẩm.
    - Các nút chức năng: **Thêm**, **Sửa**, **Xóa**, **Import CSV**, **Export CSV**, **About**.
    - Thanh tìm kiếm theo SKU hoặc Tên.
    - Khu vực hiển thị thông tin thống kê nhanh (Tổng vốn, Số mặt hàng cần nhập).
- **02 Sub Windows**:
    - Cửa sổ Thêm: Form nhập liệu sản phẩm mới.
    - Cửa sổ Sửa: Cho phép thay đổi thông tin sản phẩm đã chọn.

### 2. Yêu cầu UI/UX
- Tùy chỉnh màu sắc chữ, màu nền nút bấm và thêm **Icon** cho các button.
- Sắp xếp widget hài hòa, dễ sử dụng.
- Đảm bảo tính năng **Auto-resize/align**: Giao diện tự động co giãn khi phóng to/thu nhỏ cửa sổ.

> **[Q3]** Nếu muốn thay đổi màu sắc ở chữ/button, hay thay đổi icon button thì cần thay đổi ở hàm nào? Sửa trực tiếp trên mã nguồn rồi chạy lại chương trình.
> 
> **[Q8]** Nhóm đã tùy chỉnh Widget Table như thế nào để hiển thị dữ liệu từ model? Nếu muốn thay đổi màu nền của một dòng dữ liệu theo điều kiện (ví dụ: tô đỏ sản phẩm có tồn kho dưới ngưỡng Min Stock), nhóm sẽ tác động vào Widget nào và thực hiện thay đổi trong lớp nào?
> 
> **[Q6]** Nhóm đã sử dụng Layout Manager nào (.grid(), .pack(), hay .place()) để đảm bảo yêu cầu "Các phần đồ họa của Windows có thể auto resize/align khi tăng kích thước"? Giải thích tại sao việc sử dụng Layout Manager đó lại đáp ứng được yêu cầu này.
> 
> **[Q9]** Nếu nhóm chọn Custom Tkinter hoặc PyQT/PySide thay vì Tkinter thuần túy, nhóm phải viết lại phần nào của view? Việc chuyển đổi này có yêu cầu thay đổi logic nghiệp vụ trong controller không? Tại sao?

---

## III. CONTROLLER (File: `controller.py` hoặc `main.py`)
Điều phối hoạt động giữa Model và View.

### 1. Logic nghiệp vụ
- Tiếp nhận sự kiện từ View (click chuột, nhập văn bản) và gọi các hàm xử lý trong Model.
- Cập nhật hiển thị lên View khi dữ liệu thay đổi.

### 2. Input Validation (Kiểm tra dữ liệu)
- Không để trống thông tin khi thêm/sửa.
- Kiểm tra kiểu dữ liệu (Số lượng, giá phải là số).
- Hiển thị `messagebox` cảnh báo lỗi tương ứng.
- Đảm bảo chỉ chọn duy nhất 1 dòng khi thực hiện lệnh "Sửa".

### 3. Xử lý luồng (Multi-threading)
- Sử dụng **Thread** hoặc **Async** khi Import file CSV lớn để tránh làm treo giao diện.

> **[Q1]** Chức năng này (ví dụ: Thêm sản phẩm) được xử lý logic trong file Python nào? Hàm xử lý sự kiện khi người dùng nhấn nút này nằm ở file nào?
> 
> **[Q2]** Nếu muốn thêm một dữ liệu mới vào bảng, nhóm phải sửa những file nào trong kiến trúc MVC? Mô tả ngắn gọn thay đổi ở mỗi file.
> 
> **[Q7]** Khi thiết kế Sub Window thêm thông tin, nhóm đã đặt logic kiểm tra input validation vào lớp nào (view hay controller) và tại sao?
> 
> **[Q13]** Nhóm đã xử lý ngoại lệ (Exception Handling) cho thao tác "Xóa thông tin" như thế nào? Cụ thể, nếu người dùng cố gắng xóa một bản ghi không tồn tại trong model, đoạn code nào sẽ bắt lỗi đó và thông báo cho người dùng?
> 
> **[Q10]** Tính năng Import CSV với 10.000 dòng mất 5 giây. Nếu không sử dụng Asynctask/Thread, hiện tượng gì sẽ xảy ra với ứng dụng?
> 
> **[Q11]** Hãy mô tả cách nhóm đã sử dụng luồng (Thread) hoặc bất đồng bộ (Async) trong Python để chạy tác vụ Import CSV mà không làm treo GUI, và cách nhóm đảm bảo sau khi import xong, bảng dữ liệu trên GUI được cập nhật.
