import os
import unittest
import pandas as pd
from models import kho_hang

class TestKhoHangModel(unittest.TestCase):
    """
    Bộ kiểm thử tự động (Unit Test) cho các logic xử lý dữ liệu của PyWarehouse.
    Giúp đảm bảo các hàm tính toán và lưu trữ hoạt động chính xác.
    """
    
    def setUp(self):
        """
        Hàm thiết lập chạy trước mỗi bài test.
        Chúng ta sẽ tạo một file CSV giả lập để không làm ảnh hưởng đến dữ liệu thật.
        """
        self.test_file = os.path.join(os.path.dirname(__file__), "test_kho_hang.csv")
        # Ghi đè đường dẫn file trong model bằng file test tạm thời
        kho_hang.FILE_KHO = self.test_file
        
        # Đảm bảo file test cũ bị xóa trước khi bắt đầu
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """
        Hàm dọn dẹp chạy sau mỗi bài test.
        Xóa file test tạm thời để giữ thư mục sạch sẽ.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_01_khoi_tao_csv(self):
        """Kiểm tra việc tự động tạo file CSV mới khi chưa tồn tại."""
        kho_hang.khoi_tao_csv()
        self.assertTrue(os.path.exists(self.test_file))
        
        # Kiểm tra xem các cột có đúng yêu cầu không
        df = pd.read_csv(self.test_file)
        cac_cot_mong_muon = ["ma_sku", "ten_san_pham", "loai_san_pham", "so_luong", "gia_nhap", "gia_ban", "ngay_nhap"]
        self.assertEqual(list(df.columns), cac_cot_mong_muon)

    def test_02_them_san_pham(self):
        """Kiểm tra chức năng thêm sản phẩm mới và chặn trùng SKU."""
        kho_hang.khoi_tao_csv()
        
        data = {
            "ma_sku": "TEST01",
            "ten_san_pham": "Sản phẩm Test",
            "loai_san_pham": "Quà tặng",
            "so_luong": 10,
            "gia_nhap": 1000,
            "gia_ban": 2000,
            "ngay_nhap": "2026-01-01"
        }
        
        # Lần 1: Thêm mới (Kỳ vọng: Thành công)
        ok, msg = kho_hang.them_san_pham(data)
        self.assertTrue(ok)
        
        # Lần 2: Thêm trùng SKU (Kỳ vọng: Thất bại)
        ok_trung, msg_trung = kho_hang.them_san_pham(data)
        self.assertFalse(ok_trung)
        self.assertIn("đã tồn tại", msg_trung)

    def test_03_tinh_toan_numpy(self):
        """
        Kiểm tra các phép toán mảng bằng Numpy trong Model.
        Cụ thể là tính Tổng Vốn và Lợi Nhuận.
        """
        kho_hang.khoi_tao_csv()
        data = {
            "ma_sku": "TEST02",
            "ten_san_pham": "Máy tính",
            "loai_san_pham": "Điện tử",
            "so_luong": 5, # 5 cái
            "gia_nhap": 10000000, # 10 triệu
            "gia_ban": 12000000,  # 12 triệu
            "ngay_nhap": "2026-01-01"
        }
        kho_hang.them_san_pham(data)
        
        # Lấy danh sách để Model thực hiện tính toán realtime
        df = kho_hang.lay_danh_sach()
        
        # Kiểm tra Tổng vốn = 5 * 10.000.000 = 50.000.000
        self.assertEqual(df.iloc[0]["tong_von"], 50000000)
        
        # Kiểm tra Lợi nhuận = (12tr - 10tr) * 5 = 10.000.000
        self.assertEqual(df.iloc[0]["loi_nhuan"], 10000000)

    def test_04_thong_ke_pandas(self):
        """Kiểm tra chức năng thống kê tổng quát của kho hàng."""
        kho_hang.khoi_tao_csv()
        # Thêm 2 sản phẩm khác nhau
        kho_hang.them_san_pham({
            "ma_sku": "SKU1", "ten_san_pham": "A", "loai_san_pham": "Văn phòng",
            "so_luong": 5, "gia_nhap": 100, "gia_ban": 200, "ngay_nhap": "2026-01-01"
        })
        kho_hang.them_san_pham({
            "ma_sku": "SKU2", "ten_san_pham": "B", "loai_san_pham": "Văn phòng",
            "so_luong": 20, "gia_nhap": 200, "gia_ban": 300, "ngay_nhap": "2026-01-01"
        })
        
        tk = kho_hang.thong_ke_kho()
        
        # Tổng mặt hàng = 2
        self.assertEqual(tk["tong_mat_hang"], 2)
        # Tổng vốn = (5*100) + (20*200) = 500 + 4000 = 4500
        self.assertEqual(tk["tong_gia_tri_kho"], 4500)
        # Sản phẩm cần nhập (dưới 10) = 1 (là SKU1 có sl=5)
        self.assertEqual(tk["can_nhap_hang"], 1)

    def test_05_xoa_san_pham(self):
        """Kiểm tra chức năng xóa sản phẩm."""
        kho_hang.khoi_tao_csv()
        kho_hang.them_san_pham({
            "ma_sku": "DEL_ME", 
            "ten_san_pham": "X", 
            "loai_san_pham": "Điện tử", # Đã thêm cột loại
            "so_luong": 1, 
            "gia_nhap": 1, 
            "gia_ban": 2, 
            "ngay_nhap": "2026-01-01"
        })
        
        ok, msg = kho_hang.xoa_san_pham(["DEL_ME"])
        self.assertTrue(ok)
        df = kho_hang.lay_danh_sach()
        self.assertEqual(len(df), 0)

if __name__ == '__main__':
    unittest.main()
