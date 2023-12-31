import os
import time
from datetime import datetime
import pickle
from youtubesearchpython import VideosSearch
import yt_dlp as youtube_dl
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tinytag import TinyTag
import app.db as db

with open("data/secrets.dat","rb") as credentials:
    temp_cred=pickle.load(credentials)
    client_credentials_manager = SpotifyClientCredentials(client_id=temp_cred[0], client_secret=temp_cred[1])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    current_theme=temp_cred[3]



ydl_opts = {
    'outtmpl': "new",
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

db.init()

def change_mode(mode):
    print("changing mode to",mode)
    f=open("data/secrets.dat","rb")
    temp_list=pickle.load(f)
    f.close()
    temp_list[-1]=mode
    print(temp_list)
    f=open("data/secrets.dat","wb")
    pickle.dump(temp_list,f)
    f.close()

def check_recents():
    try:
        file=open("data/recents.dat","rb+")
    except FileNotFoundError:
        file=open("data/recents.dat","wb+")
        pickle.dump([{},{},{}],file)
    finally:
        file.close()

check_recents()

def store_recents(song):
    if ".mp3" in song:
        print("local song not adding to recents")
    else:
        file=open("data/recents.dat","rb+")
        file.seek(0,0)
        L=pickle.load(file)
        L.pop()
        L.insert(0,song)
        file.seek(0,0)
        pickle.dump(L,file)
        file.close()

def get_recents():
    file=open("data/recents.dat","rb")
    file.seek(0,0)
    recent=pickle.load(file)
    while {} in recent:
        recent.remove({})
    return list(set(recent)) #remove repeated songs

def like_song(song):
    res=db.song_search(song)
    path=os.path.join("Audio/",better_name(res["path"])+".mp3")
    db.like_song([path,res["url"],res["duration"],res["pretty_name"],res["thumbnail"],res["artists"]])
def dislike_song(song):
    # res=db.song_search(song)
    # path=os.path.join("Audio/",res["path"]+".mp3")
    db.dislike_song(song)
def if_liked(song):
    L=db.get_liked_songs()
    print("L",L)
    for i in L:
        if i["pretty_name"]==song:
            print(song,i["pretty_name"])
            return True
    return False
def get_liked_songs():
    return db.get_liked_songs()

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
    Accepts song name and uses youtube and spotify API to get metadata.
    Returns a dictionary of url, duration, prettyname and thumbnail url.
    """
    details=sp.search(q=stringy,limit=1,type="track")
    duration=details["tracks"]["items"][0]["duration_ms"]//1000 #returns in ms
    pretty_name=details["tracks"]["items"][0]["name"]
    thumbnail_url=details["tracks"]["items"][0]["album"]["images"][0]["url"]
    temp_artists=details["tracks"]["items"][0]["artists"]
    artists=""
    for i in temp_artists:
        artists+=i["name"]+", "
    artists=artists.rstrip(", ")
    videos_search = VideosSearch(pretty_name, limit = 1)
    videos=videos_search.result()
    url="https://www.youtube.com/watch?v="+videos["result"][0]["id"]
    db_search=db.song_search(pretty_name)
    if db_search:
        print("found in db")
        thumbnail_path=thumbs(better_name(pretty_name),thumbnail_url)
    else:
        print("not found in db downloading thumb")
        thumbnail_path=thumbs(better_name(pretty_name),thumbnail_url)
        db.song_insert(["Audio/"+better_name(pretty_name)+".mp3",url,duration,pretty_name,thumbnail_path,artists])
        print("added record to db")
    
    return {"path":"Audio/"+better_name(pretty_name)+".mp3","url":url,"duration":duration,"pretty_name":pretty_name,"thumbnail_path":thumbnail_path,"artists":artists}

def artist_search(pretty_name):
    search_res=db.song_search(pretty_name)
    if search_res:
        return search_res
    else:
        return search(pretty_name)

def add_playlist(header_dict):
    if len(header_dict)==1:
        db.insert_playlist_header([header_dict["name"],"Null","Null"])
    else:
        db.insert_playlist_header([x for x in header_dict.values()])

def get_playlists():
    return db.get_all_playlists()

def get_playlist_details(name):
    print(db.get_playlist_header(name))
    L=[]
    for i in db.get_playlist_header(name):
        for x in i.values():
            L.append(x)
    print(L)
    return L

def add_to_playlist(song_name,playlist_name):
    print("adding",song_name,"to",playlist_name)
    db.insert_playlist_details([playlist_name,song_name,datetime.today().strftime('%Y-%m-%d')])
    print("after",[playlist_name,song_name,datetime.today().strftime('%Y-%m-%d')])

def get_playlist_songs(name):
    names=[]
    L=db.get_playlist_detail(name)
    for song in L:
        names.append(song["pretty_name"])
    print(names)
    return names

def store_local(name):
    duration=int(TinyTag.get("Audio/"+name).duration)
    db.song_insert([name,"None",duration,name,"None","Miscellaneous"])

def get_recommmended_playlist():
    ''' list of dictionaries of key value pairs where key is playlist name and value is a list of song names'''
    #INDIA 
    featured_playlists = sp.featured_playlists(locale=None,limit=5,offset=5)
    recommended_playlist={}
    for playlist in featured_playlists['playlists']['items']:
        playlist_name=playlist["name"]
        songs = sp.playlist_tracks(playlist['id'], limit=15)
        song_names = [song['track']['name'] for song in songs["items"]]
        recommended_playlist[playlist_name] = song_names
    #WorldWide (US)
    us_recommended={}
    featured_playlists = sp.featured_playlists(country="US",limit=5,offset=5)
    for playlist in featured_playlists['playlists']['items']:
        playlist_name=playlist["name"]
        songs = sp.playlist_tracks(playlist['id'], limit=15)
        song_names = [song['track']['name'] for song in songs["items"]]
        us_recommended[playlist_name] = song_names
    recommended_playlist.update(us_recommended)
    print(recommended_playlist,len(recommended_playlist))
    return recommended_playlist

def download(url,name):
    """
    Function to download song and convert it to mp3.
    Accepts url, Actual song name (pretty_name) and filename
    """
    name=name+r".mp3"
    if os.path.isfile(os.path.join("Audio/",name)):
        print("song already cached skipping")
    else:
        #print(os.path.isfile(os.path.join("Audio/",name)))       
        while True:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    # ydl_down = threading.Thread(target=ydl.download, args=[url])
                    # ydl_down.start()

                    ydl.download([url])
                    try:
                        os.rename("new.mp3", os.path.join(r"Audio/",name))
                        break  # Break out of the loop if the file is successfully renamed
                    except FileNotFoundError:
                        print("File not found. Retrying in 1 second...")
                        time.sleep(1)
                    except FileExistsError:
                        print("Already cached")
                        try:
                            os.remove("new.mp3")
                        except IOError:
                            print("This shouldn't happen")
                        break      
    return name