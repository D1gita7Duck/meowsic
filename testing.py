import customtkinter


def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)
    file= customtkinter.filedialog.askopenfilenames(initialdir='H:\Arnav\Python\Python Workspace\meowsic\\Audio', title='Choose Song')
    print(file)


app=customtkinter.CTk()
app.geometry('500x500')
optionmenu_var = customtkinter.StringVar(value="choose")
optionmenu = customtkinter.CTkOptionMenu(app,values=["add songs", "option 2"],command=optionmenu_callback, variable=optionmenu_var )
optionmenu.pack(pady=20)

def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

combobox_var = customtkinter.StringVar(value="option 2")
combobox = customtkinter.CTkComboBox(app, values=["option 1", "option 2"],
                                     command=combobox_callback, variable=combobox_var)
combobox_var.set("option 2")
combobox.pack(pady=50)

def segmented_button_callback(value):
    print("segmented button clicked:", value)

segemented_button_var = customtkinter.StringVar(value="Value 1")
segemented_button = customtkinter.CTkSegmentedButton(app, values=["Value 1", "Value 2", "Value 3"],
                                                     command=segmented_button_callback,
                                                     variable=segemented_button_var)

segemented_button.pack()

app.mainloop()