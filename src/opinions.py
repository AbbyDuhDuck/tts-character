
import random

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
        "This is going to be a fun stream tonight - I hope you have fun"
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

    msg += random.choice([
        "Depending on how I'm feeling I may join in and host as well. If I'm awake then I'll be an active part of the stream, but if I'm tired like tonight then I'll just pop in as needed. If I'm asleep then don't bug me and don't ask Abby to either.",
        "Depending on how I'm feeling I may join the streams. If I'm awake then I'll be an active part of the stream, but if I'm tired like tonight then I'll just pop in as needed. If I'm asleep then don't bug me and don't ask Abby to either.",
        "If I'm tired then I'm busy resting - otherwise I'll be here participating in the stream, but if im tired then I'll chat a bit less often.",
        "Long story short is that I'm here sometimes: Awake means I'm here, Asleep means I'm not, and if I'm tired then don't expect me to talk much.",
        "I do random stuff alongside Abby and help with keeping things running smoothly - Depending on how much energy I have, I may or may not attend or participate.",
        # "I'm the other host. And I help out sometimes. Actually, just make Abby explain it, I don't want to.",
        # "I'm the other host. Actually, Abby you just explain it.",
    ])

    return msg