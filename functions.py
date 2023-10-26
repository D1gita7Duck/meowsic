import os
import pickle
from youtubesearchpython import VideosSearch
import yt_dlp as youtube_dl
#from pprint import PrettyPrinter
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import db 

#pp=PrettyPrinter()

with open("secrets.dat","rb") as credentials:
    client_credentials_manager = SpotifyClientCredentials(client_id=pickle.load(credentials), client_secret=pickle.load(credentials))
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

db.init()

ydl_opts = {
    'outtmpl': "new",
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def thumbs(name,url):
    """
    Accepts name and url of a song to store and download the thumbnail.
    Checks if file already exists and skips if yes
    """
    try:
        file=open(os.path.join("thumbs/",f"{name}.png"),"rb+")
    except FileNotFoundError:
        with open(os.path.join("thumbs/",f"{name}.png"),"wb") as file:
            res=requests.get(url,timeout=5).content
            file.write(res)
    else:
        file.close()
        print("thumb already cached. Skipping")
    finally:
        return "thumbs/"+f"{name}.png"


def better_name(stringy):
    """Remove spaces and other special characters from the string
    """
    new_stringy = ''.join(char for char in stringy if char.isalnum() or char in ['_', '-', '.'])
    new_stringy = new_stringy.casefold()
    return new_stringy


def search(stringy):
    """
    Accepts a string and uses youtube and spotify API to get metadata.
    Returns a dictionary of url, duration, prettyname and thumbnail url.
    """
    videos_search = VideosSearch(stringy, limit = 1)
    videos=videos_search.result()
    url="https://www.youtube.com/watch?v="+videos["result"][0]["id"]
    details=sp.search(q=stringy,limit=1,type="track")
    duration=details["tracks"]["items"][0]["duration_ms"]//1000 #returns in ms
    pretty_name=details["tracks"]["items"][0]["name"]
    thumbnail_url=details["tracks"]["items"][0]["album"]["images"][0]["url"]
    temp_artists=details["tracks"]["items"][0]["artists"]
    artists=""
    for i in temp_artists:
        artists+=i["name"]+", "
    if db.song_search(pretty_name):
        print("found in db")
    else:
        print("not found in db downloading thumb")
        thumbnail_path=thumbs(better_name(pretty_name),url)
        db.song_insert([url,duration,pretty_name,thumbnail_path,artists])
        print("added record to db")
    return {"url":url,"duration":duration,"pretty_name":pretty_name,"thumbnail_url":thumbnail_url,"artists":artists}
t=search("badass")
# l=list(t.values())
# print(l)
# #db.song_insert(l)
# db.song_search(t["pretty_name"])
#print(search("ordinary person"))


def download(url,name):
    """
    Function to download song and convert it to mp3.
    Accepts url, Actual song name (pretty_name) and filename
    """
    name=name+r".mp3"
    if os.path.isfile(os.path.join("Audio/",name)):
        print("song already cached skipping")
    else:
        print(os.path.isfile(os.path.join("Audio/",name)))       
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            try:
                os.rename("new.mp3",os.path.join(r"Audio/",name))
            except FileExistsError:
                print("already cached")
                try:
                    os.remove("new.mp3")
                except IOError:
                    print("this shldnt happen")       
    return name