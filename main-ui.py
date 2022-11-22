import tkinter as tk
import os 
import sys
import pyperclip
from static_config_parser import StaticConfigParser
from tkinter import ttk
from tkinter import simpledialog 
import engine

os.chdir(sys.path[0])

class PWControlApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (LoginPage, MenuPage, AddAccounts, LoadAccounts):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.ShowFrame('LoginPage')

    def ShowFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.attempt_count = 0
        
        logo = tk.PhotoImage(file="logo.png")
        LogoImage = tk.Label(self,image=logo)
        LogoImage.image = logo
        LogoImage.place(x=0,y=0,width=285,height=250)    
            
        config = StaticConfigParser()
        self.master_password = config.get('LOGIN', 'master_password')
        
        self.login_label = tk.Label(self, text="Master Password: ", font='arial 11')
        self.login_label.place(x=10,y=230)
        
        self.masterpass_entry = tk.Entry(self, show='*')
        self.masterpass_entry.place(x=140,y=233)

        self.LoginButton = tk.Button(self, text="Login",command=self.LoginButton)
        self.LoginButton.place(x=70,y=280,width=150,height=30)
    
    def LoginButton(self):
        password = self.masterpass_entry.get()
        if password == self.master_password:
            self.controller.ShowFrame('MenuPage')
        else:
            self.attempt_count += 1
            self.incorrect_password_alert = tk.Label(self, text=f"Incorrect password({self.attempt_count})", fg='red')
            self.incorrect_password_alert.place(x=85,y=250)
            self.masterpass_entry.delete(0, 'end')

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
           
        logo = tk.PhotoImage(file="logo.png")
        LogoImage = tk.Label(self,image=logo)
        LogoImage.image = logo
        LogoImage.place(x=0,y=0,width=285,height=250)

        add_account_button = tk.Button(self, text="Add new account", 
                        command=lambda: self.controller.ShowFrame('AddAccounts'))
        add_account_button.place(x=70,y=240,width=150,height=30)
        
        load_account_button = tk.Button(self, text="Load account", 
                        command=lambda: self.controller.ShowFrame('LoadAccounts'))
        load_account_button.place(x=70,y=280,width=150,height=30)
        
        change_masterpass_button = tk.Button(self, text="Change Master Password", command = self.MasterPassChangeDialog)
        change_masterpass_button.place(x=70,y=320,width=150,height=30)
        
    def MasterPassChangeDialog(self):
        new_mp = simpledialog.askstring('Change Master Password','Set a new master password:')
        engine.ChangeMasterPass(new_mp)


class AddAccounts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Canvas(self,width=200, height=200).pack()
        logo = tk.PhotoImage(file="logo.png")
        LogoImage = tk.Label(self,image=logo)
        LogoImage.image = logo
        LogoImage.place(x=0,y=0,width=285,height=250)

        ttk.Label(self, text="    Website/Service").pack(anchor='w')

        self.service_entry = ttk.Entry(self, width=32)
        self.service_entry.pack()
        self.service_entry.focus()

        ttk.Label(self, text="    Username").pack( anchor='w')

        self.username_entry = ttk.Entry(self, width=32)
        self.username_entry.pack()

        ttk.Label(self, text="    Password").pack(anchor='w')

        self.password_entry = ttk.Entry(self, width=32)
        self.password_entry.pack()

        pass_gen_button = ttk.Button(self, text="Generate Password", command = self.GeneratePassword)
        pass_gen_button.pack()

        save_account_button = tk.Button(self, text="Save", width=20,height=2, command = self.SaveAccount)
        save_account_button.pack()        
 
        home_button = tk.Button(self, text="Home", width=10,height=1,
                        command = lambda: self.controller.ShowFrame('MenuPage'))
        home_button.place(x=0,y=0)        
        
        load_account_button = tk.Button(self, text="Load account", width=10,height=1,
                        command = lambda: self.controller.ShowFrame('LoadAccounts'))
        load_account_button.place(x=80,y=0)
        
    def GeneratePassword(self):
        pw = engine.GenerateSecurePassword()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, pw)
        pyperclip.copy(pw)
        
    def SaveAccount(self):
        engine.SavePassword(self.username_entry.get(), self.service_entry.get(), self.password_entry.get())
        

class LoadAccounts(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        
        tk.Canvas(self,width=200, height=200).pack()
        logo = tk.PhotoImage(file="logo.png")
        LogoImage = tk.Label(self,image=logo)
        LogoImage.image = logo
        LogoImage.place(x=0,y=0,width=285,height=250)

        ttk.Label(self, text="    Website/Service").pack(anchor='w')

        self.service_entry = ttk.Entry(self, width=32)
        self.service_entry.pack()
        self.service_entry.focus()

        ttk.Label(self, text="    Username").pack( anchor='w')

        self.username_entry = ttk.Entry(self, width=32)
        self.username_entry.pack()

        ttk.Label(self, text="    Password").pack(anchor='w')

        self.password_field = ttk.Entry(self, width=32)        
        self.password_field.pack()
        ttk.Label(self, text="\n").pack()

        show_pass_button = tk.Button(self, text="Show Password", width=20, height=2, command = self.ShowPassword)
        show_pass_button.pack()  
              
        home_button = tk.Button(self, text="Home", width=10,height=1,
                        command = lambda: self.controller.ShowFrame('MenuPage'))
        home_button.place(x=0,y=0)        
                    
        add_account_button = tk.Button(self, text="Add account", width=10,height=1,
                        command = lambda: self.controller.ShowFrame('AddAccounts'))
        add_account_button.place(x=80,y=0)
        
    def ShowPassword(self):
        pw = engine.GetPassword(self.username_entry.get(), self.service_entry.get())
        self.password_field.delete(0,tk.END)
        self.password_field.insert(0,pw)
        pyperclip.copy(pw)
        return
     
def main():
    MainWindow = PWControlApp()
    MainWindow.geometry("280x420")
    MainWindow.resizable(False, False)  
    MainWindow.iconbitmap('logo.ico')
    MainWindow.title("PWControl")
    MainWindow.mainloop()
    
if __name__ == "__main__":
    main()
