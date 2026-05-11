import os
import sys
import pandas as pd
import numpy as np
import threading
from utils.logger import setup_logger

# Khởi tạo logger để ghi lại các hoạt động của chương trình
logger = setup_logger()

# ─── ĐƯỜNG DẪN FILE DỮ LIỆU ──────────────────────────────────────────
# Kiểm tra xem ứng dụng đang chạy từ file .exe hay script .py
if getattr(sys, 'frozen', False):
    # Nếu chạy từ file .exe, lưu dữ liệu trong thư mục người dùng để tránh lỗi quyền ghi
    _BASE_DIR = os.path.join(os.path.expanduser("~"), "PyWarehouse_Data")
else:
    # Nếu chạy từ code, lưu ngay tại thư mục dự án
    _BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Đường dẫn đến file CSV chứa dữ liệu kho hàng
FILE_KHO = os.path.join(_BASE_DIR, "data", "kho_hang.csv")


def khoi_tao_csv():
    """
    Khởi tạo file CSV dữ liệu mẫu nếu file chưa tồn tại.

    Hàm này kiểm tra sự tồn tại của thư mục data và file CSV. Nếu chưa có,
    nó sẽ tạo mới file với các tiêu đề cột theo đúng định dạng yêu cầu.
    """
    # Tạo thư mục data nếu chưa có
    os.makedirs(os.path.dirname(FILE_KHO), exist_ok=True)
    
    # Nếu file chưa tồn tại thì tạo mới với các cột tiêu đề
    if not os.path.exists(FILE_KHO):
        # Thêm cột "loai_san_pham" để phục vụ yêu cầu thống kê theo nhóm
        cac_cot = ["ma_sku", "ten_san_pham", "loai_san_pham", "so_luong", "gia_nhap", "gia_ban", "ngay_nhap"]
        df_moi = pd.DataFrame(columns=cac_cot)
        df_moi.to_csv(FILE_KHO, index=False, encoding="utf-8-sig")
        logger.info(f"Đã khởi tạo file kho hàng mới: {FILE_KHO}")


def lay_danh_sach():
    """
    Đọc toàn bộ danh sách sản phẩm từ file CSV và thực hiện tính toán thống kê.

    Sử dụng Pandas để load dữ liệu và Numpy để thực hiện các phép toán mảng 
    (Vectorization) nhằm tối ưu hiệu năng tính toán Tổng vốn và Lợi nhuận.

    Returns:
        pandas.DataFrame: Bảng dữ liệu chứa thông tin sản phẩm và các cột tính toán thêm.
    """
    try:
        # Đọc file CSV, đảm bảo hỗ trợ tiếng Việt (utf-8-sig)
        df = pd.read_csv(FILE_KHO, encoding="utf-8-sig")
        
        # [Q4/Q5] Sử dụng Numpy để tối ưu tính toán mảng
        # 1. Tính tổng vốn tồn kho cho từng sản phẩm = Số lượng * Giá nhập
        df["tong_von"] = np.multiply(df["so_luong"].values, df["gia_nhap"].values)
        
        # 2. Tính lợi nhuận dự kiến = (Giá bán - Giá nhập) * Số lượng
        df["loi_nhuan"] = (df["gia_ban"].values - df["gia_nhap"].values) * df["so_luong"].values
        
        return df
    except Exception as e:
        logger.error(f"Lỗi khi đọc file CSV: {e}")
        return pd.DataFrame()


def them_san_pham(data_moi):
    """
    Thêm một sản phẩm mới vào kho hàng sau khi kiểm tra tính duy nhất của SKU.

    Args:
        data_moi (dict): Dictionary chứa thông tin sản phẩm (ma_sku, ten, so_luong, ...).

    Returns:
        tuple: (bool, str) Trạng thái thành công và thông báo phản hồi.
    """
    try:
        df = lay_danh_sach()
        # Kiểm tra xem mã SKU đã tồn tại chưa (Mã SKU phải là duy nhất)
        if data_moi['ma_sku'] in df['ma_sku'].values:
            return False, "Mã SKU này đã tồn tại trong hệ thống!"
            
        df_moi = pd.DataFrame([data_moi])
        # Gộp dòng dữ liệu mới vào DataFrame hiện tại
        df = pd.concat([df[df_moi.columns], df_moi], ignore_index=True)
        
        # Lưu lại vào file CSV
        df.to_csv(FILE_KHO, index=False, encoding="utf-8-sig")
        logger.info(f"Đã thêm sản phẩm mới: {data_moi['ten_san_pham']}")
        return True, "Thêm sản phẩm thành công!"
    except Exception as e:
        logger.error(f"Lỗi thêm sản phẩm: {e}")
        return False, str(e)


def sua_san_pham(sku_cu, data_cap_nhat):
    """
    Cập nhật thông tin của một sản phẩm hiện có dựa trên mã SKU.

    Args:
        sku_cu (str): Mã SKU của sản phẩm cần chỉnh sửa.
        data_cap_nhat (dict): Dictionary chứa các trường thông tin mới cần cập nhật.

    Returns:
        tuple: (bool, str) Trạng thái thành công và thông báo phản hồi.
    """
    try:
        df = pd.read_csv(FILE_KHO, encoding="utf-8-sig")
        # Tìm vị trí của sản phẩm cần sửa dựa trên SKU
        if sku_cu not in df['ma_sku'].values:
            return False, "Không tìm thấy sản phẩm để sửa!"
            
        # Cập nhật thông tin từng trường
        idx = df.index[df['ma_sku'] == sku_cu][0]
        for key, value in data_cap_nhat.items():
            df.at[idx, key] = value
            
        # Lưu lại file CSV
        df.to_csv(FILE_KHO, index=False, encoding="utf-8-sig")
        logger.info(f"Đã cập nhật sản phẩm mã: {sku_cu}")
        return True, "Cập nhật thành công!"
    except Exception as e:
        logger.error(f"Lỗi sửa sản phẩm: {e}")
        return False, str(e)


def xoa_san_pham(danh_sach_sku):
    """
    Xóa danh sách các sản phẩm khỏi kho hàng.

    Args:
        danh_sach_sku (list): Danh sách các mã SKU cần loại bỏ.

    Returns:
        tuple: (bool, str) Trạng thái thành công và thông báo phản hồi.
    """
    try:
        df = pd.read_csv(FILE_KHO, encoding="utf-8-sig")
        # Lọc bỏ các dòng có mã SKU nằm trong danh sách cần xóa
        df = df[~df['ma_sku'].isin(danh_sach_sku)]
        
        # Lưu lại file CSV
        df.to_csv(FILE_KHO, index=False, encoding="utf-8-sig")
        logger.info(f"Đã xóa các sản phẩm: {danh_sach_sku}")
        return True, "Xóa sản phẩm thành công!"
    except Exception as e:
        logger.error(f"Lỗi xóa sản phẩm: {e}")
        return False, str(e)


def thong_ke_kho():
    """
    Thực hiện các tính toán thống kê tổng quát về tình trạng kho hàng.

    Sử dụng Pandas groupby để tính lợi nhuận gộp trung bình theo từng nhóm sản phẩm
    và xác định số lượng mặt hàng cần nhập thêm dựa trên ngưỡng Min Stock.

    Returns:
        dict: Chứa các con số thống kê (tổng mặt hàng, tổng vốn, lợi nhuận nhóm...).
    """
    df = lay_danh_sach()
    if df.empty:
        return {"tong_mat_hang": 0, "tong_gia_tri_kho": 0, "can_nhap_hang": 0, "loi_nhuan_nhom": {}}
    
    # [Q4] Tính lợi nhuận trung bình theo loại sản phẩm bằng Pandas groupby
    loi_nhuan_nhom = df.groupby("loai_san_pham")["loi_nhuan"].mean().to_dict()
    
    thong_ke = {
        "tong_mat_hang": len(df),
        "tong_gia_tri_kho": df["tong_von"].sum(),
        "can_nhap_hang": len(df[df["so_luong"] < 10]), # Ngưỡng Min Stock mặc định là 10
        "loi_nhuan_nhom": loi_nhuan_nhom
    }
    return thong_ke


def import_csv(file_path):
    """
    Nhập dữ liệu từ file CSV bên ngoài và gộp vào cơ sở dữ liệu hiện tại.

    Args:
        file_path (str): Đường dẫn đến file CSV cần import.

    Returns:
        tuple: (bool, str) Trạng thái thành công và thông báo phản hồi.
    """
    try:
        df_old = pd.read_csv(FILE_KHO, encoding="utf-8-sig")
        df_new = pd.read_csv(file_path, encoding="utf-8-sig")
        
        # Gộp dữ liệu và xóa các dòng trùng mã SKU (giữ lại dữ liệu hiện tại)
        df_combined = pd.concat([df_old, df_new]).drop_duplicates(subset=['ma_sku'], keep='first')
        
        df_combined.to_csv(FILE_KHO, index=False, encoding="utf-8-sig")
        return True, f"Đã nhập thành công {len(df_new)} dòng dữ liệu!"
    except Exception as e:
        return False, f"Lỗi Import: {str(e)}"


def export_csv(target_path):
    """
    Xuất toàn bộ dữ liệu kho hàng hiện tại ra một file CSV tại vị trí chỉ định.

    Args:
        target_path (str): Đường dẫn nơi sẽ lưu file CSV kết quả.

    Returns:
        tuple: (bool, str) Trạng thái thành công và thông báo phản hồi.
    """
    try:
        df = lay_danh_sach()
        # Lưu DataFrame ra file với định dạng utf-8-sig để hỗ trợ Excel mở tiếng Việt
        df.to_csv(target_path, index=False, encoding="utf-8-sig")
        return True, "Xuất file thành công!"
    except Exception as e:
        return False, f"Lỗi Export: {str(e)}"
