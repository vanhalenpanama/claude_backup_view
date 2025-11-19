from pathlib import Path
import os

print("!!!! 제가 만든 settings.py 파일이 로딩되었습니다 !!!!")

# 1. 기본 경로 설정
# settings.py가 config 폴더 안에 있다고 가정할 때의 경로입니다.
BASE_DIR = Path(__file__).resolve().parent.parent


# 2. 보안 및 디버그 설정 (환경변수 없이 작동하도록 하드코딩)
# 주의: 실제 배포 시에는 이 키를 변경하고 환경변수로 관리해야 안전합니다.
SECRET_KEY = 'django-insecure-change-me-for-production-use-only'

# 개발 편의를 위해 True로 설정 (False로 하면 500 에러 및 정적 파일 문제 발생 가능)
DEBUG = True

ALLOWED_HOSTS = ['*']


# 3. 애플리케이션 정의
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 사용자 앱
    # 'blog',
    'claude',
    # 'account',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # WhiteNoise: 정적 파일 서빙 (DEBUG=True일 때는 Django가 알아서 처리하지만 유지해도 무방)
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# 4. 데이터베이스 설정 (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# 5. 비밀번호 검증
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 6. 국제화 및 시간 설정
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# 7. 정적 파일 (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# [추가해야 할 부분] 프로젝트 최상위 static 폴더 경로 지정
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 주의: DEBUG=True 상태에서는 아래 WhiteNoise 압축 설정이 없어야 에러가 안 납니다.
# STATICFILES_STORAGE 설정은 삭제했습니다. (기본값 사용)


# 8. 미디어 파일 (사용자 업로드 파일)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# 9. 기타 설정
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN_REDIRECT_URL = 'home'
# LOGOUT_REDIRECT_URL = 'home'