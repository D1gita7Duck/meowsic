from youtubesearchpython import VideosSearch
import yt_dlp as youtube_dl
from pprint import PrettyPrinter
import requests
import os

#pp=PrettyPrinter()

ydl_opts = {
    'outtmpl': "Audio" + '/%(title)s.%(ext)s',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def search(stringy):
    """
    Accepts a string for searching and returns a dictionary of url,duration,prettyname and thumbnail url
    """
    videosSearch = VideosSearch(stringy, limit = 1)
    Videos=videosSearch.result()
#    pp.pprint(Videos)
    url="https://www.youtube.com/watch?v="+Videos["result"][0]["id"]
    duration=Videos["result"][0]["duration"]
    pretty_name=Videos["result"][0]["title"]
    thumbnail_url=Videos["result"][0]["thumbnails"][0]["url"]
    return {"url":url,"duration":duration,"pretty_name":pretty_name,"thumbnail_url":thumbnail_url}
#print(search("ordinary person"))

def thumbs(name,url):
    """
    Accepts name and url of a song to store and download the thumbnail
    """
    res=requests.get(url).content
#    print("res",res,"url",url)
    file=open(name+".png","wb")
    file.write(res)
    file.close()

#thumbs("blindinglights",search("blinding lights")["thumbnail_url"])

def download(url,pretty_name,name):
    """
    Function to download song and convert it to mp3.
    Accepts url, Actual song name (pretty_name) and filename
    """
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
          ydl.download([url])
          info = ydl.extract_info(url, download=False)
          info_with_audio_extension = dict(info)
          info_with_audio_extension['ext'] = "mp3"
          x=ydl.prepare_filename(info_with_audio_extension)
          os.rename(x,os.path.join("Audio/",name))
#t=search("ordinary person")
#download(t["url"],t["pretty_name"],"ordinaryperson.mp3")