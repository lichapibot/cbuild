# cbuild

Chess build tool for filtering PGN files and building polyglot books.

# Installation

## Prerequisites

### Git

https://git-scm.com/downloads

### Miniconda

https://conda.io/miniconda.html

## Cloning the project

Open the Miniconda console and clone the project:

`git clone https://github.com/lichapibot/cbuild`

Cd into the cloned folder:

`cd cbuild`

## Creating virtual env with pipenv

Install pipenv:

`pip install pipenv`

Create virtual env:

`pipenv --python /absolute/path/to/Miniconda/python-executable`

On Windows this can be something like:

`pipenv --python "C:\Users\Joe Doe\Miniconda\python.exe"`

## Installing project dependencies

Install project dependencies from Pipfile.lock:

`pipenv install`

# Usage

First run the program with the -h switch to display help:

`pipenv run python cbuild.py -h`

## Create build environment

Create a build environment for a variant ( example will use variant antichess ):

`pipenv run python cbuild.py -e antichess --variant antichess`

The `-e` swith's `antcihess` is arbitrary name for the build environment, could be `foo` as well. The `--variant` swith's `antcihess` should be a proper lichess variant key.

This will create a directory structure:

```
envs
  antichess
    zip
    source
    filtered
    book
    config.yml
    filter_logic.py    
```

File `filter_logic` is a python code snippet that has access to the `BasePgnVisitor` instance as `self` and set the boolean variable `ok` to indicate whether to include the given gamve `True` or ignore it `False` ( the code can be empty to include all games ), file `config.yml` is reserved for build configuration, currently should be left empty.

Example filter logic to filter out games less than 2200 rated:

```python
minelo = self.get_min_elo()

if minelo < 2200:
	self.ok = False
```

## Downloading files

The `zip` folder should contain `bz2` format zipped PGN files. To download the next monthly lichess database run the program with the `--nextlichessdb` switch ( you can repeat this several time to download databases for several months ).

## Building files

Running the program with `-u` switch will unzip these files to the `source` folder, which should contain the source PGN files. Running the program with `-f` switch will filter these files to the `filtered` folder. Running the program with `-b` switch will build a book from each filtered PGN and store them in the `book` folder. To merge all the books in the `book` folder into one book, use the `-m` switch. The merged book will be `merged.bin` in the env root folder.

The whole build process can be done in one step using the `-a` switch.

# Putting it all together

Activate the build environment, download the next monthly lichess database and build a merged book:

`pipenv run python cbuild.py -e antichess --nextlichessdb -a`

You can repeat this step to include more monthly databases in the build.