import tkinter as tk
import os 
import sys
import pyperclip
from config_parser import MainConfigParser
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
        
        for F in (LoginPage, MenuPage, AddAccountPage, LoadAccountPage, DeleteAccountPage):
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
            
        config = MainConfigParser()
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

        add_account_button = tk.Button(self, text="Add Account", 
                        command=lambda: self.controller.ShowFrame('AddAccountPage'))
        add_account_button.place(x=70,y=230,width=150,height=30)
        
        load_account_button = tk.Button(self, text="Load Account", 
                        command=lambda: self.controller.ShowFrame('LoadAccountPage'))
        load_account_button.place(x=70,y=270,width=150,height=30)
        
        delete_account_button = tk.Button(self, text="Delete Account", 
                        command=lambda: self.controller.ShowFrame('DeleteAccountPage'))
        delete_account_button.place(x=70,y=310,width=150,height=30)
        
        change_masterpass_button = tk.Button(self, text="Change Master Password", command = self.MasterPassChangeDialog)
        change_masterpass_button.place(x=70,y=350,width=150,height=30)
        
    def MasterPassChangeDialog(self):
        new_mp = simpledialog.askstring('Change Master Password','Set a new master password:')
        engine.ChangeMasterPass(new_mp)

class AddAccountPage(tk.Frame):
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

        ttk.Label(self, text="    Username").pack( anchor='w')

        self.username_entry = ttk.Entry(self, width=32)
        self.username_entry.pack()

        ttk.Label(self, text="    Password").pack(anchor='w')

        self.password_entry = ttk.Entry(self, width=32)
        self.password_entry.pack()

        pass_gen_button = ttk.Button(self, text="Generate Password", command = self.GeneratePassword)
        pass_gen_button.pack()

        save_account_button = tk.Button(self, text="Save", width=20,height=2, command = self.AccSave)
        save_account_button.pack()        
 
        home_button = tk.Button(self, text="Home", width=12,height=1,
                        command = self.HomeButton)
        home_button.place(x=0,y=0)        
        
        load_account_button = tk.Button(self, text="Load Account", width=12,height=1,
                        command = self.LoadAccountButton)
        load_account_button.place(x=94,y=0)
        
        delete_account_button = tk.Button(self, text="Delete Account", width=12,height=1,
                        command = self.DeleteAccountButton)
        delete_account_button.place(x=188,y=0)
        
    def DeleteEntries(self):
        self.username_entry.delete(0,tk.END)
        self.password_entry.delete(0,tk.END)
        self.service_entry.delete(0,tk.END)        

    def HomeButton(self):
        self.DeleteEntries()
        self.controller.ShowFrame('MenuPage')

    def LoadAccountButton(self):
        self.DeleteEntries()
        self.controller.ShowFrame('LoadAccountPage')

    def DeleteAccountButton(self):
        self.DeleteEntries()
        self.controller.ShowFrame('DeleteAccountPage')
        
    def GeneratePassword(self):
        password = engine.GenerateSecurePassword()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        pyperclip.copy(password)
        
    def AccSave(self):
        username = self.username_entry.get()
        service = self.service_entry.get()
        password = self.password_entry.get()
        if len(username) == 0 or len(service) == 0 or len(password) == 0:
            tk.messagebox.showerror(title="Insufficient information", message="Please fill in all the required fields")
        else:
            if not engine.MeetRequirements(password):
                if tk.messagebox.askyesno(title="Password not strong", 
                        message="The password does not meet the standard requirements and might be insecure. Do you wish to proceed?"):
                    account = engine.Account(service, username, password)
                    account.SaveAccount()
        

class LoadAccountPage(tk.Frame):
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

        ttk.Label(self, text="    Username").pack( anchor='w')

        self.username_entry = ttk.Entry(self, width=32)
        self.username_entry.pack()

        ttk.Label(self, text="    Password").pack(anchor='w')

        self.password_field = ttk.Entry(self, width=32)        
        self.password_field.pack()
        ttk.Label(self, text="\n").pack()

        show_pass_button = tk.Button(self, text="Show Password", width=20, height=2, command = self.ShowPassword)
        show_pass_button.pack()  
              
        home_button = tk.Button(self, text="Home", width=12,height=1,
                        command = self.HomeButton)
        home_button.place(x=0,y=0)        
                    
        add_account_button = tk.Button(self, text="Add Account", width=12,height=1,
                        command = self.AddAccountButton)
        add_account_button.place(x=94,y=0)
        
        delete_account_button = tk.Button(self, text="Delete Account", width=12,height=1,
                        command = self.DeleteAccountButton)
        delete_account_button.place(x=188,y=0)
        
    def DeleteEntries(self):
        self.username_entry.delete(0,tk.END)
        self.password_field.delete(0,tk.END)
        self.service_entry.delete(0,tk.END)  
        
    def HomeButton(self):
        self.DeleteEntries()
        self.controller.ShowFrame('MenuPage')
        
    def AddAccountButton(self):
        self.DeleteEntries()
        self.controller.ShowFrame('AddAccountPage')
        
    def DeleteAccountButton(self):
        self.DeleteEntries()
        self.controller.ShowFrame('DeleteAccountPage')    
        
    def ShowPassword(self):
        username = self.username_entry.get()
        service = self.service_entry.get()
        if len(username) == 0 or len(service) == 0:
            self.password_field.delete(0,tk.END)
            tk.messagebox.showerror(title="Insufficient information", message="Please fill in all the required fields")
        else:
            account = engine.Account(service, username)
            password = account.GetPassword()
            if password == None:
                tk.messagebox.showerror(title="Password Not Found", 
                        message="The account has not previously been saved to the database.")
            else:
                self.password_field.delete(0,tk.END)
                self.password_field.insert(0,password)
                pyperclip.copy(password)
     
class DeleteAccountPage(tk.Frame):
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

        ttk.Label(self, text="    Username").pack( anchor='w')

        self.username_entry = ttk.Entry(self, width=32)
        self.username_entry.pack()

        ttk.Label(self, text="\n").pack()

        show_pass_button = tk.Button(self, text="Delete Account", width=20, height=2, command = self.AccountDelete)
        show_pass_button.pack()  
              
        home_button = tk.Button(self, text="Home", width=12,height=1,
                        command = self.HomeButton)
        home_button.place(x=0,y=0)        
                    
        add_account_button = tk.Button(self, text="Add Account", width=12,height=1,
                        command = self.AddAccountButton)
        add_account_button.place(x=94,y=0)
        
        load_account_button = tk.Button(self, text="Load Account", width=12,height=1,
                        command = self.LoadAccountButton)
        load_account_button.place(x=188,y=0)
        
    def HomeButton(self):
        self.username_entry.delete(0,tk.END)
        self.service_entry.delete(0,tk.END)
        self.controller.ShowFrame('MenuPage')
        
    def AddAccountButton(self):
        self.username_entry.delete(0,tk.END)
        self.service_entry.delete(0,tk.END)
        self.controller.ShowFrame('AddAccountPage')
        
    def LoadAccountButton(self):
        self.username_entry.delete(0,tk.END)
        self.service_entry.delete(0,tk.END)
        self.controller.ShowFrame('LoadAccountPage')
        
    def AccountDelete(self):
        username = self.username_entry.get()
        service = self.service_entry.get()
        if len(username) == 0 or len(service) == 0:
            tk.messagebox.showerror(title="Insufficient information", 
                    message="Please fill in all the required fields")
        else:
            account = engine.Account(service, username)
            if tk.messagebox.askokcancel(title="Account Deletion", 
                    message="This account will be deleted from the database, do you wish to proceed?"):
                account.DeleteAccount()
            
     
def main():
    MainWindow = PWControlApp()
    MainWindow.geometry("280x420")
    MainWindow.resizable(False, False)  
    MainWindow.iconbitmap('logo.ico')
    MainWindow.title("PWControl")
    MainWindow.mainloop()
    
if __name__ == "__main__":
    main()