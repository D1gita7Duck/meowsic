import pygame.mixer
import remote.server as server
from app.widgets import app, _kill_all, show_about_page, show_manual, initialized_items

pygame.mixer.init()
server.start()

# define protocol on killing application
app.protocol("WM_DELETE_WINDOW", _kill_all)

# check whether to display manual and about pages on startup or not
if initialized_items['first_time_startup'] == True:
    app.after(0, show_about_page(_from = 'startup'))
    app.after(5, show_manual(_from = 'startup'))

# make application fullscreen
app.after(5, lambda: app.state('zoomed'))


app.mainloop()