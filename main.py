import tkinter as tk
import models.kho_hang as model
import views.giao_dien_gui as view
import controllers.dieu_khien_gui as controller

# Phiên bản của ứng dụng (Semantic Versioning)
__version__ = "1.0.0"

def main():
    """
    Hàm khởi chạy chính của ứng dụng PyWarehouse.
    Thực hiện theo các bước của kiến trúc MVC.
    """
    
    # 1. KHỞI TẠO DỮ LIỆU (MODEL)
    # Tạo file CSV và thư mục cần thiết nếu chưa tồn tại
    model.khoi_tao_csv()
    
    # 2. KHỞI TẠO GIAO DIỆN (VIEW)
    # Tạo cửa sổ gốc của Tkinter
    root = tk.Tk()
    
    # Gọi hàm xây dựng giao diện từ View
    cac_widgets = view.tao_giao_dien_chinh(root)
    
    # 3. KẾT NỐI ĐIỀU KHIỂN (CONTROLLER)
    # Gắn các logic xử lý dữ liệu vào các nút bấm trên giao diện
    controller.khoi_tao_dieu_khien(cac_widgets)
    
    # Hiển thị thông tin phiên bản ở tiêu đề hoặc log
    print(f"PyWarehouse v{__version__} đang khởi chạy...")
    
    # Bắt đầu vòng lặp sự kiện của GUI
    root.mainloop()

# Điểm bắt đầu của chương trình Python
if __name__ == "__main__":
    main()
