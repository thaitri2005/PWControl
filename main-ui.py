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
        '''
        Change the frame currently shown
        '''
        frame = self.frames[cont]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.attempt_count = 0
        #logo area
        logo = tk.PhotoImage(file="logo.png")
        LogoImage = tk.Label(self,image=logo)
        LogoImage.image = logo
        LogoImage.place(x=0,y=0,width=285,height=250)    
        #get the master password
        config = MainConfigParser()
        self.master_password = config.get('LOGIN', 'master_password')
        
        tk.Label(self, text="Master Password: ", font='arial 11').place(x=10,y=230)
        #input field for the master password
        self.masterpass_entry = tk.Entry(self, show='*')
        self.masterpass_entry.place(x=140,y=233)
        
        self.LoginButton = tk.Button(self, text="Login",command=self.LoginButton)
        self.LoginButton.place(x=70,y=280,width=150,height=30)
    
    def LoginButton(self):
        '''
        Check if the master password is correct.
        If it is correct, lead the user to the menu page.
        Otherwise, alert the user about the incorrect password
        '''
        password = self.masterpass_entry.get()
        #compare the typed in password against the master password. If correct, get to the Menupage
        if password == self.master_password:
            self.controller.ShowFrame('MenuPage')
        #show attempt count and clear the entry field if the password is incorrect
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
        '''
        Create a dialog that asks for the new master password
        Change the saved master password according to the new master password
        '''
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
        '''
        Delete the content in all input fields
        '''
        self.username_entry.delete(0,tk.END)
        self.password_entry.delete(0,tk.END)
        self.service_entry.delete(0,tk.END)        

    def HomeButton(self):
        '''
        Take the user back to the Menu Page
        '''
        self.DeleteEntries()
        self.controller.ShowFrame('MenuPage')

    def LoadAccountButton(self):
        '''
        Take the user to the Load Account Page
        '''
        self.DeleteEntries()
        self.controller.ShowFrame('LoadAccountPage')

    def DeleteAccountButton(self):
        '''
        Take the user to the Delete Account Page
        '''
        self.DeleteEntries()
        self.controller.ShowFrame('DeleteAccountPage')
        
    def GeneratePassword(self):
        '''
        Generate a password and copy it to the clipboard
        '''
        password = engine.GenerateSecurePassword()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        pyperclip.copy(password)
        
    def AccSave(self):
        '''
        Put the content typed in the input field together as an Account and save the Account to the database.
        
        If not all the required information are provided, show error to the user.
        If the password does not meet the standard requirements, notice the user
        '''
        #get the information from the input fields
        username = self.username_entry.get()
        service = self.service_entry.get()
        password = self.password_entry.get()
        #if not all boxs are filled, show error to the user
        if len(username) == 0 or len(service) == 0 or len(password) == 0:
            tk.messagebox.showerror(title="Insufficient information", message="Please fill in all the required fields")
        else:
            #if the password is not strong, notice the user
            if not engine.MeetRequirements(password):
                #if the user wish to proceed, save the password
                if tk.messagebox.askyesno(title="Password not strong", 
                        message="The password does not meet the standard requirements and might be insecure. Do you wish to proceed?"):
                    account = engine.Account(service, username, password)
                    account.SaveAccount()
            #if the password is already strong, just save it
            else:
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


        ttk.Label(self, text="\n").pack()

        show_pass_button = tk.Button(self, text="Show Password", width=20, height=2, command = self.ShowPassword)
        show_pass_button.pack()  
        
        ttk.Label(self, text="    Password").pack(anchor='w')

        self.password_field = ttk.Entry(self, width=32)        
        self.password_field.pack()
              
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
        '''
        Delete the content in all input fields
        '''
        self.username_entry.delete(0,tk.END)
        self.password_field.delete(0,tk.END)
        self.service_entry.delete(0,tk.END)  
        
    def HomeButton(self):
        '''
        Take the user back to the Menu Page
        '''
        self.DeleteEntries()
        self.controller.ShowFrame('MenuPage')
        
    def AddAccountButton(self):
        '''
        Take the user to the Add Account Page
        '''
        self.DeleteEntries()
        self.controller.ShowFrame('AddAccountPage')
        
    def DeleteAccountButton(self):
        '''
        Take the user to the Delete Account Page
        '''
        self.DeleteEntries()
        self.controller.ShowFrame('DeleteAccountPage')    
        
    def ShowPassword(self):
        '''
        Get and show the password from the database according to the username and service
        Copy the shown password to clipboard
                
        Show error if not all needed information are provided
        Show error if the account is not in the database
        '''
        #get the information needed
        username = self.username_entry.get()
        service = self.service_entry.get()
        #if any of the two required fields are not filled in, show error
        if len(username) == 0 or len(service) == 0:
            self.password_field.delete(0,tk.END)
            tk.messagebox.showerror(title="Insufficient information", 
                    message="Please fill in both the username and the service of the account")
        #if all the required entry fields are filled in, 
        # create an object of Account type 
        # and attempt to get the password of an account with the same service and username from the database
        else:
            account = engine.Account(service, username)
            password = account.GetPassword()
            #if there is no account in the database with the same service and username, 
            # let the user know that the password cannot be found
            if password == None:
                tk.messagebox.showerror(title="Password Not Found", 
                        message="The account cannot be found in the database.")
                
            else:
            #if the password is found, show the user and copy it to the clipboard
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
        
    def DeleteEntries(self):
        '''
        Delete the content in all input fields
        '''
        self.username_entry.delete(0,tk.END)
        self.service_entry.delete(0,tk.END)  
        
    def HomeButton(self):
        '''
        Take the user back to the Menu Page
        '''
        self.DeleteEntries()
        self.controller.ShowFrame('MenuPage')
        
    def AddAccountButton(self):
        '''
        Take the user to the Add Account Page
        '''
        self.DeleteEntries()
        self.controller.ShowFrame('AddAccountPage')
        
    def LoadAccountButton(self):
        '''
        Take the user to the Load Account Page
        '''
        self.DeleteEntries()
        self.controller.ShowFrame('LoadAccountPage')
        
    def AccountDelete(self):
        '''
        Delete an account with the typed in username and service
        
        Show error if not all the required fields are filled in.
        Ask the user to confirm their action of deleting the account.
        '''
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