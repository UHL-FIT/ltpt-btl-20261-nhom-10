import os
import sys
import sqlite3
import pandas as pd
import numpy as np
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

# Đường dẫn đến file Database SQLite và CSV dự phòng
FILE_DB = os.path.join(_BASE_DIR, "data", "kho_hang.db")
FILE_CSV_BACKUP = os.path.join(_BASE_DIR, "data", "kho_hang.csv")


def khoi_tao_csv():
    """
    Khởi tạo cơ sở dữ liệu SQLite và bảng kho_hang nếu chưa tồn tại.
    Nếu có dữ liệu cũ trong file CSV, tự động chuyển đổi và nhập vào SQLite.
    """
    # Tạo thư mục data nếu chưa có
    os.makedirs(os.path.dirname(FILE_DB), exist_ok=True)
    
    conn = sqlite3.connect(FILE_DB)
    cursor = conn.cursor()
    
    # Tạo bảng kho_hang
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kho_hang (
            ma_sku TEXT PRIMARY KEY,
            ten_san_pham TEXT NOT NULL,
            loai_san_pham TEXT,
            so_luong INTEGER NOT NULL DEFAULT 0,
            gia_nhap REAL NOT NULL DEFAULT 0.0,
            gia_ban REAL NOT NULL DEFAULT 0.0,
            ngay_nhap TEXT
        )
    """)
    conn.commit()
    
    # Kiểm tra xem bảng có dữ liệu chưa. Nếu chưa có, nạp dữ liệu cũ từ CSV (nếu có)
    cursor.execute("SELECT COUNT(*) FROM kho_hang")
    count = cursor.fetchone()[0]
    
    if count == 0 and os.path.exists(FILE_CSV_BACKUP):
        try:
            logger.info("Phát hiện dữ liệu CSV cũ. Đang chuyển đổi sang SQLite...")
            df = pd.read_csv(FILE_CSV_BACKUP, encoding="utf-8-sig")
            # Chỉ lấy các cột cần thiết cho DB
            cols = ["ma_sku", "ten_san_pham", "loai_san_pham", "so_luong", "gia_nhap", "gia_ban", "ngay_nhap"]
            df_db = df[cols].dropna(subset=["ma_sku", "ten_san_pham"])
            
            # Ghi vào SQLite
            df_db.to_sql("kho_hang", conn, if_exists="append", index=False)
            logger.info(f"Đã chuyển đổi thành công {len(df_db)} sản phẩm sang SQLite.")
        except Exception as e:
            logger.error(f"Lỗi khi chuyển đổi dữ liệu CSV cũ: {e}")
            
    conn.close()
    logger.info(f"Đã khởi tạo cơ sở dữ liệu SQLite: {FILE_DB}")


def lay_danh_sach():
    """
    Đọc toàn bộ danh sách sản phẩm từ SQLite và tính toán các cột Tổng vốn, Lợi nhuận.
    Trả về DataFrame tương thích với cấu trúc trước đó.
    """
    try:
        conn = sqlite3.connect(FILE_DB)
        df = pd.read_sql_query("SELECT * FROM kho_hang", conn)
        conn.close()
        
        # Sử dụng Numpy để tối ưu tính toán mảng (như bản CSV cũ)
        if not df.empty:
            df["tong_von"] = np.multiply(df["so_luong"].values, df["gia_nhap"].values)
            df["loi_nhuan"] = (df["gia_ban"].values - df["gia_nhap"].values) * df["so_luong"].values
        else:
            df["tong_von"] = pd.Series(dtype='float64')
            df["loi_nhuan"] = pd.Series(dtype='float64')
            
        return df
    except Exception as e:
        logger.error(f"Lỗi khi đọc danh sách từ SQLite: {e}")
        return pd.DataFrame()


def them_san_pham(data_moi):
    """
    Thêm một sản phẩm mới vào cơ sở dữ liệu SQLite sau khi kiểm tra SKU duy nhất.
    """
    try:
        conn = sqlite3.connect(FILE_DB)
        cursor = conn.cursor()
        
        # Kiểm tra SKU đã tồn tại chưa
        cursor.execute("SELECT 1 FROM kho_hang WHERE ma_sku = ?", (data_moi['ma_sku'],))
        if cursor.fetchone():
            conn.close()
            return False, "Mã SKU này đã tồn tại trong hệ thống!"
            
        cursor.execute("""
            INSERT INTO kho_hang (ma_sku, ten_san_pham, loai_san_pham, so_luong, gia_nhap, gia_ban, ngay_nhap)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data_moi['ma_sku'], data_moi['ten_san_pham'], data_moi['loai_san_pham'],
            data_moi['so_luong'], data_moi['gia_nhap'], data_moi['gia_ban'], data_moi['ngay_nhap']
        ))
        conn.commit()
        conn.close()
        logger.info(f"Đã thêm sản phẩm mới: {data_moi['ten_san_pham']}")
        return True, "Thêm sản phẩm thành công!"
    except Exception as e:
        logger.error(f"Lỗi thêm sản phẩm: {e}")
        return False, str(e)


def sua_san_pham(sku_cu, data_cap_nhat):
    """
    Cập nhật thông tin của một sản phẩm dựa trên mã SKU.
    """
    try:
        conn = sqlite3.connect(FILE_DB)
        cursor = conn.cursor()
        
        # Kiểm tra sản phẩm tồn tại
        cursor.execute("SELECT 1 FROM kho_hang WHERE ma_sku = ?", (sku_cu,))
        if not cursor.fetchone():
            conn.close()
            return False, "Không tìm thấy sản phẩm để sửa!"
            
        cursor.execute("""
            UPDATE kho_hang
            SET ten_san_pham = ?, loai_san_pham = ?, so_luong = ?, gia_nhap = ?, gia_ban = ?, ngay_nhap = ?
            WHERE ma_sku = ?
        """, (
            data_cap_nhat['ten_san_pham'], data_cap_nhat['loai_san_pham'],
            data_cap_nhat['so_luong'], data_cap_nhat['gia_nhap'], data_cap_nhat['gia_ban'],
            data_cap_nhat['ngay_nhap'], sku_cu
        ))
        conn.commit()
        conn.close()
        logger.info(f"Đã cập nhật sản phẩm mã: {sku_cu}")
        return True, "Cập nhật thành công!"
    except Exception as e:
        logger.error(f"Lỗi sửa sản phẩm: {e}")
        return False, str(e)


def xoa_san_pham(danh_sach_sku):
    """
    Xóa danh sách các sản phẩm khỏi cơ sở dữ liệu.
    """
    try:
        conn = sqlite3.connect(FILE_DB)
        cursor = conn.cursor()
        
        # Tạo câu truy vấn xóa động theo số lượng SKU
        placeholders = ','.join('?' for _ in danh_sach_sku)
        cursor.execute(f"DELETE FROM kho_hang WHERE ma_sku IN ({placeholders})", tuple(danh_sach_sku))
        
        conn.commit()
        conn.close()
        logger.info(f"Đã xóa các sản phẩm: {danh_sach_sku}")
        return True, "Xóa sản phẩm thành công!"
    except Exception as e:
        logger.error(f"Lỗi xóa sản phẩm: {e}")
        return False, str(e)


def thong_ke_kho():
    """
    Thống kê tổng quan từ cơ sở dữ liệu SQLite.
    """
    df = lay_danh_sach()
    if df.empty:
        return {"tong_mat_hang": 0, "tong_gia_tri_kho": 0, "can_nhap_hang": 0, "loi_nhuan_nhom": {}}
    
    # Tính lợi nhuận trung bình theo loại sản phẩm bằng Pandas groupby
    loi_nhuan_nhom = df.groupby("loai_san_pham")["loi_nhuan"].mean().to_dict()
    
    thong_ke = {
        "tong_mat_hang": len(df),
        "tong_gia_tri_kho": df["tong_von"].sum(),
        "can_nhap_hang": len(df[df["so_luong"] < 10]),
        "loi_nhuan_nhom": loi_nhuan_nhom
    }
    return thong_ke


def import_csv(file_path):
    """
    Nhập dữ liệu từ file CSV bên ngoài và ghi/gộp vào bảng SQLite.
    Bỏ qua nếu trùng mã SKU đã tồn tại trong database.
    """
    try:
        df_new = pd.read_csv(file_path, encoding="utf-8-sig")
        conn = sqlite3.connect(FILE_DB)
        cursor = conn.cursor()
        
        # Lấy danh sách các SKU hiện có trong DB
        cursor.execute("SELECT ma_sku FROM kho_hang")
        skus_existing = set(r[0] for r in cursor.fetchall())
        
        count = 0
        for _, row in df_new.iterrows():
            sku = str(row['ma_sku']).strip()
            if sku in skus_existing:
                continue
                
            cursor.execute("""
                INSERT INTO kho_hang (ma_sku, ten_san_pham, loai_san_pham, so_luong, gia_nhap, gia_ban, ngay_nhap)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                sku, row['ten_san_pham'], row['loai_san_pham'],
                int(row['so_luong']), float(row['gia_nhap']), float(row['gia_ban']), row['ngay_nhap']
            ))
            count += 1
            
        conn.commit()
        conn.close()
        return True, f"Đã nhập thành công {count} dòng dữ liệu vào SQLite!"
    except Exception as e:
        return False, f"Lỗi Import SQLite: {str(e)}"


def export_csv(target_path):
    """
    Xuất dữ liệu từ SQLite ra file CSV tại vị trí được chỉ định.
    """
    try:
        df = lay_danh_sach()
        if not df.empty:
            # Loại bỏ các cột tính toán thêm để giữ đúng schema gốc của file CSV
            df_goc = df.drop(columns=["tong_von", "loi_nhuan"], errors="ignore")
            df_goc.to_csv(target_path, index=False, encoding="utf-8-sig")
        else:
            # Nếu trống, tạo file CSV rỗng đúng cấu trúc
            cols = ["ma_sku", "ten_san_pham", "loai_san_pham", "so_luong", "gia_nhap", "gia_ban", "ngay_nhap"]
            pd.DataFrame(columns=cols).to_csv(target_path, index=False, encoding="utf-8-sig")
        return True, "Xuất file thành công!"
    except Exception as e:
        return False, f"Lỗi Export SQLite: {str(e)}"
