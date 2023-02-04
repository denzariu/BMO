import re, requests, urllib.parse, urllib.request
import vlc
import pafy
from time import sleep
import json

def get_link(vid_name):

    query_string = urllib.parse.urlencode({"search_query": vid_name})

    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())

    response = requests.get("https://www.youtube.com/watch?v=" + search_results[0]) #returns 200

    
    
    if response.status_code == requests.codes.ok:
        url = "https://www.youtube.com/watch?v=" + search_results[0]

        ### TITLE ###
        params = {"format": "json", "url": url}
        url2 = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url2 = url2 + "?" + query_string
        
        with urllib.request.urlopen(url2) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            print(data['title'])
            title = data['title']
        ###
        
        return [url, title]
    else:
        raise Exception("URL fetch did not work.")

def play_stream(url, gamepad):

    video = pafy.new(url)
    selected_stream = video.getbestaudio()

    Instance = vlc.Instance()
    player = Instance.media_player_new()

    Media = Instance.media_new(selected_stream.url)
    Media.get_mrl()

    #player.toggle_fullscreen()
    player.set_media(Media)
    player.play()

    UP    = 306
    DOWN  = 305
    LEFT  = 304
    RIGHT = 307
    ESC   = 317
    ZL    = 319
    L     = 318
    

    while player.is_playing() == False:
        sleep(1)
    while player.is_playing():

        

        for event in gamepad.read_loop():
            if event.value == 0:
                print(event.code)
                if event.code == UP or event.code == ZL:
                    player.play()

                elif event.code == DOWN or event.code == L:
                    player.pause()

                elif event.code == LEFT:
                    print("LEFT")

                elif event.code == RIGHT:
                    print("RIGHT")

                elif event.code == ESC:
                    player.stop()
                    return

        
