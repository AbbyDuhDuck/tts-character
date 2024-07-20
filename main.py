#! /usr/bin/env python3

"""Docstring Thing"""

# -=-=- Imports and Globals -=-=- #

from src.service.twitch import TwitchService
from src.service.youtube import YouTubeService
from src.shell.console import Shell



from src.opinions import UserManager, get_explain_artamis
from src.commands import CommandService
# from test import OptionSelector

from src import tts as TTS
ENGINE = TTS.Engine('artamis')
ENGINE.start()

# -=-=- Functions -=-=- #

def clean_temp():
    try:
        from shutil import rmtree
        from os import mkdir
        rmtree('./tmp/')
        mkdir('./tmp/')
    except:
        pass

## -=-=- MAIN -=-=- #

def main():
    clean_temp()

    commands = CommandService()
    users = UserManager()

    users.add_special_user_greeting('bluejayjayjay',
        "Welcome back blue-jay - its good to see you again. Abby keeps spending all her time in your streams instead of working on my code - tell her get to work next time!"
        # "Welcome blue-jay - Abby told me all about your streams. I hope you enjoy while you're here.",
        # "Oh hey Abby, its blue. Hello Bule-Jay, Abby told me all about your streams - she really enjoys them. I hope you have fun too.",
    )
    
    shell = Shell(True)
    shell.on_command(commands.use_command_string)
    shell.start()

    commands.on_out(shell._out)
    commands.on_say(ENGINE.say)
    commands.add_default_commands(users)

    twitch = TwitchService()
    twitch.on_out(shell._out)
    shell.on_stop(twitch.stop)
    twitch.on_command(commands.use_command_string)
    twitch.start()

    youtube = YouTubeService()
    youtube.on_out(shell._out)
    shell.on_stop(youtube.stop)
    youtube.on_command(commands.use_command_string)
    youtube.start()


if __name__ == "__main__":
    main()

## EOF
