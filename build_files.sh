#!/bin/bash

echo " BUILD START "

# Install the necessary libraries
python3.12 -m pip install -r requirements.txt

# Create the folder manually to be safe
mkdir -p staticfiles_build/static

# Run collectstatic to fill that folder
python3.12 manage.py collectstatic --noinput --clear

echo " BUILD END "