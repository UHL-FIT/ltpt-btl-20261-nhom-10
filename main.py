import customtkinter as ctk
import models.kho_hang as model
import views.giao_dien_gui as view
import controllers.dieu_khien_gui as controller

# Phiên bản của ứng dụng (Semantic Versioning)
__version__ = "1.1.3"

def main():
    """
    Hàm khởi chạy chính (Entry Point) của ứng dụng PyWarehouse HIỆN ĐẠI.

    Thực hiện quy trình khởi tạo 3 bước theo kiến trúc MVC:
    1. Model: Khởi tạo dữ liệu và cấu trúc file CSV.
    2. View: Xây dựng giao diện đồ họa hiện đại bằng CustomTkinter.
    3. Controller: Kết nối logic xử lý vào các thành phần giao diện.
    """
    
    # 1. KHỞI TẠO DỮ LIỆU (MODEL)
    model.khoi_tao_csv()
    
    # 2. KHỞI TẠO GIAO DIỆN (VIEW) - Dùng CTk thay vì tk.Tk
    root = ctk.CTk()
    cac_widgets = view.tao_giao_dien_chinh(root)
    
    # 3. KẾT NỐI ĐIỀU KHIỂN (CONTROLLER)
    controller.khoi_tao_dieu_khien(cac_widgets)
    
    # Hiển thị thông báo khởi chạy
    print(f"PyWarehouse v{__version__} đang khởi chạy...")
    
    # Bắt đầu vòng lặp sự kiện
    root.mainloop()

if __name__ == "__main__":
    main()
