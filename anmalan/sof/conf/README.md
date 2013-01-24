Orkesteranmälan
===============

## Filstruktur

* settings_global.py - global settings-fil för saker som ska ändras även på servern vid deploy.
* settings_local.py - lokal settings-fil som inte finns med i repot. En mall för denna finns i settings_template.py
* settings_template.py - mall för ovanstående fil

* settings_cortege.py - settings-fil för kårtegeanmälan
* settings_orchestra.py - settings-fil för orkesteranmälan

* wsgi_cortege.py, wsgi_orchestra.py - används vid deployment för respektive applikation.
