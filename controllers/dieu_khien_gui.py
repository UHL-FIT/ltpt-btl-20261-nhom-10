import threading
from tkinter import messagebox, filedialog
import models.kho_hang as model
import views.giao_dien_gui as view

def khoi_tao_dieu_khien(widgets):
    """
    Kết nối các thành phần giao diện (nút, bảng) với các hàm xử lý nghiệp vụ.

    Hàm này khởi tạo các bộ lắng nghe sự kiện (event handlers) cho các widget trong view,
    đảm bảo luồng dữ liệu giữa giao diện người dùng và cơ sở dữ liệu CSV.

    Args:
        widgets (dict): Dictionary chứa các tham chiếu tới các widget từ View.
    """
    tree = widgets["tree"]
    root = widgets["root"]

    def lam_moi_bang(query=""):
        """
        Xóa dữ liệu cũ trên bảng Treeview và nạp lại dữ liệu mới nhất từ Model.

        Hỗ trợ tính năng tìm kiếm và tự động thay đổi màu sắc dòng dựa trên số lượng tồn kho.

        Args:
            query (str, optional): Từ khóa để lọc sản phẩm theo mã SKU hoặc Tên.
        """
        # Xóa toàn bộ các dòng hiện tại trong bảng
        for item in tree.get_children():
            tree.delete(item)
        
        # Lấy danh sách sản phẩm mới nhất từ cơ sở dữ liệu
        df = model.lay_danh_sach()
        
        # Thực hiện lọc nếu người dùng có nhập từ khóa tìm kiếm
        if query:
            df = df[df['ma_sku'].str.contains(query, case=False) | 
                    df['ten_san_pham'].str.contains(query, case=False)]
        
        # Duyệt qua từng sản phẩm và nạp vào bảng
        for _, row in df.iterrows():
            # [Q8] Tô màu nền dòng nếu tồn kho thấp hơn ngưỡng Min Stock (10)
            tag = "nguy_hiem" if row['so_luong'] < 10 else "binh_thuong"
            
            tree.insert("", "end", values=(
                row['ma_sku'], row['ten_san_pham'], row['loai_san_pham'],
                row['so_luong'], f"{row['gia_nhap']:,}", f"{row['gia_ban']:,}", 
                row['ngay_nhap'], f"{row['tong_von']:,}"
            ), tags=(tag,))
        
        # Cấu hình màu sắc hiển thị cho cảnh báo nguy hiểm
        tree.tag_configure("nguy_hiem", background="#ffcccc", foreground="#c0392b")
        cap_nhat_dashboard()

    def cap_nhat_dashboard():
        """Cập nhật các con số thống kê tổng quát trên thanh trạng thái."""
        tk = model.thong_ke_kho()
        widgets["lbl_tong_hang"].config(text=f"Mặt hàng: {tk['tong_mat_hang']}")
        widgets["lbl_tong_von"].config(text=f"Vốn: {tk['tong_gia_tri_kho']:,} VNĐ")
        widgets["lbl_can_nhap"].config(text=f"Cần nhập: {tk['can_nhap_hang']}")

    # ─── XỬ LÝ SỰ KIỆN: THÊM SẢN PHẨM ────────────────────────────────
    def hanh_dong_them():
        """Hiển thị form và xử lý logic thêm sản phẩm mới."""
        form = view.hien_thi_form_nhap_lieu(root, "Thêm Sản Phẩm")
        
        def luu():
            # [Q7] Input Validation: Kiểm tra dữ liệu đầu vào
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
                # Không được bỏ trống các trường định danh chính
                if not data["ma_sku"] or not data["ten_san_pham"]:
                    messagebox.showwarning("Lỗi", "Không được để trống Mã SKU và Tên!")
                    return
                
                # Gọi Model để thực hiện lưu trữ
                ok, msg = model.them_san_pham(data)
                if ok:
                    messagebox.showinfo("Thành công", msg)
                    form["window"].destroy()
                    lam_moi_bang() # Tải lại bảng để thấy kết quả mới
                else:
                    messagebox.showerror("Lỗi", msg)
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng và Giá phải nhập bằng con số!")
                
        form["btn_luu"].config(command=luu)

    # ─── XỬ LÝ SỰ KIỆN: SỬA SẢN PHẨM ─────────────────────────────────
    def hanh_dong_sua():
        """Hiển thị form với dữ liệu cũ và xử lý cập nhật thông tin."""
        sel = tree.selection()
        # Đảm bảo người dùng chỉ chọn duy nhất 1 sản phẩm để sửa
        if len(sel) != 1:
            messagebox.showwarning("Lỗi", "Vui lòng chọn duy nhất 1 sản phẩm để sửa!")
            return
        
        # Trích xuất dữ liệu từ dòng đang được chọn trong bảng
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
                # Gọi Model để cập nhật lại dữ liệu CSV
                ok, msg = model.sua_san_pham(data_cu["ma_sku"], data_moi)
                if ok:
                    messagebox.showinfo("Xong", msg)
                    form["window"].destroy()
                    lam_moi_bang()
                else:
                    messagebox.showerror("Lỗi", msg)
            except ValueError:
                messagebox.showerror("Lỗi", "Dữ liệu con số không hợp lệ!")
                
        form["btn_luu"].config(command=luu)

    # ─── XỬ LÝ FILE: IMPORT / EXPORT (SỬ DỤNG THREADING) ─────────────
    def hanh_dong_import():
        """Mở hộp thoại chọn file CSV và thực hiện import đa luồng."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path: return
        
        # [Q11] Sử dụng luồng phụ (Thread) để tránh làm "đơ" giao diện khi file lớn
        def worker():
            ok, msg = model.import_csv(file_path)
            # Sau khi xong, dùng root.after để cập nhật giao diện từ luồng chính (Main Thread)
            root.after(0, lambda: [messagebox.showinfo("Kết quả", msg), lam_moi_bang()])
        
        threading.Thread(target=worker, daemon=True).start()

    def hanh_dong_export():
        """Mở hộp thoại lưu file và xuất toàn bộ dữ liệu kho ra CSV."""
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path: return
        ok, msg = model.export_csv(path)
        messagebox.showinfo("Xuất file", msg)

    # ─── CÁC CHỨC NĂNG BỔ TRỢ ────────────────────────────────────────
    def hanh_dong_xoa():
        """Xóa các sản phẩm đang được chọn khỏi kho hàng."""
        sel = tree.selection()
        if not sel: return
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa {len(sel)} sản phẩm?"):
            skus = [tree.item(i)['values'][0] for i in sel]
            model.xoa_san_pham(skus)
            lam_moi_bang()

    def hanh_dong_about():
        """Hiển thị thông tin giới thiệu về phần mềm."""
        messagebox.showinfo("Giới Thiệu PyWarehouse", 
                          "PyWarehouse v1.0.0\n"
                          "Phần mềm quản lý kho hàng chuẩn kiến trúc MVC.\n"
                          "Sử dụng: Pandas, Numpy, Tkinter.\n"
                          "Nhóm 2 (TT02A) - ĐH Hạ Long.")

    # Gán các hàm xử lý sự kiện vào các nút bấm tương ứng
    widgets["btn_them"].config(command=hanh_dong_them)
    widgets["btn_sua"].config(command=hanh_dong_sua)
    widgets["btn_xoa"].config(command=hanh_dong_xoa)
    widgets["btn_import"].config(command=hanh_dong_import)
    widgets["btn_export"].config(command=hanh_dong_export)
    widgets["btn_about"].config(command=hanh_dong_about)
    
    # Lắng nghe sự kiện gõ phím để tìm kiếm tức thời
    widgets["entry_tim_kiem"].bind("<KeyRelease>", lambda e: lam_moi_bang(widgets["entry_tim_kiem"].get()))

    # Tải dữ liệu lên bảng lần đầu khi ứng dụng khởi chạy
    lam_moi_bang()
