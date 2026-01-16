import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume.settings")

# Create Django WSGI application
application = get_wsgi_application()

# Point WhiteNoise to the CORRECT staticfiles_build location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

application = WhiteNoise(
    application,
    root=os.path.join(BASE_DIR, "staticfiles_build")
)

# 🔴 REQUIRED BY VERCEL
app = application
