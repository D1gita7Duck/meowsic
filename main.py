import os
import pygame.mixer
import remote.server as server
from app.widgets import app,_kill_all

app.geometry(f'{str(app.winfo_screenwidth())}x{str(app.winfo_screenheight())}')
app.title("meowsic")
app.iconbitmap(os.path.join(os.getcwd(),"app","assets", "icons", "app_icon.ico"))

pygame.mixer.init()
server.start()


app.protocol("WM_DELETE_WINDOW", _kill_all)
app.after(0, lambda: app.state('zoomed'))

app.mainloop()
