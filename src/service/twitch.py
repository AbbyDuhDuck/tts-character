#! /usr/bin/env python3

"""DocString"""

# -=-=- Imports & Globals -=-=- #

import requests
from twitchAPI.twitch import Twitch
from twitchAPI.eventsub.base import EventSubBase
from twitchAPI.object.eventsub import StreamOnlineEvent, StreamOfflineEvent
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import secret
import time

from threading import Thread

APP_ID = secret.twitch.APP_ID
APP_SECRET = secret.twitch.APP_SECRET
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = 'abbyduhduck'

# -=-=- Functions -=-=- #

# -=-=- Classes -=-=- #

# class TwitchEventService(EventSubBase):
#     def __init__(self, twitch: Twitch) -> None:
#         super().__init__(twitch)
    
#     def _build_request_header(self):
#         return super()._build_request_header()
    
#     def _get_transport(self):
#         return super()._get_transport()
    
#     def _subscribe(self, sub_type: str, sub_version: str, condition: dict, callback, event, is_batching_enabled: bool | None = None):
#         return super()._subscribe(sub_type, sub_version, condition, callback, event, is_batching_enabled)
    
#     def _unsubscribe_hook(self, topic_id: str):
#         return super()._unsubscribe_hook(topic_id)
    
#     def start(self):
#         return super().start()
    
#     def stop(self):
#         return super().stop()

class TwitchService:
    def __init__(self) -> None:
        self._is_stopping = False
        self._is_connected = False
        self._is_live = False
        self._on_out = []
        self._on_command = []
        self.token = ''
        # -=-=- #
        self.twitch = None
        self.game_name = ""

    async def _init_(self):
        # join our target channel, if you want to join multiple, either call join for each individually
        # or even better pass a list of channels as the argument
        await self.chat.join_room(TARGET_CHANNEL)
        # you can do other bot initialization things in here

    def is_live(self):
        if self.token == '' or self.token == None:
            return False

        headers = {
            'Client-ID': APP_ID,
            'Authorization': 'Bearer ' + self.token
        }

        stream = requests.get('https://api.twitch.tv/helix/streams?stream_type=live&user_login=' + TARGET_CHANNEL, headers=headers)
        stream_data = stream.json()

        if 'error' in stream_data:
            msg = f"{stream_data['error']} Error: {stream_data['message']}"
            self._out(msg, do_print=True)
            return False
        elif 'data' in stream_data and len(stream_data['data']) == 1:
            title = stream_data['data'][0]['title']
            game = stream_data['data'][0]['game_name']
            if game != self.game_name:
                self.game_name = game
                self._command_(f'!game {game}')
                print("Live:", title, game)
            return True
        return False

    def start_status_reader(self):
        def main():
            while not self._is_stopping:
                is_live = self.is_live()
                if self._is_live != is_live:
                    self._is_live = is_live
                    self._connected(self._is_connected, self._is_live)
                time.sleep(5)
        t = Thread(target=main)
        t.daemon = True
        t.start()

    def start(self):
        self.start_status_reader()
        self.start_twitch()

    def start_twitch(self):
        async def main():
            # set up twitch api instance and add user authentication with some scopes
            self.twitch = twitch = await Twitch(APP_ID, APP_SECRET)
            self.auth = auth = UserAuthenticator(twitch, USER_SCOPE)
            self.token, self.refresh_token = token, refresh_token = await auth.authenticate()
            await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

            # create chat instance
            self.chat = chat = await Chat(twitch)

            # register the handlers for the events you want

            # listen to when the bot is done starting up and ready to join channels
            chat.register_event(ChatEvent.READY, self._on_ready_event)
            # listen to chat messages
            chat.register_event(ChatEvent.MESSAGE, self._on_message_event)
            # listen to channel subscriptions
            # chat.register_event(ChatEvent.SUB, on_sub)
            # there are more events, you can view them all in this documentation
            # events = TwitchEventService(twitch)
            
            # you can directly register commands and their handlers, this will register the !reply command
            # chat.register_command('reply', test_command)

            chat.start()
        # -=-=- #
        asyncio.run(main())

    def stop(self):
        self._is_stopping = True
        self._connected(False, False)
        async def stop():
            print("Stopping Twitch")
            self.chat.stop()
            await self.twitch.close()
        asyncio.run(stop())
    
    # def _on_stream_online(self, event: StreamOnlineEvent, _):
    #     self._is_live = True
    #     self._connected(self._is_connected, self._is_live)

    # def _on_stream_offline(self, event: StreamOfflineEvent, _):
    #     self._is_live = False
    #     self._connected(self._is_connected, self._is_live)

    def _connected(self, status:bool, is_live:bool):
        self._out(f"!status Twitch {int(status)} {int(is_live)}")

    async def _on_ready_event(self, ready_event: EventData):
        self._out('Twitch Ready! Joining Channel', do_print=True)
        self._is_connected = True
        self._connected(self._is_connected, self._is_live)

        # await ready_event.chat.join_room(TARGET_CHANNEL)
        await self._init_()

    async def _on_message_event(self, message: ChatMessage):
        self._out(f"Twitch message from {message.user.name}: {message.text}", do_print=True)
        self._command_(f"!greet {message.user.name}")
        # await on_message(shell_out, 'Twitch', msg.user.name, msg.text)
    
    def on_out(self, cb: callable):
        self._on_out.append(cb)

    def _out(self, message: str, do_print:bool=False):
        # print("outing", message, self._on_out)
        if len(self._on_out) == 0:
            print(f"Out: {message}")
        else:
            for out in self._on_out: out(message, do_print=do_print)

    
    def _command_(self, raw: str):
        # if raw.lower() == '!stop':
        #     self._stop_(external=True)
        for on_command in self._on_command:
            on_command(raw)

    
    def on_command(self, cb: callable):
        self._on_command.append(cb)
        
