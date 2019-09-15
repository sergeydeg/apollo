
## Summary

Apollo is an all in one solution for managing everything event related right within Discord.

![Apollo in action](https://gyazo.com/a91e05553863aa646a1c7f4126bb4152.gif)

## Contributing

Apollo is an open source project; pull requests are encouraged and welcome.

If you are considering contributing to the project, feel free to contact Asal on the [Apollo Discord server](https://discord.gg/ZVevvh2).
There is also a [Trello board](https://trello.com/b/c0RplRku/apollo) which outlines current and future work.

## Development environment

The only real requirement is to get [Docker Compose](https://docs.docker.com/compose/install/) up and running.

Once that's done, we can build our image from the root directory of Apollo with:
```
docker-compose build
```

### Environment variables

Before we can run the application, we'll need to ensure that our environment variables are set up. Make a copy of [`.env.example`](https://github.com/jgayfer/apollo/blob/master/.env.example) as `.env`. in the root directory of Apollo.

If using Docker, the only thing you'll need to provide here is your `BOT_TOKEN`. You can get one of these by heading over
to the [Discord developer portal](https://discordapp.com/developers/applications) and creating a new application.

### Run the application

Now that our credentials are set, we can start the application.
```
# Start the database as a background process
docker-compose up -d db

# Create database tables (only needs to be run once)
docker-compose run app pipenv run python bin/setup_db.py

# Run migrations (if necessary)
docker-compose run app pipenv run alembic upgrade head

docker-compose up app
```

### Code changes

With each code change, we'll need to rebuild our image.

1. Stop the server
2. Rebuild the image: `docker-compose build`
3. Restart the server: `docker-compose run app`

### Invite the bot to a server

We can invite the bot to a server by visiting the link below (subsitute `CLIENT_ID` with your bot's client ID).
```
https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=355408
```

