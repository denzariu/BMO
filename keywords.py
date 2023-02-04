import random
import thefuzz.fuzz
import json

### Init values
FILE = open("/home/pi/Desktop/BMO/user_data.json")
JSON = json.load(FILE)
FILE.close()

name                    = JSON['name']
current_temperature     = JSON['current_temperature']
current_sky             = JSON['current_sky']
tomorrow_temperature    = JSON['tomorrow_temperature']
tomorrow_sky            = JSON['tomorrow_sky']
current_city            = JSON['current_city']

print('\n\nKeywords NAME = ' + name)
print('\n\nKeywords current_temperature = ' + str(current_temperature))

keywords = {
    'greetings':
        {
            'general': ["hi", "hello", 'hi', 'hello', 'hey', 'howdy', 'hi how are you', 'whats up', 'hey there', 'hello there', 'hey there', 'hi there'],
            'morning': ["good morning"],
            'night': ["good night"]
        },
    'goodbye':
        {
            'general': ['bye', 'goodbye', 'see later', 'see you', 'good bye']
        },
    
    'search':
        {
            'general': ['search']
        },

    'reddit':
        {
            'general': ['reddit']
        },
    
    'date':
        {
            'general': ['date', 'day']
        },
    
    'time':
        {
            'general': ['time']
        },
    
    'jokes':
        {
            'general': ["joke", "jokes"]
        },
    'note_write':
        {
            'general': ['write note']
        },

    'note_read':
        {
            'general': ["read note"]
        },
    
    'math':
        {
            'general': ["math", "mathematics", "maths"]
        },
    'game':
        {
            'general': ["game", "videogame"]
        },
    'update_info':
        {
            'update': ['update']
        },
    'facts':
        {
            'fun': ["fun fact", "fact"]
        },
    'birthday':
        {
            'general': ["my birthday"]
        },
    'translate':
        {
            'general': ["translate"]
        },
    'weather':
        {
            'today': ["current temperature", "today weather", "weather"],
            'tomorrow': ["weather tomorrow"]
        },
    'song':
        {
            'play_song': ["song"]
        },

    'others_sleep':
        {
            'sleep': ["sleep", "sleepy", "tired", "nap"]
        },

    'others_happy':
        {
            '': [""]
        },

    'others_blush':
        {
            'pretty': ["you look pretty", "you look beautiful"]
        },
    'covid':
        {
            'cases_today': ["covid cases today", "active covid today", "covid"],
            'total_cases': ["covid all time", "total covid cases", "total covid"]
        }
}

responses = {
    'greetings':
        {
            'general': ["Have a good day " + name + "!",
                        "Hi! Feels like today will be a great day, " + name + "!",
                        "Hello there!"],

            'morning': ["Good morning " + name + "!",
                        "Hello " + name + "! Have a great morning!"],

            'night': ["Good night " + name + "!",
                      "Good night " + name + "! I'd go to rest as well but I don't think I can!"]
        },
        
    'goodbye':
        {
            'general': ["Goodbye " + name + "!",
                      "Goodbye " + name + "! I'll rest with you."]
        },
    
    'search':
        {
            'general': ['Alright.']
        },
    
    'reddit':
        {
            'general': ['Connecting to Reddit...']
        },

    'date':
        {
            'general': ['NOT SET']
        },

    'time':
        {
            'general': ['NOT SET']
        },

    'jokes':
        {
            'general': ["What did the 0 say to the 8? Nice belt.",
                        "The present, the past and the future walk into a bar. It was pretty tense."]
        },
    
    'note_write':
        {
            'general': ['Taking a note...']
        },
    
    'note_read':
        {
            'general': ["You wrote the following note:"]
        },
    
    'math':
        {
            'general': ["Let's do some math!"]
        },
    
    'update_info':
        {
            'update': ["Ok, I'll update your credentials."]
        },
    
    'game':
        {
            'general': ["Let's play a game!",
                        "Game on."]
        },

    'facts':
        {
            'fun': ['A single strand of Spaghetti is called a “Spaghetto”.',
                    "At birth, a baby panda is smaller than a mouse.",
                    "If you heat up a magnet, it will lose its magnetism.",
                    "The collective group of lemurs is called a conspiracy.",
                    "While dinosaurs roamed the earth, they lived on every continent including Antarctica.",
                    'The word “kimono”, literally means a “thing to wear”. Ki is “wear”, and mono is “thing”.',
                    "Did you know that elephants can't jump?",
                    "It’s impossible to hum while holding your nose... just try it!",
                    "Cats have fewer toes on their back paws, but they still don't want them touched!",
                    "Turkeys can blush, and so can I!",
                    "A bolt of lightning is five times hotter than the sun, but no one is hotter than me!",
                    "It took nearly 1500 years to build Stonehenge, and nearly twice as much to build me.",]
        },
    'birthday':
        {
            'general': ["Happy birthday to you, " + name + "!"]
        },
    'translate':
        {
            'general': ["I'll translate!"]
        },
    'weather':
        {
            'today': [
                "The current temperature in " + current_city + " is " + str(current_temperature) + " degrees Celsius. Prepare for " + current_sky + " outside."],
            'tomorrow': [
                "The weather in " + current_city + " tomorrow will be " + tomorrow_temperature + " degrees Celsius. Prepare for " + tomorrow_sky + " outside."]
        },

    'song':
        {
            'play_song': ["So you want me to play a song..."]
        },

    'others_sleep':
        {
            'sleep': ["Maybe a nap would help.",
                      "A nap would be great right now, " + name + "!"]

        },

    'others_happy':
        {
            '': [""]
        },

    'others_blush':
        {
            'pretty': ["Oh, well, that was unexpected...",
                       "Thank you! You look stunning as well, " + name + '!']
        },
    'covid':
        {
            'cases_today': [""],
            'total_cases': [""]
        }
}

emotion = {
    'greetings': 'smile',
    
    'goodbye': 'sleep',

    'search': 'smile',

    'reddit': 'smile',

    'date': 'happy',

    'time': 'smile',

    'note_write': 'smile',
    
    'note_read': 'smile',
    
    'jokes': 'happy',

    'math': 'angry',

    'game': '',

    'update_info': '',
    
    'weather': 'weather',

    'facts': 'happy',

    'birthday': 'happy',

    'translate': 'translate',

    'song': 'song',

    'others_sleep': 'sleep',

    'others_happy': 'happy',

    'others_blush': 'blush',
    
    'covid': 'angry'

}


def reply(voiceInput, voiceInputNonToken):
    global keywords
    global responses

    response = ''
    _category = ''
    _subcategory = ''
    maxSimilarity = 0

    _string = ''
    __string = ''
    

    for category in keywords:
        for subcategory in keywords[category]:

            maxSimilarityLocal = 0

            for string in keywords[category][subcategory]:
                similarityLocal = thefuzz.fuzz.UQRatio(voiceInputNonToken, string)

                sharedWords = len(list(set(voiceInput) & set(string.split())))
                stringLen = len(string.split())

                if sharedWords == stringLen:
                    similarityLocal = min((similarityLocal * 1.35), 100)

                # if any(word in voiceInputNonToken for word in string):

                if maxSimilarityLocal <= similarityLocal:
                    maxSimilarityLocal = similarityLocal
                    _string = string

            if maxSimilarity <= maxSimilarityLocal:
                maxSimilarity = maxSimilarityLocal
                _category = category
                _subcategory = subcategory
                __string = _string

    response = responses[_category][_subcategory]
    print(__string, maxSimilarity)

    return [response[random.randint(0, response.__len__() - 1)], _category, _subcategory, emotion[_category]]


