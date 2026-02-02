from django.contrib import admin
from django.urls import path
from django.conf import settings # Thêm dòng này
from django.conf.urls.static import static # Thêm dòng này
from quan_ly_hoc_vu import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.trang_chu, name='trang_chu'),
    path('hoc-vien-moi/', views.dieu_phoi_page, name='dieu_phoi_page'),
    path('danh-sach-chi-nhanh/', views.chi_nhanh_page, name='chi_nhanh_page'),
    path('xoa-chi-nhanh/<int:cs_id>/', views.xoa_chi_nhanh, name='xoa_chi_nhanh'),
    path('chay-gis/<int:hv_id>/', views.kich_hoat_gis, name='kich_hoat_gis'),
    path('thong-ke/', views.thong_ke_page, name='thong_ke_page'),
    path('dang-ky/', views.dang_ky_page, name='dang_ky_page'),
    path('quan-ly/', views.quan_ly_page, name='quan_ly_page'),
    path('xoa-hoc-vien/<int:hv_id>/', views.xoa_hoc_vien, name='xoa_hoc_vien'),
    path('xep-lich/', views.xep_lich_page, name='xep_lich_page'),
    path('tao-du-lieu-mau/', views.tao_du_lieu_mau, name='tao_du_lieu_mau'),
    path('quan-ly-lop/', views.quan_ly_lop_page, name='quan_ly_lop_page'),
    path('xoa-lop/<int:lop_id>/', views.xoa_lop_hoc, name='xoa_lop_hoc'),
    path('hoc-phi/', views.quan_ly_hoc_phi, name='quan_ly_hoc_phi'),
    path('xoa-hoa-don/<int:hd_id>/', views.xoa_hoa_don, name='xoa_hoa_don'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
] 


# CẤU HÌNH QUAN TRỌNG: Cho phép hiển thị hình ảnh từ thư mục media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)