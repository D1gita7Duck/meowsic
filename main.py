import customtkinter as ctk
import CTkMenuBar
import CTkListbox
import pygame.mixer
from PIL import Image, ImageTk
import os

pygame.mixer.init()
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("700x700")
app.title("meowsic")
app.iconbitmap(os.getcwd()+"\\assets\icons\\app_icon.ico")


playing = 0
now_playing=0
master_playing=False

def load_music(path):
    global master_playing
    global now_playing

    if master_playing==True:
        for i in path:
            pygame.mixer.music.queue(i)
    else:
        pygame.mixer.music.load(path[0])
        for i in path[1::]:
            pygame.mixer.music.queue(i)
        now_playing=0

        #change status bar to current song name
        status_bar.configure(text=f'Now playing: {path[0].split("/")[-1]}')


def add_songs():
    # songs_paths will be a tuple of filepaths (str)
    global songs_paths
    songs_paths = ctk.filedialog.askopenfilenames(
        initialdir=os.getcwd()+"\Audio",
        title="Choose Songs",
    )
    
    load_music(songs_paths)



    for i in songs_paths:
        name = i.split("/")[-1]
        song_list.insert("END", name)
    


def song_previous():
    global now_playing
    global master_playing
    global playing
    #print(now_playing)    

    song_time_elapsed=(pygame.mixer.music.get_pos())//1000
    
    if song_time_elapsed<2:
        if now_playing-1<-len(songs_paths):now_playing=0
        song=songs_paths[now_playing-1]
        now_playing-=1
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        playing = 1
        play_button.configure(image=pause_button_icon)

        #change the highligh to current song
        song_list.selection_clear()
        song_list.activate(now_playing)
        if now_playing >= 0 :
            song_list.select(f'END{now_playing}')
        else:
            song_list.select(f'END{song_list.size()+now_playing}')

        #change status bar to current song name
        status_bar.configure(text=f'Now playing: {song.split("/")[-1]}')
        
    else:
        song=songs_paths[now_playing]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        playing = 1
        play_button.configure(image=pause_button_icon)

        #change the highligh to current song
        song_list.selection_clear()
        song_list.activate(now_playing)
        if now_playing >= 0 :
            song_list.select(f'END{now_playing}')
        else:
            song_list.select(f'END{song_list.size()+ now_playing}')

        #change status bar to current song name
        status_bar.configure(text=f'Now playing: {song.split("/")[-1]}')

def song_next():
    global playing
    global now_playing

    # pygame.mixer.music.set_endevent(pygame.MUSIC_END)
    try:
        song=songs_paths[now_playing+1]
        now_playing+=1
    except IndexError:
        now_playing=0
        song=songs_paths[now_playing]
    finally:
        print(now_playing,song)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        playing = 1
        play_button.configure(image=pause_button_icon)

        #change the highligh to current song
        song_list.selection_clear()
        song_list.activate(now_playing)
        if now_playing >= 0 :
            song_list.select(f'END{now_playing}')
        else:
            song_list.select(f'END{song_list.size() + now_playing}')

        #change status bar to current song name
        status_bar.configure(text=f'Now playing: {song.split("/")[-1]}')

def play_pause(btn: ctk.CTkButton):
    global playing
    global master_playing
    global now_playing
    master_playing=True

    if playing == 1:
        pygame.mixer.music.pause()
        btn.configure(image=play_button_icon)
        playing = 2

    elif playing == 2:
        pygame.mixer.music.unpause()
        btn.configure(image=pause_button_icon)
        playing = 1

        #change the highligh to current song
        song_list.selection_clear()
        song_list.activate(now_playing)
        if now_playing >= 0 :
            song_list.select(f'END{now_playing}')
        else:
            song_list.select(f'END{song_list.size() + now_playing}')

    elif playing == 0:
        pygame.mixer.music.play()
        btn.configure(image=pause_button_icon)
        playing = 1

        #change the highligh to current song
        song_list.selection_clear()
        song_list.activate(now_playing)
        if now_playing >= 0 :
            song_list.select(f'END{now_playing}')
        else:
            song_list.select(f'END{song_list.size() + now_playing}')


def play_on_click():
    pass


# load_music(("H:\Arnav\Python\Python Workspace\meowsic\Audio\song1.mp3",))


# Frames
master_frame = ctk.CTkFrame(app)
master_frame.pack(pady=20)

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


# Media Controls Frame
playback_controls_frame = ctk.CTkFrame(master_frame)
playback_controls_frame.grid(row=1, column=0)


# buttons folder path
icon_folder_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "assets\icons"
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

status_bar=ctk.CTkLabel(app, text='status bar' , justify= 'center' , anchor='e' )
status_bar.pack(ipady=10)


app.mainloop()
