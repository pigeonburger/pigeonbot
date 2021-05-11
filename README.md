# PigeonBot

*A simple no-coding required Discord moderation bot with its own levels system!*

PigeonBot is designed to be self-hosted, meaning that you, as a server owner, run the bot yourself! Using PigeonBot requires no programming knowledge - all you have to do is edit a settings file, and PigeonBot will take care of the rest!

# Features

- **No programming/coding knowledge required** - you just have to edit a config file.
- **Unique leveling system to encourage users engage with your server** - PigeonBot can award each user in your server with XP to assist them in leveling up to different roles (which can be auto-created). These ranks give people an incentive to stay active on your server. You can specify the number of levels, the names of the levels, and the XP required for each level!
- **Moderation** - PigeonBot can ban or kick misbehaving users under the instruction of a server moderator/admin.
- **Portable** - PigeonBot can be [downloaded](https://github.com/pygeonburger/pigeonbot/releases/latest) as an executable for Windows and Linux and run on any computer without installing any extra dependencies! Just make sure to bring the `pigeonbot.config` file with it.
- **Cross-platform** - Because PigeonBot only gets it's settings from the `pigeonbot.config` file, this file can be transferred from (for example) a Windows PC to a Linux machine and work *exactly* the same as long as you have the same `pigeonbot.config` file!

# Downloading and Installation

1. First, you'll have to get a bot token and add the bot account to your server. To do this, follow parts 2 and 3 ***ONLY*** in [this article](https://www.wikihow.com/Create-a-Bot-in-Discord) (when creating the invite link for the bot, give the bot Administrator permissions). Once you've done that, make sure you save your bot's token somewhere safe.

2. Next, [download PigeonBot](https://github.com/pygeonburger/pigeonbot/releases/latest) for your platform (*I would appreciate if someone could bundle this program for Mac using `pyinstaller`*) and extract the 2 files inside, `pigeonbot.exe` (just `pigeonbot` for Linux) and `pigeonbot.config`. It is important to keep both these files in the same folder at all times.

3. Using a text editor (such as Notepad), open the contents of `pigeonbot.config`. You will need to add multiple values to this file. The comments *inside* the `pigeonbot.config` file explain what you will need to add.

4. Once you've finished editing the config file, PigeonBot is ready to go! Windows users can start PigeonBot by double-clicking `pigeonbot.exe`, Linux users can start it by running `./pigeonbot` in the same folder as the files.


Feel free to submit any issues/suggestions on what to add next [here](https://github.com/pygeonburger/pigeonbot/issues). Pull requests are also welcome!
