#! /usr/bin/env python3

from src import tts as TTS
from src import midi



## -=-=- MAIN -=-=- #

def main():
    tts = TTS.init()
    TTS.say(tts, "hello foolish mortals")
    # save("I will speak this text")

if __name__ == "__main__":
    main()
# EOF
