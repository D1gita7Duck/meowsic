import customtkinter as ctk
import CTkMenuBar
import CTkListbox
#from app.music import add_songs,search,song_previous,play_pause,song_next,like,slide,main_lyrics,load_liked
import app.music as music
import os
from PIL import Image
import app.functions as functions
app = ctk.CTk()  # create CTk window like you do with the Tk window

# menu
menu = CTkMenuBar.CTkMenuBar(app)
file_button = menu.add_cascade("File")
edit_button = menu.add_cascade("Edit")
settings_button = menu.add_cascade("Settings")
about_button = menu.add_cascade("About")

file_dropdown = CTkMenuBar.CustomDropdownMenu(widget=file_button)
file_dropdown.add_option(option="Open", command=music.add_songs)
file_dropdown.add_option(option="Save")

file_dropdown.add_separator()

sub_menu = file_dropdown.add_submenu("Export As")
sub_menu.add_option(option=".TXT")
sub_menu.add_option(option=".PDF")

# thumbnails folder path
thumbs_folder_path = os.path.join("thumbs")


# buttons folder path
icon_folder_path = os.path.join(
    os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "assets", "icons")

)
garfield_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "garfield.png")), size=(200, 250)
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
mic_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path,"mic.png")),size=(30,30)
)
disliked_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "disliked_btn.png")), size=(30, 30)
)
like_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "like_btn.png")), size=(30, 30)
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
liked_songs_tab = master_tab.add('Liked Songs')
# Search Frame
search_frame = ctk.CTkFrame(search_tab)
search_frame.pack(fill='x', expand=True, padx=10, pady=10)

# Create a search bar
search_bar = ctk.CTkEntry(search_frame)
search_bar.pack(fill='x', expand=True, padx=10, pady=10)

search_progress=ctk.CTkProgressBar(search_frame,mode="indeterminate")
search_progress.pack(fill="x",padx=10)

# open search frame
# open_search_frame_button = ctk.CTkButton(search_frame, text="Open Search Frame" , command=open_search_frame)
# open_search_frame_button.pack()

# Create a search button
search_button = ctk.CTkButton(
    search_frame, text="Search", command=music.search, image=search_button_icon)
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

liked_songs_frame = ctk.CTkFrame(
    master=liked_songs_tab
)
liked_songs_frame.grid(row=1, pady=(20, 20), padx=(20, 20), sticky='ew')

song_metadata_frame = ctk.CTkFrame(
    master=playback_tab,
    width=300,
    height=400,
    fg_color='black',
)
song_metadata_frame.grid(row=1, column = 11, columnspan=3, rowspan=3, padx=(10,10)) 
song_metadata_frame.grid(row=0, column=11, columnspan=3,
                         rowspan=3, padx=(10, 10))
song_metadata_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
# buttons
previous_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=music.song_previous,
    image=previous_button_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state="disabled"
)
previous_button.grid(row=5, column=6, padx=(10, 10), sticky='ew')

play_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=lambda: music.play_pause(play_button),
    image=play_button_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
play_button.grid(row=5, column=7, padx=(10, 10), sticky='ew')

next_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=music.song_next,
    image=next_button_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
next_button.grid(row=5, column=8, padx=(10, 10), sticky='ew')

lyrics_button=ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=music.main_lyrics,
    image=mic_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
lyrics_button.grid(row=5,column=9,padx=(10,10),sticky="ew")

like_button = ctk.CTkButton(
    playback_controls_frame,
    text='',
    command=lambda: music.like(like_button),
    image=disliked_button_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
like_button.grid(row=5, column=0, padx=(30, 10),)


song_slider = ctk.CTkSlider(
    master=playback_controls_frame,
    from_=0,
    to=100,
    width=250,
    orientation="horizontal",
    progress_color='orange',
    button_color='#003f5a',
    button_hover_color='blue',
    command=music.slide,
    state='disabled'
)
song_slider.grid(row=5, column=2, columnspan=3, pady=20, sticky='ew')

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

liked_songs_listbox = CTkListbox.CTkListbox(
    master=liked_songs_frame,
    width=700,
    height=120,
    border_width=2,
    border_color='black',
    corner_radius=10,
    label_text='Liked Songs',
    label_anchor='center',
    fg_color="orange",
    text_color="black",
    hightlight_color='red',
    hover_color='#7fb8cc',
)

liked_songs_listbox.grid(row=0, columnspan=9, pady=(20, 20), sticky='ew')
for i in functions.get_liked_songs():
    liked_songs_listbox.insert("END",i["pretty_name"],onclick=music.load_liked)
# now playing label
# status_bar = ctk.CTkLabel(
#     master=playback_tab, text="status bar", justify="center")
# status_bar.grid(row=3, pady=(40, 20), sticky='ew')

# time labels
time_elapsed_label = ctk.CTkLabel(
    master=playback_controls_frame, text="--:--", text_color='white')
time_elapsed_label.grid(row=5, column=1, sticky='w', padx=(50, 20))


total_time_label = ctk.CTkLabel(
    master=playback_controls_frame, text="--:--", text_color='white')
total_time_label.grid(row=5, column=5, sticky='e', padx=(20, 50))


recent_label = ctk.CTkLabel(
    app, text="recently played : "+str(functions.get_recents()))
recent_label.pack()

# song metadata labels

# album art label
song_metadata_image_label = ctk.CTkLabel(
    song_metadata_frame, text='', image=garfield_icon,)
song_metadata_image_label.grid(row=0, columnspan=3, sticky='new', )

# artist name label
song_metadata_artist_label = ctk.CTkLabel(
    song_metadata_frame, text='Artist: Garfield', text_color='white')
song_metadata_artist_label.grid(row=1, columnspan=3, sticky='ew', pady=(20, 10))

# now playing label
status_bar = ctk.CTkLabel(
    master=song_metadata_frame, text='Status Bar', justify="center", text_color='white')
status_bar.grid(row=2, columnspan=3, pady=(10, 20), padx=(10, 10), sticky='ew')
