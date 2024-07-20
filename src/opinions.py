#! /usr/bin/env python3

"""DocString"""

# -=-=- Imports & Globals -=-=- #

import random

from json import load as load_json, dump as dump_json

# import commands

# -=-=- Functions -=-=- #

# -=-=- Classes -=-=- #

class UserManager:
    def __init__(self) -> None:
        self.seen_users = []
        self.returning_users = []
        # self._ignored_users = ['KofiStreamBot']
        self._ignored_users = ["Abby Duck", "abbyduhduck", 'KofiStreamBot']
        self.user_aliases = {}
        self.special_user_data = {}

    # -=-=- #
    
    def can_greet_user(self, user) -> bool:
        return True\
            and user not in self.seen_users\
            and user not in self._ignored_users
    
    def can_greet(self, *users) -> bool:
        return bool(len(self.get_valid_users(*users)))

    def get_valid_users(self, *users):
        return [u for u in users if self.can_greet_user(u)]

    def add_user(self, *users):
        for user in users:
            if user not in self.seen_users:
                self.seen_users.append(user)

    def add_returning_user(self, *users):
        for user in users:
            if user not in self.returning_users:
                self.returning_users.append(user)
    
    def is_returning_user(self, user:str) -> bool:
        return user in self.returning_users
    
    def is_special_user(self, user:str) -> bool:
        return user in self.special_user_data
    
    def set_alias(self, user, alias):
        self.user_aliases[user] = alias

    def add_special_user_greeting(self, user, *msgs):
        if user not in self.special_user_data:
            self.special_user_data[user] = {
                'greetings': [],
            }
        # -=-=- #
        for msg in msgs:
            self.special_user_data[user]['greetings'].append(msg)

    def get_called_name(self, user) -> str:
        if user in self.user_aliases:
            return self.user_aliases[user]
        return user
    
    def get_names_string(self, *users) -> str:
        users = [self.get_called_name(u) for u in users]
        if len(users) == 1:
            return users[0]
        return ', '.join(users[:-1]) + f', and {users[-1]}'

    def commit_recall(self):
        """remember the users from today in the returning people list"""
        for user in self.seen_users:
            self.add_returning_user(user)
    
    # -=-=- #

    def get_greeting(self, *users):
        users = self.get_valid_users(*users)
        special_users = [u for u in users if self.is_special_user(u)]
        returning_users = [u for u in users if u not in special_users and self.is_returning_user(u)]
        new_users = [u for u in users if u not in [*special_users, *returning_users]]

        greetings = []

        if len(new_users):
            greetings.append(self._get_greeting(self.get_names_string(*new_users)))
        
        if len(returning_users):
            greetings.append(self._get_returning_greeting(self.get_names_string(*returning_users)))

        for user in special_users:
            greetings.append(self._get_special_greeting(self.get_called_name(user)))

        return greetings
    
    def _get_user_callout(self, user_str: str):
        msg = random.choice([
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
        return msg.format(user=user_str)

    def _get_greeting(self, user_str: str):
        return self._get_user_callout(user_str) + " - " + random.choice([
            "how are you?",
            "Welcome to the stream",
            "Welcome to the stream, I hope you have fun",
            "Welcome to the stream, I hope you have fun",
            "I hope you have fun today",
            "I hope you have fun tonight",
            "I hope you have fun tonight",
            "This is going to be a fun stream today",
            "This is going to be a fun stream tonight - I hope you enjoy it",
            "This is going to be a fun stream tonight - I hope you enjoy",
        ])
    
    def _get_returning_greeting(self, user_str: str):
        return f"Hello {user_str}, welcome back."
        pass
    
    def _get_special_greeting(self, user: str):
        if user not in self.special_user_data or len(self.special_user_data[user]['greetings']) == 0:
            return self._get_greeting(user)
        return random.choice(self.special_user_data[user]['greetings']).format(user=user)


    # -=-=- #

    def load(self, filepath: str):
        """load the internal state of known viewers"""
        with open(filepath, 'r') as file:
            obj = load_json(file)

        if 'seen_users' in obj: self.seen_users = obj['seen_users']
        if 'returning_users' in obj: self.returning_users = obj['returning_users']
        if '_ignored_users' in obj: self._ignored_users = obj['_ignored_users']
        if 'user_aliases' in obj: self.user_aliases = obj['user_aliases']
        if 'special_user_data' in obj: self.special_user_data = obj['special_user_data']

    def save(self, filepath: str):
        """save the internal state of known viewers"""
        obj = {}
        obj['seen_users'] = self.seen_users
        obj['returning_users'] = self.returning_users
        obj['_ignored_users'] = self._ignored_users
        obj['user_aliases'] = self.user_aliases
        obj['special_user_data'] = self.special_user_data

        with open(filepath, 'w') as file:
            dump_json(obj, file, indent=2)

    # -=-=- #

    def greet_command(self, command, args:str):
        users = [u.strip() for u in args.split(',')]
        if self.can_greet(*users):
            users = self.get_valid_users(*users)
            print(f"Greeting: {self.get_names_string(*users)}")
            command._out(f"Greeting: {self.get_names_string(*users)}")
            msgs = self.get_greeting(*users)
            for msg in msgs:
                command._say(msg)
            self.add_user(*users)
        

class OpinionManager:
    def __init__(self) -> None:
        pass

    def add_opinion(self):
        pass

    def get_opinion(self):
        pass

    def load_all(self, path: str):
        pass

    def load(self, filepath: str):
        pass

# -=-=- OLD -=-=- #

def get_greeting(user):
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
        "Welcome to the stream, I hope you have fun",
        "I hope you have fun today",
        "I hope you have fun tonight",
        "I hope you have fun tonight",
        "This is going to be a fun stream today",
        "This is going to be a fun stream tonight - I hope you have fun",
    ])

def get_address_user_msg(user):
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

def get_explain_artamis(user='chat'):    
    msg = get_address_user_msg(user) + "\n"
    msg += random.choice([
        "My name is Artemis and I'm the A.I. host for this channel alongside Abby here.",
        "My name is Artemis and I'm the A.I. co-host for this channel alongside Abby here.",
        "I'm the A.I. host for this channel alongside Abby here. My name is Artemis.",
        "I'm the A.I. co-host for this channel alongside Abby here. My name is Artemis.",
        "I'm Artemis, and I'm an A.I.",
        "I'm Artemis, and I'm an A.I. - I have my own YouTube channel as well.",
        "I'm Artemis, and I'm an A.I. - I have my own YouTube channel as well.",
        "I am the other host on this channel, my name is Artemis and I'm also a Youtuber - check out my channel at Artemis Bot - link in the description.",
        "I am the other host on this channel, my name is Artemis and I'm also a Youtuber - check out my channel at Artemis Bot - link in the About Section.",
        "I am the other host on this channel, my name is Artemis and I'm also a Youtuber - check out my channel at Artemis Bot - link in the About Section.",
        "I am the other host on this channel, my name is Artemis and I'm also a Youtuber",
        "I am Artemis.",
        "Do I have to explain this?",
        "Do I have to explain this? Alight then",
        "I'm a bit tired but I suppose I'll explain.",
        "I'm a bit tired but I suppose I'll explain.",
    ]) + "\n"

    msg += random.choice([
        "Depending on how I'm feeling I may join in and host as well. If I'm awake then I'll be an active part of the stream, but if I'm tired like tonight then I'll just pop in as needed. If I'm asleep then don't bug me and don't ask Abby to either.",
        "Depending on how I'm feeling I may join the streams. If I'm awake then I'll be an active part of the stream, but if I'm tired like tonight then I'll just pop in as needed. If I'm asleep then don't bug me and don't ask Abby to either.",
        "If I'm tired then I'm busy resting - otherwise I'll be here participating in the stream, but if im tired then I'll chat a bit less often.",
        "Long story short is that I'm here sometimes: Awake means I'm here, Asleep means I'm not, and if I'm tired then don't expect me to talk much.",
        "Long story short is that I'm here sometimes: Awake means I'm here, Asleep means I'm not, and if I'm tired then don't expect me to talk much.",
        "I do random stuff alongside Abby and help with keeping things running smoothly - Depending on how much energy I have, I may or may not attend or participate.",
        "I'm the other host. And I help out sometimes. Actually, just make Abby explain it, I don't want to.",
        # "I'm the other host. Actually, Abby you just explain it.",
    ])

    if user.lower() == 'chat':
        msg += ' ' + random.choice([
            "",
            "Anyway - I hope you all have fun",
            "Anyway - I hope you all enjoy the stream",
        ])
    else:
        msg += ' ' + random.choice([
            "",
            "Anyway {user} - I hope you have fun today",
            "Anyway {user} - I hope you enjoy the stream",
            "Anyway - I hope you have fun today {user}",
            "Anyway - I hope you enjoy the stream",
            # "Anyway - I hope you have fun today",
        ])

    return msg.format(user=user)


if __name__ == '__main__':
    users = UserManager()
    users.add_user("Abby Duck", "AbbyDuhDuck")
    users.add_returning_user("Returning Person")
    users.add_special_user_greeting("Special Person", 
        "Hello {user} - how special to have you here.",
        "Hello {user} - its awesome to see you here tonight.",
    )

    # users.set_alias("Some Username", "The anon")
    users.set_alias("Returning Person", "The one who returns")
    # users.set_alias("Special Person", "The one who is special")

    u = ['Abby Duck', "Some Username", "Special Person", "Returning Person"]
    print(users.can_greet(*[]))
    print(users.can_greet(*u))
    for greeting in users.get_greeting(*u):
        print(greeting)

    users.add_user(*u)
    users.save("./settings/users.data")

    users = UserManager()
    users.load("./settings/users.data")
    print(users.can_greet(*u))
    for greeting in users.get_greeting(*u):
        print(greeting)
