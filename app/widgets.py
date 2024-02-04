import os
import time
import tkinter
import customtkinter as ctk
import CTkMenuBar
import CTkTable
from PIL import Image, ImageTk
import CTkListbox
import CTkToolTip
import app.music as music
import app.functions as functions
import app.theme as theme
import remote.server as server

# make ctk launch in dark theme
ctk.set_appearance_mode('dark')
# create main application window
app = ctk.CTk()  # create CTk window like you do with the Tk window
app.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,), weight=1)
app.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
app.geometry(f'{str(app.winfo_screenwidth())}x{str(app.winfo_screenheight())}')
app.title("Meowsic")
app.iconbitmap(os.path.join(os.getcwd(),"app","assets", "icons", "app_icon.ico"))


'''FUNCTIONS'''

def initialize_app():
    # get transparency
    transparency=functions.transparency
    # set application's transparency to above transparency
    app.attributes('-alpha', transparency)
    # get scaleing factor
    scale_factor=1920/app.winfo_screenwidth()
    # get current time
    current_time=time.localtime()
    # get theme
    master_theme=functions.current_theme #USE LIGHTMODE AT RISK OF BLINDING YOURSELF
    if master_theme=="dark":
        current_theme=theme.dark_mode
    else:
        current_theme=theme.light_mode
    
    # make dictionary of items to return
    d={'transparency': transparency, 
       'scale_factor': scale_factor, 
       'current_time': current_time, 
       'current_theme': current_theme, 
       'master_theme': master_theme, 
       'first_time_startup': functions.first_time_startup
       }
    return d

initialized_items=initialize_app()
app.configure(fg_color=initialized_items['current_theme']['color1'])

# kill all
def _kill_all():
    """
    destroys app and kills flask
    """
    app.destroy()
    server.kill_app()
    functions.change_transparency(initialized_items['transparency'])


def import_win_launch():
    '''
    Define top level import window
    '''
    global import_entry
    global import_window
    global import_progress
    
    import_window=ctk.CTkToplevel(app,fg_color=initialized_items['current_theme']["color1"])
    import_window.title('Import Playlist')
    import_window.geometry("300x300")
    import_window.title('Import tracks from Spotify playlist')

    import_entry=ctk.CTkEntry(import_window,placeholder_text="Enter playlist URL",fg_color=initialized_items['current_theme']["color1"],border_color=initialized_items['current_theme']["color4"],text_color=initialized_items['current_theme']["color3"],placeholder_text_color=initialized_items['current_theme']["color3"])
    import_entry.pack(pady=20)

    import_progress=ctk.CTkProgressBar(import_window,mode="indeterminate",fg_color=initialized_items['current_theme']["color1"],border_color=initialized_items['current_theme']["color2"],progress_color=initialized_items['current_theme']["color3"])
    import_progress.pack(fill="x",padx=20)


    import_button=ctk.CTkButton(
        import_window,
        text="Import to Playlist",
        command=music.import_sp_playlist_to_new_playlist,
        fg_color=initialized_items['current_theme']["color4"],
        hover_color=initialized_items['current_theme']["color4"],
        border_color=initialized_items['current_theme']["color3"],
        border_width=1,
        text_color=initialized_items['current_theme']["color6"],)
    import_button.pack(pady=20)

    # put the toplevel on top of all windows
    import_window.attributes('-topmost',True)
    import_window.focus()
    

def toggle_theme(t : str):
    '''
    Function to toggle theme.
    Accepts str "dark"/"light" as argument
    '''
    global initialized_items
    global warn_win
    print(initialized_items['current_theme'])
    if t=='dark':
        functions.change_mode("dark")
        ctk.set_appearance_mode('dark')
    else:
        functions.change_mode("light")
        ctk.set_appearance_mode('light')
    if warn_win is None:
        warn_win=ctk.CTkToplevel(app)
        warn_win.title('Warning')
        warn_win.resizable(False,False)
        app.eval(f'tk::PlaceWindow {str(warn_win)} center')
        warn_win.geometry('200x100')
        text_label=ctk.CTkLabel(master=warn_win,
                                text='Restart Required',
                                image=information_icon,
                                compound='left',
                                anchor='center',)
        text_label.pack(pady=(20,20), padx=(10,10), anchor='center')

        # put the toplevel on top of all windows
        warn_win.attributes('-topmost',True)
        warn_win.focus()


def do_popup(_event, frame):
    '''
    Rightclickmenu pops up on calling this function
    '''
    # print('EVENT IS ', _event)
    # print(app.focus_displayof())
    x1 = song_list_frame.winfo_rootx()
    y1 = song_list_frame.winfo_rooty()
    x2=song_list_frame.winfo_width()+x1
    y2=song_list_frame.winfo_height()+y1
    abs_coord_x = app.winfo_pointerx() - app.winfo_vrootx()
    abs_coord_y = app.winfo_pointery() - app.winfo_vrooty()
    print(x1,y1,x2,y2,abs_coord_x,abs_coord_y)
    if (x1<=abs_coord_x and abs_coord_x<=x2) and (y1<=abs_coord_y and abs_coord_y<=y2) and (master_tab.get() not in ['Home', 'Search', 'Discover',]) and music.loaded:
        try: 
            frame.tk_popup(abs_coord_x, abs_coord_y)
        finally: 
            frame.grab_release()

def adjust_transparency(value):
    '''
    Sets transparency to given value. 
    Stored in dict of initialized items
    '''
    app.attributes('-alpha', value)
    initialized_items['transparency']=value

def show_manual(_from = None):
    '''
    Creates a TopLevel to display Manual
    Accepts arg _from to check if function is called on startup or during runtime
    '''
    manual_win=ctk.CTkToplevel(master=app, fg_color=initialized_items['current_theme']["color1"], takefocus=True,)
    # hide window until everything is placed and centered
    manual_win.attributes('-alpha', 0)
    # Title
    manual_win.title('Application Manual')
    manual_win.resizable(False, False)
    # centering the window
    manual_win_width=550
    manual_win_height=550
    screen_width=app.winfo_screenwidth()
    screen_height=app.winfo_screenheight()
    x_coordinate=int((screen_width/2)-(manual_win_width/2))
    y_coordinate = int((screen_height/2) - (manual_win_height/2))
    manual_win.geometry("{}x{}+{}+{}".format(manual_win_width, manual_win_height, x_coordinate, y_coordinate))
    # adding textbox
    manual_textbox=ctk.CTkTextbox(
        master=manual_win,
        width=500,
        height=500,
        text_color='white',
        fg_color = initialized_items['current_theme']["color2"],
        wrap='word',
        font= ('Helvetica', 14),
    )
    manual_textbox.tag_config('important', foreground=initialized_items['current_theme']["color3"])
    manual_textbox.tag_config('center', justify='center')
    manual_textbox.tag_config('underline', underline=1)
    manual_textbox.tag_config('heading', justify='center', relief='raised', underline=1, foreground=initialized_items['current_theme']["color3"])
    # general instructions
    manual_textbox.insert('end', 'The application may freeze or not respond at times, please be patient.\n', ('center','important'))
    manual_textbox.insert('end', 'Please do not spam any button or any widget. It may cause the application to behave abnormally.\n', ('center','important'))
    manual_textbox.insert('end', '\nThe following instructions are tab specific.\n', ('center','underline'))
    # home tab instructions
    manual_textbox.insert('end', '\nHome Tab\n\n', 'heading')
    manual_textbox.insert('end', 'The buttons Your Library, Liked Songs and Discover navigate to their respective tabs.\n', 'center')
    manual_textbox.insert('end', 'Click ONCE on any song in the Recently Played box to load it into queue\n', 'center')
    # queue tab instructions
    manual_textbox.insert('end', '\nQueue Tab\n\n', 'heading')
    manual_textbox.insert('end', 'Here, you can right click on any song and avail a context menu to add a song into a playlist or delete it from queue\n', 'center')
    manual_textbox.insert('end', 'Double click on any song to play it.\n', 'center')
    # search instructions
    manual_textbox.insert('end', '\nSearch Tab\n\n', 'heading')
    manual_textbox.insert('end', 'Search for any song on the internet. Hit Enter or the Search button to search.\n', 'center')
    manual_textbox.insert('end', 'Click ONCE on any of the search results and the respective song will be added to the queue.\n', 'center')
    manual_textbox.insert('end', 'Do not spam the button please\n', 'center')
    # liked songs tab instructions
    manual_textbox.insert('end', '\nLiked Songs Tab\n\n', 'heading')
    manual_textbox.insert('end', 'View all liked songs.\n', 'center')
    manual_textbox.insert('end', 'Here, click ONCE on any song to load it into the queue.\n', 'center')
    # your library tab instructions
    manual_textbox.insert('end', '\nYour Library Tab\n\n', 'heading')
    manual_textbox.insert('end', 'View all playlists. Click on playlist name to open it.\n', 'center')
    manual_textbox.insert('end', "In a playlist's tab, click ONCE on any song to load it into the queue.\n", 'center')
    # discover tab instructions
    manual_textbox.insert('end', '\nDiscover Tab\n\n', 'heading')
    manual_textbox.insert('end', 'Find curated playlists with currently trending songs all over the world.\n', 'center') 
    manual_textbox.insert('end', 'Click on a playlist to open and click ONCE on a song to load it into queue.\n', 'center')
    # keyboard shortcuts
    manual_textbox.insert('end', '\nKeyboard Shortcuts\n\n', 'heading')
    manual_textbox.insert('end', 'Play \t Space/F7\n', 'center')
    manual_textbox.insert('end', 'Previous \t F6\n', 'center')
    manual_textbox.insert('end', 'Next \t F8\n', 'center')
    manual_textbox.configure(state='disabled')

    manual_textbox.pack(padx=(20,20), pady=(20,20))
    # make window opaque
    manual_win.attributes('-alpha', 1)
    # put the window on top if function is triggered within application
    if _from is None:
        manual_win.attributes('-topmost', True)
        manual_win.focus_set()

def show_about_page(_from = None):
    '''
    Creates a Toplevel to display About page
    Accepts arg _from to check if function is called on startup or during runtime
    '''
    about_win=ctk.CTkToplevel(master=app, fg_color=initialized_items['current_theme']["color1"], takefocus=True,)
    # hide window until everything is placed and centered
    about_win.attributes('-alpha', 0)
    # Title
    about_win.title('About')
    about_win.resizable(False, False)
    # centering
    about_win_width=550
    about_win_height=550
    screen_width=app.winfo_screenwidth()
    screen_height=app.winfo_screenheight()
    x_coordinate=int((screen_width/2)-(about_win_width/2))
    y_coordinate = int((screen_height/2) - (about_win_height/2))
    about_win.geometry("{}x{}+{}+{}".format(about_win_width, about_win_height, x_coordinate, y_coordinate))
    about_textbox=ctk.CTkTextbox(
        master=about_win,
        text_color='white',
        fg_color = initialized_items['current_theme']["color2"],
        width=500,
        height=500,
        wrap='word',
        font=('Helvetica', 20)
    )
    about_textbox.tag_config('center', justify='center')
    about_textbox.tag_config('heading', justify='center', relief='raised', underline=1, foreground=initialized_items['current_theme']["color3"], background=initialized_items['current_theme']['color2'], bgstipple='gray50')
    about_textbox.insert('end', 'Meowsic\n', 'heading')
    about_textbox.insert('end', '\nA Free, Open-Source, and Feature-Rich Music Streaming App built in Python\n', 'center')
    about_textbox.insert('end', '\nDisclaimer!\n', 'heading')
    about_textbox.insert('end', '''\nMeowsic does not own or have any affiliation with the songs and other content available through the app.
    All songs and other content are the property of their respective owners and are protected by copyright law.
    Meowsic is not responsible for any infringement of copyright or other intellectual property rights that may result from the use of the songs and other content available through the app. 
    By using the app, you agree to use the songs and other content only for personal, non-commercial purposes and in compliance with all applicable laws and regulations.\n
                        ''', 'center')
    about_textbox.insert('end', '\nFor more information, visit \nhttps://github.com/D1gita7Duck/meowsic', 'center')
    about_textbox.configure(state='disabled')

    about_textbox.pack(pady=(20,20), padx=(20,20))
    # make window visible
    about_win.attributes('-alpha', 1)
    # put the window on top if function is triggered within application
    if _from is None:
        about_win.attributes('-topmost', True)
        about_win.focus_set()

def open_playlist(value):
    #value is dictionary of kwargs of CTkTable
    music.show_playlist(value)

def open_discover_playlist(value):
    music.show_discover_playlist(value)

####

'''ICONS'''
# thumbnails folder path
thumbs_folder_path = os.path.join("thumbs")

# buttons folder path
icon_folder_path = os.path.join(
    os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "assets", "icons")
    )

# db folder path
db_folder_path = os.path.join(
    os.path.join(os.path.dirname(
        os.path.realpath(__file__)),)
    ).replace('app','data')

garfield_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "garfield.png")), size=(225//initialized_items['scale_factor'], 225//initialized_items['scale_factor'])
)
library_button_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "library_icon.png")), size=(30//initialized_items['scale_factor'], 30//initialized_items['scale_factor'])
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
delete_from_queue_tk_button_icon=ImageTk.PhotoImage(
    Image.open(os.path.join(icon_folder_path, "delete_queue_btn.png")).resize((30,30))
)
add_to_playlist_button_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "add_to_playlist_icon.png")), size=(30, 30)
)
add_to_playlist_tk_button_icon=ImageTk.PhotoImage(
    Image.open(os.path.join(icon_folder_path, "add_to_playlist_icon.png")).resize((30,30))
)
delete_playlist_button_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "delete_playlist_btn.png")), size=(30, 30)
)
discover_button_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "discover_btn.png")), size=(30, 30)
)
queue_all_songs_button_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "queue_all_songs_btn.png")), size=(30, 30)
)

information_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "info_icon.png")), size=(30, 30)
)
volume_full_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "volume_full.png")), size=(30, 30)
)
volume_2bar_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "volume_2bar.png")), size=(30, 30)
)
volume_1bar_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "volume_1bar.png")), size=(30, 30)
)
mute_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "mute_icon.png")), size=(30, 30)
)



'''WIDGETS'''

warn_win=None


# menu
menu = CTkMenuBar.CTkMenuBar(app)
menu.lift()
file_button = menu.add_cascade("File")
# edit_button = menu.add_cascade("Edit")
options_button = menu.add_cascade("Options")
help_button = menu.add_cascade("Help")

# file tab
file_dropdown = CTkMenuBar.CustomDropdownMenu(widget=file_button)
file_dropdown.add_option(option="Open", command=music.add_songs)
file_dropdown.add_option(option="Import Spotify Playlist", command=import_win_launch)

file_dropdown.add_separator()

file_dropdown.add_option(option="Exit", command=_kill_all)

# sub_menu = file_dropdown.add_submenu("Export As")
# sub_menu.add_option(option=".TXT")
# sub_menu.add_option(option=".PDF")

# options tab
options_dropdown=CTkMenuBar.CustomDropdownMenu(widget=options_button)

# light and dark mode toggle button
theme_switch=ctk.CTkSwitch(
    master=options_dropdown,
    onvalue='dark',
    offvalue='light',
    text='Dark Mode',
    command=lambda: toggle_theme(theme_switch.get()),
)
theme_switch.pack(pady=(10,10), padx=(10,10), anchor='center',fill='x',)
if initialized_items['master_theme']=="dark":
    theme_switch.select()
else:
    theme_switch.deselect()

options_dropdown.add_separator()

options_dropdown.add_option(option='Adjust Transparency', state='disabled')
transparency_slider=ctk.CTkSlider(
    master=options_dropdown,
    from_=0,
    to=1,
    state='normal',
    progress_color=initialized_items['current_theme']["color3"],
    button_color=initialized_items['current_theme']["color4"],
    button_hover_color=initialized_items['current_theme']["color5"],
    orientation="horizontal",
    command=adjust_transparency,
    width=100,
)
transparency_slider.set(initialized_items['transparency'])
transparency_slider.pack(pady=(0,10), padx=(10,10), anchor='center', fill='x')


# help tab stuff
help_dropdown=CTkMenuBar.CustomDropdownMenu(widget=help_button,)
# add option of manual
help_dropdown.add_option(option='Manual', command=show_manual)
# add option of About
help_dropdown.add_option(option='About', command=show_about_page)


#frame for tabview and metadata and misc frame
big_frame = ctk.CTkFrame(master=app, height=800,fg_color=initialized_items['current_theme']["color1"],border_width=0)
big_frame.pack(pady=(20, 20), anchor='center', fill='x', ipadx=10)
big_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
big_frame.lower()

# Create Tabview
master_tab = ctk.CTkTabview(
    master=big_frame,
    width=800//initialized_items['scale_factor'],
    height=550//initialized_items['scale_factor'],
    corner_radius=10,
    border_width=2,
    border_color=initialized_items['current_theme']["color3"],
    fg_color=initialized_items['current_theme']["color2"],
    segmented_button_selected_color=initialized_items['current_theme']["color1"],
    segmented_button_selected_hover_color=initialized_items['current_theme']["color2"],
    segmented_button_unselected_hover_color=initialized_items['current_theme']["color4"],
)
master_tab.grid(pady=(10,10), row=0, column=1, columnspan=8, padx=(30,10),)
master_tab._segmented_button.configure(font=('Helvetica', 22,))

# Create tabs
home_tab = master_tab.add('Home')
queue_tab = master_tab.add('Queue')
search_tab = master_tab.add('Search')
liked_songs_tab = master_tab.add('Liked Songs')
your_library_tab=master_tab.add('Your Library')
discover_tab=master_tab.add("Discover")
# home tab stuff
home_tab.grid_columnconfigure((0, 1, 2, 3, 4, 5,), weight=1)

# checking for morning, afternoon, evening
if initialized_items['current_time'][3] >= 7 and initialized_items['current_time'][3] < 12:
    greeting_text = 'Good Morning'
elif initialized_items['current_time'][3] >= 12 and initialized_items['current_time'][3] <= 16:
    greeting_text = 'Good Afternoon'
else:
    greeting_text = 'Good Evening'
greeting_label = ctk.CTkLabel(
    master=home_tab, text=greeting_text, font=('Helvetica', 20),text_color=initialized_items['current_theme']["color3"],width=20,height=20)
greeting_label.grid(row=0, column=5, sticky='ew', pady=(20, 20), columnspan=3,)

# division home tab into two frames
home_tab_recently_played = ctk.CTkFrame(
    master=home_tab, border_color='black', border_width=2)
home_tab_recently_played.grid(
    row=1, columnspan=3, column=6, rowspan=5, sticky='ew' , padx=(20,10))

recently_played_listbox = CTkListbox.CTkListbox(master=home_tab_recently_played,
                                                width=500//initialized_items['scale_factor'],
                                                height=200//initialized_items['scale_factor'],
                                                border_width=2,
                                                corner_radius=10,
                                                label_text='Recently Played',
                                                label_font=('Helvetica', 22) ,
                                                font=('Helvetica',18),
                                                label_anchor='center',
                                                border_color=initialized_items['current_theme']["color3"],
                                                fg_color=initialized_items['current_theme']["color3"],
                                                text_color=initialized_items['current_theme']["color6"],
                                                hightlight_color=initialized_items['current_theme']["color6"],
                                                hover_color=initialized_items['current_theme']["color4"],
                                                select_color=initialized_items['current_theme']["color5"],)
if functions.get_recents():
    for i in functions.get_recents():
        recently_played_listbox.insert('END', i,onclick=music.load_recents)
recently_played_listbox.grid(columnspan=5, sticky='ew',)

#buttons on home page
home_tab_buttons_frame=ctk.CTkFrame(
    master=home_tab, border_color=initialized_items['current_theme']["color3"], border_width=2,fg_color=initialized_items['current_theme']["color2"]
)
home_tab_buttons_frame.grid(row=1, column=0, columnspan=3, rowspan=5, sticky='ew', padx=(10,10) ,)
home_tab_buttons_frame.grid_columnconfigure(0, weight=1)

home_tab_your_library_button=ctk.CTkButton(
    master=home_tab_buttons_frame,
    width=200//initialized_items['scale_factor'],
    height=50//initialized_items['scale_factor'],
    text='Your Library',
    image=library_button_icon,
    fg_color=initialized_items['current_theme']["color4"],
    hover_color=initialized_items['current_theme']["color4"],
    border_color=initialized_items['current_theme']["color6"],
    border_width=1,
    text_color=initialized_items['current_theme']["color6"],
    anchor='center',
    command=music.show_your_library
)
home_tab_your_library_button.grid(row=0, column=0, columnspan=3, padx=(10,10), pady=(10,10), sticky='ew')

home_tab_liked_songs_button=ctk.CTkButton(
    master=home_tab_buttons_frame,
    width=200//initialized_items['scale_factor'],
    height=50//initialized_items['scale_factor'],
    text='Liked Songs',
    image=like_button_icon,
    anchor='center',
    command=music.show_liked_songs,
    fg_color=initialized_items['current_theme']["color4"],
    hover_color=initialized_items['current_theme']["color4"],
    border_color=initialized_items['current_theme']["color6"],
    border_width=1,
    text_color=initialized_items['current_theme']["color6"]
)
home_tab_liked_songs_button.grid(row=1, column=0, columnspan=3, padx=(10,10), pady=(10,10), sticky='ew')

discover_button=ctk.CTkButton(
    master=home_tab_buttons_frame,
    width=200//initialized_items['scale_factor'],
    height=50//initialized_items['scale_factor'],
    text='Discover     ',
    image=discover_button_icon,
    anchor='center',
    command=music.show_discover,
    fg_color=initialized_items['current_theme']["color4"],
    hover_color=initialized_items['current_theme']["color4"],
    border_color=initialized_items['current_theme']["color6"],
    border_width=1,
    text_color=initialized_items['current_theme']["color6"]
)
discover_button.grid(row=2, column=0, columnspan=3, padx=(10,10), pady=(10,10), sticky='ew')
# Search Frame
search_frame = ctk.CTkFrame(search_tab,fg_color=initialized_items['current_theme']["color1"])
search_frame.pack(fill='x', expand=True, padx=10, pady=10)

# Create a search bar
search_bar = ctk.CTkEntry(search_frame,fg_color=initialized_items['current_theme']["color1"],border_color=initialized_items['current_theme']["color4"],text_color=initialized_items['current_theme']["color3"],placeholder_text="Search",placeholder_text_color=initialized_items['current_theme']["color3"])
search_bar.pack(fill='x', expand=True, padx=10, pady=10)

search_progress=ctk.CTkProgressBar(search_frame,mode="indeterminate",fg_color=initialized_items['current_theme']["color1"],border_color=initialized_items['current_theme']["color2"],progress_color=initialized_items['current_theme']["color3"])
search_progress.pack(fill="x",padx=10)


# Create a search button
search_button = ctk.CTkButton(
    search_frame, 
    text="Search", 
    command=music.search, 
    image=search_button_icon,
    fg_color=initialized_items['current_theme']["color4"],
    hover_color=initialized_items['current_theme']["color4"],
    border_color=initialized_items['current_theme']["color3"],
    border_width=1,
    text_color=initialized_items['current_theme']["color6"],)  
search_button.pack(fill='x', expand=True, padx=10, pady=10)

search_listbox = CTkListbox.CTkListbox(
    master=search_frame,
    width=500//initialized_items['scale_factor'],
    height=50//initialized_items['scale_factor'],
    border_width=2,
    corner_radius=10,
    label_text='Search Results',
    label_font=('Helvetica', 22) ,
    font=('Helvetica',18),
    label_anchor='center',
    border_color=initialized_items['current_theme']["color3"],
    fg_color=initialized_items['current_theme']["color3"],
    text_color=initialized_items['current_theme']["color6"],
    hightlight_color=initialized_items['current_theme']["color6"],
    hover_color=initialized_items['current_theme']["color4"],
    select_color=initialized_items['current_theme']["color5"],
)

# song list frame
song_list_frame = ctk.CTkFrame(master=queue_tab, height=500,fg_color=initialized_items['current_theme']["color2"],border_width=0)
song_list_frame.grid(row=1, pady=20, sticky='ew', padx=(20, 20))

# Media Controls Frame
playback_controls_frame = ctk.CTkFrame(master=app, fg_color=initialized_items['current_theme']["color2"], corner_radius=20 , width=1250//initialized_items['scale_factor'])
playback_controls_frame.pack(side='bottom', pady=(20, 20), ipadx=10, expand=True, anchor='center')  # removed fill='x'
playback_controls_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12), weight=1)
# liked songs frame
liked_songs_frame = ctk.CTkFrame(master=liked_songs_tab,fg_color=initialized_items['current_theme']["color2"],border_width=0)
liked_songs_frame.grid(row=1, pady=(20, 20), padx=(20, 20), sticky='ew')

# song metadata frame
song_metadata_frame = ctk.CTkFrame(
    master=big_frame,
    width=350//initialized_items['scale_factor'],
    height=400//initialized_items['scale_factor'],
    fg_color=initialized_items['current_theme']["color2"],
    border_color=initialized_items['current_theme']["color3"],
    border_width=2
)
song_metadata_frame.grid(row=0, column=7, columnspan=3, rowspan=3,sticky="e")
song_metadata_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

# misc functions frame (add to playlist, delete from queue, add to queue)
misc_frame=ctk.CTkFrame(
    master=big_frame,
    fg_color=initialized_items['current_theme']["color2"],
    corner_radius=20,
    border_width=2,
    border_color=initialized_items['current_theme']["color3"],
)

misc_frame.grid(row=0, column=0, columnspan=3, padx=(10,10) )
misc_frame.grid_columnconfigure(0, weight=1)
misc_frame.grid_rowconfigure((0,1,2), weight=1)

# unmap misc_frame, add to playlist and delete from queue are available in context menu
misc_frame.grid_forget()

# your library stuff
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
    fg_color=initialized_items['current_theme']["color3"],
)
your_library_frame.grid(row=0, pady=(20,20), padx=(10,10),sticky='ew')
your_library_frame.grid_columnconfigure((0,1,2,3,4,5),weight=1)

playlist_table_values=[
    ['Name', 'Date Created','Songs','Duration'],
]

for i in functions.get_playlists():
    t=functions.get_playlist_details(i)
    print('playlist_details',t,i)
    playlist_table_values.append(t)


playlists_table=CTkTable.CTkTable(
    master=your_library_frame,
    values=playlist_table_values,
    command=open_playlist,
    fg_color=initialized_items['current_theme']["color2"]
)
playlists_table.grid(row=0, columnspan=9, sticky='ew')

discover_tab.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1)

discover_frame=ctk.CTkScrollableFrame(
    master=discover_tab,
    width=700,
    height=250,
    border_width=0,
    border_color='black',
    corner_radius=10,
    label_text='Recommended Playlists',
    label_anchor='center',
    fg_color=initialized_items['current_theme']["color3"],
)
discover_frame.grid(row=0, pady=(20,20), padx=(10,10),sticky='ew')
discover_frame.grid_columnconfigure((0,1,2,3,4,5),weight=1)

discover_table_values=[] 
rec_playlists=functions.get_recommmended_playlist()
for name in rec_playlists.keys():
    discover_table_values.append([name])

discover_table=CTkTable.CTkTable(
    master=discover_frame,
    values=discover_table_values,
    command=open_discover_playlist,
    fg_color=initialized_items['current_theme']["color2"]
)
discover_table.grid(row=0, columnspan=9, sticky='ew')

# misc frame buttons
add_to_playlist_label_text=ctk.StringVar(value='Add to Playlist')
print(functions.get_playlists())
add_to_playlist_options=['Create New Playlist'] + [x[0] for x in functions.get_playlists()]

add_to_playlist_menu=ctk.CTkOptionMenu(
    misc_frame,
    width=200//initialized_items['scale_factor'],
    height=35//initialized_items['scale_factor'],
    command=music.add_to_playlist,
    variable=add_to_playlist_label_text,
    values=add_to_playlist_options,
    state='disabled',
    fg_color=initialized_items['current_theme']["color4"],
    text_color=initialized_items['current_theme']["color6"]
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
    width=30//initialized_items['scale_factor'],
    height=30//initialized_items['scale_factor'],
    command=music.delete_from_queue,
    text='Delete from Queue',
    #image=delete_from_queue_button_icon,
    anchor='center',
    state='disabled',
    fg_color=initialized_items['current_theme']["color4"],
    hover_color=initialized_items['current_theme']["color4"],
    border_color=initialized_items['current_theme']["color3"],
    border_width=1,
    text_color=initialized_items['current_theme']["color6"]
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
    command=music.mute_unmute,
    image=volume_full_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
volume_button.grid(row=0,column=11,padx=(10,10),sticky="ew")

volume_slider = ctk.CTkSlider(
    master=playback_controls_frame,
    from_=0,
    to=100,
    width=150//initialized_items['scale_factor'],
    orientation="horizontal",
    progress_color=initialized_items['current_theme']["color3"],
    button_color=initialized_items['current_theme']["color4"],
    button_hover_color=initialized_items['current_theme']["color5"],
    command=music.volume,
    state='disabled'
)
volume_slider.grid(row=0, column=12, columnspan=3, pady=5, sticky='ew', padx=(10,30))
volume_slider.set(100)

song_slider = ctk.CTkSlider(
    master=playback_controls_frame,
    from_=0,
    to=100,
    width=500//initialized_items['scale_factor'],
    orientation="horizontal",
    progress_color=initialized_items['current_theme']["color3"],
    button_color=initialized_items['current_theme']["color4"],
    button_hover_color=initialized_items['current_theme']["color5"],
    command=music.slide,
    state='disabled'
)
song_slider.grid(row=0, column=2, columnspan=3, pady=20, sticky='ew')

# Songs List
song_list = CTkListbox.CTkListbox(
    master=song_list_frame,
    width=700//initialized_items['scale_factor'],
    height=120//initialized_items['scale_factor'],
    border_width=2,
    corner_radius=10,
    label_text="Songs",
    label_anchor='center',
    border_color=initialized_items['current_theme']["color2"],
    fg_color=initialized_items['current_theme']["color3"],
    text_color=initialized_items['current_theme']["color6"],
    hightlight_color=initialized_items['current_theme']["color2"],
    hover_color=initialized_items['current_theme']["color4"],
    select_color=initialized_items['current_theme']["color5"],
)

song_list.grid(row=0, columnspan=9, pady=(10, 30), sticky='ew')

# liked songs listbox
liked_songs_listbox = CTkListbox.CTkListbox(
    master=liked_songs_frame,
    width=700//initialized_items['scale_factor'],
    height=120//initialized_items['scale_factor'],
    border_width=2,
    corner_radius=10,
    label_text='Liked Songs',
    label_anchor='center',
    fg_color=initialized_items['current_theme']["color3"],
    text_color=initialized_items['current_theme']["color6"],
    hightlight_color=initialized_items['current_theme']["color2"],
    hover_color=initialized_items['current_theme']["color4"],
    select_color=initialized_items['current_theme']["color5"],
)

liked_songs_listbox.grid(row=0, columnspan=9, pady=(20, 20), sticky='ew')

for i in functions.get_liked_songs():
    liked_songs_listbox.insert("END",i["pretty_name"],onclick=music.load_liked)


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
status_bar = ctk.CTkTextbox(
    master=song_metadata_frame,
    height=40//initialized_items['scale_factor'],
    text_color='white',
    wrap='none',
    fg_color = initialized_items['current_theme']["color2"],
)

status_bar.grid(row=2, columnspan=3, pady=(10, 20), padx=(10, 10), sticky='ew')
status_bar.tag_config('center', justify='center')
status_bar.insert('end', 'Status Bar', 'center')
status_bar.configure(state='disabled')

# context menu to add songs to playlist and delete them from queue
RightClickMenu = tkinter.Menu(song_list, tearoff=False, background='#565b5e', fg='white', borderwidth=0, bd=0)
# adding delete from queue command
RightClickMenu.add_command(
    label=" Delete From Queue",
    command=music.delete_from_queue,
    image=delete_from_queue_tk_button_icon,
    compound='left',
)

# submenu for add to playlist commands
add_to_playlist_submenu=tkinter.Menu(RightClickMenu)

# create a cascade for adding to playlist
RightClickMenu.add_cascade(
    label=' Add to Playlist',
    menu=add_to_playlist_submenu,
    image=add_to_playlist_tk_button_icon,
    compound='left',
)

# add all playlists into the cascade
for playlist_name in add_to_playlist_options:
    add_to_playlist_submenu.add_command(label=playlist_name,command= lambda name=playlist_name:music.add_to_playlist(name))


'''ToolTips for Widgets'''
play_tooltip=CTkToolTip.CTkToolTip(play_button, delay=0.2 ,message='Play', justify='center', alpha=0.85, x_offset=10,)
previous_tooltip=CTkToolTip.CTkToolTip(previous_button, delay=0.2 ,message='Previous Song', justify='center',alpha=0.85, x_offset=10,)
next_tooltip=CTkToolTip.CTkToolTip(next_button, delay=0.2 ,message='Next Song', justify='center',alpha=0.85, x_offset=10,)
volume_slider_tooltip=CTkToolTip.CTkToolTip(volume_slider, delay=0.2 ,message='Volume', justify='center',alpha=0.85, x_offset=10,)
volume_button_tooltip=CTkToolTip.CTkToolTip(volume_button, delay=0.2, message='Mute', justify='center',alpha=0.85, x_offset=10,)
lyrics_tooltip=CTkToolTip.CTkToolTip(lyrics_button, delay=0.2 ,message='Show Lyrics', justify='center',alpha=0.85, x_offset=10,)
like_button_tooltip=CTkToolTip.CTkToolTip(like_button, delay=0.2 ,message='Like Song', justify='center',alpha=0.85, x_offset=10,)


'''Key Bindings'''
# bind mouse1
# <1> is a synonym for <ButtonPress-1> (aka left mouse button)
app.bind_all('<1>', lambda event: music.on_single_mouse_click(_event=event), add=True)
# bind mouse1 double-click to play a song
app.bind_all('<Double-Button-1>', lambda event: music.on_double_mouse_click(_event=event), add=True)
# bind space key to play/pause
app.bind('<space>', lambda event: music.play_pause(play_button, _event=event) if (type(app.focus_get())!=tkinter.Entry and music.loaded) else print('Focus in EntryBox (or) Music not loaded'))
# bind f8 to song_next
app.bind('<F8>', lambda event: music.song_next(_event=event) if music.loaded else print('Music not loaded'))
# bind f7 to play_pause
app.bind('<F7>', lambda event: music.play_pause(play_button, _event=event) if music.loaded else print('Music not loaded'))
# bind f6 to song_previous
app.bind('<F6>', lambda event: music.song_previous(_event=event) if music.loaded else print('Music not loaded'))
# bind enter key to search the song
app.bind('<Return>', lambda event: music.search())
# bind mouserightclick to popup the context menu
song_list.bind("<Button-3>", lambda event: do_popup(event, frame=RightClickMenu))