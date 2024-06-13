#! /usr/bin/env python3

import pyttsx3

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


## -=-=- MAIN -=-=- #

def main():
    tts = init()
    say(tts, "I will speak this text")
    # save("I will speak this text")

if __name__ == "__main__":
    main()
# EOF
