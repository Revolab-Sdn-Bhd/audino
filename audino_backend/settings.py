"""
Django settings for audino_backend project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-blf-=2iis_y6%3*1_q(08v$o-#*6ote5!0wcxn!0*!c+elt_wv"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost:3000', "localhost", "*"]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://audino-frontend-qsuua57v7q-ue.a.run.app",
    "https://app.audino.in",
    "https://*"
]
CORS_ALLOWED_HEADERS = ['*']
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "users",
    "core",
    "organizations",
    'allauth',
    'iam',
    'engine',
    # "debug_toolbar",
    'django_filters',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    'django.middleware.gzip.GZipMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "iam.views.ContextMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = {"127.0.0.1"}

ROOT_URLCONF = "audino_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",
                           'allauth.account.auth_backends.AuthenticationBackend',)


ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"

AUTH_USER_MODEL = "users.User"
WSGI_APPLICATION = "audino_backend.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": ["users.manager.TokenAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        'iam.permissions.PolicyEnforcer',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'engine.filters.SimpleFilter',
        'engine.filters.SearchFilter',
        'engine.filters.OrderingFilter',
        'engine.filters.JsonLogicFilter',
        'iam.filters.OrganizationFilterBackend',
    ),
    'SEARCH_PARAM': 'search',
    'DEFAULT_PAGINATION_CLASS':
        'engine.pagination.CustomPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'iam.schema.CustomAutoSchema',
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': os.environ.get("POSTGRES_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
os.makedirs(STATIC_ROOT, exist_ok=True)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media Handling Configuration
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ORG SETTINGS
ORG_INVITATION_CONFIRM = 'No'  # automatically accept invitations
ORG_INVITATION_EXPIRY_DAYS = 7


# IAM SETTINGS
IAM_TYPE = 'BASIC'
IAM_BASE_EXCEPTION = None  # a class which will be used by IAM to report errors


def GET_IAM_DEFAULT_ROLES(user) -> list:
    return ['user']


IAM_CONTEXT_BUILDERS = ['iam.utils.build_iam_context',]


IAM_ADMIN_ROLE = 'admin'
# Index in the list below corresponds to the priority (0 has highest priority)
IAM_ROLES = [IAM_ADMIN_ROLE, 'business', 'user', 'worker']


IAM_OPA_HOST = 'http://localhost:8181'
IAM_OPA_DATA_URL = f'{IAM_OPA_HOST}/v1/data'
# LOGIN_URL = 'rest_login'
# LOGIN_REDIRECT_URL = '/'

OBJECTS_NOT_RELATED_WITH_ORG = ['user', 'function', 'request', 'server',]

IAM_OPA_BUNDLE_PATH = os.path.join(STATIC_ROOT, 'opa', 'bundle.tar.gz')
os.makedirs(Path(IAM_OPA_BUNDLE_PATH).parent, exist_ok=True)
