#! /usr/bin/env python3

# -=-=- Imports and Globals -=-=- #

import pyttsx3


# -=-=- Classes -=-=- #


# -=-=- Functions -=-=- #

def init():
    engine = pyttsx3.init()
    engine.setProperty('rate', 135)

    voices = engine.getProperty('voices')
    print(voices)
    engine.setProperty('voice', voices[1].id)
    
    return engine


def say(tts, msg):
    tts.say(msg)
    tts.runAndWait()


## EOF
