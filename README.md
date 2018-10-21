
## Summary

Apollo is an all in one solution for managing everything event related right within Discord.

![Apollo in action](https://gyazo.com/a91e05553863aa646a1c7f4126bb4152.gif)

## Contributing

Apollo is an open source project; pull requests are encouraged and welcome.

If you are considering contributing to the project, feel free to contact Asal on the [Apollo Discord server]().
There is also a [project board](https://trello.com/b/c0RplRku/apollo) on Trello which outlines current and future units of work.

## Development Environment

The following outlines the steps for setting up a local installation of Apollo for development purposes.

### Prerequisites
- Python 3.5.2+
- Pipenv
- MySQL server

### Installation
The Python environment can be easily setup with pipenv:
```
pipenv install
pipenv shell
```

### Environment Variables

Apollo requires several environment variables in order to function. The quickest way to get
up and running will be create an `.env` file in the root directory and populate it with the
contants of [`.env.example`](https://github.com/jgayfer/apollo/blob/master/.env.example)

You will need to set the `BOT_TOKEN` environment variable to the token of your Discord bot.

The database is setup to connect to `localhost` with the the `root` user (no password).
If your database setup is different from this, you will need to uncomment and modify the commented out
database environment variables found in [`.env.example`](https://github.com/jgayfer/apollo/blob/master/.env.example)

### Database

Assuming our database credentials are correctly configured in `.env`, the database be be initialized with:
```
python bin/setup_db.py
```

### Running the bot

The app can then be run with:
```
python app.py
```
