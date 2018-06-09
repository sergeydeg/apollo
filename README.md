## Prerequisites
- Python 3.4.2+
- Pip

## Installation
Dependencies can be installed with:
```
pip3 install -r requirements.txt
```

## Dev Tools
There is an interactive python interpreter setup to allow for easy communication
with an in memory database. This project uses SQLAlchemy for the database.

The interactive database interpreter can be launched with:
```
cd bin
python3 -i console.py
```

Note that for the time being, the console must be started from within the `bin` directory.

Here is a quick example of how it might be used:
```
>>> user = User(id=7)
>>> session.add(user)
>>> session.commit()
>>> session.query(User).first().id
7
```
