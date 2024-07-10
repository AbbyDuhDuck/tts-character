#! /usr/bin/env python3

from src import tts as TTS
from test import OptionSelector

import pytchat
import os
import sys
from time import sleep as time_sleep
import threading

called_names = []
selector = OptionSelector('youtube')

youtube_id = ""
with open("./config/youtube_id.txt", "r") as file:
    file_lines = file.readlines()
    youtube_id = file_lines[0]

    
twitch_id = ""
with open("./config/twitch_id.txt", "r") as file:
    file_lines = file.readlines()
    twitch_id = file_lines[0]

stop_reader = False

print(f"Starting with YouTube ID: {youtube_id}")
print(f"Starting with Twitch ID: {twitch_id}")

chat = pytchat.create(video_id=youtube_id)
attribute_error_count = 0

#Check config folder to save the state when restarting.
if not os.path.exists("./config"):
    os.makedirs("./config")

#Set last_message
#When restart, sometime you get repeated chat, so you need last_message to avoid this.
if not os.path.exists("./config/last_message.txt"):
    with open("./config/last_message.txt", "w", encoding="utf-8") as file:
        pass
with open("./config/last_message.txt", "r", encoding="utf-8") as file:
    last_message = file.read()

while True:
    if attribute_error_count >= 20:
        with open("./config/last_message.txt", "w", encoding="utf-8") as file:
            file.write(last_message)
        """
        State saving code
        """
        print("Restarting program...")
        os.execv(sys.executable, ["python"] + sys.argv)

    try:
        for c in chat.get().sync_items():

            # inject a custom message

            with open("./config/custom_message.txt", "r") as file:
                msg = file.read()
                if msg.strip() != "":
                    print(f"saying: {msg}")
                    selector.say(msg)
                    with open("./config/custom_message.txt", "w") as f:
                        f.write("")
                    time_sleep(15)

            # -=-=- #
            message = f"{c.datetime} [{c.author.name}]- {c.message}"
            author = c.author.name
            if message == last_message:
                time_sleep(5)
            else:
                last_message = message
            # print(message)
            if not author in called_names:
                called_names.append(author)
                # call the name
                print(f"greeting: {author}")
                selector.greet(author)
                time_sleep(7)
            else:
                print(f"not greeting: {author}")

            if stop_reader:
                print ("Stopping") 
                break
    except AttributeError:
        print("AttributeError")
        chat = pytchat.create(video_id=youtube_id)#Reset chat. Not sure if this line work, maybe you can delete it.
        attribute_error_count += 1

    if stop_reader:
        print ("Stopping") 
        break

    with open("./config/custom_message.txt", "r") as file:
        msg = file.read()
        if msg.strip() != "":
            print(f"saying: {msg}")
            selector.say(msg)
            with open("./config/custom_message.txt", "w") as f:
                f.write("")
            time_sleep(15)
    
    time_sleep(5)


# -=-=- #

# from twitchchatreader import TwitchChatReader
# from twitchchatreaderevents import CommentEvent, ConnectEvent

# reader: TwitchChatReader = TwitchChatReader(twitch_id)


# # executes when a connection is established
# @reader.on("connect")
# def on_connect(event: ConnectEvent):
#     print("Connection established!")

# # executes when a comment is received
# @reader.on("comment")
# def on_connect(event: CommentEvent):
#     print(event.user.name, "|", event.comment)
#     author = event.user.name

#     if not author in called_names:
#         called_names.append(author)
#         # call the name
#         print(f"greeting: {author}")
#         selector.greet(author)
#         time_sleep(7)
#     else:
#         print(f"not greeting: {author}")

# -=-=- #

def stopper():
    while True:
        if input('"exit" to stop\n').lower() == 'exit':
            global stop_reader
            stop_reader = True
        exit(0)


def main():
    pass
    # stopper_thread = threading.Thread(target=stopper, name="Thread Stopper")
    # stopper_thread.start()

    # youtube_reader()

    # thread_youtube = threading.Thread(target=youtube_reader, name="YouTube-Name-Reader")
    # thread_youtube.start()

    # thread_twich = threading.Thread(target=twitch_reader, name="Twitch-Name-Reader")
    # thread_twich.start()


    