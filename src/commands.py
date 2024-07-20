#! /usr/bin/env python3

# -=-=- Main Source -=-=- #
'''
put docstring stuff here
'''

# -=-=- Imports & Globals -=-=- #

from typing import Callable, Self
from src.opinions import UserManager, get_explain_artamis

# -=-=- Functions -=-=- #

# -=-=- Classes -=-=- #



class CommandService:
    def __init__(self) -> None:
        self._on_out: list[Callable[[str], None]] = []
        self._on_say: list[Callable[[str], None]] = []
        self.commands = {}
        self._skip: list[str] = []

    def set_command(self, cmd:str, cb:Callable[[Self, str], None]):
        self.commands[cmd] = cb

    def skip_command(self, *cmds):
        for cmd in cmds:
            self._skip.append(cmd)

    def use_command_string(self, raw:str):
        tokens = raw.split(" ")
        cmd, args = tokens[0][1:], ' '.join(tokens[1:])
        self.use_command(cmd, args)

    def use_command(self, cmd:str, args:str):
        if cmd not in self.commands and cmd not in self._skip:
            self._out(f"Unrecognised Command `{cmd}`")
            return
        if cmd in self._skip:
            return
        # -=-=- #
        self.commands[cmd](self, args)

    def on_out(self, cb: Callable[[str], None]):
        self._on_out.append(cb)

    def _out(self, message: str):
        # print("Command Response", message, self._on_out)
        if len(self._on_out) == 0:
            print(f"Out: {message}")
        else:
            for out in self._on_out: out(message)

    def on_say(self, cb: Callable[[str], None]):
        self._on_say.append(cb)

    def _say(self, message: str):
        # print("Command Response", message, self._on_say)
        if len(self._on_say) == 0:
            print(f"Saying: {message}")
        else:
            for say in self._on_say: say(message)

    # -=-=- #

    def add_default_commands(self, users:UserManager):
        self.skip_command('stop')
        self.set_command('say', say_command)
        self.set_command('arti', artamis_command)
        self.set_command('artamis', artamis_command)
        self.set_command('greet', users.greet_command)
        self.set_command('game', game_command)


# -=-=- Default Commands -=-=- #

def say_command(command:CommandService, msg:str):
    command._say(msg)
    # -=-=- #
    print(f"Saying: {msg}")
    command._out(f"Saying: {msg}")

def artamis_command(command:CommandService, *_):
    msg = get_explain_artamis()
    # -=-=- #
    command._say(msg)
    print(f"Explaining Artamis: {msg}")
    command._out(f"Explaining Artamis: {msg}")

def game_command(command:CommandService, args:str):
    print(f"Setting Current Game: {args}")
    command._out(f"!game {args}")

# -=-=-=- test -=-=-=- #

def test():
    commands = CommandService()
    users = UserManager()

    # commands.on_out(print)
    # commands.on_say(print)
    commands.add_default_commands(users)

    # commands.set_command('say', say_command)

    commands.use_command_string("!say something interesting")
    commands.use_command_string("!greet Me, You")
    commands.use_command_string("!game Hollow Knight")
    commands.use_command_string("!stop")
    commands.use_command_string("!greet Me, Them")


if __name__ == '__main__':
    test()