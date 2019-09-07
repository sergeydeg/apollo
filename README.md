
## Summary

Apollo is an all in one solution for managing everything event related right within Discord.

![Apollo in action](https://gyazo.com/a91e05553863aa646a1c7f4126bb4152.gif)

## Contributing

Apollo is an open source project; pull requests are encouraged and welcome.

If you are considering contributing to the project, feel free to contact Asal on the [Apollo Discord server](https://discord.gg/ZVevvh2).
There is also a [project board](https://trello.com/b/c0RplRku/apollo) on Trello which outlines current and future units of work.

## Development Environment

First, you'll want to get [Docker Compose](https://docs.docker.com/compose/install/) up and running. You are of course welcome to run the
bot without Docker, though I would encourage you to give it a try.

Once that's done, we can build our image from the root directory of Apollo with:
```
docker-compose build
```

Before we can run the application, we'll need to ensure that our environment variables are set up correctly. The easiest way to do this is
to make a copy of [`.env.example`](https://github.com/jgayfer/apollo/blob/master/.env.example) as `.env`. in the root directory of Apollo.

For a default install using Docker, the only thing you'll need to provide here is your bot token. You can get one of these by heading over
to https://discordapp.com/developers/applications and creating a new application.

Now that all of our credentials are set, we can start the application. Note that the `-d` flag will cause the database to run in the background.
```
docker-compose up -d db

# Create database tables (only needs to be run once)
docker-compose run app pipenv run python bin/setup_db.py

# Run migrations if necessary
docker-compose run app pipenv run alembic upgrade head

docker-compose up app
```

Note that with each code change, we'll need to rebuild with `docker-compose build` (don't worry, it's super quick).

Assuming all has gone well, we're ready to invite the bot to a Discord server. All we need to do it visit this link, with our bot's client ID
substitued in for `CLIENT_ID_HERE`: https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID_HERE&scope=bot&permissions=355408

