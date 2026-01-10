#!/bin/bash
echo "BUILD START"

# Install dependencies
python3.12 -m pip install -r requirements.txt

# Clean old builds and create the EXACT path expected by STATIC_ROOT
rm -rf staticfiles_build
mkdir -p staticfiles_build/static

# Collect static files
python3.12 manage.py collectstatic --noinput

echo "BUILD END"