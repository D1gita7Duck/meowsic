import customtkinter as ctk
import CTkMenuBar
import CTkListbox
import pygame.mixer
from PIL import Image, ImageTk
import os
import time
import audioread
import functions
import asyncio

pygame.mixer.init()
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("1000x700")
app.title("meowsic")
app.iconbitmap(os.path.join(os.getcwd() , "assets","icons","app_icon.ico"))

playing = 0
now_playing = 0
master_playing = False
formatted_total_song_time = 0
songs_paths=[]

def load_music(t):
    global total_song_time
    global formatted_total_song_time
    global playing
    if playing==2 or playing==1:pass
    else:pygame.mixer.music.load(t)
    #inserting into list_box
    name = t.split("/")[-1]
    song_list.insert("END", name)
    print("songs_paths",songs_paths)
    print("now playing",now_playing)
    # total length of song
    with audioread.audio_open(songs_paths[now_playing]) as song_file:
        total_song_time = song_file.duration
        print(total_song_time)
        formatted_total_song_time = time.strftime(
            "%M:%S", time.gmtime(total_song_time)
        )

    # change the highlight to current song
    song_list.selection_clear()
    song_list.activate(now_playing)
    song_list.select(f"END{now_playing % len(songs_paths)}")

    #slider position
    song_slider.configure(to=total_song_time)
    song_slider.set(0)

    # change status bar to current song name
    status_bar.configure(text=f'Paused: {songs_paths[0].split("/")[-1]}')

def search():
    global songs_paths
    global playing
    if songs_paths:
        search_text = search_bar.get()
        print(search_text)
        temp_res= functions.search(search_text)
        # if pygame.mixer.music.get_busy():
        #     play_pause(play_button)
        song_name_temp=functions.download(temp_res["url"],functions.better_name(temp_res["pretty_name"]))
        temp_paths=os.path.join("Audio/",song_name_temp)
        songs_paths+=(temp_paths,)
        load_music(temp_paths)
    else:
        songs_paths=tuple()
        search_text = search_bar.get()
        print(search_text)
        temp_res=functions.search(search_text)
        song_name_temp=functions.download(temp_res["url"],functions.better_name(temp_res["pretty_name"]))
        temp_paths=os.path.join("Audio/",song_name_temp)
        songs_paths+=(temp_paths,)
        # songs_paths+=(temp_paths,)
        # song_list.insert('END', temp_paths)
        # pygame.mixer.music.load(temp_paths)
        load_music(temp_paths)
    # Get the search text


    # Clear the search bar
    search_bar.delete(0, 'end')

def open_search_frame():
    # Hide the original home screen
    master_frame.pack_forget()

    # Display the search frame
    search_frame.pack(fill='x', expand=True, padx=10, pady=10)

# Define a function to close the search frame and go back to the home screen
def close_search_frame():
    # Hide the search frame
    search_frame.pack_forget()

    # Display the original home screen
    master_frame.pack(pady=40)


def add_songs():
     # songs_paths will be a tuple of filepaths (str)
    global songs_paths
    global formatted_total_song_time
    global now_playing
    global total_song_time

    og_songs_paths = ctk.filedialog.askopenfilenames(
        initialdir=os.path.join(os.getcwd() , "Audio"),
        title="Choose Songs",
    )

    for i in og_songs_paths:
        name = i.split("/")[-1]
        song_list.insert("END", name)


    print(pygame.mixer.music.get_busy())
    if pygame.mixer.music.get_busy():
        songs_paths= (songs_paths) + (og_songs_paths)

    else:
        songs_paths=og_songs_paths+tuple()

        pygame.mixer.music.load(songs_paths[0])
        now_playing=0

        # total length of song
        with audioread.audio_open(songs_paths[now_playing]) as song_file:
            total_song_time = song_file.duration
            print(total_song_time)
            formatted_total_song_time = time.strftime(
                "%M:%S", time.gmtime(total_song_time)
            )

        # change the highlight to current song
        song_list.selection_clear()
        song_list.activate(now_playing)
        song_list.select(f"END{now_playing % len(songs_paths)}")

        #slider position
        song_slider.configure(to=total_song_time)
        song_slider.set(0)

        # change status bar to current song name
        status_bar.configure(text=f'Paused: {songs_paths[0].split("/")[-1]}')

    print(songs_paths)

def play_time():
    global songs_paths
    global now_playing
    global formatted_total_song_time
    global total_song_time
    time_elapsed = pygame.mixer.music.get_pos() 
    formatted_time_elapsed = time.strftime("%M:%S", time.gmtime(time_elapsed//1000))

    # update time label
    time_elapsed_label.configure(
        text=f"{formatted_time_elapsed} of {formatted_total_song_time}"
    )

    #move song_slider with progress of song
    song_slider.set(time_elapsed//1000)
    #print(total_song_time,time_elapsed)
    #queue?

    if time_elapsed//1000==total_song_time//1 or time_elapsed//1000<0:
        song_next()

    time_elapsed_label.after(1000, play_time)



def slide(x):
    test_label.configure(text=f'{"%.2f" % x} of {formatted_total_song_time} ')


def song_previous():
    global now_playing
    global master_playing
    global playing
    global formatted_total_song_time
    global total_song_time
    #print("now playing",now_playing)
    #print("songs",songs_paths)
    song_time_elapsed = (pygame.mixer.music.get_pos()) // 1000

    if song_time_elapsed < 2:
        song = songs_paths[(now_playing - 1) % song_list.size()]
        now_playing = (now_playing - 1) % song_list.size()
        pygame.mixer.music.load(song)
        functions.store_recents(song.split("/")[-1])
        pygame.mixer.music.play(loops=0)
        playing = 1
        play_button.configure(image=pause_button_icon)

        # total length of song
        with audioread.audio_open(songs_paths[now_playing]) as song_file:
            total_song_time = song_file.duration
            formatted_total_song_time = time.strftime(
                "%M:%S", time.gmtime(total_song_time)
            )

        # change the highlight to current song
        song_list.selection_clear()
        song_list.activate(now_playing)
        song_list.select(f"END{now_playing % song_list.size()}")

        #slider position
        song_slider.configure(to=total_song_time)
        song_slider.set(0)
        
        # change status bar to current song name
        status_bar.configure(text=f'Now playing: {song.split("/")[-1]}')

    else:
        song = songs_paths[now_playing]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        playing = 1
        play_button.configure(image=pause_button_icon)

        # total length of song
        with audioread.audio_open(songs_paths[now_playing]) as song_file:
            total_song_time = song_file.duration
            formatted_total_song_time = time.strftime(
                "%M:%S", time.gmtime(total_song_time)
            )

        # change the highlight to current song
        song_list.selection_clear()
        song_list.activate(now_playing)
        song_list.select(f"END{now_playing % song_list.size()}")

        #slider position
        song_slider.configure(to=total_song_time)
        song_slider.set(0)

        # change status bar to current song name
        status_bar.configure(text=f'Now playing: {song.split("/")[-1]}')


def song_next():
    global playing
    global now_playing
    global formatted_total_song_time
    global total_song_time
    try:
        song = songs_paths[(now_playing + 1) % song_list.size()]
        now_playing = (now_playing + 1) % song_list.size()
    except IndexError:
        song = songs_paths[now_playing]
        pygame.mixer.music.load(song)

    else:
        pygame.mixer.music.load(song)
        functions.store_recents(song.split("/")[-1])
        pygame.mixer.music.play(loops=0)
        playing = 1
        play_button.configure(image=pause_button_icon)

        # total length of song
        with audioread.audio_open(songs_paths[now_playing]) as song_file:
            total_song_time = song_file.duration
            formatted_total_song_time = time.strftime(
                "%M:%S", time.gmtime(total_song_time)
            )

        # change the highlight to current song
        song_list.selection_clear()
        song_list.activate(now_playing)
        song_list.select(f"END{now_playing % song_list.size()}")

        #slider position
        song_slider.configure(to=total_song_time)
        song_slider.set(0)

        # change status bar to current song name
        status_bar.configure(text=f'Now playing: {song.split("/")[-1]}')



def play_pause(btn: ctk.CTkButton):
    global playing
    global master_playing
    global now_playing
    master_playing = True

    if playing == 1:
        pygame.mixer.music.pause()
        # change button icon
        btn.configure(image=play_button_icon)

        # change status bar text
        status_bar.configure(text=f"Paused: {song_list.get()}")
        playing = 2

    elif playing == 2:
        pygame.mixer.music.unpause()

        # change button icon
        btn.configure(image=pause_button_icon)
        playing = 1

        # change status bar text
        status_bar.configure(text=f"Now playing: {song_list.get()}")

        # change the highlight to current song
        song_list.selection_clear()
        song_list.activate(now_playing)
        song_list.select(f"END{now_playing % song_list.size()}")

        play_time()

    elif playing == 0:
        pygame.mixer.music.play()
        functions.store_recents(song_list.get().split("/")[-1])
        # change button icon
        btn.configure(image=pause_button_icon)
        playing = 1

        # change status bar text
        status_bar.configure(text=f"Now playing: {song_list.get()}")

        # change the highlight to current song
        song_list.selection_clear()
        song_list.activate(now_playing)
        song_list.select(f"END{now_playing % song_list.size()}")

        play_time()

def play_on_click():
    pass


# load_music(("H:\Arnav\Python\Python Workspace\meowsic\Audio\song1.mp3",))


# menu
menu = CTkMenuBar.CTkMenuBar(app)
file_button = menu.add_cascade("File")
edit_button = menu.add_cascade("Edit")
settings_button = menu.add_cascade("Settings")
about_button = menu.add_cascade("About")

file_dropdown = CTkMenuBar.CustomDropdownMenu(widget=file_button)
file_dropdown.add_option(option="Open", command=add_songs)
file_dropdown.add_option(option="Save")

file_dropdown.add_separator()

sub_menu = file_dropdown.add_submenu("Export As")
sub_menu.add_option(option=".TXT")
sub_menu.add_option(option=".PDF")

# Frames
master_frame = ctk.CTkFrame(app)


# Media Controls Frame
playback_controls_frame = ctk.CTkFrame(master_frame)
playback_controls_frame.grid(row=2, column=0)
search_frame = ctk.CTkFrame(app)

# Create a search bar
search_bar = ctk.CTkEntry(search_frame)
search_bar.pack(fill='x', expand=True, padx=10, pady=10)

# Create a search button
search_button = ctk.CTkButton(search_frame, text="Search")
search_button.pack(fill='x', expand=True, padx=10, pady=10)

# Place the separate frame in the window
search_frame.pack(fill='x', expand=True, padx=10, pady=10)

# Bind the search button to a function
search_button.configure(command=search)
open_search_frame_button = ctk.CTkButton(app, text="Open Search Frame")
open_search_frame_button.pack()

# Create a button to close the search frame and go back to the home screen
close_search_frame_button = ctk.CTkButton(search_frame, text="Close Search Frame")
close_search_frame_button.pack(fill='x', expand=True, padx=10, pady=10)

# Bind the open search frame button to the open_search_frame function
open_search_frame_button.configure(command=open_search_frame)

# Bind the close search frame button to the close_search_frame function
close_search_frame_button.configure(command=close_search_frame)

# Place the search frame in the window
search_frame.pack(fill='x', expand=True, padx=10, pady=10)

# Hide the search frame by default
search_frame.pack_forget()

# buttons folder path
icon_folder_path = os.path.join(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets","icons")
    
)

# buttons images
play_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "play_btn.png")), size=(30, 30)
)
pause_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "pause_btn.png")), size=(30, 30)
)
next_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "next_btn.png")), size=(26, 26)
)
previous_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "previous_btn.png")), size=(26, 26)
)

# buttons
previous_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=song_previous,
    image=previous_button_icon,
    border_width=0,
    fg_color="transparent",
    hover=False,
    width=26,
    height=26,
)
previous_button.grid(row=0, column=0, padx=10)

play_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=lambda: play_pause(play_button),
    image=play_button_icon,
    border_width=0,
    fg_color="transparent",
    hover=False,
    width=30,
    height=30,
)
play_button.grid(row=0, column=1, padx=10)

next_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=song_next,
    image=next_button_icon,
    border_width=0,
    fg_color="transparent",
    hover=False,
    width=26,
    height=26,
)
next_button.grid(row=0, column=2, padx=10)


song_slider = ctk.CTkSlider(
    playback_controls_frame, from_=0, to=100, orientation="horizontal", progress_color='orange' , button_color = 'cyan' , button_hover_color = 'blue' , command=slide
)
song_slider.grid(columnspan=3 , pady=20)

# Songs List
song_list = CTkListbox.CTkListbox(
    app,
    width=400,
    height=50,
    label_text="Songs",
    fg_color="orange",
    text_color="purple",
)
song_list.pack(pady=20)
master_frame.pack(pady=40)
status_bar = ctk.CTkLabel(app, text="status bar", justify="center", anchor="e")
status_bar.pack(ipady=10)

time_elapsed_label = ctk.CTkLabel(app, text="time", anchor="e")
time_elapsed_label.pack(fill="x", side="bottom", ipady=10, padx=10)

recent_label=ctk.CTkLabel(app,text="recently played : "+str(functions.get_recents()))
recent_label.pack()

test_label=ctk.CTkLabel(app, text='slida text')
test_label.pack(pady=10)

app.mainloop()
