<div align="center">

[![JukeBot](juke-logo.png)](#readme)
</div>

# JukeBot
Discord music bot using [Nextcord](https://github.com/nextcord/nextcord/) and [Poetry](https://python-poetry.org/)
___

## 🧩 Installation
```
git clone https://github.com/Dysta/JukeBot 
cd JukeBot
poetry install
```

## ⚙️ Configuration
Rename `.env.example` to `.env` and fill in the values. \
If you want to use an Atlas MongoDB to enable the custom prefix system, install the extra package `poetry install -E mongouri`.

## 🚀 Launch
Run `poetry run python -m jukebot` or `poetry run task start` if you installed the dev dependencies.

## ⁉️ Other
The bot use a MongoDB database for its custom prefix system, you can have one quickly by registering on [Atlas MongoDB](https://www.mongodb.com/atlas). \
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


The bot needs `ffmpeg` to work.
### Install on Windows
Use the package manager [Chocolatey](https://community.chocolatey.org/) and run in an admin shell `choco install ffmpeg`.

### Install on Linux
Use apt, run `sudo apt install ffmpeg`.

## 🗨 Features & Commands

### Song
- [X] **`join`**
- [X] **`play`**
- [X] **`playtop`**
- [X] **`playskip`**
- [X] **`search`**
- [X] **`nowplaying`**
- [X] **`grab`**
- [ ] **`seek`**
- [X] **`loop`**
- [X] **`pause`**
- [X] **`resume`**
- [ ] **`lyrics`**
- [X] **`disconnect`**

### Queue
- [X] **`queue`**
- [ ] **`loopqueue`**
- [ ] **`move`**
- [ ] **`skipto`**
- [X] **`shuffle`**
- [X] **`remove`**
- [X] **`clear`**
- [ ] **`removedupes`**

### Utility
- [X] **`prefix`**
- [X] **`reset`**

### Effect
- [ ] **`speed`**
- [ ] **`bass`**
- [ ] **`nightcore`**
- [ ] **`slowed`**

### Others
- [X] **`avatar`**
- [X] **`info`**
- [X] **`invite`**
- [X] **`donate`**
- [X] **`watch`**
- [X] **`help`**


## 🤝 Contributing

Contributions are what make the open source community such an amazing place to be learn, 
inspire, and create. Any contributions you make are **greatly appreciated**.

1. [Fork the repository](https://github.com/Dysta/JukeBot/fork)
2. Clone your fork `git clone https://github.com/Dysta/JukeBot.git`
3. Create your feature branch `git checkout -b AmazingFeature`
4. Stage changes `git add .`
5. Commit your changes `git commit -m 'Added some AmazingFeature'`
6. Push to the branch `git push origin AmazingFeature`
7. Submit a pull request

## ❤️ Credits

Realized with ❤️ by [Dysta](https://github.com/Dysta).
