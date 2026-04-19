from django.db import models

# =========================================================
# BỘ TỪ ĐIỂN LỖI TIẾNG VIỆT (Dùng chung cho các bảng)
# =========================================================
LOI_CHUOI = {
    'blank': 'Trường này không được để trống.',
    'required': 'Vui lòng nhập thông tin vào trường này.',
    'max_length': 'Đoạn văn bản này quá dài so với quy định.'
}

LOI_SO = {
    'invalid': 'Vui lòng nhập một con số hợp lệ (không chứa chữ cái hay dấu phẩy).',
    'required': 'Vui lòng nhập số liệu.',
    'max_digits': 'Con số này quá lớn so với giới hạn cho phép.'
}

LOI_KHOA_NGOAI = {
    'required': 'Vui lòng chọn một mục từ danh sách.',
    'null': 'Trường này không được để trống.',
    'invalid_choice': 'Lựa chọn của bạn không hợp lệ.'
}

# =========================================================
# CÁC CLASS MODEL CỦA HỆ THỐNG
# =========================================================

class CoSo(models.Model):
    ten = models.CharField(max_length=100, error_messages=LOI_CHUOI)
    dia_chi = models.CharField(max_length=255, null=True, blank=True)
    mo_ta = models.TextField(null=True, blank=True, verbose_name="Mô tả chi nhánh")
    lat = models.FloatField(default=0.0, error_messages=LOI_SO)
    lon = models.FloatField(default=0.0, error_messages=LOI_SO)
    hinh_anh = models.ImageField(upload_to='co_so/', max_length=500, null=True, blank=True, 
                                 error_messages={'invalid': 'Định dạng file ảnh không hợp lệ.'})

    def __str__(self):
        return self.ten

class AnhCoSo(models.Model):
    """Bảng lưu nhiều ảnh cho mỗi Chi nhánh / Cơ sở"""
    co_so = models.ForeignKey(CoSo, on_delete=models.CASCADE, related_name='anh_co_so')
    hinh_anh = models.ImageField(upload_to='co_so/gallery/', max_length=500)
    thu_tu = models.IntegerField(default=0, help_text="Thứ tự hiển thị (0 = ảnh bìa)")
    ngay_them = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['thu_tu', 'ngay_them']

    def __str__(self):
        return f"Ảnh #{self.id} - {self.co_so.ten}"

class HocVien(models.Model):
    KHOI_CHOICES = [(i, f'Lớp {i}') for i in range(1, 13)]
    
    ten = models.CharField(max_length=100, error_messages=LOI_CHUOI)
    dia_chi = models.CharField(max_length=255, null=True, blank=True)
    khoi_lop = models.IntegerField(choices=KHOI_CHOICES, default=12, 
                                   error_messages={'invalid_choice': 'Vui lòng chọn khối lớp hợp lệ.', 'invalid': 'Khối lớp phải là số.'})
    lat = models.FloatField(default=0.0, error_messages=LOI_SO)
    lon = models.FloatField(default=0.0, error_messages=LOI_SO)
    co_so_gan_nhat = models.ForeignKey(CoSo, on_delete=models.SET_NULL, null=True, blank=True, error_messages=LOI_KHOA_NGOAI)
    hinh_anh = models.ImageField(upload_to='avatars/', max_length=500, null=True, blank=True,
                                 error_messages={'invalid': 'Định dạng file ảnh không hợp lệ.'})

    def __str__(self):
        return f"{self.ten} - Khối {self.khoi_lop}"

class KhoaHoc(models.Model):
    ten_khoa_hoc = models.CharField(max_length=150, error_messages=LOI_CHUOI)
    mo_ta = models.TextField(blank=True, null=True)
    hinh_anh = models.CharField(max_length=500, blank=True, null=True)
    hoc_phi = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, error_messages=LOI_SO)

    def __str__(self):
        return self.ten_khoa_hoc

# LƯU Ý: CHỈ CÓ DUY NHẤT 1 CLASS GIÁO VIÊN Ở ĐÂY VÀ ĐÃ CÓ tai_khoan
class GiaoVien(models.Model):
    ten = models.CharField(max_length=100, error_messages=LOI_CHUOI)
    tai_khoan = models.CharField(max_length=50, null=True, blank=True) 
    mon_day = models.CharField(max_length=50, default="Toán", error_messages=LOI_CHUOI)
    co_so = models.ForeignKey(CoSo, on_delete=models.CASCADE, null=True, error_messages=LOI_KHOA_NGOAI)
    anh_dai_dien = models.ImageField(upload_to='giao_vien/', max_length=500, null=True, blank=True,
                                     error_messages={'invalid': 'Định dạng file ảnh không hợp lệ.'})
    
    def __str__(self):
        return f"{self.ten} ({self.mon_day})"

class PhongHoc(models.Model):
    ten = models.CharField(max_length=50, error_messages=LOI_CHUOI)
    co_so = models.ForeignKey(CoSo, on_delete=models.CASCADE, error_messages=LOI_KHOA_NGOAI)
    suc_chua = models.IntegerField(default=30, help_text="Số lượng học viên tối đa", error_messages=LOI_SO)

    def __str__(self):
        return f"{self.ten} - {self.co_so.ten}"

class LopHoc(models.Model):
    TRANG_THAI = [
        ('CHO', 'Sắp mở (Đang tuyển)'),
        ('MO', 'Đang học (Running)'),
        ('HUY', 'Đã kết thúc/Hủy'),
    ]
    
    ten_lop = models.CharField(max_length=100, error_messages=LOI_CHUOI)
    giao_vien = models.ForeignKey(GiaoVien, on_delete=models.SET_NULL, null=True, error_messages=LOI_KHOA_NGOAI)
    khoa_hoc = models.ForeignKey(KhoaHoc, on_delete=models.SET_NULL, null=True, blank=True)
    si_so_toi_da = models.IntegerField(default=30, error_messages=LOI_SO)
    min_si_so = models.IntegerField(default=20, error_messages=LOI_SO) 
    trang_thai = models.CharField(max_length=10, choices=TRANG_THAI, default='CHO', 
                                  error_messages={'invalid_choice': 'Trạng thái lớp không hợp lệ.'})
    hoc_viens = models.ManyToManyField(HocVien, blank=True, related_name='cac_lop_tham_gia')

    def si_so_hien_tai(self):
        return self.hoc_viens.count()

    def phan_tram_lap_day(self):
        if self.si_so_toi_da == 0: return 0
        percent = (self.si_so_hien_tai() / self.si_so_toi_da) * 100
        return round(percent)

    def cap_nhat_trang_thai(self):
        hien_tai = self.si_so_hien_tai()
        if hien_tai >= self.min_si_so:
            self.trang_thai = 'MO'
        else:
            self.trang_thai = 'CHO'
        self.save()

    def __str__(self):
        return f"{self.ten_lop} ({self.si_so_hien_tai()}/{self.si_so_toi_da})"

class LichHoc(models.Model):
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE, related_name='lich_hoc', error_messages=LOI_KHOA_NGOAI) 
    phong = models.ForeignKey(PhongHoc, on_delete=models.SET_NULL, null=True, error_messages=LOI_KHOA_NGOAI)
    thu = models.IntegerField(choices=[(i, f"Thứ {i}") for i in range(2, 9)], 
                              error_messages={'invalid_choice': 'Vui lòng chọn ngày trong tuần hợp lệ.', 'invalid': 'Thứ phải là một số.'})
    ca = models.IntegerField(error_messages=LOI_SO) 

    def __str__(self):
        return f"{self.lop_hoc.ten_lop} - Thứ {self.thu} - Ca {self.ca}"
    
class HoaDon(models.Model):
    TRANG_THAI_THANH_TOAN = [
        ('CHUA', 'Chưa thanh toán'),
        ('CHO_DUYET', 'Chờ duyệt ảnh'), 
        ('ROI', 'Đã thanh toán'),
    ]
    hoc_vien = models.ForeignKey(HocVien, on_delete=models.CASCADE, related_name='hoa_don', error_messages=LOI_KHOA_NGOAI)
    noi_dung = models.CharField(max_length=200, default="Học phí tháng ...", error_messages=LOI_CHUOI)
    so_tien = models.DecimalField(max_digits=12, decimal_places=0, default=0, error_messages=LOI_SO)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    trang_thai = models.CharField(max_length=15, choices=TRANG_THAI_THANH_TOAN, default='CHUA')
    
    def __str__(self):
        return f"{self.hoc_vien.ten} - {self.so_tien} VNĐ"

# --- THÊM BẢNG NÀY ĐỂ LƯU NHIỀU ẢNH CHO 1 HÓA ĐƠN ---
class AnhMinhChung(models.Model):
    hoa_don = models.ForeignKey(HoaDon, on_delete=models.CASCADE, related_name='danh_sach_anh')
    hinh_anh = models.ImageField(upload_to='minh_chung/')
    ngay_tai_len = models.DateTimeField(auto_now_add=True)

class DanhGia(models.Model):
    DIEM_CHOICES = [(i, f'{i} sao') for i in range(1, 6)]
    ho_ten = models.CharField(max_length=100, error_messages=LOI_CHUOI)
    email = models.EmailField(max_length=200, null=True, blank=True)
    co_so = models.ForeignKey(CoSo, on_delete=models.CASCADE, null=True, blank=True, related_name='danh_gia')
    diem = models.IntegerField(choices=DIEM_CHOICES, default=5)
    noi_dung = models.TextField(error_messages=LOI_CHUOI)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    duyet = models.BooleanField(default=True)
    class Meta:
        ordering = ['-ngay_tao']
    def __str__(self):
        return f"{self.ho_ten} - {self.diem} sao"
    
  # --- BẢNG TIN TỨC CHÍNH ---
class TinTuc(models.Model):
    LOAI_TIN = [
        ('CONG_NGHE', 'Công Nghệ'),
        ('TUYEN_SINH', 'Tuyển Sinh'),
        ('HOC_TAP', 'Góc Học Tập'),
    ]
    tieu_de = models.CharField(max_length=200, error_messages=LOI_CHUOI)
    tom_tat = models.TextField(error_messages=LOI_CHUOI)
    noi_dung = models.TextField(error_messages=LOI_CHUOI)
    ngay_dang = models.DateTimeField(auto_now_add=True)
    loai_tin = models.CharField(max_length=50, choices=LOAI_TIN, default='CONG_NGHE')

    def __str__(self):
        return self.tieu_de

# --- BẢNG ALBUM ẢNH (CHO PHÉP 1 BÀI CÓ NHIỀU ẢNH) ---
class AnhTinTuc(models.Model):
    # Liên kết với bài viết qua thuộc tính related_name='cac_anh'
    tin_tuc = models.ForeignKey(TinTuc, on_delete=models.CASCADE, related_name='cac_anh')
    hinh_anh = models.ImageField(upload_to='tin_tuc/', max_length=500)

# Bảng bài giảng chính (Lưu tiêu đề, mô tả)
class BaiGiang(models.Model):
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE, related_name='cac_bai_giang')
    tieu_de = models.CharField(max_length=200, error_messages=LOI_CHUOI)
    mo_ta = models.TextField(blank=True, null=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ngay_tao']

    def __str__(self):
        return f"{self.tieu_de} - {self.lop_hoc.ten_lop}"

# Bảng phụ lưu danh sách nhiều Video (Hỗ trợ cả Link và File Upload)
class VideoBaiGiang(models.Model):
    bai_giang = models.ForeignKey(BaiGiang, on_delete=models.CASCADE, related_name='danh_sach_video')
    video_url = models.CharField(max_length=500, help_text="Link YouTube", null=True, blank=True)
    video_file = models.FileField(upload_to='bai_giang/videos/', null=True, blank=True) # THÊM DÒNG NÀY
# Bảng phụ lưu danh sách nhiều File đính kèm
class FileBaiGiang(models.Model):
    bai_giang = models.ForeignKey(BaiGiang, on_delete=models.CASCADE, related_name='danh_sach_file')
    file_dinh_kem = models.FileField(upload_to='bai_tap/')

# =========================================================
# CÁC TÍNH NĂNG HỌC VỤ NÂNG CAO
# =========================================================

class BaiTap(models.Model):
    """Đề bài tập / BTVN do giáo viên giao"""
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE, related_name='bai_tap')
    tieu_de = models.CharField(max_length=200, error_messages=LOI_CHUOI)
    mo_ta = models.TextField(blank=True, null=True)
    han_nop = models.DateTimeField(null=True, blank=True, verbose_name="Hạn nộp")
    file_de = models.FileField(upload_to='bai_tap/de/', null=True, blank=True, verbose_name="File đề bài")
    hinh_thuc = models.CharField(max_length=10, choices=[('ONL', 'Online'), ('OFF', 'Offline')], default='ONL')
    ngay_tao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ngay_tao']

    def __str__(self):
        return f"{self.tieu_de} - {self.lop_hoc.ten_lop}"


class NopBaiTap(models.Model):
    """Bài học viên đã nộp"""
    bai_tap = models.ForeignKey(BaiTap, on_delete=models.CASCADE, related_name='bai_nop')
    hoc_vien = models.ForeignKey(HocVien, on_delete=models.CASCADE, related_name='bai_da_nop')
    file_nop = models.FileField(upload_to='bai_tap/nop/', null=True, blank=True)
    ghi_chu = models.TextField(blank=True, null=True, verbose_name="Ghi chú / Giải trình")
    ngay_nop = models.DateTimeField(auto_now_add=True)
    diem = models.FloatField(null=True, blank=True, verbose_name="Điểm số")
    nhan_xet = models.TextField(blank=True, null=True, verbose_name="Nhận xét của GV")

    class Meta:
        unique_together = ('bai_tap', 'hoc_vien')

    def __str__(self):
        return f"{self.hoc_vien.ten} - {self.bai_tap.tieu_de}"


class ThoiGianRanh(models.Model):
    """Ca học giáo viên có thể dạy (thời gian rảnh)"""
    giao_vien = models.ForeignKey(GiaoVien, on_delete=models.CASCADE, related_name='thoi_gian_ranh')
    thu = models.IntegerField(choices=[(i, f"Thứ {i}") for i in range(2, 9)])
    ca = models.IntegerField()

    class Meta:
        unique_together = ('giao_vien', 'thu', 'ca')
        ordering = ['thu', 'ca']

    def __str__(self):
        return f"{self.giao_vien.ten} - Thứ {self.thu} Ca {self.ca}"


class XinNghi(models.Model):
    """Đơn xin nghỉ của học viên hoặc giáo viên"""
    LOAI_CHOICES = [('HV', 'Học viên'), ('GV', 'Giáo viên')]
    TRANG_THAI = [('CHO', 'Chờ duyệt'), ('DUYET', 'Đã duyệt'), ('TU_CHOI', 'Từ chối')]

    loai = models.CharField(max_length=5, choices=LOAI_CHOICES)
    hoc_vien = models.ForeignKey(HocVien, on_delete=models.CASCADE, null=True, blank=True, related_name='don_xin_nghi')
    giao_vien = models.ForeignKey(GiaoVien, on_delete=models.CASCADE, null=True, blank=True, related_name='don_xin_nghi')
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE, related_name='don_xin_nghi')
    ngay_nghi = models.DateField(verbose_name="Ngày xin nghỉ")
    ly_do = models.TextField(verbose_name="Lý do")
    trang_thai = models.CharField(max_length=10, choices=TRANG_THAI, default='CHO')
    ngay_tao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ngay_tao']

    def ten_nguoi_xin(self):
        return self.hoc_vien.ten if self.hoc_vien else (self.giao_vien.ten if self.giao_vien else "?")

    def __str__(self):
        return f"{self.ten_nguoi_xin()} xin nghỉ {self.ngay_nghi} - {self.lop_hoc.ten_lop}"


class LichBu(models.Model):
    """Lịch học bù sau khi có đơn xin nghỉ được duyệt"""
    TRANG_THAI = [
        ('CHO', 'Chờ xác nhận'),
        ('DUYET', 'Đã lên lịch'),
        ('HOAN_THANH', 'Đã dạy bù xong'),
        ('HUY', 'Đã hủy'),
    ]

    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE, related_name='lich_bu')
    xin_nghi = models.ForeignKey(XinNghi, on_delete=models.SET_NULL, null=True, blank=True, related_name='lich_bu')
    ngay_bu = models.DateField(verbose_name="Ngày dạy bù")
    ca_bu = models.IntegerField(verbose_name="Ca học bù")
    ly_do = models.TextField(blank=True, verbose_name="Ghi chú")
    trang_thai = models.CharField(max_length=15, choices=TRANG_THAI, default='CHO')
    ngay_tao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ngay_bu']

    def __str__(self):
        return f"Bù lớp {self.lop_hoc.ten_lop} - {self.ngay_bu} Ca {self.ca_bu}"


class DangKyLichBu(models.Model):
    """Học viên xác nhận tham gia / vắng buổi bù"""
    hoc_vien = models.ForeignKey(HocVien, on_delete=models.CASCADE, related_name='dang_ky_bu')
    lich_bu = models.ForeignKey(LichBu, on_delete=models.CASCADE, related_name='danh_sach_dang_ky')
    co_mat = models.BooleanField(default=True, verbose_name="Có thể tham dự")
    ghi_chu = models.TextField(blank=True, null=True)
    ngay_dang_ky = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hoc_vien', 'lich_bu')

    def __str__(self):
        trang_thai = "Tham dự" if self.co_mat else "Vắng"
        return f"{self.hoc_vien.ten} - {self.lich_bu} - {trang_thai}"