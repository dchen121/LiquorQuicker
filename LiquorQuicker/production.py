from .settings import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Parse database configuration from $DATABASE_URL
DATABASES['default'] =  dj_database_url.config()
