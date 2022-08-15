# Slack Archive Bot
## Setup
### Installing PostgreSQL

You can install PostgreSQL for your platform [here](https://www.postgresql.org/download/)

### Requirements

This bot requires python 3. It was developed in python 3.10, and should work in anything greater than 3.7. 

For linux, `python` in commands should be replaced with `python3`

1. Open your command line/terminal interface and go to the directory where Dozer's code is located.
    1. If you're not familiar with how to do that:
        1. On Windows, open CMD or Powershell. On Mac and Linux, open the Terminal. and type `cd "path/to/directory"`.
           Alternatively, on Windows, go to the directory in the File Explorer app. Click the bar that is circled in the image below and type `cmd`. Press enter and the command line should open up within that directory. Also, you can use an integrated terminal with an IDE of your choice.

2. Install dependencies with `python -m pip install -Ur requirements.txt` in your command line interface.

3. Run the bot once with `python bot.py`. This will exit, but generate a default config file in `config.json`.
    1. The bot uses [json](http://www.json.org/) for its config file

4. Add the bots tokens to the `config.json` file. 
5. Add your database connection info to `db_url` in `config.json` using the following format:

   ```postgres://user:password@host:port```

   Replace `host` with your database IP, or `localhost` if it's on the same PC. `port` is by default 5432. If the user has no password, you can remove the colon and password. The default user for the above installation is `postgres`, however we strongly suggest making a different user for security reasons using [this guide](https://www.postgresql.org/docs/current/app-createuser.html).

6. Once this setup is complete, you can rerun the bot with `python bot.py`. 