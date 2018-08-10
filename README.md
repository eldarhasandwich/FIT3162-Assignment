# Eldar and Andrews thing that does stuff

To install pyQT on linux, run:
```
sudo apt-get install python-qt4
```
To install pyQT on macosx, run:
```
brew install cartr/qt4/pyqt
```

For windows installation, visit [THIS LINK](https://www.riverbankcomputing.com/software/pyqt/download)

## Database Junk

http://initd.org/psycopg/docs/usage.html

Start the DB on linux
```
sudo service postgresql start
```
On macosx
```
pg_ctl -D /usr/local/var/postgres start
```

Populate the DB
```
psql -f snagraphs.sql
```


test