#! /usr/bin/env python3

# -=-=- Imports and Globals -=-=- #

import pyttsx3
from pygame import mixer, _sdl2 as devices
from os.path import exists as path_exists
from os import remove as path_remove

from threading import Thread
from time import sleep


# -=-=- Classes -=-=- #


class Engine:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.queue = []

        # Old Code:
        # engine = pyttsx3.init()
        # engine.setProperty('rate', 135)
        # voices = engine.getProperty('voices')
        # print(voices)
        # engine.setProperty('voice', voices[1].id)
        # -=-=- #

        # New Code:
        # Get available output devices
        # mixer.init()
        # print("Outputs:", )
        # for thing in devices.audio.get_audio_device_names(False): print(thing)
        # mixer.quit()

        # Initialize mixer with the correct device
        # Set the parameter devicename to use the VB-CABLE name from the outputs printed previously.
        # mixer.init(devicename = "CABLE Input (VB-Audio Virtual Cable)")
        
        # mixer.init()
        mixer.init(devicename = "Voicemeeter Input (VB-Audio Voicemeeter VAIO)")

        # Initialize text to speech
        engine = pyttsx3.Engine()
        
        engine.setProperty('rate', 135)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        # print(voices)

        self.engine = engine

    def start(self):
        def main():
            while True:
                sleep(1)
                if len(self.queue) == 0: continue
                if mixer.music.get_busy(): continue
                # -=-=- #
                msg = self.queue.pop(0)
                self._say(msg)

        self.main_thread = t = Thread(target=main)
        t.daemon = True
        t.start()

    def say(self, msg):
        self.queue.append(msg)
    
    def _say(self, msg):
        # self.engine.say(msg)
        # self.engine.runAndWait()
        # return 

        filepath = "tmp/{filename}.wav".format(filename=self.filename)

        # if file exists then remove!!!
        mixer.music.unload()
        if path_exists(filepath):
            path_remove(filepath)
    
        # Save speech as audio file
        self.engine.save_to_file(msg, filepath)
        self.engine.runAndWait()

        # Play the saved audio file
        mixer.music.load(filepath)
        mixer.music.play()

# -=-=- Functions -=-=- #

## EOF
