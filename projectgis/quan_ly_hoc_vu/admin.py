from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe # <--- THÊM IMPORT QUAN TRỌNG NÀY
from django.urls import reverse
from .models import CoSo, HocVien

# --- CẤU HÌNH TIÊU ĐỀ ADMIN ---
admin.site.site_header = "HỆ THỐNG QUẢN TRỊ TOÁN GIS"
admin.site.site_title = "Admin Toán GIS"
admin.site.index_title = "Bảng điều khiển quản lý học vụ"

@admin.register(CoSo)
class CoSoAdmin(admin.ModelAdmin):
    list_display = ('ten', 'dia_chi', 'lat', 'lon', 'si_so_live', 'nut_xoa_nhanh')
    list_editable = ('lat', 'lon') 
    search_fields = ('ten', 'dia_chi')
    
    # Hiển thị số lượng học viên đang theo học
    def si_so_live(self, obj):
        count = obj.hocvien_set.count()
        return format_html(
            '<b style="color: green;">{} học viên</b>', count
        )
    si_so_live.short_description = "Sĩ số hiện tại"

    # Nút Xóa Nhanh cho Cơ Sở
    def nut_xoa_nhanh(self, obj):
        return format_html(
            '<a class="button" style="background-color: #dc3545; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; text-decoration: none;" href="/admin/quan_ly_hoc_vu/coso/{}/delete/">Xóa</a>',
            obj.id
        )
    nut_xoa_nhanh.short_description = "Tác vụ"

@admin.register(HocVien)
class HocVienAdmin(admin.ModelAdmin):
    # Hiển thị đầy đủ thông tin + Nút Xóa
    list_display = ('ten', 'khoi_lop', 'hien_thi_toa_do', 'trang_thai_xep_lop', 'nut_xoa_nhanh')
    
    # Cho phép sửa nhanh Khối lớp ngay tại danh sách
    list_editable = ('khoi_lop',)
    
    # Bộ lọc và Tìm kiếm
    list_filter = ('khoi_lop', 'co_so_gan_nhat')
    search_fields = ('ten',)
    list_per_page = 20 

    # Hiển thị tọa độ đẹp hơn
    def hien_thi_toa_do(self, obj):
        return f"{obj.lat:.4f}, {obj.lon:.4f}"
    hien_thi_toa_do.short_description = "GPS (Lat, Lon)"

    # Trạng thái xếp lớp (ĐÃ SỬA LỖI TẠI ĐÂY)
    def trang_thai_xep_lop(self, obj):
        if obj.co_so_gan_nhat:
            # Có biến thì dùng format_html
            return format_html(
                '<span style="color: blue;">✅ {}</span>', 
                obj.co_so_gan_nhat.ten
            )
        # Không có biến (chuỗi tĩnh) thì dùng mark_safe để tránh lỗi TypeError
        return mark_safe('<span style="color: red;">⚠️ Chưa xếp</span>')
    
    trang_thai_xep_lop.short_description = "Cơ sở phân công"

    # --- NÚT XÓA NHANH ---
    def nut_xoa_nhanh(self, obj):
        return format_html(
            '<a class="button" style="background-color: #dc3545; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; text-decoration: none;" href="/admin/quan_ly_hoc_vu/hocvien/{}/delete/">Xóa Ngay</a>',
            obj.id
        )
    nut_xoa_nhanh.short_description = "Hành Động"