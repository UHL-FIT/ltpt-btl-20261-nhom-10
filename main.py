import tkinter as tk
import models.kho_hang as model
import views.giao_dien_gui as view
import controllers.dieu_khien_gui as controller

# Phiên bản của ứng dụng (Semantic Versioning)
__version__ = "1.0.0"

def main():
    """
    Hàm khởi chạy chính (Entry Point) của ứng dụng PyWarehouse.

    Thực hiện quy trình khởi tạo 3 bước theo kiến trúc MVC:
    1. Model: Khởi tạo dữ liệu và cấu trúc file CSV.
    2. View: Xây dựng các thành phần giao diện đồ họa.
    3. Controller: Kết nối logic xử lý vào các thành phần giao diện.
    """
    
    # 1. KHỞI TẠO DỮ LIỆU (MODEL)
    # Đảm bảo file CSV và các thư mục cần thiết đã sẵn sàng
    model.khoi_tao_csv()
    
    # 2. KHỞI TẠO GIAO DIỆN (VIEW)
    # Tạo cửa sổ gốc Tkinter và thiết lập các Widget
    root = tk.Tk()
    cac_widgets = view.tao_giao_dien_chinh(root)
    
    # 3. KẾT NỐI ĐIỀU KHIỂN (CONTROLLER)
    # Gắn logic nghiệp vụ vào các sự kiện trên giao diện
    controller.khoi_tao_dieu_khien(cac_widgets)
    
    # Hiển thị thông báo khởi chạy trong Console để debug
    print(f"PyWarehouse v{__version__} đang khởi chạy...")
    
    # Bắt đầu vòng lặp sự kiện chính của ứng dụng
    root.mainloop()

# Điểm bắt đầu thực thi của chương trình Python
if __name__ == "__main__":
    main()
