# Tour Booking (Django)

## Install
pip install django

## Run
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## URLs
/                      - tours list
/tours/<id>/           - tour detail (book + reviews)
/bookings/mine/        - my bookings
/bookings/sales-by-country/ - sales stats
/admin/                - admin panel
/login/ /signup/       - auth

## Seed demo data
python manage.py seed
# or reset:
python manage.py seed --reset
