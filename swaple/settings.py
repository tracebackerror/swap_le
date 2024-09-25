import os
import dj_database_url
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY','(!&6*!a9x(g#2tba@125a^$t_s+*1882+jd3$@k3=er)q!2id$')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =  True

DEBUG_PROPAGATE_EXCEPTIONS  = True
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap-responsive.html"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

ALLOWED_HOSTS = [
  'swaple-shivam9172873031.codeanyapp.com',
  'swaple.in',
  'www.swaple.in',
  'swaple-prod.herokuapp.com',
  'swaple.herokuapp.com',
  '127.0.0.1',
  'localhost',
  '192.168.1.207',
  '192.168.1.209',
  
]

#Custom Authentication ModelBackend
#AUTH_USER_MODEL = 'users.SwapLeUserModel' 


# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'guardian',
    'django_tables2',
    'django_filters',
    'bootstrap3',
    'crispy_forms',
    'ckeditor',
    'home',
    'licenses',
    'institutions',
    'staff',
    'students',
    'assesments',
    'library',
    'fees',
    'section',
    'widget_tweaks',
    'easy_pdf',
    'django_extensions',
    'localflavor',
    'django_countries',
    'bootstrap4',
    'django_user_agents',
    'import_export',
    'meta',
    'taggit',
    # 'tz_detect',  # Uncomment if needed
]


GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'allauth.account.middleware.AccountMiddleware',  # Add this line
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'django_user_agents.middleware.UserAgentMiddleware',
    #'tz_detect.middleware.TimezoneMiddleware',
]

#TZ_DETECT_COUNTRIES = ( 'US', 'IN', 'JP', 'BR', 'RU', 'DE', 'FR', 'GB', 'CN',)
ROOT_URLCONF = 'swaple.urls'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                    os.path.join(BASE_DIR, '/templates/'),
                    os.path.realpath(BASE_DIR + '/templates')
                 ],
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

WSGI_APPLICATION = 'swaple.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'swapple',
        'USER': 'postgres',
        'PASSWORD': 'Agilent@123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
     #"allauth.account.auth_backends.AuthenticationBackend",
    'guardian.backends.ObjectPermissionBackend',
   
)

SITE_ID = 1


ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



CRISPY_TEMPLATE_PACK = 'bootstrap4'

'''
password reset settings
for testing and printing mail on console uncomment below
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
'''


#for sending link to the mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'saffronspice8@gmail.com'
EMAIL_HOST_PASSWORD = 'Shiv@1234s'
DEFAULT_FROM_EMAIL = "Swaple Support <noreply@swaple.com>"



