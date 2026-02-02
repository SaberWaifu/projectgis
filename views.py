import random # Cần thiết để random học sinh vào lớp
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count 
from math import radians, cos, sin, asin, sqrt

# Import đầy đủ các Model và Tool hỗ trợ
from .utils import chay_tool_dieu_phoi
from .ga_solver import GeneticScheduler
from .models import CoSo, HocVien, LichHoc, GiaoVien, PhongHoc, LopHoc 

# --- HÀM PHỤ TRỢ ---
def tinh_khoang_cach_haversine(lat1, lon1, lat2, lon2):
    """Tính khoảng cách giữa 2 điểm tọa độ (km)"""
    R = 6371 
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

# --- CÁC VIEW CHÍNH ---

def trang_chu(request):
    return render(request, 'trang_chu.html')

def dieu_phoi_page(request):
    return render(request, 'index.html', {
        'hoc_vien': HocVien.objects.all(), 
        'co_so': CoSo.objects.all()
    })

def chi_nhanh_page(request):
    return render(request, 'chi_nhanh.html', {'co_so': CoSo.objects.all()})

def thong_ke_page(request):
    du_lieu = CoSo.objects.annotate(so_hv=Count('hocvien'))
    thong_ke_khoi = HocVien.objects.values('khoi_lop').annotate(count=Count('id'))
    return render(request, 'thong_ke.html', {'du_lieu': du_lieu, 'thong_ke_khoi': thong_ke_khoi})

def kich_hoat_gis(request, hv_id):
    chay_tool_dieu_phoi(hv_id)
    return redirect('dieu_phoi_page')

def dang_ky_page(request):
    ket_qua = None 
    if request.method == "POST":
        ten = request.POST.get('ten')
        khoi = request.POST.get('khoi_lop')
        lat = float(request.POST.get('lat'))
        lon = float(request.POST.get('lon'))
        
        hv = HocVien.objects.create(ten=ten, khoi_lop=khoi, lat=lat, lon=lon)
        
        # Chạy GIS tìm cơ sở gần nhất
        min_dist = float('inf')
        best_cs = None
        for cs in CoSo.objects.all():
            d = tinh_khoang_cach_haversine(lat, lon, cs.lat, cs.lon)
            if d < min_dist:
                min_dist = d
                best_cs = cs
        
        if best_cs:
            hv.co_so_gan_nhat = best_cs
            hv.save()
            ket_qua = {'hoc_vien': hv, 'co_so': best_cs, 'khoang_cach': round(min_dist, 2)}

    return render(request, 'dang_ky.html', {'ket_qua': ket_qua})

def quan_ly_page(request):
    if request.method == "POST":
        try:
            hv = HocVien.objects.create(
                ten=request.POST.get('ten'),
                khoi_lop=request.POST.get('khoi_lop'),
                lat=float(request.POST.get('lat')),
                lon=float(request.POST.get('lon'))
            )
            chay_tool_dieu_phoi(hv.id)
            messages.success(request, f"Đã thêm {hv.ten} thành công!")
        except Exception as e:
            messages.error(request, f"Lỗi: {e}")
        return redirect('quan_ly_page')

    return render(request, 'quan_ly.html', {'danh_sach': HocVien.objects.all().order_by('-id')})

def xoa_hoc_vien(request, hv_id):
    get_object_or_404(HocVien, id=hv_id).delete()
    messages.success(request, "Đã xóa học viên.")
    return redirect('quan_ly_page')

# --- LOGIC XẾP LỊCH & TẠO DỮ LIỆU ---

def xep_lich_page(request):
    """Trang hiển thị và xử lý xếp lịch AI"""
    if request.method == "POST":
        try:
            ga = GeneticScheduler()
            success = ga.run()
            if success:
                messages.success(request, "Đã xếp lịch tự động thành công!")
            else:
                messages.warning(request, "Chưa xếp được. Có thể do thiếu Lớp Học 'Đã Mở' hoặc thiếu Phòng.")
        except Exception as e:
            messages.error(request, f"Lỗi hệ thống: {str(e)}")
        return redirect('xep_lich_page')

    lich_hoc = LichHoc.objects.all().order_by('thu', 'ca')
    return render(request, 'xep_lich.html', {'lich_hoc': lich_hoc})

def tao_du_lieu_mau(request):
    tat_ca_co_so = CoSo.objects.all()
    if not tat_ca_co_so.exists():
        messages.error(request, "Cần tạo Cơ sở trước!")
        return redirect('xep_lich_page')

    # --- XÓA SẠCH DỮ LIỆU CŨ ĐỂ TẠO MỚI CHO ĐẸP ---
    LichHoc.objects.all().delete()
    LopHoc.objects.all().delete()
    # ----------------------------------------------

    count_lop = 0
    hoc_viens = list(HocVien.objects.all())

    for cs in tat_ca_co_so:
        # 1. Tạo Giáo Viên
        gv_toan, _ = GiaoVien.objects.get_or_create(ten=f"Thầy Toán ({cs.ten})", mon_day="Toán", co_so=cs)
        gv_ly, _ = GiaoVien.objects.get_or_create(ten=f"Cô Lý ({cs.ten})", mon_day="Lý", co_so=cs)
        gv_anh, _ = GiaoVien.objects.get_or_create(ten=f"Cô Anh ({cs.ten})", mon_day="Anh", co_so=cs)

        # 2. Tạo Phòng
        PhongHoc.objects.get_or_create(ten="P.101 (30 chỗ)", suc_chua=30, co_so=cs)
        PhongHoc.objects.get_or_create(ten="P.102 (30 chỗ)", suc_chua=30, co_so=cs)
        PhongHoc.objects.get_or_create(ten="Lab (40 chỗ)", suc_chua=40, co_so=cs)

        # 3. Tạo 6 LỚP CHO MỖI CƠ SỞ
        ds_lop = [
            ("Toán 6A Nâng Cao", gv_toan),
            ("Toán 9C Ôn Thi", gv_toan),
            ("Toán 8B Cơ Bản", gv_toan),
            ("Lý 8B Cơ Bản", gv_ly),
            ("Lý 9A Nâng Cao", gv_ly),
            ("Anh 6C Giao Tiếp", gv_anh)
        ]

        for ten_lop, gv in ds_lop:
            lop = LopHoc.objects.create(
                ten_lop=f"{ten_lop} - {cs.ten}",
                giao_vien=gv,
                min_si_so=5,
                trang_thai='MO'
            )
            
            # Random học sinh
            if len(hoc_viens) >= 5:
                so_luong = random.randint(5, min(10, len(hoc_viens)))
                lop.hoc_viens.set(random.sample(hoc_viens, so_luong))
                lop.save()
            
            count_lop += 1

    messages.success(request, f"Đã Reset và tạo mới {count_lop} lớp học!")
    return redirect('xep_lich_page')

def dang_ky_lop(request, lop_id, hv_id):
    """Xử lý học viên đăng ký vào lớp -> Tự động mở lớp nếu đủ người"""
    lop = get_object_or_404(LopHoc, id=lop_id)
    hoc_vien = get_object_or_404(HocVien, id=hv_id)
    
    lop.hoc_viens.add(hoc_vien)
    lop.cap_nhat_trang_thai()

    return redirect('xep_lich_page')
# views.py

def xoa_tool_dieu_phoi(request, hv_id):
    """Gỡ bỏ kết quả phân công GIS cho học viên cụ thể"""
    # Lấy học viên hoặc trả về 404 nếu không tồn tại
    hoc_vien = get_object_or_404(HocVien, id=hv_id)
    
    # Reset kết quả từ tool điều phối
    hoc_vien.co_so_gan_nhat = None
    hoc_vien.save()
    
    # Gửi thông báo cho người dùng thông qua hệ thống messages
    messages.info(request, f"Đã gỡ bỏ kết quả điều phối của học viên {hoc_vien.ten}.")
    
    # Điều hướng về trang quản lý
    return redirect('quan_ly_page')