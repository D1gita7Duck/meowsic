import os
import time
import atexit
import threading
import customtkinter as ctk
from flask import Flask, request
import audioread
from PIL import Image
import pygame.mixer
import CTkListbox
import CTkMenuBar
import functions
import remote.remote as remote


flask_app = Flask(__name__)

pygame.mixer.init()
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
# Themes: blue (default), dark-blue, green
ctk.set_default_color_theme("dark-blue")


@flask_app.route('/control', methods=['POST'])
def control_music_player():
    action = request.form.get('action')
    if action == 'play_pause':
        play_pause(play_button)
    elif action == 'song_previous':
        song_previous()
    elif action == 'song_next':
        song_next()
    return "OK"


def run_flask():
    flask_app.run(host='0.0.0.0', port=5000)


def run_client_side():
    remote.app.run(host="0.0.0.0", port=80)


flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()
client_side_thread = threading.Thread(target=run_client_side)
client_side_thread.daemon = True
client_side_thread.start()


def kill_app():
    func = flask_thread._stop
    try:
        app.destroy()
        func()
    except:
        print("closing app")


app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("1000x700")
app.title("meowsic")
app.iconbitmap(os.path.join(os.getcwd(), "assets", "icons", "app_icon.ico"))
app.protocol("WM_DELETE_WINDOW", kill_app)

playing = 0
now_playing = 0
master_playing = False
formatted_total_song_time = 0
songs_paths = []


def load_music(t):
    global total_song_time
    global formatted_total_song_time
    global playing
    if playing == 2 or playing == 1:
        pass
    else:
        pygame.mixer.music.load(t)

    # inserting into list_box
    name = t.split("/")[-1]
    song_list.insert("END", name)
    print("songs_paths", songs_paths)
    print("now playing", now_playing)

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

    # slider position
    song_slider.configure(to=total_song_time)
    song_slider.set(0)

    # update time labels
    time_elapsed_label.configure(
        text=f'{time.strftime("%M:%S", time.gmtime(0))}')
    total_time_label.configure(text=f'{formatted_total_song_time}')

    # change status bar to current song name
    status_bar.configure(text=f'Paused: {songs_paths[0].split("/")[-1]}')


def search():
    global songs_paths
    global playing
    if songs_paths:
        search_text = search_bar.get()
        print(search_text)
        temp_res = functions.search(search_text)
        # if pygame.mixer.music.get_busy():
        #     play_pause(play_button)
        song_name_temp = functions.download(
            temp_res["url"], functions.better_name(temp_res["pretty_name"]))
        temp_paths = os.path.join("Audio/", song_name_temp)
        songs_paths += (temp_paths,)
        load_music(temp_paths)
    else:
        songs_paths = tuple()
        search_text = search_bar.get()
        print(search_text)
        temp_res = functions.search(search_text)
        song_name_temp = functions.download(
            temp_res["url"], functions.better_name(temp_res["pretty_name"]))
        temp_paths = os.path.join("Audio/", song_name_temp)
        songs_paths += (temp_paths,)
        # songs_paths+=(temp_paths,)
        # song_list.insert('END', temp_paths)
        # pygame.mixer.music.load(temp_paths)
        load_music(temp_paths)
    # Get the search text
    # Clear the search bar
    search_bar.delete(0, 'end')


def open_search_frame():

    # Display the search frame
    search_frame.pack(fill='x', expand=True, padx=10, pady=10)

# Define a function to close the search frame and go back to the home screen


def close_search_frame():
    # Hide the search frame
    search_frame.pack_forget()


def add_songs():
    global songs_paths
    global formatted_total_song_time
    global now_playing
    global total_song_time

    # og_songs_paths will be a tuple of filepaths (str)
    og_songs_paths = ctk.filedialog.askopenfilenames(
        initialdir=os.path.join(os.getcwd(), "Audio"),
        title="Choose Songs",
    )

    # putting song names into playlist
    for i in og_songs_paths:
        name = i.split("/")[-1]
        song_list.insert("END", name)

    print(pygame.mixer.music.get_busy())

    if pygame.mixer.music.get_busy():
        songs_paths = (songs_paths) + (og_songs_paths)

    else:
        songs_paths = og_songs_paths+tuple()

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
        song_list.selection_clear()
        song_list.activate(now_playing)
        song_list.select(f"END{now_playing % len(songs_paths)}")

        # slider position
        song_slider.configure(to=total_song_time)
        song_slider.set(0)

        # change status bar to current song name
        status_bar.configure(text=f'Paused: {songs_paths[0].split("/")[-1]}')

        # update time labels
        time_elapsed_label.configure(
            text=time.strftime("%M:%S", time.gmtime(0)))
        total_time_label.configure(text=f'{formatted_total_song_time}')

    print(songs_paths)


def play_time():
    global songs_paths
    global now_playing
    global formatted_total_song_time
    global total_song_time

    time_elapsed = pygame.mixer.music.get_pos()
    # print(f'time_elapsed {time_elapsed}')
    formatted_time_elapsed = time.strftime(
        "%M:%S", time.gmtime(time_elapsed//1000))

    # update time label
    time_elapsed_label.configure(
        text=f'{formatted_time_elapsed}'
    )

    # move song_slider with progress of song
    song_slider.set(time_elapsed//1000)

    # queue?
    if time_elapsed//1000 == total_song_time//1:
        song_slider.set(total_song_time)
        song_next()

    #test_label.configure(text=f'slider: {song_slider.get()} and time_elapsed: {time_elapsed//1000}')

    time_elapsed_label.after(1000, play_time)


def slide(x):
    pygame.mixer.music.set_pos(x)
    play_time()


def song_previous():
    global now_playing
    global master_playing
    global playing
    global formatted_total_song_time
    global total_song_time
    # print("now playing",now_playing)
    # print("songs",songs_paths)
    song_time_elapsed = (pygame.mixer.music.get_pos()) // 1000

    if song_time_elapsed < 2:
        song = songs_paths[(now_playing - 1) % len(songs_paths)]
        now_playing = (now_playing - 1) % len(songs_paths)
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
        song_list.select(f"END{now_playing % len(songs_paths)}")

        # slider position
        song_slider.configure(to=total_song_time)
        song_slider.set(0)

        # update time labels
        time_elapsed_label.configure(
            text=f'{time.strftime("%M:%S", time.gmtime(0))}')
        total_time_label.configure(text=f'{formatted_total_song_time}')

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
        song_list.select(f"END{now_playing % len(songs_paths)}")

        # slider position
        song_slider.configure(to=total_song_time)
        song_slider.set(0)

        # update time labels
        time_elapsed_label.configure(
            text=f'{time.strftime("%M:%S", time.gmtime(0))}')
        total_time_label.configure(text=f'{formatted_total_song_time}')

        # change status bar to current song name
        status_bar.configure(text=f'Now playing: {song.split("/")[-1]}')


def song_next():
    global playing
    global now_playing
    global formatted_total_song_time
    global songs_paths
    global total_song_time

    try:
        song = songs_paths[(now_playing + 1) % len(songs_paths)]
        print(songs_paths[(now_playing + 1) % len(songs_paths)])
        now_playing = (now_playing + 1) % len(songs_paths)
    except IndexError:
        song = songs_paths[now_playing % len(songs_paths)]
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
        song_list.select(f"END{now_playing % len(songs_paths)}")

        # slider position
        song_slider.configure(to=total_song_time)
        song_slider.set(0)

        # update time labels
        time_elapsed_label.configure(
            text=f'{time.strftime("%M:%S", time.gmtime(0))}')
        total_time_label.configure(text=f'{formatted_total_song_time}')

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
        song_list.select(f"END{now_playing % len(songs_paths)}")

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
        song_list.select(f"END{now_playing % len(songs_paths)}")

        play_time()


def play_on_click():
    pass


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

# buttons folder path
icon_folder_path = os.path.join(
    os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "assets", "icons")

)

# button icons
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
search_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "search_btn.png")), size=(30, 30)
)


# Create Tabview
master_tab = ctk.CTkTabview(
    master=app,
    width=800,
    height=550,
    corner_radius=10,
    border_width=1,
    border_color='black',
    fg_color='#ebd9c8',
    segmented_button_selected_color='#003f5a',
    segmented_button_selected_hover_color='#4b85a8',
    segmented_button_unselected_hover_color='#7fb8cc',
)
master_tab.pack(pady=50)

# Create tabs
playback_tab = master_tab.add('Home')
search_tab = master_tab.add('Search')

# Search Frame
search_frame = ctk.CTkFrame(search_tab)
search_frame.pack(fill='x', expand=True, padx=10, pady=10)

# Create a search bar
search_bar = ctk.CTkEntry(search_frame)
search_bar.pack(fill='x', expand=True, padx=10, pady=10)

# open search frame
# open_search_frame_button = ctk.CTkButton(search_frame, text="Open Search Frame" , command=open_search_frame)
# open_search_frame_button.pack()

# Create a search button
search_button = ctk.CTkButton(
    search_frame, text="Search", command=search, image=search_button_icon)
search_button.pack(fill='x', expand=True, padx=10, pady=10)

# Create a button to close the search frame and go back to the home screen
# close_search_frame_button = ctk.CTkButton(search_frame, text="Close Search Frame", command=close_search_frame)
# close_search_frame_button.pack(fill='x', expand=True, padx=10, pady=10)

# # Hide the search frame by default
# search_frame.pack_forget()


# song list frame
song_list_frame = ctk.CTkFrame(master=playback_tab, fg_color='#ebd9c8')
song_list_frame.grid(row=1, pady=20, sticky='ew', padx=(20, 20))

# Media Controls Frame
playback_controls_frame = ctk.CTkFrame(
    master=playback_tab, fg_color='black', corner_radius=20)
playback_controls_frame.grid(row=2,  sticky='ew', padx=(20, 20))


# buttons
previous_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=song_previous,
    image=previous_button_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
)
previous_button.grid(row=5, column=5, padx=(10, 10), sticky='ew')

play_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=lambda: play_pause(play_button),
    image=play_button_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
)
play_button.grid(row=5, column=6, padx=(10, 10), sticky='ew')

next_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=song_next,
    image=next_button_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
)
next_button.grid(row=5, column=7, padx=(10, 10), sticky='ew')


song_slider = ctk.CTkSlider(
    master=playback_controls_frame,
    from_=0,
    to=100,
    width=250,
    orientation="horizontal",
    progress_color='orange',
    button_color='#003f5a',
    button_hover_color='blue',
    command=slide
)
song_slider.grid(row=5, column=1, columnspan=3, pady=20, sticky='ew')

# Songs List
song_list = CTkListbox.CTkListbox(
    master=song_list_frame,
    width=700,
    height=120,
    border_width=2,
    border_color='black',
    corner_radius=10,
    label_text="Songs",
    label_anchor='center',
    fg_color="orange",
    text_color="black",
    hightlight_color='red',
    hover_color='#7fb8cc',
)

song_list.grid(row=0, columnspan=9, pady=(10, 30), sticky='ew')

# now playing label
status_bar = ctk.CTkLabel(
    master=playback_tab, text="status bar", justify="center")
status_bar.grid(row=3, pady=(40, 20), sticky='ew')

# time labels
time_elapsed_label = ctk.CTkLabel(
    master=playback_controls_frame, text="--:--", text_color='white')
time_elapsed_label.grid(row=5, column=0, sticky='w', padx=(50, 20))


total_time_label = ctk.CTkLabel(
    master=playback_controls_frame, text="--:--", text_color='white')
total_time_label.grid(row=5, column=4, sticky='e', padx=(20, 50))


recent_label = ctk.CTkLabel(
    app, text="recently played : "+str(functions.get_recents()))
recent_label.pack()


atexit.register(kill_app)

# testing
# test_label = ctk.CTkLabel(app, text='slida text')
# test_label.pack(pady=10)

app.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
app.mainloop()
