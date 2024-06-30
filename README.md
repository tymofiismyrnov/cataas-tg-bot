# Cat as a Service Telegram Bot

This bot returns a random cat picture or gif, or a picture with text that you type in.

## Description

The bot uses the [Cataas API](https://cataas.com/) to fetch cat images and gifs. It's a fun and simple bot for cat lovers!

### Features

- Get a random cat picture
- Get a random cat gif
- Get a cat picture with custom text
- Get a cat gif with custom text

## Usage

You can either build the Docker image yourself or use the pre-built image.

### Building the Image

To build the image using the Dockerfile in the repo:

```sh
docker build -t cataas-tg-bot .
```

### Using the Pre-built Image

Alternatively, you can use the image that is automatically built on every commit to the main branch

```sh
docker pull tymofiismyrnov/cataas-tg-bot:latest
```

### Running the Image

To run the image, you need to provide a single environment variable TG_BOT_TOKEN

```sh
docker run -e TG_BOT_TOKEN=<your-telegram-bot-token> tymofiismyrnov/cataas-tg-bot:latest
```

## Credits

- The bot uses the [Cataas API](https://cataas.com/) authored by [Kevin Balicot](https://twitter.com/kevinbalicot).
