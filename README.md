<div align="center">

[![juke-banner](https://cdn.discordapp.com/attachments/829356508696412231/948936347752747038/juke-banner.png)](#readme)
</div>

# JukeBot
[![Powered by Disnake](https://custom-icon-badges.herokuapp.com/badge/-Powered%20by%20Disnake-0d1620?logo=nextcord)](https://github.com/DisnakeDev/disnake "Powered by Disnake")
[![Powered by Poetry](https://custom-icon-badges.herokuapp.com/badge/-Powered%20by%20Poetry-0d1620?logo=poetry)](https://python-poetry.org "Powered by Poetry") \
Discord music bot written in Python 3 
___

## 🧩 Installation
```
git clone https://github.com/Dysta/JukeBot 
cd JukeBot
poetry install
```

## ⚙ Configuration
Rename `.env.example` to `.env` and fill in the values.

## 🚀 Launch
Run `poetry run task start`.

## ⁉ Other
The bot needs `ffmpeg` to work.
### Install on Windows
Use the package manager [Chocolatey](https://community.chocolatey.org/) and run in an admin shell `choco install ffmpeg`.

### Install on Linux
Use apt, run `sudo apt install ffmpeg`.

___

## 🌐 Deployment
Rename `.env.example` to `.env` and fill in the values. \
Run `docker-compose up -d`.

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
  - [X] **`avatar`**
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
