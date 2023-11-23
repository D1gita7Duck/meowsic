from multiprocessing import dummy
import os
import time
from datetime import datetime
import threading
from tkinter import W
import pygame.mixer
import customtkinter as ctk
from PIL import Image
import audioread
import app.functions as functions
import app.lyrics as lyrics
import app.import_spotify as import_spotify

pygame.mixer.init()

playing = 0
now_playing = 0
master_playing = False
formatted_total_song_time = 0
songs_paths = list()
liked_songs_paths = dict()
liked = False
loaded=False
open_playlist=None
def load_music(t,pretty_name):
    """
    Loads music into queue. Accepts filename, pretty_name of song.
    """
    import app.widgets as widgets
    global total_song_time
    global formatted_total_song_time
    global playing
    global liked
    global loaded
    global master_playing

    if playing == 2 or playing == 1 or loaded:
        pass
    else:
        loaded=True
        pygame.mixer.music.load(t)
        # update metadata
        # album art
        album_art = widgets.ctk.CTkImage(Image.open(os.path.join(
            thumbs_folder_path, f'{os.path.basename(t)[:-4]+".png"}')), size=(200, 200))
        widgets.song_metadata_image_label.configure(image=album_art)

        # artist name
        widgets.song_metadata_artist_label.configure(
            text=f'Artist: {functions.artist_search(pretty_name)["artists"].split(",")[0]}')
        print("this is artist","{}".format(os.path.basename(t).rstrip(".mp3")))
            
        # total length of song
        with audioread.audio_open(t) as song_file:
            total_song_time = song_file.duration
            print(total_song_time)
            formatted_total_song_time = time.strftime(
                "%M:%S", time.gmtime(total_song_time)
            )

        # slider position
        widgets.song_slider.configure(to=total_song_time)
        widgets.song_slider.set(0)

        # update time labels
        widgets.time_elapsed_label.configure(
            text=f'{time.strftime("%M:%S", time.gmtime(0))}')
        widgets.total_time_label.configure(text=f'{formatted_total_song_time}')

        # change status bar to current song name
        widgets.status_bar.configure(text=f'Paused: {widgets.song_list.get()}')

        if functions.if_liked(pretty_name):
            liked=True
            widgets.like_button.configure(image=widgets.like_button_icon)

        else:
            liked=False
            widgets.like_button.configure(image=widgets.disliked_button_icon)
            
        #enable buttons
        widgets.like_button.configure(state='normal')
        widgets.previous_button.configure(state='normal')
        widgets.play_button.configure(state='normal')
        widgets.next_button.configure(state='normal')
       # widgets.song_slider.configure(state='normal')     TEMPORARY FIX
        widgets.lyrics_button.configure(state="normal")
        widgets.add_to_playlist_menu.configure(state='normal')
        widgets.delete_from_queue_button.configure(state='normal')
        widgets.volume_button.configure(state="normal")
        widgets.volume_slider.configure(state="normal")

    master_playing=True
    # inserting into list_box
    widgets.song_list.insert("END", pretty_name)
    # change the highlight to current song
    widgets.song_list.selection_clear()
    widgets.song_list.activate(now_playing)
    widgets.song_list.select(f"END{now_playing % len(songs_paths)}")

    widgets.master_tab.set('Queue')

    print("songs_paths", songs_paths)
    print("now playing", now_playing)

    




def search():
    """
    Searches from string from search bar contents
    """
    import app.widgets as widgets
    global songs_paths
    global playing
    global temp_res
    widgets.search_progress.set(0)

    if songs_paths:
        search_text = widgets.search_bar.get()
        print(search_text)
        widgets.search_progress.start()
        temp_res = functions.search(search_text)

        # Download the song in a separate thread
        download_thread = threading.Thread(target=download_and_load, args=(temp_res,))
        download_thread.start()

    else:
        # Reset the songs_paths tuple
        songs_paths = list()
        search_text = widgets.search_bar.get()
        print(search_text)
        widgets.search_progress.start()
        temp_res = functions.search(search_text)

        # Download the song in a separate thread
        download_thread = threading.Thread(target=download_and_load, args=(temp_res,))
        download_thread.start()

def load_playlist_song():
    """
    load fn for playlist songs
    """
    import app.widgets as widgets
    print("load playlist called")
    temp_res = functions.search(playlist_listbox.get())
    # Download the song in a separate thread
    download_thread = threading.Thread(target=download_and_load, args=(temp_res,))
    download_thread.start()

def load_liked():
    """
    load fn for liked songs
    """
    import app.widgets as widgets
    print("load liked called")
    temp_res = functions.search(widgets.liked_songs_listbox.get())
    # Download the song in a separate thread
    download_thread = threading.Thread(target=download_and_load, args=(temp_res,))
    download_thread.start()

def load_recents():
    """
    load fn for recently played songs
    """
    import app.widgets as widgets
    print("load recents called")
    temp_res = functions.search(widgets.recently_played_listbox.get())
    # Download the song in a separate thread
    download_thread = threading.Thread(target=download_and_load, args=(temp_res,))
    download_thread.start()

def download_and_load(temp_res):
    import app.widgets as widgets
    """
    Function to download and load the song
    """
    global songs_paths
    song_name_temp = functions.download(
        temp_res["url"], functions.better_name(temp_res["pretty_name"]))
    temp_paths = os.path.join("Audio/", song_name_temp)
    songs_paths += (temp_paths,)

    # Stop the search progress bar
    widgets.search_progress.stop()

    # Load the downloaded song
    load_music(temp_paths, temp_res["pretty_name"])
    widgets.search_bar.delete(0, 'end')
    # Reset the progress bar
    widgets.search_progress.set(0)

    widgets.master_tab.set('Queue')
    # update status bar
    print("loaded",loaded)
    if "None" in widgets.status_bar.cget("text"):
        print(temp_res["pretty_name"])
        widgets.status_bar.configure(text=f'Paused: {temp_res["pretty_name"]}')


def add_songs():
    """
    fn to add local songs
    """
    import app.widgets as widgets
    global songs_paths
    global formatted_total_song_time
    global now_playing
    global total_song_time
    global master_playing

    # og_songs_paths will be a tuple of filepaths (str)
    og_songs_paths = widgets.ctk.filedialog.askopenfilenames(
        initialdir=os.path.join(os.getcwd(), "Audio"),
        title="Choose Songs",
    )

    # putting song names into playlist
    for i in og_songs_paths:
        widgets.song_list.insert("END", os.path.basename(i))

    print(pygame.mixer.music.get_busy())

    if pygame.mixer.music.get_busy() or loaded:
        songs_paths = (songs_paths) + list(og_songs_paths)

    else:
        songs_paths = list(og_songs_paths)

        pygame.mixer.music.load(songs_paths[0])
        now_playing = 0

        # total length of song
        with audioread.audio_open(songs_paths[now_playing]) as song_file:
            total_song_time = song_file.duration
            print(total_song_time)
            formatted_total_song_time = time.strftime(
                "%M:%S", time.gmtime(total_song_time)
            )

        # change the highlight to current song
        widgets.song_list.selection_clear()
        widgets.song_list.activate(now_playing)
        widgets.song_list.select(f"END{now_playing % len(songs_paths)}")

        # slider position
        widgets.song_slider.configure(to=total_song_time)
        widgets.song_slider.set(0)

        # change status bar to current song name
        widgets.status_bar.configure(text=f'Paused: {songs_paths[0].split("/")[-1]}')

        # update time labels
        widgets.time_elapsed_label.configure(
            text=time.strftime("%M:%S", time.gmtime(0)))
        widgets.total_time_label.configure(text=f'{formatted_total_song_time}')
        # update metadata
        widgets.song_metadata_image_label.configure(image=widgets.garfield_icon)
        widgets.song_metadata_artist_label.configure(text='Miscellaneous')
        widgets.song_metadata_image_label.grid(row=0, columnspan=3, sticky='new')
        
    widgets.like_button.configure(state='normal')
    widgets.previous_button.configure(state='normal')
    widgets.play_button.configure(state='normal')
    widgets.next_button.configure(state='normal')
    #widgets.song_slider.configure(state='normal')    TEMPORARY FIX
    widgets.lyrics_button.configure(state="normal")
    widgets.add_to_playlist_menu.configure(state='normal')
    widgets.delete_from_queue_button.configure(state='normal')

    widgets.master_tab.set('Queue')

    print(songs_paths)


def play_time():
    """
    runtime fn to update slider and time_elapsed label
    """
    import app.widgets as widgets
    global songs_paths
    global now_playing
    global formatted_total_song_time
    global total_song_time

    time_elapsed = pygame.mixer.music.get_pos()
    # print(f'time_elapsed {time_elapsed}')
    formatted_time_elapsed = time.strftime(
        "%M:%S", time.gmtime(time_elapsed//1000))

    # update time label
    widgets.time_elapsed_label.configure(
        text=f'{formatted_time_elapsed}'
    )

    # move song_slider with progress of song
    widgets.song_slider.set(time_elapsed//1000)

    # queue?
    if time_elapsed//1000 == total_song_time//1:
        widgets.song_slider.set(total_song_time)
        song_next()

    #test_label.configure(text=f'slider: {song_slider.get()} and time_elapsed: {time_elapsed//1000}')

    widgets.time_elapsed_label.after(1000, play_time)


def slide(x):
    pygame.mixer.music.set_pos(x)
    play_time()


def song_previous():
    """
    Rewinds song if song has been playing for more than 2 seconds.
    Else loads previous song into queue
    """
    import app.widgets as widgets
    global now_playing
    global master_playing
    global playing
    global formatted_total_song_time
    global total_song_time
    global liked
    global liked_songs_paths
    # print("now playing",now_playing)
    # print("songs",songs_paths)

    song_time_elapsed = (pygame.mixer.music.get_pos()) // 1000

    if song_time_elapsed < 2:
        song = songs_paths[(now_playing - 1) % len(songs_paths)]
        now_playing = (now_playing - 1) % len(songs_paths)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        playing = 1
        widgets.play_button.configure(image=widgets.pause_button_icon)

        # total length of song
        with audioread.audio_open(songs_paths[now_playing]) as song_file:
            total_song_time = song_file.duration
            formatted_total_song_time = time.strftime(
                "%M:%S", time.gmtime(total_song_time)
            )

        # change the highlight to current song
        widgets.song_list.selection_clear()
        widgets.song_list.activate(now_playing)
        widgets.song_list.select(f"END{now_playing % len(songs_paths)}")
        functions.store_recents(widgets.song_list.get())
        # slider position
        widgets.song_slider.configure(to=total_song_time)
        widgets.song_slider.set(0)

        # update time labels
        widgets.time_elapsed_label.configure(
            text=f'{time.strftime("%M:%S", time.gmtime(0))}')
        widgets.total_time_label.configure(text=f'{formatted_total_song_time}')

        # change status bar to current song name
        widgets.status_bar.configure(text=f'Now playing: {widgets.song_list.get()}')
    
        # update metadata
        try:
            # update album art
            album_art = widgets.ctk.CTkImage(Image.open("thumbs/"+ f'{songs_paths[now_playing][5:-4]+".png"}'), size=(200, 200))
            # artist name
            widgets.song_metadata_artist_label.configure(
                text=f'Artist: {functions.artist_search(widgets.song_list.get())["artists"].split(",")[0]}')
        except KeyError:
            print(f'No artist given')
            widgets.song_metadata_artist_label.configure(text='Miscellaneous')
        except:
            print(f'no album art')
            widgets.song_metadata_image_label.configure(image=widgets.garfield_icon)
            widgets.song_metadata_artist_label.configure(text='Miscellaneous')
            widgets.song_metadata_image_label.grid(row=0, columnspan=3, sticky='new', )
        else:
            widgets.song_metadata_image_label.configure(image=album_art)
            widgets.song_metadata_image_label.grid(row=0, columnspan=3, sticky='new', )
            
        if functions.if_liked(widgets.song_list.get()):
            liked=True
            widgets.like_button.configure(image=widgets.like_button_icon)

        else:
            liked=False
            widgets.like_button.configure(image=widgets.disliked_button_icon)


    else:
        song = songs_paths[now_playing]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        playing = 1
        widgets.play_button.configure(image=widgets.pause_button_icon)

        # total length of song
        with audioread.audio_open(songs_paths[now_playing]) as song_file:
            total_song_time = song_file.duration
            formatted_total_song_time = time.strftime(
                "%M:%S", time.gmtime(total_song_time)
            )

        # change the highlight to current song
        widgets.song_list.selection_clear()
        widgets.song_list.activate(now_playing)
        widgets.song_list.select(f"END{now_playing % len(songs_paths)}")

        # slider position
        widgets.song_slider.configure(to=total_song_time)
        widgets.song_slider.set(0)

        # update time labels
        widgets.time_elapsed_label.configure(
            text=f'{time.strftime("%M:%S", time.gmtime(0))}')
        widgets.total_time_label.configure(text=f'{formatted_total_song_time}')



def song_next():
    """
    loads next song in queue 
    """
    import app.widgets as widgets
    global playing
    global now_playing
    global formatted_total_song_time
    global songs_paths
    global total_song_time
    global liked_songs_paths
    global liked

    try:
        song = songs_paths[(now_playing + 1) % len(songs_paths)]
        print(songs_paths[(now_playing + 1) % len(songs_paths)])
        now_playing = (now_playing + 1) % len(songs_paths)
    except IndexError:
        song = songs_paths[now_playing % len(songs_paths)]
        pygame.mixer.music.load(song)

    else:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        playing = 1
        widgets.play_button.configure(image=widgets.pause_button_icon)

        # total length of song
        with audioread.audio_open(songs_paths[now_playing]) as song_file:
            total_song_time = song_file.duration
            formatted_total_song_time = time.strftime(
                "%M:%S", time.gmtime(total_song_time)
            )

        # change the highlight to current song
        widgets.song_list.selection_clear()
        widgets.song_list.activate(now_playing)
        widgets.song_list.select(f"END{now_playing % len(songs_paths)}")
        functions.store_recents(widgets.song_list.get())
        # slider position
        widgets.song_slider.configure(to=total_song_time)
        widgets.song_slider.set(0)

        # update time labels
        widgets.time_elapsed_label.configure(
            text=f'{time.strftime("%M:%S", time.gmtime(0))}')
        widgets.total_time_label.configure(text=f'{formatted_total_song_time}')

        # change status bar to current song name
        widgets.status_bar.configure(text=f'Now playing: {widgets.song_list.get()}')

        if functions.if_liked(widgets.song_list.get()):
            liked=True
            widgets.like_button.configure(image=widgets.like_button_icon)

        else:
            liked=False
            widgets.like_button.configure(image=widgets.disliked_button_icon)

        # update metadata
        try:
            # update album art
            #print("album art dir",os.path.join("thumbs/", f'{songs_paths[now_playing][5:-4]+".png"}'))
            album_art = widgets.ctk.CTkImage(Image.open("thumbs/"+ f'{songs_paths[now_playing][5:-4]+".png"}'), size=(200, 200))
            
            # artist name
            print("song list artist get",f'Artist: {functions.artist_search(widgets.song_list.get())["artists"].split(",")[0]}')
            widgets.song_metadata_artist_label.configure(
                text=f'Artist: {functions.artist_search(widgets.song_list.get())["artists"].split(",")[0]}')
        except KeyError:
            print(f'No artist given')
            widgets.song_metadata_artist_label.configure(text='Miscellaneous')
        except:
            print(f'no album art')
            widgets.song_metadata_image_label.configure(image=widgets.garfield_icon)
            widgets.song_metadata_artist_label.configure(text='Miscellaneous')
            widgets.song_metadata_image_label.grid(row=0, columnspan=3, sticky='new', )
        else:
            widgets.song_metadata_image_label.configure(image=album_art)
            widgets.song_metadata_image_label.grid(row=0, columnspan=3, sticky='new', )


def play_pause(btn: ctk.CTkButton):
    """
    Accepts ctkbutton as argument and changes button icon wrt playing state.
    Also pauses and unpauses current song.
    """
    import app.widgets as widgets
    global playing
    global master_playing
    global now_playing
    master_playing = True

    if playing == 1:
        pygame.mixer.music.pause()
        # change button icon
        btn.configure(image=widgets.play_button_icon)

        # change status bar text
        widgets.status_bar.configure(text=f"Paused: {widgets.song_list.get()}")
        playing = 2

    elif playing == 2:
        pygame.mixer.music.unpause()

        # change button icon
        btn.configure(image=widgets.pause_button_icon)
        playing = 1

        # change status bar text
        widgets.status_bar.configure(text=f"Now playing: {widgets.song_list.get()}")

        # change the highlight to current song
        widgets.song_list.selection_clear()
        widgets.song_list.activate(now_playing)
        widgets.song_list.select(f"END{now_playing % len(songs_paths)}")

        play_time()

    elif playing == 0:
        pygame.mixer.music.play()
        functions.store_recents(os.path.basename(widgets.song_list.get()))
        # change button icon
        btn.configure(image=widgets.pause_button_icon)
        playing = 1

        # change status bar text
        widgets.status_bar.configure(text=f"Now playing: {widgets.song_list.get()}")

        # change the highlight to current song
        widgets.song_list.selection_clear()
        widgets.song_list.activate(now_playing)
        widgets.song_list.select(f"END{now_playing % len(songs_paths)}")

        play_time()


def like(btn: ctk.CTkButton):
    """
    Accepts ctkbutton as argument and changes icon to liked/unliked wrt liked status.
    Also calls required backend fns to like/dislike
    """
    import app.widgets as widgets
    global liked
    global songs_paths
    global liked_songs_paths
    global now_playing

    if not(functions.if_liked(widgets.song_list.get())):
        # change button image
        btn.configure(image=widgets.like_button_icon)
        # mark song as liked
        liked = True
        # insert into liked_songs table
        functions.like_song(widgets.song_list.get())

        # add song path to list of liked songs paths
        # liked_songs_paths[songs_paths[now_playing]
        #                   ] = songs_paths[now_playing].split('/')[-1]
        # insert into liked_songlistbox
        widgets.liked_songs_listbox.insert(
            "END", widgets.song_list.get())

        print(f'liked')
    else:
        # change button image
        btn.configure(image=widgets.disliked_button_icon)
        # mark song as disliked
        liked = False
        # remove from liked_songs_paths
        functions.dislike_song(widgets.song_list.get())
        widgets.liked_songs_listbox.delete("all")
        for i in functions.get_liked_songs():
            widgets.liked_songs_listbox.insert("END",i["pretty_name"])

        print(f'disliked')

def show_liked_songs():
    #called from liked songs btn on homepage of application
    import app.widgets as widgets
    widgets.master_tab.set('Liked Songs')


def play_on_click():
    pass
def volume(value):
    pygame.mixer.music.set_volume(value/100)
def mute():
    import app.widgets as widgets
    if pygame.mixer.music.get_volume()!=0:
        pygame.mixer.music.set_volume(0)
        widgets.volume_button.configure(image=widgets.mute_icon)
    else:
        pygame.mixer.music.set_volume(widgets.volume_slider.get())
        widgets.volume_button.configure(image=widgets.volume_icon)
def main_lyrics():
    """
    Searches for and Displays lyrics
    """
    import app.widgets as widgets
    res=functions.search(widgets.song_list.get())
    lyrics.show_lyrics(res["pretty_name"],res["artists"].split(",")[0],widgets.app)

def add_to_playlist(choice):
    import app.widgets as widgets
    print(choice)
    add_to_playlist_var=ctk.StringVar(value='Add to Playlist')
    widgets.add_to_playlist_menu.configure(variable=add_to_playlist_var)
    if choice=='Create New Playlist':
        create_playlist_dialog=ctk.CTkInputDialog(text='Give Playlist Name:', title = 'Creating a Playlist')
        playlist_name=create_playlist_dialog.get_input()
        print(playlist_name)
        functions.add_playlist({"name":playlist_name,"art_location":"nothing","date":datetime.today().strftime('%Y-%m-%d')})
        widgets.add_to_playlist_options.append(playlist_name)
        widgets.add_to_playlist_menu.configure(values=widgets.add_to_playlist_options)
        functions.add_to_playlist(widgets.song_list.get(),playlist_name)
    else:
        functions.add_to_playlist(widgets.song_list.get(),choice)
def delete_from_queue():
    import app.widgets as widgets
    global now_playing
    current_song_index=widgets.song_list.curselection()
    print(current_song_index)
    if current_song_index!=now_playing:
        songs_paths.pop(current_song_index)
        widgets.song_list.delete(current_song_index)
    else:
        incorrect_delete_queue_win=ctk.CTkToplevel(widgets.app)
        incorrect_delete_queue_win.geometry('200x100')
        incorrect_delete_queue_win.focus()
        text_label=ctk.CTkLabel(master=incorrect_delete_queue_win,
                                text='Incorrect Operation',
                                image=widgets.information_icon,
                                compound='left',
                                anchor='center',)
        text_label.pack(pady=(20,20), padx=(10,10), anchor='center')

def show_playlist(value):
    import app.widgets as widgets
    global playlist_frame
    global playlist_listbox
    global open_playlist
    print("show playlist called")
    if open_playlist:widgets.master_tab.delete(open_playlist)
    if value["column"]!=0 or value["value"]=="Name":pass
    else:
        playlist_tab=widgets.master_tab.add(value["value"])
        open_playlist=value["value"]
        playlist_frame=ctk.CTkFrame(master=playlist_tab)
        playlist_frame.pack()
        playlist_listbox = widgets.CTkListbox.CTkListbox(
            master=playlist_frame,
            width=700,
            height=250,
            border_width=2,
            border_color='black',
            corner_radius=10,
            label_text='Playlists',
            label_anchor='center',
            fg_color="orange",
            text_color="black",
            hightlight_color='red',
            hover_color='#7fb8cc',)

       # widgets.playlist_listbox.configure(master=playlist_frame)
        playlist_listbox.pack()
        for i in functions.get_playlist_songs(value["value"]):
            playlist_listbox.insert("END",i,onclick=load_playlist_song)


def show_your_library():
    import app.widgets as widgets
    widgets.master_tab.set('Your Library')



def import_from_spotify(playlist):
    import app.widgets as widgets
    L=import_spotify.get_spotify_playlist_tracks(playlist)
    for i in L:
        i=i.lstrip("123456789. ")
        print("syncing",i)
        temp_res=functions.search(i)
        functions.like_song(temp_res["pretty_name"])
        widgets.liked_songs_listbox.insert(
            "END", temp_res["pretty_name"],onclick=load_liked)
        print("liked",i)
    print("all songs imported to liked songs")

def import_sp_playlist():
    # Import the necessary module
    import app.widgets as widgets
    # Get the url from the import entry
    url = widgets.import_entry.get()
    # Create an Event object to signal the completion of the import process
    done_event = threading.Event()
    # Create a new thread to handle the import process
    import_thread = threading.Thread(target=run_import, args=[url])
    # Start the import progress bar
    widgets.import_progress.start()
    # Start the import thread
    import_thread.start()
    
def run_import(url):
    import app.widgets as widgets
    import_from_spotify(url)
    widgets.import_progress.stop()

#DEFINITIONS
thumbs_folder_path = os.path.join("thumbs")

# buttons folder path
icon_folder_path = os.path.join(
    os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "assets", "icons")
)
