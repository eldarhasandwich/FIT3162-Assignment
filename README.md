# Eldar and Andrews thing that does stuff

To install pyQT on linux, run:
```
sudo apt-get install python-qt4
```
To install pyQT on macosx, run:
```
brew install cartr/qt4/pyqt
```

For windows installation, visit [this link](https://www.riverbankcomputing.com/software/pyqt/download)

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

## Tests

Get pytest 
```
pip install -U pytest
```

Run tests
```
pytest
```

# Project Structure

Application is started with `python application.py`. `application.py` contains the functions to generate the UI for the PyQt application as well as bindings to other classes in the project so that the user can access them.

Graphs are imported into the database using the function `EnronOutputToAdjList()` in `enron_output_to_adjlist.py` to generate and Adjacency List, then `PushAdjListToDB()` in `databaseController.py` inserts the adjList into the database.

`classes/AdjacencyList.py` contains the class definition for adjacency lists used to store them in working memory a they are needed.

`graph_statistics.py` contains the class which handles performing statistical analyses on graphs 

`test_adjacency_list.py` contains tests to ensure functionality of `AdjacencyList.py`

`test_database_controller.py` contains tests to ensure functionality of `databaseController.py`

`test_graph_statistics.py` contains tests to ensure functionality of `graphStatistics.py`