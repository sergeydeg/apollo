## Prerequisites
- Python 3.4.2+
- MySQL server

## Installation
Dependencies can be easily installed with pip:
```
pip3 install -r requirements.txt
```

## Setup
Before we can get things running, we need to setup the database. You'll need to 
set the `DB_USER` env variable, as well as the `DB_PASS` env variable if you
are connecting to MySQL with a password.

Once this is done, the database can be setup with:
```
python3 bin/setup_db.py
```

Before the app can be run, you'll need to set the `BOT_TOKEN` env variable with the
token of your Discord bot.

The app can then be run with:
```
python3 app.py
```

## Database Console
There is an interactive python interpreter setup to allow for easy communication
with an in memory database. This project uses SQLAlchemy for the database.

The interactive database interpreter can be launched with:
```
python3 -i bin/console.py
```

Here is a quick example of how it might be used:
```
>>> user = User(id=7)
>>> session.add(user)
>>> session.commit()
>>> session.query(User).first().id
7
```
