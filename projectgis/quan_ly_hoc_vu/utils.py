import math
from .models import CoSo, HocVien

def tinh_khoang_cach_haversine(lat1, lon1, lat2, lon2):
    """
    Sử dụng công thức Haversine có ép kiểu dữ liệu để tránh lỗi so sánh chuỗi.
    """
    try:
        # Ép kiểu sang số thực (float) để so sánh chính xác
        lat1, lon1 = float(lat1), float(lon1)
        lat2, lon2 = float(lat2), float(lon2)
        
        R = 6371.0 # Bán kính Trái đất (km)
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        
        a = math.sin(dphi / 2)**2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    except (ValueError, TypeError):
        return float('inf') # Trả về vô cùng nếu dữ liệu lỗi

def chay_tool_dieu_phoi(hoc_vien_id):
    """
    Thuật toán tìm Min Distance (Khoảng cách ngắn nhất)
    """
    try:
        hv = HocVien.objects.get(id=hoc_vien_id)
        tat_ca_co_so = CoSo.objects.all()
        
        if not tat_ca_co_so.exists():
            return False

        # Đặt giá trị nhỏ nhất ban đầu là Vô Cùng
        khoang_cach_min = float('inf')
        co_so_gan_nhat = None

        print(f"--- Đang tính cho: {hv.ten} ---")

        # Duyệt qua tất cả cơ sở để so sánh
        for cs in tat_ca_co_so:
            d = tinh_khoang_cach_haversine(hv.lat, hv.lon, cs.lat, cs.lon)
            print(f" -> Đến {cs.ten}: {d:.2f} km")
            
            # Logic tìm số nhỏ nhất
            if d < khoang_cach_min:
                khoang_cach_min = d
                co_so_gan_nhat = cs
        
        # Lưu kết quả tốt nhất
        if co_so_gan_nhat:
            hv.co_so_gan_nhat = co_so_gan_nhat
            hv.save()
            print(f"==> CHỐT: {co_so_gan_nhat.ten} ({khoang_cach_min:.2f} km)")
            return True
            
    except Exception as e:
        print(f"Lỗi: {e}")
        return False