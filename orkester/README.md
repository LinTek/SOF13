Orkesteranmälan
===============

Systemet är byggt i Python/Django (www.djangoproject.com), dels eftersom att det
är awesome och dels eftersom att utvecklingen av ett system i Java EE blev onödigt
bökigt för ett en så pass simpelt system.

## Mappstruktur

* ./media - här samlas alla uppladdade filer
* ./static - vid deployment samlas alla statiska filer hit
* ./sof - kod, templates och liknande

Projektet har två settings-filer. En lokal settings-fil för t.ex. debugging
och databas-inställningar, som inte finns i repot. Det finns dock en bra
mall för hur denna kan se ut; settings-template.py.

Den globala settings-filen finns i sof/conf/settings.py, där man kan ändra
sådant som man vill även ska ändras vid deployment och liknande.


# Praktiska småsaker

## Databas-migrations

Om man ändrar attributen i någon databasmodell måste eventuellt databasens
struktur uppdateras. Detta görs med hjälp av *south* och så kallade migrations.

För att skapa en ny migration och köra alla migrations

    dj schemamigration orkester --auto
    dj migrate


## Typiskt vardags-workflow

    git pull
    wo sof
    dj migrate
    dj runserver


## Deployment på SOF-servern

Servern kör projektet med Apache + mod_wsgi. Undertecknad är mer van vid
nginx + gunicorn, så om någon tycker att något är konstigt gjort så kan det
mycket väl vara så. Nåväl. Det funkar iaf.

Det finns en väldigt basic apache config-fil i /etc/apache2/sites-available/orkester.sof13.se
Som framgår av denna ligger själva projektet i en home-mapp till den egna
användaren django-sof13.

Vill man göra saker är det lättast att bara su:a till användaren.

    sudo su - django-sof13

Nu kan man gå in i repositoryt och köra en git pull, samt köra samma kommandon
för databas-migrations och liknande som lokalt. Dock krävs här även att man
kör collectstatic om man ändrat några statiska filer.

    dj collectstaic

Efter att man ändrat något måste mod_wsgi laddas om för att uppdateringen ska
slå igenom (detsamma gäller i princip alla ramverk och tekniker, vissa gör
dock detta automatiskt). Ett alternativ är att göra en reload av apache2.

    sudo /etc/init.d/apache2 reload

Det ska även gå att istället bara uppdatera wsgi.py-filen som ligger i
conf-mappen.

    touch sof/conf/wsgi.py


## Typiskt deployment-workflow
Om någon orkar i framtiden kan man istället använda *fabric* och skiva en
fabfile som sköter deploy. Vi har dock prioriterat bort detta.

    ssh sof@lysator.liu.se
    sudo su - django-sof13
    cd sof13/orkester
    git pull
    touch sof/conf/wsgi.py

Om man skapat några migrations respektive lagt till någon statisk fil (bilder,
css men inte t.ex. templates är statiska filer) krävs även att man kör:

    wo sof
    dj migrate
    dj collectstatic


# Installation av utvecklingsmiljö

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


Se till att du står i mappen orkester i SOF13-repositoryt.
Gör ett par roliga saker med pythonpath för att slippa manage.py

    echo "export DJANGO_SETTINGS_MODULE=settings" >> ~/.virtualenvs/sof/bin/postactivate
    add2virtualenv .


Man vill även aliasa django-admin.py till *dj* och workon till *wo*.

    echo "alias dj='django-admin.py'" >> ~/.bashrc
    echo "alias wo='workon'" >> ~/.bashrc

Starta om skalet igen.

Kopiera filen settings_template.py till settings.py. Modifiera sedan den nya
filen så att den stämmer för dina databas-inställningar och liknande.

    cp settings_template.py settings.py


Skapa en mysql-databas, kör t.ex. mysql och sedan

    create database sof13;

(man kan naturligtvis köra postgres istället om man vill, bara ändra den
lokala settings-filen och installera *psycopg2* med pip)


## Sista stegen

Aktivera ditt virtualenv

    wo sof


Bygg databasstruktur

    dj syncdb
    dj migrate


Kör development-servern

    dj runserver
