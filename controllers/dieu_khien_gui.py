import threading
from tkinter import messagebox, filedialog
import models.kho_hang as model
import views.giao_dien_gui as view

def khoi_tao_dieu_khien(widgets):
    """Điều phối hoạt động giữa Model và View."""
    tree = widgets["tree"]
    root = widgets["root"]

    def lam_moi_bang(query=""):
        """Nạp lại bảng và thống kê."""
        for item in tree.get_children():
            tree.delete(item)
        
        df = model.lay_danh_sach()
        if query:
            df = df[df['ma_sku'].str.contains(query, case=False) | 
                    df['ten_san_pham'].str.contains(query, case=False)]
        
        for _, row in df.iterrows():
            # [Q8] Thay đổi màu nền dòng nếu tồn kho thấp (Min Stock < 10)
            tag = "nguy_hiem" if row['so_luong'] < 10 else "binh_thuong"
            
            tree.insert("", "end", values=(
                row['ma_sku'], row['ten_san_pham'], row['loai_san_pham'],
                row['so_luong'], f"{row['gia_nhap']:,}", f"{row['gia_ban']:,}", 
                row['ngay_nhap'], f"{row['tong_von']:,}"
            ), tags=(tag,))
        
        tree.tag_configure("nguy_hiem", background="#ffcccc", foreground="#c0392b")
        cap_nhat_dashboard()

    def cap_nhat_dashboard():
        tk = model.thong_ke_kho()
        widgets["lbl_tong_hang"].config(text=f"Mặt hàng: {tk['tong_mat_hang']}")
        widgets["lbl_tong_von"].config(text=f"Vốn: {tk['tong_gia_tri_kho']:,} VNĐ")
        widgets["lbl_can_nhap"].config(text=f"Cần nhập: {tk['can_nhap_hang']}")

    # ─── THÊM / SỬA ──────────────────────────────────────────
    def hanh_dong_them():
        form = view.hien_thi_form_nhap_lieu(root, "Thêm Sản Phẩm")
        def luu():
            # [Q7/NFR3] Input Validation
            try:
                data = {
                    "ma_sku": form["e_sku"].get().strip(),
                    "ten_san_pham": form["e_ten"].get().strip(),
                    "loai_san_pham": form["e_loai"].get().strip(),
                    "so_luong": int(form["e_sl"].get()),
                    "gia_nhap": float(form["e_gn"].get()),
                    "gia_ban": float(form["e_gb"].get()),
                    "ngay_nhap": form["e_ng"].get().strip()
                }
                if not data["ma_sku"] or not data["ten_san_pham"]:
                    messagebox.showwarning("Lỗi", "Không được để trống thông tin!")
                    return
                
                ok, msg = model.them_san_pham(data)
                if ok:
                    messagebox.showinfo("Xong", msg)
                    form["window"].destroy()
                    lam_moi_bang()
                else:
                    messagebox.showerror("Lỗi", msg)
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng và Giá phải là số!")
        form["btn_luu"].config(command=luu)

    def hanh_dong_sua():
        sel = tree.selection()
        if len(sel) != 1: # Đảm bảo chỉ chọn duy nhất 1 dòng
            messagebox.showwarning("Lỗi", "Vui lòng chọn duy nhất 1 sản phẩm để sửa!")
            return
        
        vals = tree.item(sel[0])['values']
        data_cu = {
            "ma_sku": vals[0], "ten_san_pham": vals[1], "loai_san_pham": vals[2],
            "so_luong": vals[3], "gia_nhap": str(vals[4]).replace(",", ""),
            "gia_ban": str(vals[5]).replace(",", ""), "ngay_nhap": vals[6]
        }
        form = view.hien_thi_form_nhap_lieu(root, "Sửa Sản Phẩm", data_cu)
        def luu():
            try:
                data_moi = {
                    "ten_san_pham": form["e_ten"].get().strip(),
                    "loai_san_pham": form["e_loai"].get().strip(),
                    "so_luong": int(form["e_sl"].get()),
                    "gia_nhap": float(form["e_gn"].get()),
                    "gia_ban": float(form["e_gb"].get()),
                    "ngay_nhap": form["e_ng"].get().strip()
                }
                ok, msg = model.sua_san_pham(data_cu["ma_sku"], data_moi)
                if ok:
                    messagebox.showinfo("Xong", msg)
                    form["window"].destroy()
                    lam_moi_bang()
                else:
                    messagebox.showerror("Lỗi", msg)
            except ValueError:
                messagebox.showerror("Lỗi", "Dữ liệu số không hợp lệ!")
        form["btn_luu"].config(command=luu)

    # ─── IMPORT / EXPORT (MULTI-THREADING) ────────────────────
    def hanh_dong_import():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path: return
        
        # [Q11] Sử dụng Thread để tránh treo GUI
        def worker():
            ok, msg = model.import_csv(file_path)
            # Quay lại luồng chính để cập nhật giao diện
            root.after(0, lambda: [messagebox.showinfo("Kết quả", msg), lam_moi_bang()])
        
        threading.Thread(target=worker, daemon=True).start()

    def hanh_dong_export():
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path: return
        ok, msg = model.export_csv(path)
        messagebox.showinfo("Xuất file", msg)

    # ─── CÁC CHỨC NĂNG KHÁC ───────────────────────────────────
    def hanh_dong_xoa():
        sel = tree.selection()
        if not sel: return
        if messagebox.askyesno("Xác nhận", "Xóa các sản phẩm đã chọn?"):
            skus = [tree.item(i)['values'][0] for i in sel]
            model.xoa_san_pham(skus)
            lam_moi_bang()

    def hanh_dong_about():
        messagebox.showinfo("About PyWarehouse", "PyWarehouse v1.0.0\nDự án quản lý kho hàng MVC chuyên sâu.\nSử dụng: Pandas, Numpy, Tkinter.")

    # Gán sự kiện
    widgets["btn_them"].config(command=hanh_dong_them)
    widgets["btn_sua"].config(command=hanh_dong_sua)
    widgets["btn_xoa"].config(command=hanh_dong_xoa)
    widgets["btn_import"].config(command=hanh_dong_import)
    widgets["btn_export"].config(command=hanh_dong_export)
    widgets["btn_about"].config(command=hanh_dong_about)
    widgets["entry_tim_kiem"].bind("<KeyRelease>", lambda e: lam_moi_bang(widgets["entry_tim_kiem"].get()))

    lam_moi_bang()
