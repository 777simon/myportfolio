#!/bin/bash
echo "BUILD START"

pip install -r requirements.txt

#!/bin/bash
python manage.py collectstatic --noinput

echo "BUILD END"
