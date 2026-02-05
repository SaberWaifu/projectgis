from django.urls import path # Dòng này định nghĩa hàm 'path'
from . import views

urlpatterns = [
    path('', views.trang_chu, name='trang_chu'),
    path('hoc-vien-moi/', views.dieu_phoi_page, name='dieu_phoi_page'),
    path('quan-ly/', views.quan_ly_page, name='quan_ly_page'),
    path('xoa-hoc-vien/<int:hv_id>/', views.xoa_hoc_vien, name='xoa_hoc_vien'),
    path('xoa-tool/<int:hv_id>/', views.xoa_tool_dieu_phoi, name='xoa_tool_dieu_phoi'),
    path('chay-gis/<int:hv_id>/', views.kich_hoat_gis, name='kich_hoat_gis'),
    path('xep-lich/', views.xep_lich_page, name='xep_lich_page'),
    path('tao-du-lieu-mau/', views.tao_du_lieu_mau, name='tao_du_lieu_mau'),
]