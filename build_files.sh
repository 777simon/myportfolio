#!/bin/bash
echo "BUILD START"

python3.12 -m pip install -r requirements.txt

# DO NOT create subfolders
rm -rf staticfiles_build
mkdir -p staticfiles_build

python3.12 manage.py collectstatic --noinput

echo "BUILD END"
