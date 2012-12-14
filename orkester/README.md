Developer-installation
======================

Installera virtualenv and virtualenvwrapper.

    pip install virtualenv
    pip install virtualenvwrapper


Lägg till i .bashrc/.zshrc -filen. Starta sedan om skalet.

    source /usr/local/bin/virtualenvwrapper.sh


Skapa ett virtualenv:

    mkvirtualenv sof


Installera dependencies:

    pip install -r requirements.txt


Gör ett par roliga saker med pythonpath för att slippa manage.py

    echo "export DJANGO_SETTINGS_MODULE=sof.settings" >> ~/.virtualenvs/sof/bin/postactivate
    add2virtualenv ~/path/to/orkester-folder/in/sof/project


Starta om skalet igen. Aktivera ditt virtualenv med:

    workon sof


Kör development-servern med:

    django-admin.py runserver


Hett tips är att aliasa djangoadmin.py till **dj** och workon till **wo**.
