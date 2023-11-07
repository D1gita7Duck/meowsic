import customtkinter as ctk
app=ctk.CTk()
app.geometry("900x700")


frame=ctk.CTkScrollableFrame(app,fg_color="#000000",width=500,height=500)
label=ctk.CTkLabel(frame,text="lyric")
frame.pack()
label.pack()
lyric="""[Verse 1]
You were the shadow to my light
Did you feel us?
Another star, you fade away
Afraid our aim is out of sight
Wanna see us alight

[Pre-Chorus]
Where are you now?
Where are you now?
Where are you now?
Was it all in my fantasy?
Where are you now?
Were you only imaginary?

[Chorus]
Where are you now?
Atlantis, under the sea, under the sea
Where are you now? Another dream
The monster's running wild inside of me
I'm faded, I'm faded
So lost, I'm faded, I'm faded
So lost, I'm faded

[Verse 2]
These shallow waters never met what I needed
I'm letting go, a deeper dive
Eternal silence of the sea
I'm breathing, alive
"""

label.configure(text=lyric)

app.mainloop()