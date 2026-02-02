import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    
    'unfold',
    'unfold.contrib.filters',
    #'simpleui',
    
    'core',
    'vault',

    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    
    "rest_framework",           # A API
    "rest_framework.authtoken", # Necessário para auth
    "dj_rest_auth",             # Endpoints de Login/Logout
    "allauth",                  # O cérebro do registro
    "allauth.account",          # Contas locais
    "allauth.socialaccount",    # Login Social
    "dj_rest_auth.registration",# Endpoint de Registro
    
]

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

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

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
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "nexus-auth",
    "JWT_AUTH_REFRESH_COOKIE": "nexus-refresh-token",
    "REGISTER_SERIALIZER": "dj_rest_auth.registration.serializers.RegisterSerializer",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# --- ALLAUTH CONFIGURATION ---
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

ACCOUNT_LOGIN_METHODS = {'email'}

ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

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



# --- SIMPLEUI CONFIGURATION ---

# # 1. Privacidade e Limpeza (Remove anúncios e tracking)
# SIMPLEUI_HOME_INFO = False 
# SIMPLEUI_ANALYSIS = False 

# # 2. Tema Padrão
# # Opções: 'default', 'admin.lte.css', 'element.css', 'layui.css'
# # Para um visual mais "Apple/Clean", o padrão ou element costumam ser melhores.
# SIMPLEUI_DEFAULT_THEME = 'element.css' 

# # 3. Menu e Ícones
# SIMPLEUI_ICON = {
#     'Acessos': 'fas fa-shield-alt',
#     'Usuários': 'fas fa-user',
#     'Grupos': 'fas fa-users-cog',
# }

# # 4. Logo e Títulos
# SIMPLEUI_LOGO = 'https://www.djangoproject.com/m/img/logos/django-logo-negative.png' # Ou um caminho '/static/img/logo.png'
# SIMPLEUI_HOME_TITLE = 'Dashboard Nexus'
# SIMPLEUI_HOME_PAGE = '/admin/core/user/'

#--- UNFOLD ADMIN CONFIGURATION ---
UNFOLD = {
    "SITE_TITLE": "NEXUS Admin",
    "SITE_HEADER": "Nexus Enterprise",
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
        ],
    },
}

AUTH_USER_MODEL = "core.User"

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
