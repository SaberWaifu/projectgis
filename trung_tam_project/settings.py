import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4#aee&otybo#us@uu*+!@+^n_558@wq+*znnf83tm!fv1!-twu'

# Tắt chế độ DEBUG để Django hiện trang 404 thực tế
DEBUG = True

# Cho phép mọi tên miền truy cập (hoặc điền ['127.0.0.1', 'localhost'])
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',              # Trang Admin (cấu hình Social Apps)
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',              # BẮT BUỘC cho allauth
    'django.contrib.humanize',

    # Bộ thư viện Allauth (đăng nhập Google)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'quan_ly_hoc_vu', # App quản lý học vụ của bạn
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'trung_tam_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ===================================================================
# [ĐÃ SỬA] CẤU HÌNH DATABASE CHÍNH THỨC: POSTGRESQL
# ===================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'toan_gis_db',          # Tên database bạn vừa tạo trong pgAdmin
        'USER': 'postgres',             # User mặc định của PostgreSQL
        'PASSWORD': '123456',                # MẬT KHẨU PostgreSQL của bạn
        'HOST': 'localhost',            # Chạy trên máy cá nhân
        'PORT': '5432',                 # Cổng mặc định của PostgreSQL
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

# ĐÃ XÓA toàn bộ cấu hình JAZZMIN_SETTINGS và JAZZMIN_UI_CONFIG ở đây.

# ===================================================================
# CẤU HÌNH DJANGO-ALLAUTH (Đăng nhập Google / Facebook)
# ===================================================================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
LOGIN_REDIRECT_URL = 'trang_nguoi_dung'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

# Cấu hình Google OAuth (Client ID & Secret Key)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '591813788561-c4fumk161pmto28nimn4m6qda0kvesn7.apps.googleusercontent.com',
            'secret': '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',
            'key': '',
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

# ===================================================================
# CẤU HÌNH GỬI EMAIL TỰ ĐỘNG BẰNG GMAIL
# ===================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'uoa2704@gmail.com'  # Email của Thầy

# Dán mã 16 chữ cái của Thầy vào đây (XÓA KHOẢNG TRẮNG)
EMAIL_HOST_PASSWORD = 'vvicemxpaqfjynko'