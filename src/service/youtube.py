#! /usr/bin/env python3

"""DocString"""

# -=-=- Imports & Globals -=-=- #

import secret
import pytchat
from time import sleep

from lxml import html
import requests

import asyncio

# -=-=- Functions -=-=- #

def get_stream_id(channel_id):
    page = requests.get(f"https://www.youtube.com/embed/live_stream?channel={channel_id}")
    if page.status_code == 200:
        tree = html.fromstring(page.content)
        links = tree.xpath('//link[@rel="canonical"]')
        if links:
            id = links[0].attrib['href'].split("watch?v=")[1]
            return id
    return False

# -=-=- Classes -=-=- #

class YouTubeService:
    def __init__(self) -> None:
        self._on_out = []
        self._on_command = []

        self._is_connected = False
        self._is_live = False
        self._is_stopping = False

        self.chat = None
        self.video_id = get_stream_id(secret.youtube.CHANNEL_ID)

    def start(self):
        def main():
            if not self.video_id:
                msg = f"Cannot Find YouTube Stream Link for channel ID: {secret.youtube.CHANNEL_ID}"
                self._out(msg, do_print=True)
                self.video_id = secret.youtube.VIDEO_ID
            self._out(f"Found YouTube Stream ID: {self.video_id}", do_print=True)
            # -=-=- #
            # chat = LiveChatAsync(secret.youtube.VIDEO_ID, callback = func)
            # self.chat = chat = pytchat.create(secret.youtube.VIDEO_ID)
            self.chat = chat = pytchat.create(self.video_id)
            chat.get()
            
            # return livechat
            while chat.is_alive() and not chat.is_replay():
                if self._is_connected != chat.is_alive() or self._is_live == chat.is_replay():
                    self._connected(chat.is_alive(), not chat.is_replay())
                # if chat.is_replay():
                #     sleep(5)
                #     continue
                # -=-=- #
                # sync chat
                for c in chat.get().sync_items():
                    self._out(f"Youtube message from {c.author.name}: {c.message}", do_print=True)
                    self._command_(f"!greet {c.author.name}")
                    # print(f"{c.datetime} [{c.author.name}]- {c.message}")
                # print("--")
                sleep(1)
            self._connected(chat.is_alive(), not chat.is_replay())
            
            return not chat.is_replay()
        
        async def loop():
            while not self._is_stopping:
                if not main():
                    break
                if not self._is_stopping:
                    self._out("Restarting YouTube", do_print=True)
        
        asyncio.run(loop())


    def stop(self):
        print("Stopping YouTube")
        self._connected(False, False)
        if self.chat:
            self.chat.terminate()
    
    def on_out(self, cb: callable):
        self._on_out.append(cb)

    def _out(self, message: str, do_print:bool=False):
        # print("outing", message, self._on_out)
        if len(self._on_out) == 0:
            print(f"Out: {message}")
        else:
            for out in self._on_out: out(message, do_print=do_print)
    
    def _connected(self, status:bool, is_live:bool):
        self._is_connected = status
        self._is_live = is_live
        self._out(f"!status YouTube {int(status)} {int(is_live)}")

    
    def _command_(self, raw: str):
        if raw.lower() == '!stop':
            self._stop_(external=True)
        for on_command in self._on_command:
            on_command(raw)

    
    def on_command(self, cb: callable):
        self._on_command.append(cb)
        