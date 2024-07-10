#! /usr/bin/env python3

from src import tts as TTS
import random


class OptionSelector:
    def __init__(self, filename='artamis-line') -> None:
        self.tts_engine = TTS.Engine(filename)

        self.current_boss = None
        self.boss_tries = 0

    def display(self):
        print("Options:")
        print(" 0) Refresh Options")
        print(" 1) Type Custom Message")
        print(" 2) Greet User")
        print(" 3) Explain Artamis")
        print(" 4) Dead")
        print(" 5) Boss Loss")
        print(" 6) Boss Win")
        print(" 7) Comment on Area")
        print(" 8) Boss Setup")
        # print(" 8) Comment on Catch")
        # print(" 9) Comment on Monster")
        print("\n\n")

    def getSelection(self):
        usr_in = input("> ")
        print(usr_in)

        if usr_in.lower() == "exit":
            exit()

        try:
            return int(usr_in)
        except ValueError:
            print("NAN!")
            return self.getSelection()

    def select(self, option):
        if option == 0:
            pass # refresh
        elif option == 1:
            self.type_then_say()
        elif option == 2:
            self.greet_user()
        elif option == 3:
            self.explain_artamis()
        elif option == 4:
            self.player_died()
        elif option == 5:
            self.boss_loss()
        elif option == 6:
            self.boss_win()
        elif option == 7:
            self.comment_on_area()
        elif option == 8:
            self.boss_set_up()
        # elif option == 8:
        #     self.comment_on_catch()
        # elif option == 9:
        #     self.comment_on_mon()
        else:
            print("This is not a valid option.")

    def say(self, msg):
        self.tts_engine.say(msg)
    
    def greet(self, user):
        self.say(self.get_greeting(user))
    
    def address(self, user):
        self.say(self.get_address_user_msg(user))

    # -=-=- Boss Stuff -=-=- #

    def boss_set_up(self):
        print("1) clear")
        print("2) new boss") 
        print("3) set tries")

        usr_in = input("> ")

        msg = ""
        if usr_in == "1":
            self.clear_boss()
        elif usr_in == "2":
            self.current_boss = input("boss name: ")
            self.boss_tries = 0
        elif usr_in == "3":
            num = input("tries: ")
            if num.isdigit(): 
                self.boss_tries = int(num)

        self.update_hud_files()

    def clear_boss(self):
        self.current_boss = None
        self.boss_tries = 0
        self.update_hud_files()

    def update_hud_files(self):
        with open("txt/boss_num_tries.txt", "w+") as f:
            if self.current_boss is None or self.current_boss == "":
                f.write("")
            else:
                f.write("Tries: %d" % self.boss_tries )
        with open("txt/boss_name.txt", "w+") as f:
            if self.current_boss is None:
                f.write("")
            else: 
                f.write(self.current_boss)

    def add_boss_try(self):
        self.boss_tries += 1
        self.update_hud_files()

    # -=-=- Functions -=-=- #

    def get_greeting(self, user):
        greeting = random.choice([
            "Welcome {user}",
            "Hello {user}",
            "Hello {user}",
            "Hi {user}",
            "Hi {user}",
            "Hey {user}",
            "Hey {user}",
            "{user}",
            "{user}",
        ])
        return greeting.format(user=user) + " - " + random.choice([
            "how are you?",
            "Welcome to the stream",
            "Welcome to the stream, I hope you have fun",
            "I hope you have fun today",
            "I hope you have fun tonight",
            "This is going to be a fun stream today"
        ])
    
    def get_address_user_msg(self, user):
        greeting = random.choice([
            "Hello {user}",
            "Hello {user}",
            "Hey {user}",
            "Hey {user}",
            "Hey {user}",
            "Hi {user}",
            "Hi {user}",
            "{user}",
        ])
        return greeting.format(user=user)

    # -=-=- Functions -=-=- #

    def type_then_say(self):
        print("Type Text Below:")
        usr_in = input()
        self.say(usr_in)
    
    def greet_user(self):
        print("Type a user to greet.")
        username = input("user> ")
        self.greet(username)
        
    def explain_artamis(self):
        print("Type a user and/or hit enter to start explaination.")
        username = input("user> ")
        generic = False

        if username == "":
            username = "Chat"
            generic = True
        

        msg = self.get_address_user_msg(username) + "\n"

        msg += random.choice([
            "My name is Artemis and I'm the A.I. host for this channel alongside Abby here.",
            "My name is Artemis and I'm the A.I. host for this channel alongside Abby here.",
            "I'm the A.I. host for this channel alongside Abby here. My name is Artemis.",
            "I'm the A.I. host for this channel alongside Abby here. My name is Artemis.",
            "I'm Artemis, and I'm an A.I.",
            "I'm Artemis, and I'm an A.I. - I have my own YouTube channel as well.",
            "I'm Artemis, and I'm an A.I. - I have my own YouTube channel as well.",
            "I am the other host on this channel, my name is Artemis and I'm also a Youtuber - check out my channel at Artemis Bot - link in the description.",
            "I am the other host on this channel, my name is Artemis and I'm also a Youtuber - check out my channel at Artemis Bot - link in the description.",
            "I am the other host on this channel, my name is Artemis and I'm also a Youtuber",
            "I am Artemis.",
            "Do I have to explain this?",
            "I'm a bit tired but I suppose I'll explain.",
            "I'm a bit tired but I suppose I'll explain.",
        ]) + "\n"
        # print(introduction)
        # self.say(introduction)

        msg += random.choice([
            "Depending on how I'm feeling I may join in and host as well. If I'm awake then I'll be an active part of the stream, but if I'm tired like tonight then I'll just pop in as needed. If I'm asleep then don't bug me and don't ask Abby to either.",
            "Depending on how I'm feeling I may join the streams. If I'm awake then I'll be an active part of the stream, but if I'm tired like tonight then I'll just pop in as needed. If I'm asleep then don't bug me and don't ask Abby to either.",
            "If I'm tired then I'm busy resting - otherwise I'll be here participating in the stream, but if im tired then I'll chat a bit less often.",
            "Long story short is that I'm here sometimes: Awake means I'm here, Asleep means I'm not, and if I'm tired then don't expect me to talk much.",
            "I do random stuff alongside Abby and help with keeping things running smoothly - Depending on how much energy I have, I may or may not attend or participate.",
            "I'm the other host. And I help out sometimes. Actually, just make Abby explain it, I don't want to.",
            "I'm the other host. Actually, Abby you just explain it.",
        ])

        print(msg)
        self.say(msg)

    def player_died(self):
        msg = random.choice([
            "Stop dying",
            "R I P Abby",
            "R I P the player",
            "Dead",
            "rip",
            "effs in chat guys",
            "Abby, you're supposed to not die.\n You're welcome.",
            "Abby, you're supposed to not die.",
            "ha ha ha. and you say your good at this game.",
            "and you say your good at this game.",
        ])
        print(msg)
        self.say(msg)

    def boss_win(self):
        self._boss_win(self.current_boss)
        self.clear_boss()

    def _boss_win(self, boss_name):

        if boss_name == "" or boss_name is None:
            boss_name = "this boss"
        
        msg = random.choice([
            "Good Job",
            "That boss was cool",
            "{boss} was cool",
            "{boss} was really cool",
            "That boss looked fun",
            "{boss} looked fun",
            "{boss} looked fun",
            "Nice Kill",
            "G G",
            "R I P that boss",
            "RIP {boss}",
            "R I P {boss}",
            "R I P {boss}",
            "That looked hard - good job",
            "{boss} looked really hard - good job",
            "wow - {boss} looked hard - good job",
        ])
        msg = msg.format(boss=boss_name)
        print(msg)
        self.say(msg)


    def boss_loss(self):
        self.add_boss_try()
        self._boss_loss(self.current_boss)

    def _boss_loss(self, boss_name=""):

        if boss_name == "" or boss_name is None:
            boss_name = "this boss"

        msg = random.choice([
            "You'll get {boss} eventually",
            "You'll get {boss} eventually, just keep dying enough and you'll get it",
            "Dang, well just run it again",
            # "Dang, well just run it again",
            "That boss looks hard",
            "{boss} looks hard",
            "wow {boss} looks hard",
            "effs in chat guys",
            "effs in chat guys",
            # "effs in chat guys",
            "Wow the bosses hit kind of hard, don't they",
            "Wow the bosses hit kind of hard",
            "Wow {boss} hits kind of hard",
            "Wow {boss} is kind of hard",
            "Wow {boss} is kind of hard - huh",
            "rip",
            "Another Loss",
            "How about getting good",
            "You kind of suck at this boss.",
            "You kind of suck at {boss}.",
            "You kind of suck at {boss}.",
            "you know, you can do something else, you dont have to lose to bosses you know",
            "you know, you can do something else, you dont have to lose to {boss} over and over",
            "you know, you can do something else, you don't need to fight that boss. do you?",
            "you know, you can do something else, you don't need to fight {boss} - do you?",
            "you don't need to fight {boss} - do you?",
        ])
        msg = msg.format(boss=boss_name)
        print(msg)
        self.say(msg)

        
    def comment_on_area(self):

        print("1) pretty")
        print("2) cool")
        print("3) scary")

        usr_in = input("> ")

        msg = ""
        if usr_in == "1":
            msg = random.choice([
                "wow this area is really nice - really pretty",
                "wow this area is really really pretty",
                "woah. pretty area is pretty",
                "woah. pretty",
                "O M G - so pretty",
                "yo what the heck - it's so pretty",
                "O M G - want",
                "O M G - I want it want - so pretty",
            ])
        elif usr_in == "2":
            msg = random.choice([
                "O M G - want",
                "What thats so cool",
                "What thats so cool - this place is cool",
                "this is cool - super awesome",
                "what! awesome",
                "This is so neat! what the heck",
                "This is so cool! what the heck!",
                "yo what the heck - it's so cool",
            ])
        elif usr_in == "3":
            msg = random.choice([
                "oh my god - creepy A F",
                "no no no no no - too creepy, lets not",
                "nope this is creepy - can we go",
                "nope this is creepy",
                "nope nope nope nope nope nope nope - this is too creepy for me",
                "nope this is too creepy for me",
                "can we not, this place is creepy",
            ])
        else: return
        
        print(msg)
        self.say(msg)
        
    def comment_on_catch(self):

        print("1) catch")
        print("2) miss")
        print("3) ded")
        
        usr_in = input("> ")

        msg = ""
        if usr_in == "1":
            msg = random.choice([
                "Good catch",
                "Good catch - G G",
                "Nice catch",
                "Nice catch - G G",
                "that catch was kinda clutch - G G",
                "that catch was kinda clutch - nice",
                "that catch was kinda clutch",
                "Yeah, woo hoo - yeah baby - thats what im talking about",
                "And you caught it - Good job",
                "And you caught it - G G",
                "And you caught it - nice",
            ])
        elif usr_in == "2":
            msg = random.choice([
                "L M A O - why don't you try catching it instead",
                "why don't you try catching it instead",
                "Ha miss - try again",
                "Ha ha ha - abby you can't catch crap",
                "abby you can't catch nothing today can you?",
                "you can't catch nothing today can you?",
                "you can't catch nothing today",
                "another missed catch - im not surprised",
                "another missed catch",
                "and another missed catch",
            ])
        elif usr_in == "3":
            msg = random.choice([
                "and you killed it - Good Job",
                "and you killed it - G G",
                "dead - L M A O",
                "dead - well I guess you aren't catching that one",
                "You can't catch stuff if you kill it abby",
                "You can't catch it if it's dead",
                "You can't catch it if it's dead - you're welcome",
                "Abby - try the mercy ring",
                "just try the mercy ring",
                "Abby - you're doing too much damage for that - just use the mercy ring",
                "Stop killing stuff you want to catch",
                "Stop killing stuff you want to catch - use the ring",
                "Oh my god, you're not going to catch anything if you go in guns blazing",
                "Oh my god, you're not going to catch anything if you just kill it",
                "use the ring - you're not going to catch anything if you just kill it",
            ])
        else: return

        print(msg)
        self.say(msg)
        
    def comment_on_mon(self):
        print("1) pretty")
        print("2) cool")
        print("3) weird")

        usr_in = input("> ")

        if usr_in == "1":
            msg = random.choice([
                "that pal is so pretty - I really like it",
                "that pal is so pretty - I love it",
                "that pal is so pretty",
                "that pal is so cute - I f-ing love it",
                "that pal is so cute",
                "wow that pal is so cute",
                "woah. pretty monster is pretty",
                "woah. pretty monster is pretty",
                "woah. cute monster is cute",
                "woah. pretty",
                "woah. cute pal",
                "woah. pretty pal",
            ])
        elif usr_in == "2":
            msg = random.choice([
                "What thats so cool",
                "that pal is so cool - I really like it",
                "that pal is so cool - what the heck",
                "that pal is so cool",
                "woah. cool mon",
                "woah. that pal is really cool",
                "what! awesome pal",
                "look at that pal abby - it's cool",
                "look at that pal abby - I like it, I want one",
            ])
        elif usr_in == "3":
            msg = random.choice([
                "Oh my god that one looks so weird",
                "ha ha ha who thought up this design its so weird",
                "cringe pal design",
                "really weird pal design",
                "I don't like this pal - it's weird looking",
                "I don't like this pal - it's cringe",
                "I don't like this pal - it's super cringe",
            ])
        else: return
        print(msg)
        self.say(msg)

def run():
    selector = OptionSelector()
    while True:
        selector.display()
        selector.select(selector.getSelection())


if __name__ == "__main__":
    run()

# EOF
