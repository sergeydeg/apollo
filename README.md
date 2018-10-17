## Prerequisites
- Python 3.5.2+
- Pipenv
- MySQL server

## Installation
The environment can be easily setup with pipenv:
```
pipenv install
pipenv shell
```

## Setup
Before we can get things running, we need to setup the database. You'll need to 
set the `DB_USER` env variable, as well as the `DB_PASS` env variable if you
are connecting to MySQL with a password.

Once this is done, the database can be setup with:
```
python bin/setup_db.py
```

Before the app can be run, you'll need to create an `.env` file. Please look at the `.env.example` file and set the `BOT_TOKEN` env variable with the token of your Discord bot.


The app can then be run with:
```
python app.py
```
