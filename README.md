# JukeBot
[![Powered by Disnake](https://custom-icon-badges.herokuapp.com/badge/-Powered%20by%20Disnake-0d1620?logo=nextcord)](https://github.com/DisnakeDev/disnake "Powered by Disnake")
[![Powered by Poetry](https://custom-icon-badges.herokuapp.com/badge/-Powered%20by%20uv-0d1620?logo=uv)](https://docs.astral.sh/uv/ "Powered by uv") \
Discord music bot written in Python 3 
___

## 🧩 Deployment without Docker
```
git clone https://github.com/Dysta/JukeBot 
cd JukeBot
uv sync --locked
```

## ⚙ Configuration
Rename `.env.example` to `.env` and fill in the values.

## 🚀 Launch
Run `uv run task start`.

## ⁉ Other
The bot needs [ffmpeg](https://ffmpeg.org/) and [ffprobe](https://ffmpeg.org/) to work.

### Install on Windows
Use the package manager [Chocolatey](https://community.chocolatey.org/) and run in an **admin shell** `choco install ffmpeg`.

### Install on Linux
Use **apt**, run `sudo apt install ffmpeg`.

### Install on MacOS
Use **brew**, run `brew install ffmpeg`.

___

## 🌐 Deployment with Docker
Download and rename `.env.example` to `.env` and fill in the values. \
Run `docker run --name jukebot --restart on-failure:3 --env-file .env dysta/jukebot`.

___

## 🧰 Mise
Clone the project then in your terminal type `mise install` then `mise run install`. It will download both `ffmpeg` and `ffprobe` binary, add in the path and your good to go !

___

<details>
  <summary><h2>🗨 Features & Commands</h2></summary>
  <br>
    
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
</details>

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
