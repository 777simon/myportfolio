#!/bin/bash

echo " BUILD START "

# Install dependencies
python3.12 -m pip install -r requirements.txt

# Manually create the output directory to ensure Vercel sees it
mkdir -p staticfiles_build/static

# Collect static files into the specific directory defined in settings.py
python3.12 manage.py collectstatic --noinput --clear

echo " BUILD END "