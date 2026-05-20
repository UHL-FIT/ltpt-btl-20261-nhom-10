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

    def sap_xep_cot(col, reverse):
        """
        Sắp xếp dữ liệu trong bảng khi nhấn vào tiêu đề cột.
        Hỗ trợ sắp xếp cả chuỗi văn bản và con số.
        """
        # Lấy toàn bộ dữ liệu trong cột
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        
        try:
            # Thử chuyển đổi sang số để sắp xếp theo giá trị (giá tiền, số lượng)
            # Loại bỏ dấu phẩy ngăn cách hàng nghìn trước khi chuyển đổi
            l.sort(key=lambda t: float(str(t[0]).replace(',', '')), reverse=reverse)
        except ValueError:
            # Nếu không phải số (ví dụ: tên SP, mã SKU) thì sắp xếp theo chuỗi
            l.sort(reverse=reverse)

        # Sắp xếp lại các dòng trên giao diện
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        # Đổi chiều sắp xếp cho lần nhấn tiếp theo
        tree.heading(col, command=lambda: sap_xep_cot(col, not reverse))

    def cap_nhat_bo_loc():
        """
        Cập nhật danh sách giá trị cho dropdown lọc phân loại.

        Lấy danh sách các loại sản phẩm hiện có từ DataFrame và cập nhật
        vào CTkOptionMenu để người dùng luôn thấy các tùy chọn mới nhất.
        """
        df = model.lay_danh_sach()
        # Lấy danh sách phân loại duy nhất, bỏ qua giá trị rỗng
        danh_sach_loai = ["Tất cả"] + sorted(df["loai_san_pham"].dropna().unique().tolist())
        widgets["filter_loai"].configure(values=danh_sach_loai)

    def lam_moi_bang(query=""):
        """
        Xóa dữ liệu cũ trên bảng Treeview và nạp lại dữ liệu mới nhất từ Model.

        Hỗ trợ tính năng tìm kiếm, lọc theo phân loại và tình trạng tồn kho.
        Ba bộ lọc hoạt động đồng thời (stacking): kết quả phải thỏa mãn cả ba điều kiện.

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
        
        # Lọc theo phân loại sản phẩm (từ dropdown)
        loai_da_chon = widgets["filter_loai"].get()
        if loai_da_chon != "Tất cả":
            df = df[df['loai_san_pham'] == loai_da_chon]

        # Lọc theo tình trạng tồn kho (từ dropdown)
        ton_kho_da_chon = widgets["filter_ton_kho"].get()
        if ton_kho_da_chon == "Sắp hết hàng":
            df = df[df['so_luong'] < 10]
        elif ton_kho_da_chon == "Còn hàng":
            df = df[df['so_luong'] >= 10]
        
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
        widgets["lbl_tong_hang"].configure(text=f"Mặt hàng: {tk['tong_mat_hang']}")
        widgets["lbl_tong_von"].configure(text=f"Vốn: {tk['tong_gia_tri_kho']:,} VNĐ")
        widgets["lbl_can_nhap"].configure(text=f"Cần nhập: {tk['can_nhap_hang']}")

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
                    cap_nhat_bo_loc()
                    lam_moi_bang(query=widgets["entry_tim_kiem"].get())
                else:
                    messagebox.showerror("Lỗi", msg)
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng và Giá phải nhập bằng con số!")
                
        form["btn_luu"].configure(command=luu)

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
                    cap_nhat_bo_loc()
                    lam_moi_bang(query=widgets["entry_tim_kiem"].get())
                else:
                    messagebox.showerror("Lỗi", msg)
            except ValueError:
                messagebox.showerror("Lỗi", "Dữ liệu con số không hợp lệ!")
                
        form["btn_luu"].configure(command=luu)

    # ─── XỬ LÝ FILE: IMPORT / EXPORT (SỬ DỤNG THREADING) ─────────────
    def hanh_dong_import():
        """Mở hộp thoại chọn file CSV và thực hiện import đa luồng."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path: return
        
        # [Q11] Sử dụng luồng phụ (Thread) để tránh làm "đơ" giao diện khi file lớn
        def worker():
            ok, msg = model.import_csv(file_path)
            # Sau khi xong, dùng root.after để cập nhật giao diện từ luồng chính (Main Thread)
            root.after(0, lambda: [messagebox.showinfo("Kết quả", msg), cap_nhat_bo_loc(), lam_moi_bang(query=widgets["entry_tim_kiem"].get())])
        
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
            cap_nhat_bo_loc()
            lam_moi_bang(query=widgets["entry_tim_kiem"].get())

    def hanh_dong_about():
        """Hiển thị thông tin giới thiệu về phần mềm."""
        messagebox.showinfo("Giới Thiệu PyWarehouse", 
                          "PyWarehouse v1.2.0\n"
                          "Phần mềm quản lý kho hàng.\n"
                          "Sử dụng: Pandas, Numpy, Tkinter.\n"
                          "Nhóm 10 (TT02A) - ĐH Hạ Long.")

    # Hàm tiện ích để gọi lam_moi_bang khi dropdown thay đổi
    def khi_bo_loc_thay_doi(_=None):
        """Callback khi người dùng thay đổi giá trị bộ lọc dropdown."""
        lam_moi_bang(query=widgets["entry_tim_kiem"].get())

    # Gán các hàm xử lý sự kiện vào các nút bấm tương ứng
    widgets["btn_them"].configure(command=hanh_dong_them)
    widgets["btn_sua"].configure(command=hanh_dong_sua)
    widgets["btn_xoa"].configure(command=hanh_dong_xoa)
    widgets["btn_import"].configure(command=hanh_dong_import)
    widgets["btn_export"].configure(command=hanh_dong_export)
    widgets["btn_about"].configure(command=hanh_dong_about)

    # Gắn callback cho bộ lọc dropdown
    widgets["filter_loai"].configure(command=khi_bo_loc_thay_doi)
    widgets["filter_ton_kho"].configure(command=khi_bo_loc_thay_doi)
    
    # [NEW] Gắn sự kiện sắp xếp khi nhấn vào tiêu đề cột
    for col in tree["columns"]:
        tree.heading(col, command=lambda c=col: sap_xep_cot(c, False))

    # Lắng nghe sự kiện gõ phím để tìm kiếm tức thời
    widgets["entry_tim_kiem"].bind("<KeyRelease>", lambda e: lam_moi_bang(e.widget.get()))

    # Cập nhật danh sách phân loại và tải dữ liệu lần đầu
    cap_nhat_bo_loc()
    lam_moi_bang()
