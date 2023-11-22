import customtkinter as ctk
import CTkMenuBar
import CTkListbox
#from app.music import add_songs,search,song_previous,play_pause,song_next,like,slide,main_lyrics,load_liked
import app.music as music
import os
from PIL import Image
import app.functions as functions
import app.import_spotify as import_spotify
import time
import CTkTable
app = ctk.CTk()  # create CTk window like you do with the Tk window
app.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,), weight=1)
app.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

scale_factor=1920/app.winfo_screenwidth()

current_time=time.localtime()

# thumbnails folder path
thumbs_folder_path = os.path.join("thumbs")


# buttons folder path
icon_folder_path = os.path.join(
    os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "assets", "icons")

)
garfield_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "garfield.png")), size=(200//scale_factor, 200//scale_factor)
)
library_button_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "library_icon.png")), size=(30//scale_factor, 30//scale_factor)
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
lyrics_button_icon_white=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path,"song_lyrics_white.png")),size=(30,30)
)
lyrics_button_icon_orange=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path,"song_lyrics_orange.png")),size=(30,30)
)
disliked_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "disliked_btn.png")), size=(30, 30)
)
like_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "like_btn.png")), size=(30, 30)
)
add_to_queue_button_icon= ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "add_queue_btn.png")), size=(30, 30)
)
delete_from_queue_button_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "delete_queue_btn.png")), size=(30, 30)
)
information_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "info_icon.png")), size=(30, 30)
)
volume_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "volume_icon.png")), size=(30, 30)
)
mute_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "mute_icon.png")), size=(30, 30)
)
#define top level import window
def import_win_launch():
    global import_entry
    global import_window
    global import_progress
    
    import_window=ctk.CTkToplevel(app)
    import_window.geometry("300x300")
    import_window.title('Import tracks from Spotify playlist')


    import_entry=ctk.CTkEntry(import_window,placeholder_text="Enter playlist URL")
    import_entry.pack(pady=20)

    import_progress=ctk.CTkProgressBar(import_window,mode="indeterminate")
    import_progress.pack(fill="x",padx=20)


    import_button=ctk.CTkButton(import_window,text="Import",command=music.import_sp_playlist)
    import_button.pack(pady=20)

# menu
menu = CTkMenuBar.CTkMenuBar(app)
menu.lift()
file_button = menu.add_cascade("File")
edit_button = menu.add_cascade("Edit")
settings_button = menu.add_cascade("Settings")
about_button = menu.add_cascade("About")

file_dropdown = CTkMenuBar.CustomDropdownMenu(widget=file_button)
file_dropdown.add_option(option="Open", command=music.add_songs)
file_dropdown.add_option(option="Import Spotify Playlist", command=import_win_launch)
file_dropdown.add_option(option="Save")

file_dropdown.add_separator()

sub_menu = file_dropdown.add_submenu("Export As")
sub_menu.add_option(option=".TXT")
sub_menu.add_option(option=".PDF")

#frame for tabview and metadata and misc frame
big_frame = ctk.CTkFrame(master=app, height=800)
big_frame.pack(pady=(20, 20), anchor='center', fill='x', ipadx=10,)
big_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
big_frame.lower()

# Create Tabview
master_tab = ctk.CTkTabview(
    master=big_frame,
    width=800//scale_factor,
    height=550//scale_factor,
    corner_radius=10,
    border_width=1,
    border_color='black',
    fg_color='#ebd9c8',
    segmented_button_selected_color='#003f5a',
    segmented_button_selected_hover_color='#4b85a8',
    segmented_button_unselected_hover_color='#7fb8cc',
)
master_tab.grid(pady=(10,10), row=0, column=1, columnspan=8, padx=(30,10),)
master_tab._segmented_button.configure(font=('Helvetica', 22,))

# Create tabs
home_tab = master_tab.add('Home')
queue_tab = master_tab.add('Queue')
search_tab = master_tab.add('Search')
liked_songs_tab = master_tab.add('Liked Songs')
your_library_tab=master_tab.add('Your Library')
# home tab stuff
home_tab.grid_columnconfigure((0, 1, 2, 3, 4, 5,), weight=1)

# checking for morning, afternoon, evening
if current_time[3] >= 7 and current_time[3] < 12:
    greeting_text = 'Good Morning'
elif current_time[3] >= 12 and current_time[3] <= 16:
    greeting_text = 'Good Afternoon'
else:
    greeting_text = 'Good Evening'
greeting_label = ctk.CTkLabel(
    master=home_tab, text=greeting_text, font=('Helvetica', 20),text_color="black",width=20,height=20)
greeting_label.grid(row=0, column=5, sticky='ew', pady=(20, 20), columnspan=3,)

# division home tab into two frames
home_tab_recently_played = ctk.CTkFrame(
    master=home_tab, border_color='black', border_width=2)
home_tab_recently_played.grid(
    row=1, columnspan=3, column=6, rowspan=5, sticky='ew' , padx=(20,10))

recently_played_listbox = CTkListbox.CTkListbox(master=home_tab_recently_played,
                                                width=600//scale_factor,
                                                height=300//scale_factor,
                                                border_width=2,
                                                border_color='black',
                                                corner_radius=10,
                                                label_text='Recently Played',
                                                label_font=('Helvetica', 22) ,
                                                font=('Helvetica',18),
                                                label_anchor='center',
                                                fg_color="orange",
                                                text_color="black",
                                                hightlight_color='red',
                                                hover_color='#7fb8cc',)
if functions.get_recents():
    for i in functions.get_recents():
        recently_played_listbox.insert('END', i,onclick=music.load_recents)
recently_played_listbox.grid(columnspan=5, sticky='ew',)

#buttons on home page
home_tab_buttons_frame=ctk.CTkFrame(
    master=home_tab, border_color='black', border_width=2,
)
home_tab_buttons_frame.grid(row=1, column=0, columnspan=3, rowspan=5, sticky='ew', padx=(10,10) ,)
home_tab_buttons_frame.grid_columnconfigure(0, weight=1)

home_tab_your_library_button=ctk.CTkButton(
    master=home_tab_buttons_frame,
    width=200//scale_factor,
    height=50//scale_factor,
    text='Your Library',
    image=library_button_icon,
    anchor='center',
    command=music.show_your_library
)
home_tab_your_library_button.grid(row=0, column=0, columnspan=3, padx=(10,10), pady=(10,10), sticky='ew')

home_tab_liked_songs_button=ctk.CTkButton(
    master=home_tab_buttons_frame,
    width=200//scale_factor,
    height=50//scale_factor,
    text='Liked Songs',
    image=like_button_icon,
    anchor='center',
    command=music.show_liked_songs,
)
home_tab_liked_songs_button.grid(row=1, column=0, columnspan=3, padx=(10,10), pady=(10,10), sticky='ew')

discover_button=ctk.CTkButton(
    master=home_tab_buttons_frame,
    width=200,
    height=50,
    text='Discover',
    anchor='center',
)
discover_button.grid(row=2, column=0, columnspan=3, padx=(10,10), pady=(10,10), sticky='ew')
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
song_list_frame = ctk.CTkFrame(master=queue_tab, fg_color='#ebd9c8' , height=500)
song_list_frame.grid(row=1, pady=20, sticky='ew', padx=(20, 20))

# Media Controls Frame
playback_controls_frame = ctk.CTkFrame(master=app, fg_color='black', corner_radius=20 , width=1250//scale_factor)
playback_controls_frame.pack(side='bottom', pady=(20, 20), ipadx=10, expand=True, anchor='center')  # removed fill='x'
playback_controls_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12), weight=1)
# liked songs frame
liked_songs_frame = ctk.CTkFrame(master=liked_songs_tab)
liked_songs_frame.grid(row=1, pady=(20, 20), padx=(20, 20), sticky='ew')

# song metadata frame
song_metadata_frame = ctk.CTkFrame(
    master=big_frame,
    width=350//scale_factor,
    height=400//scale_factor,
    fg_color='black',
)
song_metadata_frame.grid(row=0, column=7, columnspan=3, rowspan=3, )
song_metadata_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

# misc functions frame (add to playlist, delete from queue, add to queue)
misc_frame=ctk.CTkFrame(master=big_frame, fg_color='black', corner_radius=20)
misc_frame.grid(row=0, column=0, columnspan=3, padx=(10,10) )
misc_frame.grid_columnconfigure(0, weight=1)
misc_frame.grid_rowconfigure((0,1,2), weight=1)
your_library_tab.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1)

your_library_frame=ctk.CTkScrollableFrame(
    master=your_library_tab,
    width=700,
    height=250,
    border_width=0,
    border_color='black',
    corner_radius=10,
    label_text='Playlists',
    label_anchor='center',
    fg_color="orange",
)
your_library_frame.grid(row=0, pady=(20,20), padx=(10,10),sticky='ew')
your_library_frame.grid_columnconfigure((0,1,2,3,4,5),weight=1)
playlist_table_values=[
    ['Name', 'Date Created','Songs','Duration'],
]
for i in functions.get_playlists():
    t=functions.get_playlist_details(i)
    print(t,i)
    playlist_table_values.append(t)
print("VALUES",playlist_table_values)
playlists_table=CTkTable.CTkTable(
    master=your_library_frame,
    values=playlist_table_values,
)
playlists_table.grid(row=0, columnspan=9, sticky='ew')

# your_library_playlists_listbox=CTkListbox.CTkListbox(
#     master=your_library_tab,
#     width=700,
#     height=250,
#     border_width=2,
#     border_color='black',
#     corner_radius=10,
#     label_text='Playlists',
#     label_anchor='center',
#     fg_color="orange",
#     text_color="black",
#     hightlight_color='red',
#     hover_color='#7fb8cc',
# )
# your_library_playlists_listbox.grid(row=0, columnspan=9, pady=(20, 20), padx=(10,10), sticky='ew')
# # add existing playlists into listbox
# for i in [x[0] for x in functions.get_playlists()]:
#     your_liblirary_playlists_listbox.insert('END', i, onclick=music.show_playlist)


# misc frame buttons
add_to_playlist_label_text=ctk.StringVar(value='Add to Playlist')
print(functions.get_playlists())
add_to_playlist_options=[x[0] for x in functions.get_playlists()]
add_to_playlist_options.append('Create New Playlist')
add_to_playlist_menu=ctk.CTkOptionMenu(
    misc_frame,
    width=200//scale_factor,
    height=35//scale_factor,
    command=music.add_to_playlist,
    variable=add_to_playlist_label_text,
    values=add_to_playlist_options,
    state='disabled',
)
add_to_playlist_menu.grid(row=0, column=0, columnspan=2,  padx=(10,10), pady=(20,10), sticky='ew')

# add to queue
# add_to_queue_button=ctk.CTkButton(
#     misc_frame,
#     width=200,
#     height=30,
#     command=music.add_to_queue,
#     text='Add to Queue',
#     image=add_to_queue_button_icon,
#     anchor='center'
# )
# add_to_queue_button.grid(row=1, column=0, columnspan=2, padx=(10,10), pady=(10,20), sticky='ew')

# delete from queue
delete_from_queue_button=ctk.CTkButton(
    misc_frame,
    width=200//scale_factor,
    height=30//scale_factor,
    command=music.delete_from_queue,
    text='Delete from Queue',
    image=delete_from_queue_button_icon,
    anchor='center',
    state='disabled',
)
delete_from_queue_button.grid(row=1, column=0, columnspan=2, padx=(10,10), pady=(10,20), sticky='ew')

#playback controls buttons
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
like_button.grid(row=0, column=0, padx=(30, 10),)

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
previous_button.grid(row=0, column=6, padx=(10, 10), sticky='ew')

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
play_button.grid(row=0, column=7, padx=(10, 10), sticky='ew')

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
next_button.grid(row=0, column=8, padx=(10, 10), sticky='ew')

lyrics_button=ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=music.main_lyrics,
    image=lyrics_button_icon_white,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
lyrics_button.grid(row=0,column=9,padx=(10,30),sticky="ew")
volume_button=ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=music.mute,
    image=volume_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
volume_button.grid(row=0,column=11,padx=(10,30),sticky="ew")
volume_slider = ctk.CTkSlider(
    master=playback_controls_frame,
    from_=0,
    to=100,
    width=150//scale_factor,
    orientation="horizontal",
    progress_color='orange',
    button_color='#003f5a',
    button_hover_color='blue',
    command=music.volume,
    state='disabled'
)
volume_slider.grid(row=0, column=12, columnspan=3, pady=5, sticky='ew')
volume_slider.set(100)
song_slider = ctk.CTkSlider(
    master=playback_controls_frame,
    from_=0,
    to=100,
    width=500//scale_factor,
    orientation="horizontal",
    progress_color='orange',
    button_color='#003f5a',
    button_hover_color='blue',
    command=music.slide,
    state='disabled'
)
song_slider.grid(row=0, column=2, columnspan=3, pady=20, sticky='ew')

# Songs List
song_list = CTkListbox.CTkListbox(
    master=song_list_frame,
    width=700//scale_factor,
    height=120//scale_factor,
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
    width=700//scale_factor,
    height=120//scale_factor,
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
#     master=queue_tab, text="status bar", justify="center")
# status_bar.grid(row=3, pady=(40, 20), sticky='ew')



# time labels
time_elapsed_label = ctk.CTkLabel(
    master=playback_controls_frame, text="--:--", text_color='white')
time_elapsed_label.grid(row=0, column=1, sticky='w', padx=(50, 20))


total_time_label = ctk.CTkLabel(
    master=playback_controls_frame, text="--:--", text_color='white')
total_time_label.grid(row=0, column=5, sticky='e', padx=(20, 50))


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
status_bar = ctk.CTkLabel(master=song_metadata_frame, text='Status Bar', justify="center", text_color='white')
status_bar.grid(row=2, columnspan=3, pady=(10, 20), padx=(10, 10), sticky='ew')


