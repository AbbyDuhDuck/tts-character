#! /usr/bin/env python3

"""DocString"""

# -=-=- Imports & Globals -=-=- #

import sys
from threading import Thread
import asyncio
from time import sleep

import curses
import math
from curses import wrapper
from curses.textpad import Textbox, rectangle
from os import system

SYSTEM_TITLE = "Artamis Streaming Console"
system("title " + SYSTEM_TITLE)

FIFO_PATH = f'./tmp/out.fifo'
CONSOLE_PATH = __file__

# curses.init_pair(30, curses.COLOR_BLUE, curses.COLOR_BLACK)
# BLUE_TEXT = curses.color_pair(30)

# -=-=- Functions -=-=- #

# -=-=- Classes -=-=- #


class Shell:
    def __init__(self):
        self.print_log = ""
        self.pipe_status = False
        self.twitch_status = False
        self.twitch_is_live = False
        self.youtube_status = False
        self.youtube_is_live = False

        self.stopping = False

    def _run_(self, stdscr: curses.window):
        self._init_(stdscr)

        self._writer_thread_ = t = Thread(target=self._writer_())
        t.daemon = False
        t.start()

        self._reader_thread_ = t = Thread(target=self._reader_())
        t.daemon = True
        t.start()

    def _stop_(self):
        self.stopping = True
        self.print("Shell Stopping...")
        self._out('!stop')

    def _init_(self, stdscr: curses.window):
        self.stdscr = stdscr
        # -=-=- #
        stdscr.clear()
        stdscr.addstr("Starting...")
        stdscr.refresh()
        # -=- #
        w = curses.COLS-1
        h = 15
        p = 8

        rectangle(stdscr, 0, 0, 2, w)
        rectangle(stdscr, 2, 0, h+3, w)
        rectangle(stdscr, h+3, 0, h+p+3, w)
        stdscr.refresh()
        # -=-=- #
        self.status_window = curses.newwin(1, w-3, 1, 2)
        self.log_window = curses.newwin(h, w-2, 3, 1)
        self.log_window.scrollok(True)
        self.prompt_window = curses.newwin(p-2, w-2, h+4, 1)
        # self.prompt_window.scrollok(True)
        self.text_window = curses.newwin(1, w-2, h+4+p-2, 1)
        # -=-=- #
        self._update_status()
        
        curses.raw()
        curses.cbreak()
        curses.noecho()

    def _update_status(self):
        status = ""

        connection = ""
        # -=- #
        if self.twitch_status:
            connection += "Tw"
            if not self.twitch_is_live:
                connection += "*"
            connection += " "
        if self.youtube_status:
            connection += "YT"
            if not self.youtube_is_live:
                connection += "*"
            connection += " "
        # -=- #
        if self.pipe_status and not connection:
            connection = "Connecting"
        if not connection:
            status += "Status: Offline"
        else:
            status += "Status: %s" % connection.strip()
        
        self.status_window.clear()
        self.status_window.addstr(0, 0, status)
        self.status_window.refresh()

    
    def print(self, line: str, ending='\n'):
        win = self.log_window
        # -=-=- #
        self.print_log += line + ending
        
        win.addstr(0, 0, self.print_log.strip())
        win.refresh()
    
    def input(self, prompt:str="", input_prompt:str=">", hide:bool=False):
        self.prompt_window.clear()
        self.prompt_window.addstr(0, 0, prompt)
        self.prompt_window.refresh()
        self.text_window.clear()
        self.text_window.addstr(0, 0, input_prompt)
        self.text_window.refresh()
        # -=-=- # 
        usr_in = ""
        while True:
            key = self.text_window.getkey(0,0)
            # -=-=- # 
            if key in ('\n', '\r'):
                break # return pressed
            elif key in "1234567890!- ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                usr_in += key
            elif str(key) in ('\b', '\x7f'):
                usr_in = usr_in[:-1]
            # elif not key in "!@#$%^&*()_+=\\/.,\"':;[]{{<>}}":
            #     print(f"Unknown Keypress: `{key}`")
            # -=-=- # 
            self.text_window.clear()
            if not hide:
                self.text_window.addstr(0, 0, "%s %s" % (input_prompt, usr_in))
            self.text_window.refresh()

        # -=-=- # 
        self.text_window.clear()
        self.text_window.refresh()
        self.prompt_window.clear()
        self.prompt_window.refresh()
        return usr_in
    
    def _status_(self, opt, status, is_live='0', *_):
        if opt == "Twitch":
            try: self.twitch_status = bool(int(status))
            finally: 
                self.print(f"Twitch Chat - {self.twitch_status and 'Connected' or 'Disconnected'}")
            # -=-=- #
            try: self.twitch_is_live = bool(int(is_live))
            finally: 
                self.print(f"Twitch Stream {self.twitch_is_live and 'is' or 'is not'} Live")
            # -=-=- #
            self._update_status()
        if opt == "YouTube":
            try: self.youtube_status = bool(int(status))
            finally:
                self.print(f"YouTube Chat - {self.youtube_status and 'Connected' or 'Disconnected'}")
            # -=-=- #
            try: self.youtube_is_live = bool(int(is_live))
            finally:
                self.print(f"YouTube Stream {self.youtube_is_live and 'is' or 'is not'} Live")
            # -=-=- #
            self._update_status()
    
    def _command_(self, raw: str):
        if not raw.startswith('!'): return
        # -=-=- #
        cmd = raw.split(' ')
        cmd, args = cmd[0][1:], cmd[1:]
        # -=-=- #
        if cmd == '!': cmd = 'say'
        # -=-=- #
        if cmd == 'stop':
            self._stop_()
        elif cmd in ['arti', 'artamis', 'greet', 'say']:
            # should never recieve these commands from the server
            self._out(f"!{cmd} {' '.join(args)}")
        elif cmd == 'status':
            self._status_(*args)
        else:
            self.print(f'Unknown Command `{cmd}` - {args}')

    def _reader_(self):
        def _main():
            out_fifo = open(FIFO_PATH, 'r+', encoding='utf-8', errors='ignore')
            # self.print(str(out_fifo))
            self.print("Connected to Artamis!")
            self.pipe_status = True
            self._update_status()
            while True:
                sys_in = out_fifo.readline().strip()
                out_fifo.flush()
                if sys_in == '': continue
                # -=-=- #
                if sys_in.startswith('!'):
                    self._command_(sys_in)
                else:
                    self.print(sys_in)
                sleep(0.4)
        return _main

    def _out(self, msg):
            print(msg, file=sys.stderr)

    def _writer_(self):
        
            # sys.stderr.write(msg + "\n")
            # sys.stderr.flush()
        def _main():
            # -=- Heading -=- #
            title = "-=- Artamis Streaming Tool -[^v^]- by AbbyDuhDuck -=-"
            stop = "Type STOP to stop"
            y1 = math.floor((curses.COLS-len(title))/2-2)
            y2 = math.floor((curses.COLS-len(stop))/2-2)
            msg = f"\n{' '*y1}{title}\n\n{' '*y2}{stop}\n\n Press ENTER to continue."
            _ = self.input(msg, input_prompt="", hide=True)
            # -=- Main Loop -=- #
            prompt = "Type STOP to stop\n\n!say [...] -> say something\n!artamis !arti -> explain artamis\n!greet [user]"
            while not self.stopping:
                usr_in = self.input(prompt)
                if usr_in.lower() == 'stop':
                    self._stop_()
                elif usr_in.startswith('!'):
                    self._command_(usr_in)
                else:
                    self.print(f"Unknown Input: {usr_in}")
            sleep(3)
        return _main


# -=-=-=- MAIN -=-=-=- #

def __main__():
    shell = Shell()
    wrapper(shell._run_)

if __name__ == "__main__":
    __main__()

# EOF
