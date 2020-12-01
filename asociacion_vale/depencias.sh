sudo apt install python3-pip
if [[ ! $(pip3 list|grep "Django") ]]; then
    pip install Django
fi

if [[ ! $(pip3 list|grep "djongo") ]]; then
    pip install djongo
fi

if [[ ! $(pip3 list|grep "crum") ]]; then
    pip install django-crum
fi

if [[ ! $(pip3 list|grep "django-cors-headers") ]]; then
    pip install django-cors-headers
fi

if [[ ! $(pip3 list|grep "django-ckeditor") ]]; then
    pip install django-ckeditor
fi

pip install django-referrer-policy
python -m pip install Pillow
pip install django-crum
pip install pyfcm
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python3 manage.py shell

sudo python3 manage.py makemigrations
sudo python3 manage.py migrate

sudo python3 manage.py runserver
#pip install django-cors-headers
#pip install django-ckeditor

#error de virtual env
#https://stackoverflow.com/questions/46210934/importerror-couldnt-import-django
#sudo pip install virtualenv
#cd ~/newproject

#virtualenv newenv
#source newenv/bin/activate
#pip install django
#django-admin --version
#deactivate