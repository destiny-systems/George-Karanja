#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py seed_portfolio
python manage.py shell < seed_all_galleries.py
python manage.py shell < seed_unit_rooms.py
python manage.py shell < force_fix_all_images.py
python manage.py shell < force_floor_plans.py
python manage.py shell < seed_location_advantages.py
python manage.py shell < seed_construction.py
python manage.py generate_booklets
