"""
build.py
========
Script đóng gói ứng dụng PyWarehouse thành file .exe cho Windows.
"""

import subprocess
import sys
import os
import shutil

# --- CẤU HÌNH ---
TEN_APP = "PyWarehouse"
FILE_MAIN = "main.py"
THU_MUC_DATA = "data"
THU_MUC_ASSETS = "assets"
ICON_FILE = r"assets\app_icon.ico"


def kiem_tra_pyinstaller():
    """Kiểm tra và cài đặt PyInstaller nếu cần."""
    try:
        import PyInstaller
        print(f"  [OK] PyInstaller {PyInstaller.__version__} đã sẵn sàng")
    except ImportError:
        print("  [..] Đang cài đặt PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def xoa_build_cu():
    """Dọn dẹp các thư mục build cũ."""
    for folder in ["build", "dist", f"{TEN_APP}.spec"]:
        if os.path.exists(folder):
            if os.path.isdir(folder):
                shutil.rmtree(folder)
            else:
                os.remove(folder)
            print(f"  [DEL] Đã xóa: {folder}")


def build():
    """Chạy PyInstaller để đóng gói thành file .exe duy nhất."""
    print("\n" + "=" * 50)
    print(f"  ĐÔNG GÓI ỨNG DỤNG {TEN_APP.upper()}")
    print("=" * 50)

    kiem_tra_pyinstaller()

    print("\n  [1/3] Dọn dẹp bản build cũ...")
    xoa_build_cu()

    print(f"\n  [2/3] Đang đóng gói {FILE_MAIN} -> {TEN_APP}.exe...")

    # Cấu hình lệnh chạy PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", TEN_APP,
        "--noconfirm",          # Không hỏi lại khi ghi đè
        "--windowed",           # Ẩn cửa sổ console (chế độ GUI)
        "--onefile",            # Đóng gói tất cả thành 1 file .exe duy nhất
        "--clean",              # Xóa cache cũ
        # Đưa các thư mục cần thiết vào bundle
        "--add-data", f"{THU_MUC_DATA};{THU_MUC_DATA}",
        "--add-data", f"{THU_MUC_ASSETS};{THU_MUC_ASSETS}",
        # Đảm bảo các thư viện này được nhận diện
        "--hidden-import", "pandas",
        "--hidden-import", "numpy",
    ]

    # Thêm icon nếu tồn tại
    if ICON_FILE and os.path.exists(ICON_FILE):
        cmd.extend(["--icon", ICON_FILE])

    cmd.append(FILE_MAIN)

    # Chạy lệnh
    result = subprocess.run(cmd)

    if result.returncode == 0:
        exe_path = os.path.join("dist", f"{TEN_APP}.exe")
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print("\n" + "=" * 50)
        print("  [OK] ĐÓNG GÓI THÀNH CÔNG!")
        print(f"  File: {os.path.abspath(exe_path)}")
        print(f"  Dung lượng: {size_mb:.1f} MB")
        print("=" * 50)
        return True
    else:
        print("\n  [FAIL] Đóng gói thất bại!")
        return False


if __name__ == "__main__":
    build()
