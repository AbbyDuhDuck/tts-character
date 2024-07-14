#! /usr/bin/env python3

"""DocString"""

# -=-=- Imports & Globals -=-=- #

from twitchAPI.twitch import Twitch
from twitchAPI.eventsub.base import EventSubBase
from twitchAPI.object.eventsub import StreamOnlineEvent, StreamOfflineEvent
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import secret

APP_ID = secret.twitch.APP_ID
APP_SECRET = secret.twitch.APP_SECRET
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = 'abbyduhduck'

# -=-=- Functions -=-=- #

# -=-=- Classes -=-=- #

class TwitchService:
    def __init__(self) -> None:
        self._is_connected = False
        self._is_live = False
        self._on_out = []
        self._on_command = []

    async def _init_(self):
        # join our target channel, if you want to join multiple, either call join for each individually
        # or even better pass a list of channels as the argument
        await self.chat.join_room(TARGET_CHANNEL)
        # you can do other bot initialization things in here

    def start(self):
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
            # events = EventSubBase(twitch)

            # events.listen_stream_online(TARGET_CHANNEL, self._on_stream_online)
            # events.listen_stream_offline(TARGET_CHANNEL, self._on_stream_offline)

            # you can directly register commands and their handlers, this will register the !reply command
            # chat.register_command('reply', test_command)

            # return twitch, chat
            chat.start()
        asyncio.run(main())
    
    def stop(self):
        self._connected(False, False)
        async def stop():
            print("Stopping Twitch")
            self.chat.stop()
            await self.twitch.close()
        asyncio.run(stop())
    
    def _on_stream_online(self, event: StreamOnlineEvent, _):
        self._is_live = True
        self._connected(self._is_connected, self._is_live)

    def _on_stream_offline(self, event: StreamOfflineEvent, _):
        self._is_live = False
        self._connected(self._is_connected, self._is_live)

    def _connected(self, status:bool, is_live:bool):
        self._out(f"!status Twitch {int(status)} {int(is_live)}")

    async def _on_ready_event(self, ready_event: EventData):
        print('Bot is ready for work, joining channels')
        self._is_connected = True
        self._connected(self._is_connected, self._is_live)

        # await ready_event.chat.join_room(TARGET_CHANNEL)
        await self._init_()

    async def _on_message_event(self, message: ChatMessage):
        msg = f"Twitch message from {message.user.name}: {message.text}"
        # TODO: add an on message event
        print(msg)
        self._out(msg)
        self._command_(f"!try_greet {message.user.name}")
        # await on_message(shell_out, 'Twitch', msg.user.name, msg.text)
    
    def on_out(self, cb: callable):
        self._on_out.append(cb)

    def _out(self, message: str):
        print("outing", message, self._on_out)
        if len(self._on_out) == 0:
            print(f"Out: {message}")
        else:
            for out in self._on_out: out(message)

    
    def _command_(self, raw: str):
        # if raw.lower() == '!stop':
        #     self._stop_(external=True)
        for on_command in self._on_command:
            on_command(raw)

    
    def on_command(self, cb: callable):
        self._on_command.append(cb)
        
