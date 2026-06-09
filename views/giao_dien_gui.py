import customtkinter as ctk
from tkinter import ttk, messagebox
import os

# Cấu hình giao diện mặc định
ctk.set_appearance_mode("System")  # Chế độ "System", "Dark" hoặc "Light"
ctk.set_default_color_theme("blue") # Chủ đề màu: "blue", "green", "dark-blue"

def tao_giao_dien_chinh(root):
    """
    Khởi tạo giao diện chính HIỆN ĐẠI cho PyWarehouse bằng CustomTkinter.

    Xây dựng bố cục bao gồm thanh công cụ, bảng dữ liệu (Treeview) và thanh thống kê.
    Hỗ trợ tính năng tự động co giãn khi người dùng thay đổi kích thước cửa sổ.

    Args:
        root (ctk.CTk): Cửa sổ gốc của ứng dụng CustomTkinter.

    Returns:
        dict: Chứa các tham chiếu tới các widget chính (nút, bảng, ô nhập liệu...).
    """
    root.title("PyWarehouse - Quản Lý Kho Hàng - v1.3.1")
    root.geometry("1400x750")
    
    # [Q6] Cấu hình trọng số co giãn
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    # ─── THANH CÔNG CỤ (TOOLBAR) ──────────────────────────────
    # Dùng CTkFrame để có bo góc và màu sắc hiện đại
    toolbar = ctk.CTkFrame(root, corner_radius=10)
    toolbar.grid(row=0, column=0, sticky="ew", padx=15, pady=15)

    # Các nút bấm hiện đại (Tự động bo góc và có hiệu ứng hover)
    btn_them = ctk.CTkButton(toolbar, text="➕ Thêm Mới", fg_color="#2ecc71", hover_color="#27ae60", width=120, font=("Arial", 13, "bold"))
    btn_them.pack(side="left", padx=10, pady=10)

    btn_sua = ctk.CTkButton(toolbar, text="✏️ Sửa", fg_color="#3498db", hover_color="#2980b9", width=100, font=("Arial", 13, "bold"))
    btn_sua.pack(side="left", padx=10, pady=10)

    btn_xoa = ctk.CTkButton(toolbar, text="🗑️ Xóa", fg_color="#e74c3c", hover_color="#c0392b", width=100, font=("Arial", 13, "bold"))
    btn_xoa.pack(side="left", padx=10, pady=10)

    btn_import = ctk.CTkButton(toolbar, text="📥 Nhập CSV", fg_color="#9b59b6", hover_color="#8e44ad", width=120, font=("Arial", 13, "bold"))
    btn_import.pack(side="left", padx=10, pady=10)

    btn_export = ctk.CTkButton(toolbar, text="📤 Xuất CSV", fg_color="#f39c12", hover_color="#d35400", width=120, font=("Arial", 13, "bold"))
    btn_export.pack(side="left", padx=10, pady=10)

    btn_bieu_do = ctk.CTkButton(toolbar, text="📊 Biểu Đồ", fg_color="#16a085", hover_color="#1abc9c", width=110, font=("Arial", 13, "bold"))
    btn_bieu_do.pack(side="left", padx=10, pady=10)

    # ─── BỘ LỌC DỮ LIỆU (FILTER DROPDOWNS) ──────────────────
    # Dropdown lọc theo phân loại sản phẩm (nội dung được cập nhật động từ Controller)
    filter_loai = ctk.CTkOptionMenu(toolbar, values=["Tất cả"], width=140,
                                     fg_color="#1abc9c", button_color="#16a085",
                                     button_hover_color="#0e8c73",
                                     font=("Arial", 12, "bold"))
    filter_loai.pack(side="left", padx=5, pady=10)

    # Dropdown lọc theo tình trạng tồn kho
    filter_ton_kho = ctk.CTkOptionMenu(toolbar, values=["Tất cả", "Sắp hết hàng", "Còn hàng"], width=150,
                                        fg_color="#1abc9c", button_color="#16a085",
                                        button_hover_color="#0e8c73",
                                        font=("Arial", 12, "bold"))
    filter_ton_kho.pack(side="left", padx=5, pady=10)

    # Ô tìm kiếm hiện đại
    entry_tim_kiem = ctk.CTkEntry(toolbar, placeholder_text="🔍 Tìm mã SKU hoặc tên...", width=250, height=35)
    entry_tim_kiem.pack(side="right", padx=15, pady=10)

    # ─── BẢNG DỮ LIỆU (TREEVIEW) ─────────────────────
    # Treeview vẫn dùng thư viện ttk nhưng đặt trong CTkFrame để đồng bộ
    frame_bang = ctk.CTkFrame(root, corner_radius=10)
    frame_bang.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)

    style = ttk.Style()
    style.configure("Treeview", rowheight=30, font=("Arial", 10))
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

    cac_cot = ("sku", "ten", "loai", "sl", "gia_n", "gia_b", "ngay", "tong")
    tree = ttk.Treeview(frame_bang, columns=cac_cot, show="headings")

    # Định nghĩa tiêu đề cho từng cột
    tree.heading("sku", text="Mã SKU")
    tree.heading("ten", text="Tên Sản Phẩm")
    tree.heading("loai", text="Phân Loại")
    tree.heading("sl", text="Tồn Kho")
    tree.heading("gia_n", text="Giá Nhập")
    tree.heading("gia_b", text="Giá Bán")
    tree.heading("ngay", text="Ngày Nhập")
    tree.heading("tong", text="Tổng Vốn")

    # Căn chỉnh độ rộng và vị trí text trong các cột
    tree.column("sku", width=80, anchor="center")
    tree.column("ten", width=250)
    tree.column("loai", width=120)
    tree.column("sl", width=80, anchor="center")
    tree.column("gia_n", width=100, anchor="e")
    tree.column("gia_b", width=100, anchor="e")
    tree.column("ngay", width=110, anchor="center")
    tree.column("tong", width=130, anchor="e")

    tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # ─── THANH THỐNG KÊ (DASHBOARD) ──────────────────────────
    status_bar = ctk.CTkFrame(root, height=60, corner_radius=0)
    status_bar.grid(row=2, column=0, sticky="ew", pady=(10, 0))

    lbl_tong_hang = ctk.CTkLabel(status_bar, text="Mặt hàng: 0", font=("Arial", 14, "bold"))
    lbl_tong_hang.pack(side="left", padx=30, pady=15)

    lbl_tong_von = ctk.CTkLabel(status_bar, text="Vốn: 0 VNĐ", font=("Arial", 14, "bold"))
    lbl_tong_von.pack(side="left", padx=30, pady=15)

    lbl_can_nhap = ctk.CTkLabel(status_bar, text="Cần nhập: 0", font=("Arial", 14, "bold"), text_color="#e74c3c")
    lbl_can_nhap.pack(side="left", padx=30, pady=15)

    # Nút chuyển đổi giao diện Sáng/Tối (nhãn tiếng Việt)
    # Ánh xạ tiếng Việt → giá trị CustomTkinter
    def doi_giao_dien(lua_chon):
        bang_doi = {"Hệ thống": "System", "Tối": "Dark", "Sáng": "Light"}
        ctk.set_appearance_mode(bang_doi.get(lua_chon, "System"))

    btn_theme = ctk.CTkOptionMenu(status_bar, values=["Hệ thống", "Tối", "Sáng"], 
                                 command=doi_giao_dien, width=100)
    btn_theme.pack(side="right", padx=20)

    # Nút Giới Thiệu — đặt ở thanh trạng thái, bên trái nút đổi giao diện
    btn_about = ctk.CTkButton(status_bar, text="ℹ️ Giới Thiệu", fg_color="#95a5a6", hover_color="#7f8c8d", width=120, font=("Arial", 13, "bold"))
    btn_about.pack(side="right", padx=10)

    # Trả về widgets (bao gồm cả bộ lọc mới)
    return {
        "root": root, "tree": tree, "btn_them": btn_them, "btn_sua": btn_sua,
        "btn_xoa": btn_xoa, "btn_import": btn_import, "btn_export": btn_export,
        "btn_bieu_do": btn_bieu_do, "btn_about": btn_about,
        "entry_tim_kiem": entry_tim_kiem,
        "filter_loai": filter_loai, "filter_ton_kho": filter_ton_kho,
        "lbl_tong_hang": lbl_tong_hang, "lbl_tong_von": lbl_tong_von, "lbl_can_nhap": lbl_can_nhap
    }


def hien_thi_form_nhap_lieu(parent, tieu_de, data_cu=None):
    """
    Tạo một cửa sổ phụ (Sub Window) dưới dạng popup để người dùng nhập/sửa thông tin.

    Args:
        parent (ctk.CTkToplevel/ctk.CTk): Cửa sổ cha để gắn popup vào.
        tieu_de (str): Tiêu đề hiển thị của cửa sổ popup.
        data_cu (dict, optional): Dữ liệu cũ để điền sẵn vào form khi thực hiện Sửa.

    Returns:
        dict: Chứa các tham chiếu tới các ô nhập liệu (Entry) và nút Lưu.
    """
    window = ctk.CTkToplevel(parent)
    window.title(tieu_de)
    window.geometry("450x550")
    window.grab_set()

    frame = ctk.CTkFrame(window, corner_radius=15)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(frame, text=tieu_de, font=("Arial", 20, "bold")).pack(pady=20)

    def tao_o_nhap(label_text, default_val=""):
        f = ctk.CTkFrame(frame, fg_color="transparent")
        f.pack(fill="x", padx=30, pady=5)
        ctk.CTkLabel(f, text=label_text, width=100, anchor="w").pack(side="left")
        e = ctk.CTkEntry(f, width=200)
        e.pack(side="right")
        if default_val: e.insert(0, default_val)
        return e

    e_sku = tao_o_nhap("Mã SKU:", data_cu['ma_sku'] if data_cu else "")
    if data_cu: e_sku.configure(state="disabled")
    
    e_ten = tao_o_nhap("Tên SP:", data_cu['ten_san_pham'] if data_cu else "")
    e_loai = tao_o_nhap("Phân loại:", data_cu['loai_san_pham'] if data_cu else "")
    e_sl = tao_o_nhap("Số lượng:", data_cu['so_luong'] if data_cu else "")
    e_gn = tao_o_nhap("Giá nhập:", data_cu['gia_nhap'] if data_cu else "")
    e_gb = tao_o_nhap("Giá bán:", data_cu['gia_ban'] if data_cu else "")
    e_ng = tao_o_nhap("Ngày nhập:", data_cu['ngay_nhap'] if data_cu else "")

    btn_luu = ctk.CTkButton(frame, text="💾 LƯU DỮ LIỆU", font=("Arial", 15, "bold"), height=45)
    btn_luu.pack(pady=30, padx=30, fill="x")

    return {
        "window": window, "btn_luu": btn_luu, "e_sku": e_sku, "e_ten": e_ten,
        "e_loai": e_loai, "e_sl": e_sl, "e_gn": e_gn, "e_gb": e_gb, "e_ng": e_ng
    }

def hien_thi_bieu_do(parent, lay_du_lieu_fn):
    """
    Hiển thị cửa sổ phụ chứa biểu đồ phân tích dữ liệu kho hàng bằng Matplotlib.
    Bố cục gồm 2 biểu đồ:
    1. Biểu đồ cột: Top 5 sản phẩm tồn kho nhiều nhất.
    2. Biểu đồ tròn: Cơ cấu chủng loại sản phẩm.
    """
    df = lay_du_lieu_fn()
    if df.empty:
        messagebox.showwarning("Cảnh báo", "Không có dữ liệu để vẽ biểu đồ!")
        return

    # Import matplotlib các module cần thiết
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    # Tạo cửa sổ popup
    window = ctk.CTkToplevel(parent)
    window.title("Thống Kê Trực Quan Kho Hàng - v1.4.0")
    window.geometry("950x650")
    window.grab_set()

    # Khung giao diện chính
    frame = ctk.CTkFrame(window, corner_radius=15)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Tiêu đề
    ctk.CTkLabel(frame, text="BIỂU ĐỒ PHÂN TÍCH KHO HÀNG", font=("Arial", 18, "bold")).pack(pady=10)

    # Cấu hình phong cách hiển thị (sử dụng biểu đồ cột và tròn sạch sẽ)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5), dpi=100)
    fig.patch.set_facecolor('#EAEAEA')  # Màu nền đồng bộ

    # 1. Vẽ biểu đồ 1: Top 5 tồn kho nhiều nhất
    top5 = df.nlargest(5, 'so_luong')
    ax1.bar(top5['ten_san_pham'].str.slice(0, 15) + '...', top5['so_luong'], color='#3498db', edgecolor='black')
    ax1.set_title("Top 5 Sản Phẩm Tồn Kho", fontsize=11, fontweight='bold')
    ax1.set_ylabel("Số lượng", fontsize=9)
    ax1.tick_params(axis='x', rotation=30, labelsize=8)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # 2. Vẽ biểu đồ 2: Tỷ lệ loại sản phẩm
    loai_counts = df['loai_san_pham'].value_counts()
    ax2.pie(loai_counts, labels=loai_counts.index, autopct='%1.1f%%', startangle=90, 
            colors=['#2ecc71', '#e67e22', '#9b59b6', '#f1c40f', '#e74c3c'])
    ax2.set_title("Cơ Cấu Chủng Loại", fontsize=11, fontweight='bold')

    plt.tight_layout()

    # Nhúng biểu đồ vào Tkinter Canvas
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    # Nút đóng
    btn_dong = ctk.CTkButton(frame, text="Đóng", command=window.destroy, width=120)
    btn_dong.pack(pady=10)

