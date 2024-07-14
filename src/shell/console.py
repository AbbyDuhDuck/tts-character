#! /usr/bin/env python3

"""DocString"""

# -=-=- Imports & Globals -=-=- #

# from twitchAPI.twitch import Twitch
# from twitchAPI.oauth import UserAuthenticator
# from twitchAPI.type import AuthScope, ChatEvent
# from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
# import asyncio
# import secret

# import pytchat
# from pytchat import LiveChatAsync
from os import set_blocking
from sys import executable
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE
from time import sleep

from src.shell.console_window import FIFO_PATH, CONSOLE_PATH

from threading import Thread

# from src import tts as TTS
# from src import opinions
# from test import OptionSelector

# -=-=- Functions -=-=- #

# -=-=- Classes -=-=- #

class Shell:
    def __init__(self, keep_alive=False):
        self._on_stop = []
        self._on_command = []
        self.stopping = False
        self.keep_alive = keep_alive

    def start(self):
        self._make_console_window_()
        self._connect_()

    def _make_console_window_(self):

        # set internal fifo
        self.fifo_out = open(FIFO_PATH, 'w+', encoding='utf-8', errors='ignore')
        # print("fifo_out:", fifo_out)

        self.process = proc = Popen(
            [executable, CONSOLE_PATH],
            creationflags=CREATE_NEW_CONSOLE,
            stderr=PIPE,
            pipesize=4096,  # Linux has like 65k which is just too much for us.
            bufsize=4096,  # No effect I guess. But better safe than sorry.
            encoding='utf-8', errors='ignore',
        )
        # set other internal fifo
        self.fifo_in = proc.stderr
        # Un-block the file so no read locking.
        set_blocking(proc.stderr.fileno(), False)

        print("Console Started")
    
    def _connect_(self):
        def main():
            while not self.stopping:
                # sync internal messages
                self.fifo_in.flush()
                usr_in = self.fifo_in.readline().strip()
                if usr_in != '':
                    if usr_in.startswith('!'):
                        self._command_(usr_in)
                    else:
                        print("Recieved:", usr_in)
                sleep(0.5)

        self.main_thread = t = Thread(target=main)
        t.daemon = not self.keep_alive
        t.start()
    
    def _out(self, message: str):
        print(message, file=self.fifo_out)
        self.fifo_out.flush()
        # print(message.strip() + "\n", file=self.fifo_out)
    
    def _stop_(self, external=False):
        self.stopping = True

        for on_stop in self._on_stop:
            on_stop()

        if not external:
            self._out("!stop")
        print("Stopping Console Controller")
        self._out("Stopping Console Controller")

    def on_stop(self, cb: callable):
        self._on_stop.append(cb)

    def _command_(self, raw: str):
        if raw.lower() == '!stop':
            self._stop_(external=True)
        for on_command in self._on_command:
            on_command(raw)

    
    def on_command(self, cb: callable):
        self._on_command.append(cb)
        

if __name__ == "__main__":
    shell = Shell(keep_alive=True)
    shell.start()