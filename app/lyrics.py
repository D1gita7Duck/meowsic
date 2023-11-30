import pickle
import customtkinter as ctk
import lyricsgenius

with open("data/secrets.dat","rb") as cred:
    genius = lyricsgenius.Genius(pickle.load(cred)[2])

def kill_and_change_icon():
    import app.widgets as widgets
    widgets.lyrics_button.configure(image=widgets.lyrics_button_icon_white)
    root.destroy()

def show_lyrics(song,artist,app):
    """
    Takes songname,artist,root_window as arguments and makes a new toplevel with web-scraped lyrics
    """
    import app.widgets as widgets
    global root
    root = ctk.CTkToplevel(app)
    root.title("Lyrics")
    root.geometry("400x600")
    scrollable_frame = ctk.CTkScrollableFrame(root, width=400, height=600)
    song=song.split("(")[0] #temporary fix
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

    # make the toplevel appear on top
    root.attributes('-topmost', True)
    root.focus()
    
    widgets.lyrics_button.configure(image=widgets.lyrics_button_icon_orange)

    root.protocol('WM_DELETE_WINDOW', kill_and_change_icon)
    root.mainloop()
