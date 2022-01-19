<div align="center">

[![JukeBot](juke-logo.png)](#readme)
</div>

# JukeBot
Discord music bot using [Nextcord](https://github.com/nextcord/nextcord/) and [Poetry](https://python-poetry.org/)
___

## Installation
```
git clone https://github.com/Dysta/JukeBot 
cd JukeBot
poetry install
```

## Configuration
Rename `.env.example` into `.env` and fill the values. \
If you want to use an Atlas MongoDB to enable custom prefix system, install extra package `poetry install -E mongouri`.

## Usage
Run `poetry run python -m jukebot` or `poetry run task start` if you installed the dev dependencies.

## Other
The bot use a MongoDB for its custom prefix system, you can have one quickly by register you on [Atlas MongoDB](https://www.mongodb.com/atlas). \
If you want to disable custom prefix system to do a quick setup, go to `jukebot/__main__.py` and replace
```py
bot = JukeBot(
    command_prefix=prefix.get_prefix,
    help_command=HelpHandler(),
    activity=Game(f"{os.environ['BOT_PREFIX']}help"),
    intents=intents.get(),
    owner_ids=get_ids(),
)
```
with
```py
bot = JukeBot(
    command_prefix=commands.when_mentioned_or(os.environ['BOT_PREFIX']),
    help_command=HelpHandler(),
    activity=Game(f"{os.environ['BOT_PREFIX']}help"),
    intents=intents.get(),
    owner_ids=get_ids(),
)
```


The bot need `ffmpeg` to work.
### Install on Windows
Use the package manager [Chocolatey](https://community.chocolatey.org/) and run in a admin shell `choco install ffmpeg`.

### Install on Linux
Use apt, run `sudo apt install ffmpeg`.