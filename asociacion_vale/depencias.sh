sudo apt install python3-pip
if [[ ! $(pip3 list|grep "Django") ]]; then
    python3 -m pip install Django
fi

if [[ ! $(pip3 list|grep "djongo") ]]; then
    python3 -m pip install djongo
fi

if [[ ! $(pip3 list|grep "django-cors-headers") ]]; then
    python3 -m pip install django-cors-headers
fi

if [[ ! $(pip3 list|grep "django-ckeditor") ]]; then
    python3 -m pip install django-ckeditor
fi

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python3 manage.py shell

sudo python3 manage.py makemigrations
sudo python3 manage.py migrate

sudo python3 manage.py runserver
#pip install django-cors-headers
#pip install django-ckeditor