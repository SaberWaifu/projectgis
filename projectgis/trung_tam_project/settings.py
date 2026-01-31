import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4#aee&otybo#us@uu*+!@+^n_558@wq+*znnf83tm!fv1!-twu'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'jazzmin',  # Giao diện Admin hiện đại
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quan_ly_hoc_vu', # App quản lý học vụ của bạn
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trung_tam_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Thêm processor để xử lý ảnh (media)
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'trung_tam_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 1. Việt hóa ngôn ngữ và Múi giờ
LANGUAGE_CODE = 'vi' # Chuyển sang tiếng Việt

TIME_ZONE = 'Asia/Ho_Chi_Minh' # Múi giờ Việt Nam

USE_I18N = True

USE_TZ = True

# 2. Cấu hình Static và Media (Xử lý hình ảnh Cơ sở/Học viên)
STATIC_URL = 'static/'

# Đường dẫn lưu trữ ảnh thực tế tải lên
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 3. Nâng cấp cấu hình JAZZMIN (Giao diện Admin Dashboard)
JAZZMIN_SETTINGS = {
    "site_title": "Toán GIS Admin",
    "site_header": "Toán GIS",
    "site_brand": "TOÁN GIS CẤP 2",
    "welcome_sign": "Chào mừng Thầy đến với hệ thống quản lý học vụ!",
    "copyright": "Trung Tâm Toán GIS 2026", #
    "search_model": ["quan_ly_hoc_vu.HocVien"],
    "topmenu_links": [
        {"name": "Trang Chủ Web", "url": "/", "new_window": True},
        {"name": "Điều Phối GIS", "url": "/hoc-vien-moi/", "new_window": True},
        {"name": "Báo Cáo Thống Kê", "url": "/thong-ke/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "quan_ly_hoc_vu.CoSo": "fas bi-building",
        "quan_ly_hoc_vu.HocVien": "fas bi-people",
    },
}

# Tùy chỉnh màu sắc Admin nhìn chuyên nghiệp hơn
JAZZMIN_UI_CONFIG = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_fixed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly", # Giao diện phẳng hiện đại
}