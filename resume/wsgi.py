import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume.settings')

# Get Django application
application = get_wsgi_application()

# Absolute path to staticfiles_build inside resume/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # resume/

# Attach WhiteNoise
application = WhiteNoise(
    application,
    root=os.path.join(BASE_DIR, "staticfiles_build"),  # resume/staticfiles_build
    prefix='/static/'  # ensures static URL is correct
)

# Vercel expects this exact variable
app = application
