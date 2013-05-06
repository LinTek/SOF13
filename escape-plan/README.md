Escape-plan / Plan B
====================

Ett funktionärs- och biljettsystem för utvecklare med deadlines. Se gärna även
../anmalan/README.md som innehåller mer info. Denna applikations virtualenv
på SOF-servern heter dock *funkis* istället för *sof*.


# Deploya
Överlag kan du använda informationen i ../anmalan/README.md, med skillnaden
att man får göra  ``wo funkis`` istället för ``wo sof`` om man behöver köra
migrations eller starta ett python-skal. Config-filen för Apache hittar man
i /etc/apache2/sites-available/funkis.sof13.se,

    sudo su - django-sof13
    cd sof13/escape-plan/
    git pull
    touch sof/conf/wsgi.py

Om man skapat några migrations respektive lagt till någon statisk fil (bilder,
css, javascript) krävs även att man kör:

    wo funkis
    dj migrate
    dj collectstatic

# Installation av utvecklingsmiljö

## Vad behöver jag?
En dator med Linux/MacOS X är att föredra, Windows borde funka fint också
men är otestat. Instruktionerna nedan förutsätter Linux. Som IDE brukar
man i allmänhet bara köra en bra texteditor, såsom Sublime Text 2, samt en
bra terminal. iTerm2 kan rekommenderas för mac.

## Det här verkar ju jättekrångligt
Vi har valt att använda virtualenv och virtualenvwrapper eftersom att det gör
det möjligt att köra flera python-projekt på samma dator oberoende av varandra.
Det går att skippa stora delar om man vill. Men annars är det bara att följa
instruktionerna och köra på.

## System-dependencies

    sudo apt-get install libmysqlclient-dev python-dev python-setuptools

Om man vill ha stöd för jpeg och png när man installerar PIL krävs även

    sudo apt-get install libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev


## Virtualenv och Python-dependencies

Installera pip, virtualenv and virtualenvwrapper (eventuellt krävs root)

    sudo easy_install pip
    sudo pip install virtualenv
    sudo pip install virtualenvwrapper


Lägg till i .bashrc/.zshrc -filen. Starta sedan om skalet.

    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc


Skapa ett virtualenv:

    mkvirtualenv sof


Installera dependencies:

    sudo pip install -r requirements.txt


Se till att du står i mappen esacpe-plan i SOF13-repositoryt.
Gör ett par roliga saker med pythonpath för att slippa manage.py

    echo "export DJANGO_SETTINGS_MODULE=settings" >> ~/.virtualenvs/sof/bin/postactivate
    add2virtualenv .


Man vill även aliasa django-admin.py till *dj* och workon till *wo*.

    echo "alias dj='django-admin.py'" >> ~/.bashrc
    echo "alias wo='workon'" >> ~/.bashrc

Starta om skalet igen.

Kopiera filen ./sof/conf/settings_template.py till ./sof/conf/settings_local.py.
Modifiera sedan den nya filen så att den stämmer för dina databas-inställningar
och liknande.

    cd /sof/conf
    cp settings_template.py settings_local.py


Skapa en mysql-databas, kör t.ex. mysql och sedan

    create database sof13;

(man kan naturligtvis köra postgres istället om man vill, bara att ändra den
lokala settings-filen samt installera *psycopg2* med pip)


## Sista stegen

Aktivera ditt virtualenv

    wo sof


Bygg databasstruktur

    dj syncdb
    dj migrate


Kör development-servern

    dj runserver
