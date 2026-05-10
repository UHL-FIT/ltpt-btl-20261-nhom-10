"""
utils/logger.py
===============
Cấu hình logging cho PyWarehouse.
Ghi log ra file (data/app.log) và hiển thị trên console.
"""

import os
import sys
import logging

# Xác định thư mục cơ sở để lưu dữ liệu
if getattr(sys, 'frozen', False):
    # Nếu đóng gói thành file .exe, lưu vào thư mục người dùng
    _BASE_DIR = os.path.join(os.path.expanduser("~"), "PyWarehouse_Data")
else:
    # Nếu chạy script bình thường, lưu vào thư mục dự án
    _BASE_DIR = os.path.dirname(os.path.dirname(__file__))

_LOG_DIR = os.path.join(_BASE_DIR, "data")
_LOG_FILE = os.path.join(_LOG_DIR, "app.log")


def setup_logger(name="pywarehouse"):
    """
    Khởi tạo bộ ghi log (logger) cho ứng dụng.
    """
    # Tạo thư mục logs nếu chưa có
    os.makedirs(_LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)

    # Nếu logger đã có handler thì không thêm nữa để tránh lặp log
    if logger.handlers:
        return logger

    # Thiết lập mức độ ghi log thấp nhất là DEBUG (ghi tất cả)
    logger.setLevel(logging.DEBUG)

    # Cấu hình ghi log ra file
    fh = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fmt_file = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(module)s.%(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(fmt_file)

    # Cấu hình hiển thị log ra màn hình console (chỉ các cảnh báo quan trọng)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    fmt_console = logging.Formatter("  ⚠️ [%(levelname)s] %(message)s")
    ch.setFormatter(fmt_console)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
