# JukeBot
[![Powered by Disnake](https://custom-icon-badges.herokuapp.com/badge/-Powered%20by%20Disnake-0d1620?logo=nextcord)](https://github.com/DisnakeDev/disnake "Powered by Disnake")
[![Powered by Poetry](https://custom-icon-badges.herokuapp.com/badge/-Powered%20by%20uv-0d1620?logo=uv)](https://docs.astral.sh/uv/ "Powered by uv") \
Discord music bot written in Python 3 

___
## 💻 Developping the bot
If you want to contribute to the developpement :
```
git clone https://github.com/Dysta/JukeBot 
cd JukeBot
uv sync --locked
```

### ⚙ Configuration
Rename `.env.example` to `.env` and fill in the values.

### 🚀 Launch
Run `uv run task start`.

## ➕ Other
The bot needs [FFmpeg](https://ffmpeg.org/) and [FFprobe](https://ffmpeg.org/) to work. It also require a [Deno](https://deno.com/) backend to correctly bypass Youtube bot protection.

### Install on Windows
Use [Chocolatey](https://community.chocolatey.org/), run `choco install ffmpeg`.

### Install on Linux
Use **apt**, run `sudo apt install ffmpeg`.

### Install on MacOS
Use **brew**, run `brew install ffmpeg`.

### Install Deno
Follow the [Deno guide](https://docs.deno.com/runtime/getting_started/installation/)

## 🧰 Mise
The project include a [mise](https://mise.jdx.dev/) configuration to quickly setup the local environment, I recommend to use this method.

In your terminal type `mise install` then `mise run install`. \
It will download `uv`, `python`, install the dependencies and setup both `ffmpeg` and `ffprobe` binary in your path.

> [!NOTE]
> **All** the scripts in `mise` aren't compatible with **Windows** since it use the `bash` syntaxe. \
> It also didn't install Deno since the bot detection from Youtube isn't triggered with a customer IP. \
> **The docker image does include Deno since this is this one that is supposed to run on a production environment.**

___

## 🌐 Running with Docker
If you just want to run the bot for your personnal use without dealing with any installation :
```bash
mkdir -p jukebot
cd jukebot
curl -fsSLo .env https://raw.githubusercontent.com/Dysta/JukeBot/main/.env.example
# edit .env to fill in the values
docker run --name jukebot --restart on-failure:3 --env-file .env dysta/jukebot
```

___

## 🗨 Features & Commands
A non exhaustive list of the commands supported by the bot.

### Music
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
  - [X] **`share`**
### Queue
  - [X] **`queue`**
  - [X] **`loopqueue`**
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
  - [X] **`info`**
  - [X] **`invite`**
  - [X] **`donate`**
  - [X] **`watch`**
  - [X] **`help`**

___

## 🤝 Contributing

Contributions are what make the open source community an amazing place to learn, be inspired, and create. 
Any contributions you make are **greatly appreciated**.

1. [Fork the repository](https://github.com/Dysta/JukeBot/fork)
2. Clone your fork `git clone https://github.com/Dysta/JukeBot.git`
3. Create your feature branch `git checkout -b AmazingFeature`
4. Stage changes `git add .`
5. Commit your changes `git commit -m 'Added some AmazingFeature'`
6. Push to the branch `git push origin AmazingFeature`
7. Submit a pull request

## ❤️ Credits

Released with ❤️ by [Dysta](https://github.com/Dysta).
