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

# --- 2. CÁC MODEL MỚI (XẾP LỊCH) ---
class GiaoVien(models.Model):
    # Dòng này phải thụt vào trong so với chữ 'class'
    ten = models.CharField(max_length=100)
    mon_day = models.CharField(max_length=50, default="Toán") # Toán, Lý, Hóa
    co_so = models.ForeignKey(CoSo, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.ten} ({self.mon_day})"

class PhongHoc(models.Model):
    ten = models.CharField(max_length=50)
    co_so = models.ForeignKey(CoSo, on_delete=models.CASCADE)
    # THÊM MỚI: Sức chứa tối đa của phòng
    suc_chua = models.IntegerField(default=30, help_text="Số lượng học viên tối đa")

    def __str__(self):
        return f"{self.ten} (Chứa: {self.suc_chua})"

class LopHoc(models.Model):
    TRANG_THAI = [
        ('CHO', 'Đang chờ (Chưa đủ HS)'),
        ('MO', 'Đã mở lớp (Sẵn sàng)'),
        ('HUY', 'Hủy lớp'),
    ]
    
    ten_lop = models.CharField(max_length=100) # Ví dụ: Toán 6 Nâng Cao
    giao_vien = models.ForeignKey(GiaoVien, on_delete=models.CASCADE)
    
    # Logic: Lớp này dự kiến bao nhiêu trò
    si_so_du_kien = models.IntegerField(default=0)
    
    # Logic: Điều kiện mở lớp (Thầy nói > 20 mới mở)
    min_si_so = models.IntegerField(default=20) 
    
    trang_thai = models.CharField(max_length=10, choices=TRANG_THAI, default='CHO')
    
    # Danh sách học viên đăng ký vào lớp này (Many-to-Many)
    hoc_viens = models.ManyToManyField(HocVien, blank=True)

    def cap_nhat_trang_thai(self):
        """Hàm tự động kiểm tra xem có đủ người để mở lớp không"""
        hien_tai = self.hoc_viens.count()
        if hien_tai >= self.min_si_so:
            self.trang_thai = 'MO'
        else:
            self.trang_thai = 'CHO'
        self.save()

    def __str__(self):
        return f"{self.ten_lop} ({self.hoc_viens.count()}/{self.min_si_so})"

# Cập nhật LichHoc để xếp lịch cho cả LỚP chứ không phải từng em lẻ
class LichHoc(models.Model):
    # Thay vì hoc_vien lẻ, ta xếp cho cả LopHoc
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE, null=True) 
    phong = models.ForeignKey(PhongHoc, on_delete=models.CASCADE, null=True)
    thu = models.IntegerField()
    ca = models.IntegerField()
    
    # ...