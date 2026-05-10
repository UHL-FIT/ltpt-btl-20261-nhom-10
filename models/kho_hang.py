import os
import sys
import pandas as pd
import numpy as np
import threading
from utils.logger import setup_logger

# Khởi tạo logger
logger = setup_logger()

# ─── ĐƯỜNG DẪN FILE DỮ LIỆU ──────────────────────────────────────────
if getattr(sys, 'frozen', False):
    _BASE_DIR = os.path.join(os.path.expanduser("~"), "PyWarehouse_Data")
else:
    _BASE_DIR = os.path.dirname(os.path.dirname(__file__))

FILE_KHO = os.path.join(_BASE_DIR, "data", "kho_hang.csv")


def khoi_tao_csv():
    """Tạo file dữ liệu mẫu nếu file chưa tồn tại."""
    os.makedirs(os.path.dirname(FILE_KHO), exist_ok=True)
    if not os.path.exists(FILE_KHO):
        # Thêm cột "loai_san_pham" để phục vụ yêu cầu thống kê theo nhóm
        cac_cot = ["ma_sku", "ten_san_pham", "loai_san_pham", "so_luong", "gia_nhap", "gia_ban", "ngay_nhap"]
        df_moi = pd.DataFrame(columns=cac_cot)
        df_moi.to_csv(FILE_KHO, index=False, encoding="utf-8-sig")
        logger.info(f"Đã khởi tạo file kho hàng mới: {FILE_KHO}")


def lay_danh_sach():
    """Đọc toàn bộ danh sách sản phẩm và tính toán các cột thống kê."""
    try:
        df = pd.read_csv(FILE_KHO, encoding="utf-8-sig")
        
        # [Q4/Q5] Sử dụng Numpy để tối ưu tính toán mảng
        # Tính tổng vốn = Số lượng * Giá nhập
        df["tong_von"] = np.multiply(df["so_luong"].values, df["gia_nhap"].values)
        
        # Tính lợi nhuận từng món = (Giá bán - Giá nhập) * Số lượng
        df["loi_nhuan"] = (df["gia_ban"].values - df["gia_nhap"].values) * df["so_luong"].values
        
        return df
    except Exception as e:
        logger.error(f"Lỗi khi đọc file CSV: {e}")
        return pd.DataFrame()


def them_san_pham(data_moi):
    """Thêm sản phẩm mới (Kiểm tra SKU duy nhất)."""
    try:
        df = lay_danh_sach()
        if data_moi['ma_sku'] in df['ma_sku'].values:
            return False, "Mã SKU này đã tồn tại!"
            
        df_moi = pd.DataFrame([data_moi])
        # Dùng concat để thêm dòng mới vào bảng
        df = pd.concat([df[df_moi.columns], df_moi], ignore_index=True)
        
        df.to_csv(FILE_KHO, index=False, encoding="utf-8-sig")
        return True, "Thêm sản phẩm thành công!"
    except Exception as e:
        logger.error(f"Lỗi thêm sản phẩm: {e}")
        return False, str(e)


def sua_san_pham(sku_cu, data_cap_nhat):
    """Sửa thông tin sản phẩm theo SKU."""
    try:
        df = pd.read_csv(FILE_KHO, encoding="utf-8-sig")
        if sku_cu not in df['ma_sku'].values:
            return False, "Không tìm thấy sản phẩm!"
            
        idx = df.index[df['ma_sku'] == sku_cu][0]
        for key, value in data_cap_nhat.items():
            df.at[idx, key] = value
            
        df.to_csv(FILE_KHO, index=False, encoding="utf-8-sig")
        return True, "Cập nhật thành công!"
    except Exception as e:
        logger.error(f"Lỗi sửa sản phẩm: {e}")
        return False, str(e)


def xoa_san_pham(danh_sach_sku):
    """Xóa danh sách sản phẩm theo SKU."""
    try:
        df = pd.read_csv(FILE_KHO, encoding="utf-8-sig")
        df = df[~df['ma_sku'].isin(danh_sach_sku)]
        df.to_csv(FILE_KHO, index=False, encoding="utf-8-sig")
        return True, "Xóa sản phẩm thành công!"
    except Exception as e:
        logger.error(f"Lỗi xóa sản phẩm: {e}")
        return False, str(e)


def thong_ke_kho():
    """
    Tính toán thống kê kho hàng.
    Yêu cầu: Tính lợi nhuận gộp trung bình theo từng nhóm sản phẩm.
    """
    df = lay_danh_sach()
    if df.empty:
        return {"tong_mat_hang": 0, "tong_gia_tri_kho": 0, "can_nhap_hang": 0, "loi_nhuan_nhom": {}}
    
    # Tính lợi nhuận trung bình theo loại sản phẩm bằng Pandas groupby
    loi_nhuan_nhom = df.groupby("loai_san_pham")["loi_nhuan"].mean().to_dict()
    
    thong_ke = {
        "tong_mat_hang": len(df),
        "tong_gia_tri_kho": df["tong_von"].sum(),
        "can_nhap_hang": len(df[df["so_luong"] < 10]), # Ngưỡng Min Stock = 10
        "loi_nhuan_nhom": loi_nhuan_nhom
    }
    return thong_ke


def import_csv(file_path):
    """Đọc dữ liệu từ file bên ngoài và gộp vào kho hiện tại."""
    try:
        df_old = pd.read_csv(FILE_KHO, encoding="utf-8-sig")
        df_new = pd.read_csv(file_path, encoding="utf-8-sig")
        
        # Gộp dữ liệu, xóa trùng SKU (ưu tiên dữ liệu cũ)
        df_combined = pd.concat([df_old, df_new]).drop_duplicates(subset=['ma_sku'], keep='first')
        
        df_combined.to_csv(FILE_KHO, index=False, encoding="utf-8-sig")
        return True, f"Đã nhập thành công {len(df_new)} dòng dữ liệu!"
    except Exception as e:
        return False, f"Lỗi Import: {str(e)}"


def export_csv(target_path):
    """Xuất toàn bộ kho hàng ra file CSV tại vị trí chọn."""
    try:
        df = lay_danh_sach()
        df.to_csv(target_path, index=False, encoding="utf-8-sig")
        return True, "Xuất file thành công!"
    except Exception as e:
        return False, f"Lỗi Export: {str(e)}"
