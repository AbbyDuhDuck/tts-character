#! /usr/bin/env python3

"""Docstring Thing"""

# -=-=- Imports and Globals -=-=- #

from src.service.twitch import TwitchService
from src.service.youtube import YouTubeService
from src.shell.console import Shell


from src import tts as TTS
from src import opinions
# from test import OptionSelector
ENGINE = TTS.Engine('artamis')
ENGINE.start()

called_users = ['KofiStreamBot']

# -=-=- Functions -=-=- #

def clean_temp():
    try:
        from shutil import rmtree
        from os import mkdir
        rmtree('./tmp/')
        mkdir('./tmp/')
    except:
        pass

def on_command(shell: Shell):
    def _func(raw: str):
        raw = raw.split(' ')
        cmd, args = raw[0][1:], raw[1:]
        print(f"Recieved Command `{cmd}` - {args}")

        if cmd == 'say':
            msg = ' '.join(args)
            shell._out(f"Saying: {msg}")
            ENGINE.say(msg)
        elif cmd in ('arti', 'artamis'):
            msg = opinions.get_explain_artamis()
            shell._out(f"Saying: {msg}")
            ENGINE.say(msg)
        elif cmd == 'try_greet':
            if len(args) == 0: return
            if not args[0] in called_users:
                _func(f"!greet {' '.join(args)}")

        elif cmd == 'greet':
            user = ' '.join(args)
            msg = opinions.get_greeting(user)
            shell._out(f"Greeting User: {user}")
            ENGINE.say(msg)
        else:
            shell._out(f"Recieved User Command `{cmd}` - {args}")
    return _func

## -=-=- MAIN -=-=- #

def main():
    clean_temp()

    shell = Shell(True)
    shell.on_command(on_command(shell))
    shell.start()

    twitch = TwitchService()
    twitch.on_out(shell._out)
    shell.on_stop(twitch.stop)
    twitch.on_command(on_command(shell))
    twitch.start()

    youtube = YouTubeService()
    youtube.on_out(shell._out)
    shell.on_stop(youtube.stop)
    youtube.on_command(on_command(shell))
    youtube.start()

if __name__ == "__main__":
    main()

## EOF
