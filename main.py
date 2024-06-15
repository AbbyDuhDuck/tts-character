#! /usr/bin/env python3


# -=-=- Imports and Globals -=-=- #

from src import gui
from src import tts as TTS
from src import midi


## -=-=- MAIN -=-=- #

def main():
    # tts = TTS.init()
    # TTS.say(tts, "hello foolish mortals")
    # save("I will speak this text")
    gui.run()

if __name__ == "__main__":
    main()


## EOF
