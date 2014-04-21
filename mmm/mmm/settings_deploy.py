DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mmmdb',
        'USER': 'mmmadmin',
        'PASSWORD': 'mmmadmin',
        'HOST': 'mmmdb.cdrbqxg7zaha.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}

MEDIA_ROOT = '/srv/MMM/mmm/mmm/media/'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mmm.umich@gmail.com'
EMAIL_HOST_PASSWORD = 'uRt6tyXhlM8YMMDxjSUINQ'