from flask import Flask, jsonify, request
import models.kho_hang as model

app = Flask(__name__)

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    API endpoint: Lấy danh sách sản phẩm dưới dạng JSON.
    """
    df = model.lay_danh_sach()
    if df.empty:
        return jsonify([])
    # Chuyển đổi DataFrame sang list dict để trả về JSON
    res = df.to_dict(orient="records")
    return jsonify(res)

@app.route('/api/products', methods=['POST'])
def add_product():
    """
    API endpoint: Thêm mới một sản phẩm từ JSON request body.
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Yêu cầu rỗng!"}), 400
        
    # Validation cơ bản
    required_fields = ["ma_sku", "ten_san_pham", "so_luong", "gia_nhap", "gia_ban"]
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Thiếu trường bắt buộc: {field}"}), 400
            
    # Gán các giá trị phân loại và ngày nhập mặc định nếu thiếu
    data_moi = {
        "ma_sku": str(data["ma_sku"]).strip(),
        "ten_san_pham": str(data["ten_san_pham"]).strip(),
        "loai_san_pham": str(data.get("loai_san_pham", "Khác")).strip(),
        "so_luong": int(data["so_luong"]),
        "gia_nhap": float(data["gia_nhap"]),
        "gia_ban": float(data["gia_ban"]),
        "ngay_nhap": str(data.get("ngay_nhap", "2026-05-26")).strip()
    }
    
    ok, msg = model.them_san_pham(data_moi)
    if ok:
        return jsonify({"success": True, "message": msg}), 201
    else:
        return jsonify({"success": False, "message": msg}), 400

@app.route('/api/products/<sku>', methods=['DELETE'])
def delete_product(sku):
    """
    API endpoint: Xóa sản phẩm theo mã SKU.
    """
    ok, msg = model.xoa_san_pham([sku])
    if ok:
        return jsonify({"success": True, "message": f"Đã xóa sản phẩm {sku} thành công!"})
    else:
        return jsonify({"success": False, "message": msg}), 400

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    API endpoint: Lấy số liệu thống kê tổng quát của kho hàng.
    """
    tk = model.thong_ke_kho()
    return jsonify(tk)

def run_server():
    """
    Khởi chạy server Flask trên cổng 5000 tại localhost (127.0.0.1)
    """
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
