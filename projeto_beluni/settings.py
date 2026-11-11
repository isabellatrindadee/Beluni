import os
from pathlib import Path

# Caminho principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


# SEGURANÇA
# Em desenvolvimento, utiliza uma chave local padrão.
# Em produção, configure DJANGO_SECRET_KEY no ambiente.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-chave-local-apenas-para-desenvolvimento'
)

# DEBUG pode ser ativado ou desativado por variável de ambiente.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'

# Hosts permitidos
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        'DJANGO_ALLOWED_HOSTS',
        '127.0.0.1,localhost'
    ).split(',')
    if host.strip()
]


# APLICAÇÕES
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'disciplinas',
    'estudante',
    'atividade',
    'notificacao',
    'meta',
]


# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# URLS
ROOT_URLCONF = 'projeto_beluni.urls'


# TEMPLATES
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
            ],
        },
    },
]


# WSGI
WSGI_APPLICATION = 'projeto_beluni.wsgi.application'


# BANCO DE DADOS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# VALIDAÇÃO DE SENHAS
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


# INTERNACIONALIZAÇÃO
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Bahia'

USE_I18N = True

USE_TZ = True


# ARQUIVOS ESTÁTICOS
STATIC_URL = 'static/'


# AUTENTICAÇÃO
LOGIN_URL = 'login_estudante'

LOGIN_REDIRECT_URL = 'inicio'

LOGOUT_REDIRECT_URL = 'login_estudante'


# CHAVE PRIMÁRIA PADRÃO
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
