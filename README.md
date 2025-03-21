# Auto_accept
A bot which is automatically accept join request in telegram groups and welcome new members.

# deploy on vps
* 1 `sudo apt update && sudo apt upgrade -y`

* 2 `sudo apt install --no-install-recommends -y python3-lxml python3-psycopg2 libpq-dev libcurl4-openssl-dev libxml2-dev libxslt1-dev python3-pip python3-sqlalchemy openssl wget curl git libffi-dev libjpeg-dev libwebp-dev python3 python3-dev pv tree mediainfo nano nodejs libreadline-dev libyaml-dev gcc zlib1g ffmpeg libssl-dev libgconf-2-4 libxi6 unzip libopus0 libopus-dev python3-virtualenv tmux libmagickwand-dev`
  
* 3 Clone the GitHub repo
`git clone --branch for-fast https://github.com/rishabhops/Auto_accept && cd Auto_accept`


* 5 Install requirements to run the bot `pip3 install -r requirements.txt`

* 6 fill vars `nano vars.py`

* 7 start screen `tmux`

* 8 start the bot `python3 bot.py`

# close the terminal ctrl+b then d
