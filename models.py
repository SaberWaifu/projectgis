from django.db import models

# --- 1. CÁC MODEL CŨ (Giữ nguyên) ---
class CoSo(models.Model):
    ten = models.CharField(max_length=100)
    dia_chi = models.CharField(max_length=255, null=True, blank=True) 
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    hinh_anh = models.ImageField(upload_to='co_so/', null=True, blank=True)

    def __str__(self):
        return self.ten

class HocVien(models.Model):
    ten = models.CharField(max_length=100)
    dia_chi = models.CharField(max_length=255, null=True, blank=True)
    khoi_lop = models.IntegerField(choices=[(6, 'Lớp 6'), (8, 'Lớp 8'), (9, 'Lớp 9')])
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    co_so_gan_nhat = models.ForeignKey(CoSo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.ten} - Khối {self.khoi_lop}"

# --- 2. CÁC MODEL MỚI (XẾP LỊCH & QUẢN LÝ LỚP) ---

class GiaoVien(models.Model):
    ten = models.CharField(max_length=100)
    mon_day = models.CharField(max_length=50, default="Toán") # Toán, Lý, Hóa
    co_so = models.ForeignKey(CoSo, on_delete=models.CASCADE, null=True)
    # Thêm ảnh đại diện để hiện lên thẻ lớp học
    anh_dai_dien = models.ImageField(upload_to='giao_vien/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.ten} ({self.mon_day})"

class PhongHoc(models.Model):
    ten = models.CharField(max_length=50) # VD: Phòng 101
    co_so = models.ForeignKey(CoSo, on_delete=models.CASCADE)
    suc_chua = models.IntegerField(default=30, help_text="Số lượng học viên tối đa")

    def __str__(self):
        return f"{self.ten} - {self.co_so.ten}"

class LopHoc(models.Model):
    TRANG_THAI = [
        ('CHO', 'Sắp mở (Đang tuyển)'),
        ('MO', 'Đang học (Running)'),
        ('HUY', 'Đã kết thúc/Hủy'),
    ]
    
    ten_lop = models.CharField(max_length=100)
    giao_vien = models.ForeignKey(GiaoVien, on_delete=models.SET_NULL, null=True)
    

    si_so_toi_da = models.IntegerField(default=30)
    

    min_si_so = models.IntegerField(default=20) 
    
    trang_thai = models.CharField(max_length=10, choices=TRANG_THAI, default='CHO')
    

    hoc_viens = models.ManyToManyField(HocVien, blank=True, related_name='cac_lop_tham_gia')

    def si_so_hien_tai(self):
        """Đếm số học sinh đang có trong lớp"""
        return self.hoc_viens.count()

    def phan_tram_lap_day(self):
        """Tính % để vẽ thanh Progress Bar"""
        if self.si_so_toi_da == 0: return 0
        percent = (self.si_so_hien_tai() / self.si_so_toi_da) * 100
        return round(percent)

    def cap_nhat_trang_thai(self):
        """Hàm tự động chuyển trạng thái nếu đủ người"""
        hien_tai = self.si_so_hien_tai()
        if hien_tai >= self.min_si_so:
            self.trang_thai = 'MO'
        else:
            self.trang_thai = 'CHO'
        self.save()

    def __str__(self):
        return f"{self.ten_lop} ({self.si_so_hien_tai()}/{self.si_so_toi_da})"

class LichHoc(models.Model):
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE, related_name='lich_hoc') 
    phong = models.ForeignKey(PhongHoc, on_delete=models.SET_NULL, null=True)
    

    thu = models.IntegerField(choices=[(i, f"Thứ {i}") for i in range(2, 9)])

    ca = models.IntegerField() 

    def __str__(self):
        return f"{self.lop_hoc.ten_lop} - Thứ {self.thu} - Ca {self.ca}"
    
class HoaDon(models.Model):
    TRANG_THAI_THANH_TOAN = [
        ('CHUA', 'Chưa thanh toán'),
        ('ROI', 'Đã thanh toán'),
    ]
    
    hoc_vien = models.ForeignKey(HocVien, on_delete=models.CASCADE, related_name='hoa_don')
    noi_dung = models.CharField(max_length=200, default="Học phí tháng ...")
    so_tien = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    trang_thai = models.CharField(max_length=10, choices=TRANG_THAI_THANH_TOAN, default='ROI')
    
    def __str__(self):
        return f"{self.hoc_vien.ten} - {self.so_tien}"