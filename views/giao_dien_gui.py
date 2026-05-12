import tkinter as tk
from tkinter import ttk, messagebox
import os

def tao_giao_dien_chinh(root):
    """
    Khởi tạo giao diện chính cho phần mềm PyWarehouse.

    Xây dựng bố cục bao gồm thanh công cụ, bảng dữ liệu (Treeview) và thanh thống kê.
    Hỗ trợ tính năng tự động co giãn khi người dùng thay đổi kích thước cửa sổ.

    Args:
        root (tk.Tk): Cửa sổ gốc của ứng dụng Tkinter.

    Returns:
        dict: Chứa các tham chiếu tới các widget chính (nút, bảng, ô nhập liệu...).
    """
    # ─── PHẦN 1: CẤU HÌNH CỬA SỔ ─────────────────────────────────────
    root.title("PyWarehouse - Quản Lý Kho Hàng")
    root.geometry("1100x700")
    
    # [Q6] Cấu hình trọng số để các thành phần tự động co giãn theo cửa sổ
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    # ─── THANH CÔNG CỤ (TOOLBAR) ──────────────────────────────
    toolbar = tk.Frame(root, pady=10, padx=10, bg="#ecf0f1")
    toolbar.grid(row=0, column=0, sticky="ew")

    # [Q3] Nút bấm có màu sắc và icon (Emoji làm placeholder cho icon)
    btn_them = tk.Button(toolbar, text="➕ Thêm", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), width=10)
    btn_them.pack(side=tk.LEFT, padx=5)

    btn_sua = tk.Button(toolbar, text="✏️ Sửa", bg="#3498db", fg="white", font=("Arial", 10, "bold"), width=10)
    btn_sua.pack(side=tk.LEFT, padx=5)

    btn_xoa = tk.Button(toolbar, text="🗑️ Xóa", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), width=10)
    btn_xoa.pack(side=tk.LEFT, padx=5)

    btn_import = tk.Button(toolbar, text="📥 Nhập CSV", bg="#9b59b6", fg="white", font=("Arial", 10, "bold"), width=12)
    btn_import.pack(side=tk.LEFT, padx=5)

    btn_export = tk.Button(toolbar, text="📤 Xuất CSV", bg="#f39c12", fg="white", font=("Arial", 10, "bold"), width=12)
    btn_export.pack(side=tk.LEFT, padx=5)

    btn_about = tk.Button(toolbar, text="ℹ️ Giới Thiệu", bg="#95a5a6", fg="white", font=("Arial", 10, "bold"), width=12)
    btn_about.pack(side=tk.LEFT, padx=5)

    # Ô tìm kiếm sản phẩm
    tk.Label(toolbar, text=" 🔍 Tìm kiếm:", bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
    entry_tim_kiem = tk.Entry(toolbar, width=25)
    entry_tim_kiem.pack(side=tk.LEFT, padx=5)

    # ─── BẢNG DỮ LIỆU (TREEVIEW) ─────────────────────
    frame_bang = tk.Frame(root)
    frame_bang.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    # [Q8] Widget Table hiển thị dữ liệu từ Model
    cac_cot = ("sku", "ten", "loai", "sl", "gia_n", "gia_b", "ngay", "tong")
    tree = ttk.Treeview(frame_bang, columns=cac_cot, show="headings")

    # Thiết lập tiêu đề cho từng cột
    tree.heading("sku", text="Mã SKU")
    tree.heading("ten", text="Tên Sản Phẩm")
    tree.heading("loai", text="Phân Loại")
    tree.heading("sl", text="Tồn Kho")
    tree.heading("gia_n", text="Giá Nhập")
    tree.heading("gia_b", text="Giá Bán")
    tree.heading("ngay", text="Ngày Nhập")
    tree.heading("tong", text="Tổng Vốn")

    # Căn chỉnh độ rộng và vị trí text trong các cột
    tree.column("sku", width=80, anchor=tk.CENTER)
    tree.column("ten", width=200)
    tree.column("loai", width=120)
    tree.column("sl", width=80, anchor=tk.CENTER)
    tree.column("gia_n", width=100, anchor=tk.E)
    tree.column("gia_b", width=100, anchor=tk.E)
    tree.column("ngay", width=100, anchor=tk.CENTER)
    tree.column("tong", width=120, anchor=tk.E)

    # Thanh cuộn dọc cho bảng
    sb = ttk.Scrollbar(frame_bang, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=sb.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    sb.pack(side=tk.RIGHT, fill=tk.Y)

    # ─── THÔNG TIN THỐNG KÊ (DASHBOARD) ──────────────────────────
    status_bar = tk.Frame(root, bd=1, relief=tk.SUNKEN, pady=10, bg="#dfe6e9")
    status_bar.grid(row=2, column=0, sticky="ew")

    lbl_tong_hang = tk.Label(status_bar, text="Mặt hàng: 0", font=("Arial", 10, "bold"), bg="#dfe6e9")
    lbl_tong_hang.pack(side=tk.LEFT, padx=20)

    lbl_tong_von = tk.Label(status_bar, text="Vốn: 0 VNĐ", font=("Arial", 10, "bold"), bg="#dfe6e9")
    lbl_tong_von.pack(side=tk.LEFT, padx=20)

    lbl_can_nhap = tk.Label(status_bar, text="Cần nhập: 0", font=("Arial", 10, "bold"), fg="#d63031", bg="#dfe6e9")
    lbl_can_nhap.pack(side=tk.LEFT, padx=20)

    # Trả về các tham chiếu để Controller có thể điều khiển
    return {
        "root": root, "tree": tree, "btn_them": btn_them, "btn_sua": btn_sua,
        "btn_xoa": btn_xoa, "btn_import": btn_import, "btn_export": btn_export,
        "btn_about": btn_about, "entry_tim_kiem": entry_tim_kiem,
        "lbl_tong_hang": lbl_tong_hang, "lbl_tong_von": lbl_tong_von, "lbl_can_nhap": lbl_can_nhap
    }

def hien_thi_form_nhap_lieu(parent, tieu_de, data_cu=None):
    """
    Tạo một cửa sổ phụ (Sub Window) dưới dạng popup để người dùng nhập/sửa thông tin.

    Args:
        parent (tk.Toplevel/tk.Tk): Cửa sổ cha để gắn popup vào.
        tieu_de (str): Tiêu đề hiển thị của cửa sổ popup.
        data_cu (dict, optional): Dữ liệu cũ để điền sẵn vào form khi thực hiện Sửa.

    Returns:
        dict: Chứa các tham chiếu tới các ô nhập liệu (Entry) và nút Lưu.
    """
    window = tk.Toplevel(parent)
    window.title(tieu_de)
    window.geometry("400x500")
    window.grab_set() # Ngăn tương tác với cửa sổ chính khi đang mở form

    # Frame chính của form
    form = tk.Frame(window, padx=20, pady=20)
    form.pack(fill=tk.BOTH, expand=True)

    # Hàm nội bộ hỗ trợ tạo nhanh các dòng nhãn và ô nhập
    def tao_dong(label_text, row):
        tk.Label(form, text=label_text).grid(row=row, column=0, sticky="w", pady=8)
        entry = tk.Entry(form, width=30)
        entry.grid(row=row, column=1, pady=8)
        return entry

    # Tạo các trường dữ liệu cho form
    e_sku = tao_dong("Mã SKU:", 0)
    e_ten = tao_dong("Tên sản phẩm:", 1)
    e_loai = tao_dong("Phân loại:", 2)
    e_sl = tao_dong("Số lượng:", 3)
    e_gn = tao_dong("Giá nhập:", 4)
    e_gb = tao_dong("Giá bán:", 5)
    e_ng = tao_dong("Ngày nhập:", 6)

    # Nếu là chức năng Sửa, điền dữ liệu cũ và khóa ô mã SKU
    if data_cu:
        e_sku.insert(0, data_cu['ma_sku'])
        e_sku.config(state='disabled')
        e_ten.insert(0, data_cu['ten_san_pham'])
        e_loai.insert(0, data_cu.get('loai_san_pham', ''))
        e_sl.insert(0, data_cu['so_luong'])
        e_gn.insert(0, data_cu['gia_nhap'])
        e_gb.insert(0, data_cu['gia_ban'])
        e_ng.insert(0, data_cu['ngay_nhap'])

    # Nút lưu dữ liệu
    btn_luu = tk.Button(form, text="💾 Lưu Thông Tin", bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), pady=10)
    btn_luu.grid(row=7, column=0, columnspan=2, sticky="ew", pady=25)

    return {
        "window": window, "btn_luu": btn_luu, "e_sku": e_sku, "e_ten": e_ten,
        "e_loai": e_loai, "e_sl": e_sl, "e_gn": e_gn, "e_gb": e_gb, "e_ng": e_ng
    }
