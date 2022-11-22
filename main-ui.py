import tkinter as tk
from tkinter import font as tkfont
import os 
import sys
import pyperclip
from static_config_parser import StaticConfigParser
from tkinter import ttk
from tkinter import simpledialog 
import engine

os.chdir(sys.path[0])

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, StartPage, Page1, Page2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('LoginPage')

    def show_frame(self, cont):
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
        self.login_entry = tk.Entry(self, show='*')
        self.login_label.place(x=10,y=230)
        self.login_entry.place(x=140,y=233)


        self.login_button = tk.Button(self, text="Login",command=self.login_button)
        self.login_button.place(x=70,y=280,width=150,height=30)
    
    def login_button(self):
        password = self.login_entry.get()
        if password == self.master_password:
            self.controller.show_frame('StartPage')
        else:
            self.attempt_count += 1
            self.incorrect_password_label = tk.Label(self, text=f"Incorrect password({self.attempt_count})", fg='red')
            self.incorrect_password_label.place(x=85,y=250)
            self.login_entry.delete(0, 'end')

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        def PassChangeButton():
            new_mp = simpledialog.askstring('Change Master Password','Set a new master password:')
            engine.ChangeMainPass(new_mp)
            
        
        
        logo = tk.PhotoImage(file="logo.png")
        LogoImage = tk.Label(self,image=logo)
        LogoImage.image = logo
        LogoImage.place(x=0,y=0,width=285,height=250)

        new_account = tk.Button(self, text="Add new account", 
                        command=lambda: controller.show_frame('Page1'))
        new_account.place(x=70,y=240,width=150,height=30)
        load_account = tk.Button(self, text="Load account", 
                        command=lambda: controller.show_frame('Page2'))
        load_account.place(x=70,y=280,width=150,height=30)
        
        change_masterpass = tk.Button(self, text="Change Master Password", command = PassChangeButton)
        change_masterpass.place(x=70,y=320,width=150,height=30)
        
        logout = tk.Button(self, text="Logout", command = lambda: controller.show_frame('LoginPage'))
        logout.place(x=70,y=360,width=150,height=30)



class Page1(tk.Frame):
	
    def __init__(self, parent, controller):

        def gen_pass():
            pw = engine.pw_gen()
            password_entry.delete(0, tk.END)
            password_entry.insert(0, pw)
            pyperclip.copy(pw)
            
        def save_acc():
            engine.save_pass(username_entry.get(), web_entry.get(), password_entry.get())

        tk.Frame.__init__(self, parent)
        
        canvas = tk.Canvas(self,width=200, height=200)
        canvas.pack()
        logo = tk.PhotoImage(file="logo.png")
        LogoImage = tk.Label(self,image=logo)
        LogoImage.image = logo
        LogoImage.place(x=0,y=0,width=285,height=250)


        website = ttk.Label(self, text="    Website")
        website.pack(anchor='w')

        web_entry = ttk.Entry(self, width=32)
        web_entry.pack()
        web_entry.focus()

        username = ttk.Label(self, text="    Username")
        username.pack( anchor='w')

        username_entry = ttk.Entry(self, width=32)
        username_entry.pack()


        password = ttk.Label(self, text="    Password")
        password.pack(anchor='w')

        password_entry = ttk.Entry(self, width=32)
        password_entry.pack()

        pass_button = ttk.Button(self, text="Generate Password", command=gen_pass)
        pass_button.pack()

        save_account = tk.Button(self, text="Save", width=20,height=2, command=save_acc)
        save_account.pack()        
 
        home_button = tk.Button(self, text="Home", width=10,height=1,
                        command=lambda: controller.show_frame('StartPage'))
        home_button.place(x=0,y=0)        
        
        load_account_button = tk.Button(self, text="Load account", width=10,height=1,
                        command=lambda: controller.show_frame('Page2'))
        load_account_button.place(x=80,y=0)
        

class Page2(tk.Frame):
    def __init__(self, parent, controller):

        def show_password():
            
            pw = engine.get_pass(username_entry.get(), web_entry.get())
            password_field.delete(0,tk.END)
            password_field.insert(0,pw)
            pyperclip.copy(pw)
            return
        
        tk.Frame.__init__(self, parent)
        
        canvas = tk.Canvas(self,width=200, height=200)
        canvas.pack()
        logo = tk.PhotoImage(file="logo.png")
        LogoImage = tk.Label(self,image=logo)
        LogoImage.image = logo
        LogoImage.place(x=0,y=0,width=285,height=250)

        website = ttk.Label(self, text="    Website")
        website.pack(anchor='w')

        web_entry = ttk.Entry(self, width=32)
        web_entry.pack()
        web_entry.focus()


        username = ttk.Label(self, text="    Username")
        username.pack( anchor='w')

        username_entry = ttk.Entry(self, width=32)
        username_entry.pack()

        password = ttk.Label(self, text="    Password")
        password.pack(anchor='w')

        password_field = ttk.Entry(self, width=32)
        
        password_field.pack()
        
        ttk.Label(self, text="\n").pack()

        show_pass_button = tk.Button(self, text="Show Password", width=20, height=2, command=show_password)
        show_pass_button.pack()  
              
        home_button = tk.Button(self, text="Home", width=10,height=1,
                        command=lambda: controller.show_frame('StartPage')   )
        home_button.place(x=0,y=0)        
        
            
        add_account_button = tk.Button(self, text="Add account", width=10,height=1,
                        command=lambda: controller.show_frame('Page1'))
        
        add_account_button.place(x=80,y=0)
     
def main():
    app = Application()
    app.geometry("280x420")
    app.resizable(False, False)  
    app.iconbitmap('logo.ico')
    app.title("PWControl")
    app.mainloop()
    
if __name__ == "__main__":
    main()
