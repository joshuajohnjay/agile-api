# agile-project-api
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)
### Installation

This project requires sqlite, fast-api, python v3+ to run.

Install the dependencies using poetry.
```sh
$ cd agile-api
$ poetry install
```
Initialize database records 
```sh
$ python seed.py
```

Run test cases 
```sh
$ pytest -v
```

Run the application 
```sh
$ cd agile-api
$ uvicorn main:app --reload
```
