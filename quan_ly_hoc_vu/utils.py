import math
import requests
from django.db import transaction
from .models import CoSo, HocVien


def tinh_khoang_cach_heuristic(lat1, lon1, lat2, lon2):
    """
    Hàm tính toán khoảng cách không gian Heuristic.
    Bao gồm:
    1. Khoảng cách đường thẳng (Đường chim bay).
    2. Hệ số đường vòng đô thị (Detour Index).
    3. Logic vật cản địa lý (Qua sông, kẹt xe,...).
    """
    try:
        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
        
        # 1. Tính khoảng cách gốc (Công thức mặt cầu Trái Đất)
        R = 6371.0 
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        
        a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        khoang_cach_goc = R * c
        
        khoang_cach_uoc_tinh = khoang_cach_goc * 1.35
        
        penalty_km = 0.0
        
        if (lon1 < 106.72 and lon2 > 106.72) or (lon1 > 106.72 and lon2 < 106.72):
            penalty_km += 2.5
          
        if (10.77 <= lat1 <= 10.78) or (10.77 <= lat2 <= 10.78):
            penalty_km += 1.5
           
        if khoang_cach_goc < 0.5:
            penalty_km += 0.3

        khoang_cach_cuoi_cung = khoang_cach_uoc_tinh + penalty_km
        
        return khoang_cach_cuoi_cung

    except (ValueError, TypeError):
        return float('inf')


def lay_duong_di_thuc_te(lat1, lon1, lat2, lon2):
    """
    Gọi API OSRM (Open Source Routing Machine) để lấy khoảng cách 
    và thời gian lái xe thực tế dựa trên bản đồ giao thông.
    """
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get("code") == "Ok":
            distance_meters = data["routes"][0]["distance"]
            duration_seconds = data["routes"][0]["duration"]
            return {
                "distance_km": distance_meters / 1000.0,
                "duration_min": duration_seconds / 60.0
            }
        return None
    except Exception as e:
        print(f"Lỗi gọi API OSRM: {e}")
        return None


def chay_tool_dieu_phoi(hoc_vien_id):
    """
    Kết hợp Lọc không gian thông minh (Heuristic) và Phân tích mạng lưới (OSRM API)
    để tìm ra cơ sở gần nhất và tối ưu nhất về thời gian di chuyển.
    """
    try:
        hv = HocVien.objects.get(id=hoc_vien_id)
        tat_ca_co_so = CoSo.objects.all()
        
        if not tat_ca_co_so.exists():
            return False

        print(f"\n=== BẮT ĐẦU PHÂN TÍCH GIS (HEURISTIC) CHO: {hv.ten} ===")
        
        # BƯỚC 1: LỌC KHÔNG GIAN BẰNG THUẬT TOÁN HEURISTIC
        danh_sach_tiem_nang = []
        for cs in tat_ca_co_so:
            d_heuristic = tinh_khoang_cach_heuristic(hv.lat, hv.lon, cs.lat, cs.lon)
            
            # Lọc các cơ sở có khoảng cách dự đoán (đã bao gồm vật cản) <= 15km
            if d_heuristic <= 15.0: 
                danh_sach_tiem_nang.append({
                    "co_so": cs,
                    "heuristic_dist": d_heuristic
                })

        if not danh_sach_tiem_nang:
            print("❌ Không có cơ sở nào trong bán kính phục vụ (15km).")
            return False
            
        # Sắp xếp và lấy Top 3 cơ sở có khoảng cách dự đoán thấp nhất
        danh_sach_tiem_nang = sorted(danh_sach_tiem_nang, key=lambda x: x["heuristic_dist"])[:3]
        
        best_co_so = None
        min_drive_time = float('inf')
        actual_distance = 0

        print(f"-> Đang phân tích Network Routing cho {len(danh_sach_tiem_nang)} cơ sở tiềm năng...")

        # BƯỚC 2: PHÂN TÍCH LỘ TRÌNH THỰC TẾ (OSRM API)
        for item in danh_sach_tiem_nang:
            cs = item["co_so"]
            route_info = lay_duong_di_thuc_te(hv.lat, hv.lon, cs.lat, cs.lon)
            
            if route_info:
                d_km = route_info["distance_km"]
                t_min = route_info["duration_min"]
                print(f"   + Tuyến đến {cs.ten}: {d_km:.2f} km | Mất khoảng {t_min:.1f} phút lái xe")
                
                # Cập nhật kết quả tốt nhất
                if t_min < min_drive_time:
                    min_drive_time = t_min
                    actual_distance = d_km
                    best_co_so = cs
            else:
                # BƯỚC 3: CƠ CHẾ DỰ PHÒNG (FALLBACK) NẾU API LỖI
                print(f"   + Tuyến đến {cs.ten}: Lỗi API, dùng khoảng cách Heuristic {item['heuristic_dist']:.2f} km")
                if item["heuristic_dist"] < min_drive_time:
                    min_drive_time = item["heuristic_dist"]
                    actual_distance = item["heuristic_dist"]
                    best_co_so = cs

        # BƯỚC 4: GHI NHẬN KẾT QUẢ VÀO CSDL
        if best_co_so:
            with transaction.atomic():
                hv.co_so_gan_nhat = best_co_so
                hv.save()
                
            print(f"==> ✅ [CHỐT HỒ SƠ] Đã xếp vào {best_co_so.ten} (Cách {actual_distance:.2f} km)")
            return True
            
        return False

    except Exception as e:
        print(f"❌ Lỗi nghiêm trọng trong quá trình xử lý GIS: {e}")
        return False