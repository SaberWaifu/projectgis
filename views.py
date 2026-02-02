import random 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum
from math import radians, cos, sin, asin, sqrt

# Import Models & Tools
from .utils import chay_tool_dieu_phoi
from .ga_solver import GeneticScheduler
from .models import CoSo, HocVien, LichHoc, GiaoVien, PhongHoc, LopHoc , HoaDon

def login_view(request):
    """Trang đăng nhập hệ thống"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xin chào, {user.username}!")
            return redirect('trang_chu') # Đăng nhập xong về Trang chủ
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """Đăng xuất"""
    logout(request)
    messages.info(request, "Đã đăng xuất thành công.")
    return redirect('login')

# --- HÀM PHỤ TRỢ ---
def tinh_khoang_cach_haversine(lat1, lon1, lat2, lon2):
    R = 6371 
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

# --- CÁC VIEW CHÍNH (GIỮ NGUYÊN) ---

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

# Trong quan_ly_hoc_vu/views.py

def chi_nhanh_page(request):
    """Trang quản lý danh sách chi nhánh (Cơ sở)"""
    
    # --- 1. XỬ LÝ THÊM MỚI (POST) ---
    if request.method == "POST":
        try:
            ten = request.POST.get('ten')
            dia_chi = request.POST.get('dia_chi')
            lat = request.POST.get('lat')
            lon = request.POST.get('lon')
            
            # Kiểm tra dữ liệu cơ bản
            if not ten or not lat or not lon:
                messages.error(request, "Vui lòng nhập Tên và Tọa độ (Lat/Lon)!")
            else:
                CoSo.objects.create(
                    ten=ten,
                    dia_chi=dia_chi,
                    lat=float(lat),
                    lon=float(lon)
                )
                messages.success(request, f"Đã khai trương cơ sở: {ten}")
        except Exception as e:
            messages.error(request, f"Lỗi hệ thống: {e}")
        return redirect('chi_nhanh_page')

    # --- 2. HIỂN THỊ DANH SÁCH (GET) ---
    danh_sach = CoSo.objects.all().order_by('-id')
    
    # Thống kê nhanh
    stats = {
        'total': danh_sach.count(),
        'total_students': HocVien.objects.count()
    }
    
    return render(request, 'chi_nhanh.html', {
        'co_so': danh_sach,
        'stats': stats
    })

def xoa_chi_nhanh(request, cs_id):
    """Xóa một chi nhánh"""
    try:
        cs = get_object_or_404(CoSo, id=cs_id)
        ten = cs.ten
        cs.delete()
        messages.success(request, f"Đã đóng cửa và xóa: {ten}")
    except Exception as e:
        messages.error(request, "Lỗi khi xóa: " + str(e))
    return redirect('chi_nhanh_page')

# --- LOGIC XẾP LỊCH ---

def xep_lich_page(request):
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

    LichHoc.objects.all().delete()
    LopHoc.objects.all().delete()

    count_lop = 0
    hoc_viens = list(HocVien.objects.all())

    for cs in tat_ca_co_so:
        gv_toan, _ = GiaoVien.objects.get_or_create(ten=f"Thầy Toán ({cs.ten})", mon_day="Toán", co_so=cs)
        gv_ly, _ = GiaoVien.objects.get_or_create(ten=f"Cô Lý ({cs.ten})", mon_day="Lý", co_so=cs)
        gv_anh, _ = GiaoVien.objects.get_or_create(ten=f"Cô Anh ({cs.ten})", mon_day="Anh", co_so=cs)

        PhongHoc.objects.get_or_create(ten="P.101 (30 chỗ)", suc_chua=30, co_so=cs)
        PhongHoc.objects.get_or_create(ten="P.102 (30 chỗ)", suc_chua=30, co_so=cs)
        PhongHoc.objects.get_or_create(ten="Lab (40 chỗ)", suc_chua=40, co_so=cs)

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
            
            if len(hoc_viens) >= 5:
                so_luong = random.randint(5, min(10, len(hoc_viens)))
                lop.hoc_viens.set(random.sample(hoc_viens, so_luong))
                lop.save()
            
            count_lop += 1

    messages.success(request, f"Đã Reset và tạo mới {count_lop} lớp học!")
    return redirect('xep_lich_page')

def dang_ky_lop(request, lop_id, hv_id):
    lop = get_object_or_404(LopHoc, id=lop_id)
    hoc_vien = get_object_or_404(HocVien, id=hv_id)
    lop.hoc_viens.add(hoc_vien)
    lop.cap_nhat_trang_thai()
    return redirect('xep_lich_page')

# --- MỚI: TRANG QUẢN LÝ LỚP HỌC ---
def quan_ly_lop_page(request):
    # --- 1. XỬ LÝ LƯU DỮ LIỆU (POST) ---
    if request.method == "POST":
        try:
            # Lấy dữ liệu từ các ô input
            ten_nhap = request.POST.get('ten_lop')
            mon_hoc = request.POST.get('mon_hoc')
            khoi = request.POST.get('khoi')
            giao_vien_id = request.POST.get('giao_vien')

            # Kiểm tra dữ liệu
            if not ten_nhap or not giao_vien_id:
                messages.error(request, "Thiếu tên lớp hoặc giáo viên!")
            else:
                # Tạo tên lớp đầy đủ (Ví dụ: "Toán 6A - Toán - Khối 6")
                # Để tận dụng các trường thầy nhập trên form
                ten_day_du = f"{ten_nhap}" 
                if mon_hoc and khoi:
                    ten_day_du = f"{ten_nhap} ({mon_hoc} {khoi})"

                # Lưu vào Database
                LopHoc.objects.create(
                    ten_lop=ten_day_du,
                    giao_vien_id=giao_vien_id,
                    min_si_so=10,
                    trang_thai='CHO',
                    si_so_toi_da=30
                )
                messages.success(request, f"Đã mở lớp {ten_day_du} thành công!")
                
        except Exception as e:
            print(f"Lỗi Save: {e}") # Xem lỗi ở cửa sổ đen (Terminal)
            messages.error(request, f"Lỗi hệ thống: {str(e)}")
            
        return redirect('quan_ly_lop_page')

    # --- 2. HIỂN THỊ DỮ LIỆU (GET) ---
    search_query = request.GET.get('q', '')
    ds_lop = LopHoc.objects.all().select_related('giao_vien').prefetch_related('hoc_viens').order_by('-id')
    
    if search_query:
        ds_lop = ds_lop.filter(ten_lop__icontains=search_query)

    stats = {
        'total_class': ds_lop.count(),
        'total_student': HocVien.objects.count(),
        'active_class': ds_lop.filter(trang_thai='MO').count()
    }
    
    # Lấy danh sách giáo viên để hiện trong Modal
    ds_giao_vien = GiaoVien.objects.all()

    return render(request, 'quan_ly_lop.html', {
        'ds_lop': ds_lop,
        'stats': stats,
        'ds_giao_vien': ds_giao_vien
    })
    
    
    # Trong quan_ly_hoc_vu/views.py

def xoa_lop_hoc(request, lop_id):
    """Hàm xử lý xóa lớp học"""
    try:
        lop = get_object_or_404(LopHoc, id=lop_id)
        ten_lop = lop.ten_lop
        lop.delete()
        messages.success(request, f"Đã xóa lớp {ten_lop} thành công!")
    except Exception as e:
        messages.error(request, f"Lỗi khi xóa: {str(e)}")
    
    return redirect('quan_ly_lop_page')

# Trong views.py

def quan_ly_hoc_phi(request):
    """Trang quản lý thu chi / học phí"""
    
    # 1. XỬ LÝ TẠO HÓA ĐƠN MỚI (POST)
    if request.method == "POST":
        try:
            hv_id = request.POST.get('hoc_vien')
            so_tien = request.POST.get('so_tien')
            noi_dung = request.POST.get('noi_dung')
            
            if not hv_id or not so_tien:
                messages.error(request, "Vui lòng chọn học viên và nhập số tiền!")
            else:
                hv = HocVien.objects.get(id=hv_id)
                HoaDon.objects.create(
                    hoc_vien=hv,
                    so_tien=so_tien,
                    noi_dung=noi_dung,
                    trang_thai='ROI'
                )
                messages.success(request, f"Đã lập phiếu thu cho: {hv.ten}")
        except Exception as e:
            messages.error(request, f"Lỗi: {e}")
        return redirect('quan_ly_hoc_phi')

    # 2. LẤY DỮ LIỆU HIỂN THỊ
    ds_hoa_don = HoaDon.objects.all().select_related('hoc_vien').order_by('-ngay_tao')
    ds_hoc_vien = HocVien.objects.all() # Để hiện trong Modal chọn người đóng tiền

    # Thống kê tổng doanh thu
    tong_doanh_thu = ds_hoa_don.aggregate(Sum('so_tien'))['so_tien__sum'] or 0
    
    stats = {
        'total_revenue': tong_doanh_thu,
        'total_invoices': ds_hoa_don.count(),
        'recent_paid': ds_hoa_don.filter(trang_thai='ROI').count()
    }

    return render(request, 'quan_ly_hoc_phi.html', {
        'ds_hoa_don': ds_hoa_don,
        'ds_hoc_vien': ds_hoc_vien,
        'stats': stats
    })

def xoa_hoa_don(request, hd_id):
    try:
        hd = get_object_or_404(HoaDon, id=hd_id)
        hd.delete()
        messages.success(request, "Đã hủy hóa đơn thành công!")
    except Exception as e:
        messages.error(request, "Lỗi: " + str(e))
    return redirect('quan_ly_hoc_phi')

