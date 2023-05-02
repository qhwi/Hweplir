# Hweplir - Discord CTF Management bot

Hweplir is a self-hosted bot that I created for personal servers, comprises of some basic CTF management commands *(mainly for display CTFs info, fast create/delete with CTFTime API integration, auto hide/view CTF discussion Categories)*. 

This bot makes use of the new Discord slash command and Buttons using `discord.py` 2.0!

Contribution and suggestion is highly welcome:)


# Setup


## Create the bot

First, head to <a href="https://discord.com/developers/applications">Discord's Developer Portal</a>, and create a new Application.

Next, config your bot information in the `General Information` and `Bot` section.

Note: make sure to enable all Intents + Copy the bot's `TOKEN` and store it somewhere safe for now.

Finally, go to `OAuth2/URL Generator` and generate a bot invite url, then add the bot to your server!


## Installation

First, clone this repository:

```
git clone https://github.com/qhwi/Hweplir
```
### Dependency

- discord.py 2.x
```
pip install discord.py
```
- Python 3.8 or newer

### Config
Hweplir requires some secret environment variables:
```
TOKEN=
SERVER_ID=
VIEW_ALL_CTF_ROLEID=
LOG_CHANNELID=
```
Copy your saved bot's TOKEN and ID of the desired server, to **create `.env` file** that defined the required variables. 

Alternatively, you can just replace the value directly in `main.py` :P

Finally, **create a role** named **`<<<VIEW_ALL_CTF>>>`** in your server. **Copy** the Role ID and replace it in `main.py`. Also **assign** this role to your bot.

### Hosting for free using Repl

Create a web application with a file like this, and include `keep_alive()` when run bot with `main.py`.
```python
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "hello world"
def run():
  app.run(host='0.0.0.0',port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()
```

Then using services such as UptimeRobot to ping the app every 5 minutes:) Run `main.py` as normal.

Note: Instead of create `.env` file, simply create new Secret for `TOKEN` and `SERVER_ID`.


# Commands

To show commands list, use `/help`. To read command's description and required variables, just type `/` and scroll through each.

<img src="https://github.com/qhwi/Hweplir/blob/main/image/help.png" width="400">

*[To be Updated]*
 
