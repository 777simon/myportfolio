#!/bin/bash
echo "BUILD START"

# Install dependencies
python3.12 -m pip install -r requirements.txt

# Clean old builds and create the EXACT path expected by STATIC_ROOT
mkdir -p staticfiles_build

# Collect static files
python3.12 manage.py collectstatic --noinput

echo "BUILD END"