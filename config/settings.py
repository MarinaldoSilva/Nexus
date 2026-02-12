import os
from datetime import timedelta
from pathlib import Path

from django.urls import reverse_lazy
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    #'unfold',
    #'unfold.contrib.filters',
    #'simpleui',
    "cloudinary_storage",
    "cloudinary",
    "core",
    "vault",
    "audit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",  # Necessário para auth
    "dj_rest_auth",  # Endpoints de Login/Logout
    "allauth",  # O cérebro do registro
    "allauth.account",  # Contas locais
    "allauth.socialaccount",  # Login Social
    "dj_rest_auth.registration",  # Endpoint de Registro
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "audit.middleware.AuditMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DATETIME_FORMAT": "%d/%m/%Y %H:%M:%S",
    "DATE_FORMAT": "%d/%m/%Y",
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "nexus-auth",
    "JWT_AUTH_REFRESH_COOKIE": "nexus-refresh-token",
    "REGISTER_SERIALIZER": "dj_rest_auth.registration.serializers.RegisterSerializer",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --- ALLAUTH CONFIGURATION ---
ACCOUNT_SIGNUP_FIELDS = ["email"]
ACCOUNT_LOGIN_METHODS = {"email"}

# --- CONFIGURAÇÕES DO ALLAUTH ---
# Diz ao Django que usamos o sistema de sites (obrigatório para allauth)

SITE_ID = 1
# Não exige verificação de email
ACCOUNT_EMAIL_VERIFICATION = "none"
# Permite logar com email? Sim.
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
# Evita que o allauth tente adivinhar usernames
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# --- UNFOLD ADMIN CONFIGURATION ---
UNFOLD = {
    "SITE_TITLE": "NEXUS Admin",
    "SITE_HEADER": "Nexus Voult",
    "SITE_URL": "/",
    # 1. Configuração de Cores (Paleta Azul Enterprise)
    "COLORS": {
        "primary": {
            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",
            "600": "37 99 235",  # Cor Principal
            "700": "29 78 216",
            "800": "30 64 175",
            "900": "30 58 138",
            "950": "23 37 84",
        },
    },
    # 2. Configuração do Menu Lateral (Sidebar)
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Acessos",
                "separator": True,
                "items": [
                    {
                        "title": "Usuários",
                        "icon": "people",
                        "link": reverse_lazy("admin:core_user_changelist"),
                    },
                    {
                        "title": "Grupos",
                        "icon": "lock",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": "Arquivos",
                "separator": True,
                "items": [
                    {
                        "title": "Arquivos",
                        "icon": "files",
                        "link": reverse_lazy("admin:vault_file_changelist"),
                    },
                ],
            },
        ],
    },
}

AUTH_USER_MODEL = "core.User"

MEDIA_URL = "/files/"  # Cloudinary usa /files/ ou URL completa
MEDIA_ROOT = os.path.join(BASE_DIR, "files")  # Fallback

# --- CLOUDINARY CONFIGURATION ---
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    "RESOURCE_TYPE": "auto",  # para acitar arquivos DOCX/PDF/MP4 até 100MB
    # Timeout maior para arquivos grandes não travarem no meio
    "CURL_OPTIONS": {
        "timeout": 60,
    },
}

# configuração Cloudiinary
# STORAGES = {
#     "default": {
#         #cloudinary_storage.storage.MediaCloudinaryStorage /para usar midias
#         #cloudinary_storage.storage.RawMediaCloudinaryStorage
#         "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     },
# }

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


DATA_UPLOAD_MAX_MEMORY_SIZE = 10737418240
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB

LANGUAGE_CODE = "pt-br"
DATETIME_FORMAT = "d/m/Y H:i:s"
DATE_FORMAT = "d/m/Y"

DATETIME_INPUT_FORMATS = [
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%d/%m/%Y",
]

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True

STATIC_URL = "static/"
