import pickle
import customtkinter as ctk
import lyricsgenius

with open("secrets.dat","rb") as cred:
    genius = lyricsgenius.Genius(pickle.load(cred)[2])



def show_lyrics(song,artist,app):
    """
    Takes songname,artist,root_window as arguments and makes a new toplevel with web-scraped lyrics
    """
    root = ctk.CTkToplevel(app)
    root.title("Lyrics")
    root.geometry("400x600")
    scrollable_frame = ctk.CTkScrollableFrame(root, width=400, height=600)
    try:
        song=genius.search_song(song,artist)
        lyrics=song.lyrics[:-5]
        #print(lyrics)
    except:
        print("No lyrics found.")
        lyrics="not found"
    
    Label_lyrics=ctk.CTkLabel(scrollable_frame)
    Label_lyrics.configure(text=lyrics)
    Label_lyrics.pack()
    scrollable_frame.pack()

    root.mainloop()
