from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import secret

import pytchat
from pytchat import LiveChatAsync
import os
import sys
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE

from src import tts as TTS
from src import opinions
from test import OptionSelector

called_names = []
selector = OptionSelector('twitch')

APP_ID = secret.twitch.APP_ID
APP_SECRET = secret.twitch.APP_SECRET
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = 'abbyduhduck'

SYSTEM_TITLE = "Artamis Streaming Tool"
os.system("title " + SYSTEM_TITLE)

ENGINE = TTS.Engine('artamis')
ENGINE.start()

def start_shell():
    pass

# this will be called when the event READY is triggered, which will be on bot start
def on_ready(shell_out):
    async def _on_ready(ready_event: EventData):
        print('Bot is ready for work, joining channels')
        _print(shell_out, "!status Twitch 1")
        # join our target channel, if you want to join multiple, either call join for each individually
        # or even better pass a list of channels as the argument
        await ready_event.chat.join_room(TARGET_CHANNEL)
        # you can do other bot initialization things in here
    return _on_ready


# this will be called whenever a message in a channel was send by either the bot OR another user
def on_twitch_message(shell_out):
    async def _on_twitch_message(msg: ChatMessage):
        # print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')
        await on_message(shell_out, 'Twitch', msg.user.name, msg.text)
    return _on_twitch_message

# this will be called whenever someone subscribes to a channel
# async def on_sub(sub: ChatSub):
#     print(f'New subscription in {sub.room.name}:\\n'
#           f'  Type: {sub.sub_plan}\\n'
#           f'  Message: {sub.sub_message}')


# this will be called whenever the !reply command is issued
async def test_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply('you did not tell me what to reply with')
    else:
        await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')


# async def start_chatbot(proc, shell_out):
    

# async def init_youtube():
    
        
        
        
        # print("--")
        # await asyncio.sleep(1)

def _command_(shell_out, raw:str):
    raw = raw.split(' ')
    cmd, args = raw[0][1:], raw[1:]
    # print(f"Recieved User Command `{cmd}` - {args}")
    # _print(shell_out, f"Recieved User Command `{cmd}` - {args}")
    if cmd == 'say':
        msg = ' '.join(args)
        _print(shell_out, f"Saying: {msg}")
        ENGINE.say(msg)
    elif cmd in ('arti', 'artamis'):
        msg = opinions.get_explain_artamis()
        _print(shell_out, f"Saying: {msg}")
        ENGINE.say(msg)
    elif cmd == 'greet':
        user = ', '.join(args)
        msg = opinions.get_greeting(user)
        _print(shell_out, f"Greeting User: {user}")
        ENGINE.say(msg)
    else:
        _print(shell_out, f"Recieved User Command `{cmd}` - {args}")


def _print(shell_out, msg:str):
    print(msg.strip() + '\n', file=shell_out)
    shell_out.flush()

async def on_message(shell_out, platform, author, message):
    print(f'{platform}: {author} - {message}')

    if not author in called_names:
        called_names.append(author)
        msg = opinions.get_greeting(author)
        _print(shell_out, f"Greeting {platform} user: {author}")
        ENGINE.say(msg)


async def stop_all(twitch, twitch_chat, youtube_chat):
    twitch_chat.stop()
    await twitch.close()
    youtube_chat.terminate()
    print("Closing Gracefully")
    exit(0)

#callback function is automatically called periodically.
async def func(chatdata):
  print("thingy")
  print(chatdata)
  for c in chatdata.items:
    print(f"{c.datetime} [{c.author.name}]-{c.message} {c.amountString}")
    await chatdata.tick_async()

# def run_option_chooser():
#    while True:
      
async def options_menu():
    while True:
        if input("> ") == "stop":
            print("Stopping")
            exit(0)

def main():
    # proc, out = start_shell()
    # input('press enter')
    # while True:
    #     usr_in = p.stderr.readline().decode("utf-8").strip()
    #     if usr_in == '':
    #         continue

        
    # asyncio.run(start_chatbot(proc, out))
    # asyncio.run(init_youtube())


    from src.service.twitch import TwitchService
    from src.service.youtube import YouTubeService
    from src.shell.console import Shell

    shell = Shell(True)
    shell.start()

    twitch = TwitchService()
    twitch.on_out(shell._out)
    shell.on_stop(twitch.stop)
    twitch.start()

    youtube = YouTubeService()
    youtube.on_out(shell._out)
    shell.on_stop(youtube.stop)
    youtube.start()


if __name__=='__main__':
    main()
    # asyncio.run_coroutine_threadsafe(main(), asyncio.get_event_loop())
    # try:
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(run_chatbot())
    # except asyncio.exceptions.CancelledError:
    #     pass



