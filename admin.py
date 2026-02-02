from django.contrib import admin
from .models import CoSo, HocVien

# Cấu hình tiêu đề trang Admin chuẩn tiếng Việt
admin.site.site_header = "HỆ THỐNG QUẢN TRỊ TOÁN GIS"
admin.site.site_title = "Admin Toán GIS"
admin.site.index_title = "Bảng điều khiển quản lý học vụ"

@admin.register(CoSo)
class CoSoAdmin(admin.ModelAdmin):
    # list_display giúp hiện tên cơ sở như một đường dẫn để bấm vào Sửa
    list_display = ('ten', 'lat', 'lon', 'so_luong_hoc_vien')
    
    # Cho phép sửa nhanh tọa độ Lat/Lon ngay tại bảng danh sách
    list_editable = ('lat', 'lon') 
    
    search_fields = ('ten',)
    
    # Hàm hiển thị số lượng học viên
    def so_luong_hoc_vien(self, obj):
        count = obj.hocvien_set.count()
        return f"{count} học viên"
    so_luong_hoc_vien.short_description = "Sĩ số hiện tại"

@admin.register(HocVien)
class HocVienAdmin(admin.ModelAdmin):
    # Hiển thị danh sách học viên khối 6, 8, 9
    list_display = ('ten', 'khoi_lop', 'hien_thi_toa_do', 'co_so_gan_nhat')
    
    # Cho phép sửa nhanh khối lớp ngay tại bảng mà không cần bấm vào chi tiết
    list_editable = ('khoi_lop',)
    
    # Bộ lọc nhanh bên phải giúp lọc theo lớp hoặc cơ sở
    list_filter = ('khoi_lop', 'co_so_gan_nhat')
    search_fields = ('ten',)
    
    def hien_thi_toa_do(self, obj):
        return f"{obj.lat}, {obj.lon}"
    hien_thi_toa_do.short_description = "Tọa độ (Lat, Lon)"

    # Thêm hành động xóa hàng loạt đã được Django tích hợp sẵn
    actions = ['delete_selected']