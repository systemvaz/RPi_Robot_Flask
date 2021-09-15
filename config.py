import os

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Number of threads to use (2 per core)
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)
CSRF_ENABLED = True

# Secret key for signing data
CSFR_SESSION_KEY = '0af096491bc0bdaf6d951492'

# Secret key for signing cookies
SECRET_KEY = 'ead09facbbd7c50bbd2e0b21'