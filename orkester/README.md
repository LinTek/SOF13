Developer-installation
======================

## System-dependencies

    sudo apt-get install libmysqlclient-dev python-dev python-setuptools

Och om man vill även

    sudo apt-get install libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev


## Virtualenv och dependencies

Installera pip, virtualenv and virtualenvwrapper (eventuellt krävs root)

    sudo easy_install pip
    sudo pip install virtualenv
    sudo pip install virtualenvwrapper


Lägg till i .bashrc/.zshrc -filen. Starta sedan om skalet.

    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc


Skapa ett virtualenv:

    mkvirtualenv sof


Installera dependencies:

    pip install -r requirements.txt


Gör ett par roliga saker med pythonpath för att slippa manage.py

    echo "export DJANGO_SETTINGS_MODULE=settings" >> ~/.virtualenvs/sof/bin/postactivate
    add2virtualenv /path/to/orkester/folder/in/sof/project


Hett tips är att aliasa djangoadmin.py till **dj** och workon till **wo**.

    echo "alias dj='djangoadmin.py'" >> ~/.bashrc
    echo "alias wo='workon'" >> ~/.bashrc


Starta om skalet igen. Aktivera ditt virtualenv med:

    workon sof


Kör development-servern med:

    django-admin.py runserver


## Databas

Skapa en mysql-databas, kör t.ex. mysql och sedan

    create database sof13;

Login till denna kan konfigureras i settings.py.
