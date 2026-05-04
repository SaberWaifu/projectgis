from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from quan_ly_hoc_vu import views

# [THÊM MỚI] Import thư viện phục vụ file tĩnh cho môi trường DEBUG = False
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),                  
    path('accounts/', include('allauth.urls')),       
    path('', views.trang_chu, name='trang_chu'),
    path('co-so/<int:cs_id>/', views.co_so_detail, name='co_so_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dang-ky-tai-khoan/', views.dang_ky_tai_khoan, name='dang_ky_tai_khoan'),
    path('dang-ky/', views.dang_ky_page, name='dang_ky_page'),
    path('khoa-hoc/', views.trang_khoa_hoc, name='trang_khoa_hoc'),
    path('trang-nguoi-dung/', views.trang_nguoi_dung, name='trang_nguoi_dung'),
    path('giao-vien/', views.trang_giao_vien, name='trang_giao_vien'), 
    path('user-dang-ky-lop/<int:lop_id>/', views.user_dang_ky_lop, name='user_dang_ky_lop'),
    path('thong-ke/', views.thong_ke_page, name='thong_ke_page'),
    path('hoc-vien-moi/', views.dieu_phoi_page, name='dieu_phoi_page'),
    path('chay-gis/<int:hv_id>/', views.kich_hoat_gis, name='kich_hoat_gis'),
    path('quan-ly/', views.quan_ly_page, name='quan_ly_page'),
    path('xoa-hoc-vien/<int:hv_id>/', views.xoa_hoc_vien, name='xoa_hoc_vien'),
    path('quan-ly-giao-vien/', views.quan_ly_giao_vien, name='quan_ly_giao_vien'),
    path('xoa-giao-vien/<int:gv_id>/', views.xoa_giao_vien, name='xoa_giao_vien'),
    path('danh-sach-chi-nhanh/', views.chi_nhanh_page, name='chi_nhanh_page'),
    path('xoa-anh-co-so/<int:anh_id>/', views.xoa_anh_co_so, name='xoa_anh_co_so'),
    path('sua-chi-nhanh/<int:id>/', views.sua_chi_nhanh, name='sua_chi_nhanh'),
    path('xoa-chi-nhanh/<int:cs_id>/', views.xoa_chi_nhanh, name='xoa_chi_nhanh'),
    path('quan-ly-lop/', views.quan_ly_lop_page, name='quan_ly_lop_page'),
    path('xoa-lop/<int:lop_id>/', views.xoa_lop_hoc, name='xoa_lop_hoc'),
    path('dang-ky-lop-admin/<int:lop_id>/<int:hv_id>/', views.dang_ky_lop, name='dang_ky_lop'), 
    path('xep-lich/', views.xep_lich_page, name='xep_lich_page'),
    path('tao-du-lieu-mau/', views.tao_du_lieu_mau, name='tao_du_lieu_mau'),
    path('hoc-phi/', views.quan_ly_hoc_phi, name='quan_ly_hoc_phi'),
    path('cap-nhat-hoc-phi/<int:hd_id>/', views.cap_nhat_trang_thai, name='cap_nhat_trang_thai'),
    path('xoa-hoa-don/<int:hd_id>/', views.xoa_hoa_don, name='xoa_hoa_don'),
    path('hoc-phi/xuat-excel/', views.xuat_excel_hoc_phi, name='xuat_excel_hoc_phi'),
    path('quan-ly-khoa-hoc/', views.quan_ly_khoa_hoc, name='quan_ly_khoa_hoc'),
    path('xoa-khoa-hoc/<int:kh_id>/', views.xoa_khoa_hoc, name='xoa_khoa_hoc'),
    path('thanh-toan/', views.thanh_toan_page, name='thanh_toan'),
    path('xu-ly-thanh-toan/', views.xu_ly_thanh_toan, name='xu_ly_thanh_toan'),
    path('quen-mat-khau/', views.quen_mat_khau, name='quen_mat_khau'),
    path('quan-ly-tai-khoan/', views.quan_ly_tai_khoan, name='quan_ly_tai_khoan'),
    path('danh-gia/', views.danh_gia_page, name='danh_gia_page'),
    path('xoa-danh-gia/<int:dg_id>/', views.xoa_danh_gia, name='xoa_danh_gia'),
    path('tin-tuc/', views.trang_tin_tuc, name='trang_tin_tuc'),
    path('quan-ly-tin-tuc/', views.quan_ly_tin_tuc, name='quan_ly_tin_tuc'),
    path('sua-tin-tuc/<int:tin_id>/', views.sua_tin_tuc, name='sua_tin_tuc'),
    path('xoa-tin-tuc/<int:tin_id>/', views.xoa_tin_tuc, name='xoa_tin_tuc'),
    path('lop-hoc/<int:lop_id>/bai-giang/', views.bai_giang_hoc_vien, name='bai_giang_hoc_vien'),
    path('giao-vien/lop-hoc/<int:lop_id>/bai-giang/', views.quan_ly_bai_giang_gv, name='quan_ly_bai_giang_gv'),
    path('doi-mat-khau/', views.doi_mat_khau, name='doi_mat_khau'),
    path('xoa-tai-khoan/', views.xoa_tai_khoan, name='xoa_tai_khoan'),
    path('lop/<int:lop_id>/bai-tap/', views.bai_tap_hoc_vien, name='bai_tap_hoc_vien'),
    path('lop/<int:lop_id>/quan-ly-bai-tap/', views.quan_ly_bai_tap_gv, name='quan_ly_bai_tap_gv'),
    path('bai-tap/<int:bt_id>/nop/', views.nop_bai_tap, name='nop_bai_tap'),
    path('bai-tap/<int:bt_id>/cham/', views.cham_bai_tap, name='cham_bai_tap'),
    path('thoi-gian-ranh/', views.thoi_gian_ranh_gv, name='thoi_gian_ranh_gv'),
    path('thoi-gian-ranh-admin/', views.xem_thoi_gian_ranh_admin, name='thoi_gian_ranh_admin'),
    path('lop/<int:lop_id>/xin-nghi/', views.xin_nghi, name='xin_nghi'),
    path('quan-ly-xin-nghi/', views.quan_ly_xin_nghi, name='quan_ly_xin_nghi'),
    path('tao-lich-bu/', views.tao_lich_bu, name='tao_lich_bu'),
    path('lich-bu/', views.xem_lich_bu, name='xem_lich_bu'),
    path('lich-bu/<int:lb_id>/dang-ky/', views.dang_ky_lich_bu, name='dang_ky_lich_bu'),
    path('gioi-thieu/', views.trang_gioi_thieu, name='trang_gioi_thieu'),
    path('quan-ly-gioi-thieu/', views.quan_ly_gioi_thieu, name='quan_ly_gioi_thieu'),
    path('sua-gioi-thieu/<int:gt_id>/', views.sua_gioi_thieu, name='sua_gioi_thieu'),
    path('xoa-gioi-thieu/<int:gt_id>/', views.xoa_gioi_thieu, name='xoa_gioi_thieu'),
    path('xoa-anh-gioi-thieu/<int:anh_id>/', views.xoa_anh_gioi_thieu, name='xoa_anh_gioi_thieu'),
]

# =================================================================
# CẤU HÌNH QUAN TRỌNG: Hiển thị hình ảnh cho cả True và False
# =================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # ÉP Django chạy file ảnh ở chế độ Production (DEBUG = False)
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]