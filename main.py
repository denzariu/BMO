import audiomath; #audiomath.RequireAudiomathVersion( '1.12.0' )
import speech_recognition as SR  # NB: python -m pip install SpeechRecognition
import pyttsx3

voice_engine = pyttsx3.init()
#voices = voice_engine.getProperty('voices')
#voice_engine.setProperty('voice', voices[1].id)
voice_engine.setProperty('rate', 100)  

r = SR.Recognizer()

# Features
import features.requests.covid_cases as covid_data 

# Info about stuff
import wikipedia

# Summarizer - not that good
# from gensim.summarization import summarize

# Math
import math_parser

# Shazam - not really working as expected
#from ShazamAPI import Shazam

# Translate
from translate_text import translate_it

# JSON
import json

# Sys
from sys import stdout

from time import sleep

# Jokes
import pyjokes

# Added OS commands
from os import system, path

import time
import datetime

# Subprocess Control
import subprocess

# Requests - for location
import requests

# Random
import random

# Joycon
from evdev import InputDevice, ecodes

# Bluetooth
# syscall at the moment

# Play Youtube Audio
import play_audio as AUDIO

# Weather
import python_weather
client = python_weather.Client()

# Reddit API
import urllib.request
import praw

# Variables
reddit       = ''
weather      = ''
gifPlayer    = ''
gifPlayer_b  = ''
response     = ''
responseGIF  = ''
_responseGIF = ''
skip_everything = False

testing       = False
input_test    = ['weather today']
input_nr      = 0
gamepad       = None

# Joystick Button Codes
UP    = 306
DOWN  = 305
LEFT  = 304
RIGHT = 307
HOME  = 317
ESC   = 312

# Voice

SELECTED_VOICE    = ''
SELECTED_MODIFIER = ''
SELECTED_THEME    = ''
SELECTED_COLOR    = ''

BMO_wakeup   = ['hey', 'hello', 'listen']
BMO_shutdown = ['shutdown', 'shut down', 'close', 'off']
BMO_voice = ' pitch +540 tempo -s 1.70 speed 0.82 treble +6 gain -B +1'
BMO_greetings = []

############# Don't change ############
class BMO_Hears( SR.AudioSource ): # descent from AudioSource is required purely to pass an assertion in Recognizer.listen()
    def __init__( self, device=None, chunkSeconds=1024/44100.0 ):  # 1024 samples at 44100 Hz is about 23 ms
        self.recorder = None
        self.device = device
        self.chunkSeconds = chunkSeconds
    def __enter__( self ):
        self.nSamplesRead = 0
        self.recorder = audiomath.Recorder( audiomath.Sound( 30, nChannels=1 ), loop=True, device=self.device )
        # Attributes required by Recognizer.listen():
        self.CHUNK = audiomath.SecondsToSamples( self.chunkSeconds, self.recorder.fs, int )
        self.SAMPLE_RATE = int( self.recorder.fs )
        self.SAMPLE_WIDTH = self.recorder.sound.nbytes
        return self
    def __exit__( self, *blx ):
        self.recorder.Stop()
        self.recorder = None
    def read( self, nSamples ):
        sampleArray = self.recorder.ReadSamples( self.nSamplesRead, nSamples )
        self.nSamplesRead += nSamples
        return self.recorder.sound.dat2str( sampleArray )
    @property
    def stream( self ): # attribute must be present to pass an assertion in Recognizer.listen(), and its value must have a .read() method
        return self if self.recorder else None


######################## \ #########################

def BMO_listen():

    ############## INITS ################
    global input_nr
    global input_test
    global responseGIF
    global _responseGIF
    global gifPlayer
    global weather
    global gamepad
    global reddit
    
    ############## GREET ################
    system('play /home/pi/Desktop/BMO/Assets/BMO_sound.mp3 pitch -900 tempo 1.4 rate 48k speed 0.85')
    speak(BMO_greetings[random.randint(0, len(BMO_greetings) - 1)], '')
    #system("gtts-cli \""+ BMO_greetings[random.randint(0, len(BMO_greetings) - 1)] +"\" | play -t mp3 -" + BMO_voice)
    
    ########## GET VOICE INPUT ##########
    with BMO_Hears() as source:
    
        if testing is False:
            print('\nSay something to the %s...' % source.__class__.__name__) 
            # Recognize voice:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            print('\nOKI, Recorded!\n')
    try:
        
        if testing is False:
            voiceInput = r.recognize_google(audio)
        else:
            voiceInput = input_test[input_nr]
            input_nr = input_nr + 1
            script = "gtts-cli \""+ "I've heard: " + voiceInput +"\" | play -t mp3 -" + BMO_voice

        print(voiceInput)
        skip_everything = False

    except Exception as e:
        speak('\nI didn\'t catch that.\n', '')
        print(e)
        skip_everything = True


    if skip_everything is False:
        
        
        ################## Input Processing ################
        
        ### Inits
        response = "I couldn't understand"
        voiceInput = voiceInput.lower()
        
        ### Delete a sequence of words
        wordsToDelete = ['can you', 'could you', 'do you']
        for word in wordsToDelete:
            voiceInput = voiceInput.replace(word, " ")
        print("\nVOICE INPUT AFTER FILTERING 1: " + voiceInput + "\n")
        
        ### Delete words in token
        wordsToDelete = ["something", "should", "let's", "what", "where", "which", "how", "when", "who", "is", "are", "makes", "made", "make", "did", "do", "to", "the", "of", "from", "against", "and", "or","you", "me", "we", "us", "your", "my", "mine", 'yours', "could", "would", "may", "might", "let", "possibly", 'tell', "give", "told", "gave", "know", "knew", 'a', 'am', 'an', 'i', 'like', 'has', 'have', 'need', 'will', 'be', "this", 'that', "for"]
        voiceInputNonToken = [" ".join([w for w in voiceInput.split() if not w in wordsToDelete])]
        voiceInputNonToken = voiceInputNonToken[0]
        voiceInput = voiceInputNonToken.split()
        print("\nVOICE INPUT AFTER FILTERING 2: " + voiceInputNonToken + "\n")
        
        
        ################## Recognition part #################
        
        [response, response_category, response_subcategory, responseGIF] = reply(voiceInput, voiceInputNonToken)


        #################### GIF PLAY #######################

        # Display the current gif response if it differs from the last one
        # If it does, kill the last subprocess
        if _responseGIF != responseGIF:
            if _responseGIF != '' and responseGIF != '':
                gifPlayer.terminate()
                print("Process deleted.")
            else:
                print("Process couldn't be closed.")

            gifPlayer = subprocess.Popen(['/usr/bin/python3.9', '/home/pi/Desktop/BMO/play_GIF.py', 'BMO_' + responseGIF + 'T', 'gif', SELECTED_COLOR])
            _responseGIF = responseGIF


        ################### Play sound ######################
        
        if response_category == 'facts' or response_category == 'birthday':
            speak(response, '--slow')

        elif response_category == 'jokes':
            speak(pyjokes.get_joke(), '--slow')

        elif response_category == 'time':
            time = datetime.datetime.now().strftime('%H:%M')  # %H:%M for 24 hr format 
            speak('The current time is ' + time, '--slow')
            print(time)
        elif response_category == 'date':
            time = datetime.datetime.now()
            day = time.strftime("%d") + ' '
            month = time.strftime("%B") + ', '
            year = time.strftime("%Y")
            day_of_week = time.strftime("%A")
            speak('Current date is ' + day + month + year + " of course. It's also " + day_of_week + '.', '')

        elif response_category == 'update_info':
            #gifPlayer.terminate()
            init_user(True)
        else:
            speak(response, '')


        ################ TEST SPECIAL REQUESTS ##############


        ################ SONG ##############
        if response_category == 'song':
            
            speak("What\'s the name of the song you\'d like to hear?", '')

            with BMO_Hears() as source:
                try:
                    #r.adjust_for_ambient_noise(0.75)
                    audio = r.listen(source)
                    search_song = r.recognize_google(audio)
                    print('\nI\'ve heard: "%s"\n' % search_song)

                except Exception as e:
                    print(e)
                    speak("I've heard nothing.", '')
                    print('\nI\'ve heard nothing.\n')
                    
                speak("It might take a bit to find it...", '')
                [link, title] = AUDIO.get_link(search_song)
                show_text(title)
                AUDIO.play_stream(link, gamepad)

        ########### REDDIT POSTS ###########
        elif response_category == 'reddit':
            speak('Search for a subreddit.', '')
            
            # Keyboard
            from keyboard import set_field, display_keyboard

            set_field('subreddit')
            display_keyboard(SELECTED_THEME)
            [JSON, FILE] = get_JSON()
            subreddit = reddit.subreddit(JSON['subreddit'])
            hot_posts_subreddit = subreddit.hot(limit=5)
            speak('Here are the hottest posts on the ' + JSON['subreddit'] + ' subreddit:', '')
            for post in hot_posts_subreddit:
                
                print(post.url)
                post_is_image = False
                if post.url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
                    post_is_image = True
                
                    try:
                        url = post.url
                        urllib.request.urlretrieve(url, "Desktop/BMO/Assets/Reddit/images/reddit.jpg")
                        post_image = subprocess.Popen(['/usr/bin/python3.9', '/home/pi/Desktop/BMO/play_GIF.py', 'Reddit/images/reddit', 'jpg', SELECTED_COLOR])
                    except Exception as e:
                        print(e)
                        print('Picture wasn\'t downloaded.')
                speak(post.title, '')

                if post_is_image is False:
                    speak(post.selftext, '')
                    sleep(2)
                else:
                    if post.url.endswith(('.gif')):
                        sleep(10)
                    else:
                        sleep(5)
                    post_image.terminate()
                

        ############ WIKI SEARCH ###########
        elif response_category == 'search':
            try:
                speak("What's the subject of your search?", '')
                
                with BMO_Hears() as source:
                    try:
                        audio = r.listen(source, timeout=2)
                        topic = r.recognize_google(audio)
                        print('\nI\'ve heard: "%s"\n' % topic)
                        
                        try:
                            # perfrom the search
                            topic_suggested = wikipedia.search(topic, results = 1)
                            print('Suggested topic: ' + topic_suggested[0])
                            speak(wikipedia.summary(topic_suggested, auto_suggest = False, sentences = 1), '')
                            print("\nSuccessfully Searched")
                          
                        except Exception as e:
                            print (e)
                            print("An Unknown Error Occurred When Searching")
                       

                    except Exception as e:
                        print(e)
                        speak("I didn't catch that.", '')
                
              
            except:  
                # printing error message
                print("An Error Occurred During Search")


        ############ TRANSLATE ############
        elif response_category == 'translate':

            speak("To which language would you want to translate?", '')
            lang = ''
            text = ''
            with BMO_Hears() as source:
                try:
                    audio = r.listen(source, timeout=2)
                    lang = r.recognize_google(audio)
                    print('\nI\'ve heard: "%s"\n' % lang)

                except Exception as e:
                    print(e)
                    speak("I didn't catch that.", '')

            speak("What do you want to translate?", '')
            with BMO_Hears() as source:
                try:
                    #time.sleep(1.5)  ### Era 2.5, de testat
                    print('\nSpeak now:\n')
                    audio2 = r.listen(source, timeout=4)
                    text = r.recognize_google(audio2)
                    print('\nI\'ve heard: "%s"\n' % text)
                    [answer, country] = translate_it(lang, text)
                    if country == '':
                        speak(answer, '')
                    else:
                        speak("The translation would be: ", '')
                        speak(answer, '--lang=' + country + ' --slow')
                except Exception as e:
                    print(e)
                    speak("I didn't catch that.", '')
                    
            
        ################ PLAY A GAME ###############

        elif response_category == 'game':
            try_to_connect_joystick()
            gameWindow = subprocess.Popen(['chocolate-doom','-iwad', '/home/pi/Desktop/BMO/Games/DOOM/DOOM1.WAD'])

            for event in gamepad.read_loop():
                if event.value == 0:
                    print(event.code)
                    if event.code == 312:
                            gameWindow.kill()
                            break
            
        ###################### Math ######################## 
        
        elif response_category == 'math':
            speak("I can do addition, subtraction, multiplication, and division. What would you like to know?", '')
            it_worked = False
            with BMO_Hears() as source:
                try:
                    audio = r.listen(source)
                    math = r.recognize_google(audio)
                    show_text('"' + math + '"')
                    it_worked = True
                except Exception as e:
                    print(e)
                    speak("I've heard nothing.", '')

                if it_worked == True:
                    try:
                        math_question = math_parser.text2int(math)
                        print(math_question)
                        math_answer = math_parser.do_math(math_question)
                        speak('The answer is ' + math_answer, '')
                        
                    except Exception as e:
                        print(e)
                        speak("The equation is incorrect. I've heard: " + math, '')

        ####################### NOTES #########################

        elif response_category == 'note_write':

            speak("Shoot!", '')
            with BMO_Hears() as source:
                try:
                    audio = r.listen(source, timeout=5)
                    text = r.recognize_google(audio)
                    print('\nI\'ve heard: "%s"\n' % text)
                    FILE = open("/home/pi/Desktop/BMO/Notes/note.txt", "w")
                    FILE.write(text)
                    FILE.close()
                    speak('Saved!', '')
                    
                except Exception as e:
                    print(e)
                    speak("I didn't catch that.", '')

        elif response_category == 'note_read':
            with BMO_Hears() as source:
                try:
                    with open('/home/pi/Desktop/BMO/Notes/note.txt', 'r') as FILE:
                        text = FILE.read()
                        FILE.close()
                    speak(text, '')
                    
                except Exception as e:
                    print(e)
                    speak("I didn't catch that.", '')
                    
                    
        ####################### COVID #########################
        elif response_category == 'covid':
            speak("Cases for which country?", '')
            with BMO_Hears() as source:
                try:
                    audio = r.listen(source, timeout=5)
                    country = r.recognize_google(audio)
                    if response_subcategory == 'cases_today':
                        cases = covid_data.cases_of_covid(country)
                        speak(f"There's been {cases} Covid cases in {country} today.", '')
                    elif response_subcategory == 'total_cases':
                        cases = covid_data.cases_of_covid_alltime(country)
                        speak(f"There's been {cases} Covid cases in {country} until now.", '')
                    
                except Exception as e:
                    print(e)
                    speak("I didn't catch that.", '')
            
                
            
        ################### Joycon Control ##################

        ########## TO DO: CALL FUNCTION FROM MAIN LOOP TO PREVENT STACK OF ##########
        # try:
        #     if gamepad is None:
        #         print('Trying to connect')
        #         try_to_connect_joystick()
        #     print('Joystick connected')
            
        #     for event in gamepad.read_loop():
        #         if event.value == 0:
        #             print(event.code)
        #             if event.code == HOME:
        #                     return BMO_listen()
        #             elif event.code == ESC:
        #                     if gifPlayer != '': 
        #                         gifPlayer.terminate()
        #                     gifPlayer_b.terminate()
        #                     return
        # except Exception as e:
        #     print('Joystick not connected')
        #     print('Exception: ' + e)
        #     try_to_connect_joystick()
        #     for event in gamepad.read_loop():
        #         if event.value == 0:
        #             print(event.code)
        #             if event.code == HOME:
        #                     return BMO_listen()
        #             elif event.code == ESC:
        #                     if gifPlayer != '':
        #                         gifPlayer.terminate()
        #                     gifPlayer_b.terminate()
        #                     return

        
    while True:
        with BMO_Hears() as source:
            try:
                audio = r.listen(source, timeout=5)
                text_rec = r.recognize_google(audio)
                print('\nI\'ve heard: "%s"\n' % text_rec)
                if any(word in text_rec.split() for word in BMO_wakeup):
                    return BMO_listen()
                if any(word in text_rec.split() for word in BMO_shutdown):
                    try:
                        gifPlayer.terminate()
                    except:
                        print("No GIF player playing. (except the main one)")
                    return
                    
            except Exception as e:
                print(e)
                show_text('Tell me a wake up phrase.')
                #speak("D'oh.", '')

    
######################## / #########################

#################### JOYSTICK ######################

def try_to_connect_joystick():

    global gamepad
    print('Waiting for joystick connection.')

    show_message = True
    connected = False
    while connected == False:
        gamepad = connect_joystick()
        if gamepad is not None:
            print('Joystick connected')
            speak("The joystick is connected.", '')
            connected = True
        else:
            if show_message == True:
                speak("Please connect your joystick.", '')
                show_message = False

            #AUTOCONNECT
            try:
                import bluetooth_wrapper
                
            except:
                print("Waiting for input on joystick")
            

def connect_joystick():

    print('---')
    try:
        event = subprocess.check_output("cat /proc/bus/input/devices | grep -Poz '(\"Joy-Con \(L\)\"[\s\S]+?)\Kevent\d+'", shell=True, encoding='UTF-8', universal_newlines=True)
        event = event[0:6]
        print('Connected to: ' + event)
        if event != '':
            return InputDevice('/dev/input/' + event)
        else:
            print('Joystick not found!')
            return None
            
    except Exception as e:
        print(e)
        print('Joystick not found - Exception')
        return None    
    


################## TEXT ON SCREEN ##################
def show_text(TXT):
    FILE = open("/home/pi/Desktop/BMO/text_output.o", "w")
    FILE.write(TXT)
    FILE.close()

# e.g. args = '--slow' 
def speak(TXT, args):
    show_text(TXT)
    
    if SELECTED_VOICE == '0':
        if SELECTED_MODIFIER == '0':
            BMO_voice = ' pitch +540 tempo -s 1.70 speed 0.82 treble +6 gain -B +1'
        elif SELECTED_MODIFIER == '1':
            BMO_voice = ''
        system('gtts-cli "' + TXT + '" ' + args + ' | play -t mp3 -' + BMO_voice)
    elif SELECTED_VOICE == '1' or SELECTED_VOICE == '':
        voice_engine.say(TXT)
        voice_engine.runAndWait()
        voice_engine.stop()
    elif SELECTED_VOICE == '2':
        system('echo "' + TXT + '" | festival --tts')
        
    #if SELECTED_VOICE == 0:
    #system('gtts-cli "' + TXT +'" '+ args +' | play -t mp3 -' + BMO_voice)
    ##system('echo "' + TXT + '" | festival --tts') 
    #elif SELECTED_VOICE == 1:
    #    voice_engine.say('This is my voice in ' + voice.id + '. Do you like it?')
    #    engine.runAndWait()

################### WIFI CONNECT ###################

def create_wifi(SSID, password):
  config_lines = [
    '\n',
    'network={',
    '\tssid="{}"'.format(SSID),
    '\tpsk="{}"'.format(password),
    '\tkey_mgmt=WPA-PSK',
    '}'
  ]

  config = '\n'.join(config_lines)
  print(config)

  with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+") as wifi:
    wifi.write(config)

  print("Wifi config added")

####################### THEME ######################
def theme_select(fetch_json):

    global SELECTED_THEME
    global SELECTED_COLOR

    if fetch_json:
        [JSON, FILE] = get_JSON()
        SELECTED_THEME    = JSON['theme']
    
    if SELECTED_THEME == 'lightgreen':
        SELECTED_COLOR = '#90c49f'
    elif SELECTED_THEME == 'rosepurple':
        SELECTED_COLOR = '#c490b5'
    elif SELECTED_THEME == 'autumnorange':
        SELECTED_COLOR = '#f9b168'
    else:
        SELECTED_COLOR = '#90c49f'
    
####################### JSON #######################
    
def write_JSON(JSON):
    FILE = open("/home/pi/Desktop/BMO/user_data.json", "w")
    json.dump(JSON, FILE)
    FILE.close()

def get_JSON():
    FILE = open("/home/pi/Desktop/BMO/user_data.json", "r")
    JSON = json.load(FILE)
    FILE.close()
    return [JSON, FILE]

#def get_user_data(JSON, name):
#    return JSON[name]
    
################### User Data Init #################


def init_user(update_info):

    global BMO_greetings
    global SELECTED_VOICE
    global SELECTED_MODIFIER
    global SELECTED_THEME
    global SELECTED_COLOR
    global gifPlayer_b
    global reddit

    
    # Read JSON
    [JSON, FILE] = get_JSON()
    JSON_theme          = JSON['theme']
    JSON_voice_modifier = JSON['voice_modifier']
    JSON_voice          = JSON['voice']
    JSON_name           = JSON['name']
    JSON_age            = JSON['age']
    JSON_current_city   = JSON['current_city']
    JSON_reddit_id      = JSON['reddit']['client_id']
    JSON_reddit_secret  = JSON['reddit']['client_secret']
    JSON_reddit_user    = JSON['reddit']['username']
    JSON_reddit_pw      = JSON['reddit']['pw']
    JSON_reddit_agent   = JSON['reddit']['user_agent']
    
    # Keyboard module
    from keyboard import set_field, display_keyboard
    # Weather module
    from features.weather.weather import weather_in_city
    # Reddit module
    reddit = praw.Reddit(client_id=JSON_reddit_id, client_secret=JSON_reddit_secret, username=JSON_reddit_user, password=JSON_reddit_pw, user_agent=JSON_reddit_agent)

    gifPlayer_b = subprocess.Popen(['/usr/bin/python3.9', '/home/pi/Desktop/BMO/play_GIF.py', 'BMO_smileT', 'gif', SELECTED_COLOR])    

    # Greet user
    if JSON_name == '' or JSON_age == '' or JSON_current_city == '':
        speak("Hello! I am now your personal assistant. I'd like to know a few things about you so we can get started.", '')
        sleep(1)
    
    print('!!THEME: ' + JSON_theme)
    # Check for voice & theme preference
    if JSON_theme == '' or JSON_voice == '' or JSON_voice_modifier == '' or update_info is True:
        from theme_select import display_menu
        speak("How should I look and sound?", '')
        display_menu(JSON_theme, JSON_voice, JSON_voice_modifier)
        
    # Update the voice & theme & location
    [JSON, FILE] = get_JSON()
    SELECTED_VOICE    = JSON['voice']
    SELECTED_MODIFIER = JSON['voice_modifier']
    SELECTED_THEME    = JSON['theme']
    IPSTACK_KEY       = JSON['ipstack_key']
    WEATHER_KEY       = JSON['weather_key']
    theme_select(fetch_json=False)

    # Weather fetch lat / long / city
    send_url = "http://api.ipstack.com/check?access_key=" + IPSTACK_KEY
    geo_req = requests.get(send_url)
    geo_json = json.loads(geo_req.text)
    latitude = geo_json['latitude']
    longitude = geo_json['longitude']
    city = geo_json['city']
    
    weather = weather_in_city(latitude, longitude, WEATHER_KEY)

    if JSON_theme != SELECTED_THEME:
        gifPlayer_b.terminate()
        gifPlayer_b = subprocess.Popen(['/usr/bin/python3.9', '/home/pi/Desktop/BMO/play_GIF.py', 'BMO_smileT', 'gif', SELECTED_COLOR])
   
    ###################### POPULATE JSON ########################
    
    if JSON_name == '' or update_info is True:
        speak("What's your name?", '')
        sleep(1)
        set_field('name')
        display_keyboard(SELECTED_THEME)

    if JSON_age == '' or update_info is True:
        speak("How old are you?", '')
        sleep(1)
        set_field('age')
        display_keyboard(SELECTED_THEME)

    # Check if there's an active network connection

    wifi_ip = subprocess.check_output(['hostname', '-I'])
    print(wifi_ip)
    if wifi_ip != b'\n':
        print('Connected to WIFI')
    else:
        print('Not connected to WIFI...')
        print('Trying to connect...')

        speak("Please enter WiFi's name", '')
        set_field('wifi_ssid')
        sleep(1)
        display_keyboard(SELECTED_THEME)

        speak("Now please enter the password", '')
        set_field('wifi_pw')
        sleep(1)
        display_keyboard(SELECTED_THEME)

        [JSON, FILE]      = get_JSON()

        create_wifi(JSON['wifi_ssid'], JSON['wifi_pw'])
        system('wpa_cli -i wlan0 reconfigure')

        speak("Please wait 10 seconds so I can ready up my voice", '')
        time.sleep(12)

        wifi_ip2 = subprocess.check_output(['hostname', '-I'])
        print(wifi_ip2)
        if wifi_ip2 != b'\n':
            print('Connected to WIFI')
            speak('Alright, Wifi connected!', '')
        else:
            print('Still not connected. Restart the device.')
            speak('Try to restart', '')

    
    [JSON, FILE]      = get_JSON()

    if update_info is False:
        [JSON, FILE]      = get_JSON()
        try: 
            # Write to JSON
            JSON['current_city']         = city
            JSON['current_temperature']  = weather[0]
            JSON['current_sky']          = weather[2]
            #JSON['tomorrow_temperature'] = str(weather.forecasts[1].temperature)
            #JSON['tomorrow_sky']         = str(weather.forecasts[1].sky_text)
        except Exception as e:
            print(e)     
            show_text('Weather could not be fetched at the moment, API failure.')

    write_JSON(JSON)

    # Response dictionary
    from keywords import reply
    
    # Init greetings
    name = JSON['name']
    
    print('\nName: ' + name)
    BMO_greetings = ['Yes?',
                     'Yes, ' + name + '?',
                     'How can I help?',
                     'Beep boop']

####################### MAIN #######################

if __name__ == '__main__':

    show_text('')

    
    # Update the theme
    theme_select(fetch_json=True)
    print('The current THEME COLOR is: ' + SELECTED_COLOR)
    
    # Play intro sequence
    intro = subprocess.Popen(['/usr/bin/python3.9', '/home/pi/Desktop/BMO/play_GIF.py', 'BMO_intro', 'gif', SELECTED_COLOR])
    sleep(2)

    init_user(update_info=False)

    # Import of all replies
    from keywords import reply

    if testing is False:
        try_to_connect_joystick()

    # Calling main function
    BMO_listen()

    # Close active sessions
    if gamepad:
        gamepad.close()
    gifPlayer_b.terminate()
    intro.terminate()