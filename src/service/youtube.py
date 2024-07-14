#! /usr/bin/env python3

"""DocString"""

# -=-=- Imports & Globals -=-=- #

import secret
import pytchat
from time import sleep

# from pytchat import LiveChatAsync

# -=-=- Functions -=-=- #

# -=-=- Classes -=-=- #

class YouTubeService:
    def __init__(self) -> None:
        self._on_out = []
        self._on_command = []

    def start(self):
        # chat = LiveChatAsync(secret.youtube.VIDEO_ID, callback = func)
        self.chat = chat = pytchat.create(secret.youtube.VIDEO_ID)
        self._connected(True, chat.is_replay()) 
        
        # return livechat
        while chat.is_alive() and not chat.is_replay():
            print("--")
            # sync chat
            for c in chat.get().sync_items():
                msg = f"Youtube message from {c.author.name}: {c.message}"
                # TODO: add an on message event
                print(msg)
                self._out(msg)
                self._command_(f"!try_greet {c.author.name}")
                # print(f"{c.datetime} [{c.author.name}]- {c.message}")
                # await on_message(shell_out, 'YouTube', c.author.name, c.message)
            sleep(1)
        self._connected(chat.is_alive(), not chat.is_replay())

    def stop(self):
        print("Stopping YouTube")
        self._connected(False, False)
        self.chat.terminate()
    
    def on_out(self, cb: callable):
        self._on_out.append(cb)

    def _out(self, message: str):
        print("outing", message, self._on_out)
        if len(self._on_out) == 0:
            print(f"Out: {message}")
        else:
            for out in self._on_out: out(message)
    
    def _connected(self, status:bool, is_live:bool):
        self._out(f"!status YouTube {int(status)} {int(is_live)}")

    
    def _command_(self, raw: str):
        if raw.lower() == '!stop':
            self._stop_(external=True)
        for on_command in self._on_command:
            on_command(raw)

    
    def on_command(self, cb: callable):
        self._on_command.append(cb)
        