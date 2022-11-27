import tkinter as tk
import pyperclip
from config_parser import GetConfigPaster, ChangeConfigPasterValue
from tkinter import ttk
from tkinter import simpledialog 
import engine

class PWControlApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (LoginPage, MenuPage, AddAccountPage, LoadAccountPage, DeleteAccountPage, SettingsPage):
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
        LogoImage.place(x=0,y=0,width=280,height=250)    
        #get the master password

        self.master_password = GetConfigPaster('LOGIN', 'master_password')
        
        tk.Label(self, text="Master Password: ", font='arial 11').place(x=10,y=230)
        #input field for the master password
        self.masterpass_entry = tk.Entry(self, show='*')
        self.masterpass_entry.place(x=140,y=233)
        
        self.LoginButton = tk.Button(self, text="Login",command=self.LoginButton)
        self.LoginButton.place(x=66,y=280,width=150,height=30)
    
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
        LogoImage.place(x=0,y=0,width=280,height=250)

        add_account_button = tk.Button(self, text="Add Account", 
                        command=lambda: self.controller.ShowFrame('AddAccountPage'))
        add_account_button.place(x=66,y=230,width=150,height=30)
        
        load_account_button = tk.Button(self, text="Load Account", 
                        command=lambda: self.controller.ShowFrame('LoadAccountPage'))
        load_account_button.place(x=66,y=270,width=150,height=30)
        
        delete_account_button = tk.Button(self, text="Delete Account", 
                        command=lambda: self.controller.ShowFrame('DeleteAccountPage'))
        delete_account_button.place(x=66,y=310,width=150,height=30)
        
        settings_button = tk.Button(self, text="Settings", 
                        command=lambda: self.controller.ShowFrame('SettingsPage'))
        settings_button.place(x=66,y=350,width=150,height=30)        

class AddAccountPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Canvas(self,width=200, height=200).pack()
        logo = tk.PhotoImage(file="logo.png")
        LogoImage = tk.Label(self,image=logo)
        LogoImage.image = logo
        LogoImage.place(x=0,y=0,width=280,height=250)

        ttk.Label(self, text="    Website/Service").pack(anchor='w')

        self.service_entry = ttk.Entry(self, width=32)
        self.service_entry.pack()

        ttk.Label(self, text="    Username").pack( anchor='w')

        self.username_entry = ttk.Entry(self, width=32)
        self.username_entry.pack()

        ttk.Label(self, text="    Password").pack(anchor='w')

        self.password_entry = ttk.Entry(self, width=32)
        self.password_entry.pack()

        pass_gen_button = ttk.Button(self, text="Generate Password", command = self.GeneratePass)
        pass_gen_button.pack()
        self.password_generated = ''

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
        
    def GeneratePass(self):
        '''
        Generate a password and copy it to the clipboard
        '''
        self.password_generated = engine.GeneratePassword()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, self.password_generated)
        pyperclip.copy(self.password_generated)
        
    def AccSave(self):
        '''
        Put the content typed in the input field together as an Account and save the Account to the database.
        
        If not all the required information are provided, show error to the user.
        If the password the user typed in does not meet the standard requirements, notice the user. Don't show the alert if the password is generated
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
            if not engine.MeetStandardRequirements(password) and self.password_generated!=password:
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
        LogoImage.place(x=0,y=0,width=280,height=250)

        ttk.Label(self, text="    Website/Service").pack(anchor='w')

        self.service_entry = ttk.Entry(self, width=32)
        self.service_entry.pack()

        ttk.Label(self, text="    Username").pack( anchor='w')

        self.username_entry = ttk.Entry(self, width=32)
        self.username_entry.pack()


        ttk.Label(self, text="\n\n\n").pack()

        show_pass_button = tk.Button(self, text="Show Password", width=20, height=2, command = self.ShowPassword)
        show_pass_button.place(x=66,y=295)

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
            #if the password is found, show the user and copy it to the clipboard
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
        LogoImage.place(x=0,y=0,width=280,height=250)

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
        Show error if the account does not exist in the database
        Ask the user to confirm their action of deleting the account.
        '''
        username = self.username_entry.get()
        service = self.service_entry.get()
        if len(username) == 0 or len(service) == 0:
            tk.messagebox.showerror(title="Insufficient information", 
                    message="Please fill in all the required fields")
        else:
            account = engine.Account(service, username)
            password = account.GetPassword()
            #let the user know if there is no account in the database with the same service and username
            if password == None:
                tk.messagebox.showerror(title="Account Not Found", 
                        message="The account cannot be found in the database.")
            else:
                if tk.messagebox.askokcancel(title="Account Deletion", 
                        message="This account will be deleted from the database, do you wish to proceed?"):
                    account.DeleteAccount()
        
            
class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        
        ttk.Label(self, text="Password Generator Settings", font= "Ariel 11").place(x=44,y=75)
        
        #for each type of characters, check against the config file for the initial state
        
        ttk.Label(self, text="Uppercase letters").place(x=45,y=117)
        if eval(GetConfigPaster("PASSWORD_PREFERENCE", "upper")):
            self.upper_characters_state_button = tk.Button(self, text='ON', width=10, command = self.UpperCharsStateButton)
        else:
            self.upper_characters_state_button = tk.Button(self, text='OFF', width=10, command = self.UpperCharsStateButton)
        self.upper_characters_state_button.place(x=170,y=110,width=70,height=30)
        
        ttk.Label(self, text="Lowercase letters").place(x=45,y=147)
        if eval(GetConfigPaster("PASSWORD_PREFERENCE", "lower")):
            self.lower_characters_state_button = tk.Button(self, text='ON', width=10, command = self.LowerCharsStateButton)
        else:
            self.lower_characters_state_button = tk.Button(self, text='OFF', width=10, command = self.LowerCharsStateButton)
        self.lower_characters_state_button.place(x=170,y=140,width=70,height=30)
        
        ttk.Label(self, text="Digits").place(x=45,y=177)
        if eval(GetConfigPaster("PASSWORD_PREFERENCE", "digit")):
            self.digits_state_button = tk.Button(self, text='ON', width=10, command = self.DigitsStateButton)
        else:
            self.digits_state_button = tk.Button(self, text='OFF', width=10, command = self.DigitsStateButton)
        self.digits_state_button.place(x=170,y=170,width=70,height=30)
        
        ttk.Label(self, text="Special characters").place(x=45,y=207)
        if eval(GetConfigPaster("PASSWORD_PREFERENCE", "special")):
            self.special_characters_button = tk.Button(self, text='ON', width=10, command = self.SpecialCharactersStateButton)
        else:
            self.special_characters_button = tk.Button(self, text='OFF', width=10, command = self.SpecialCharactersStateButton)
        self.special_characters_button.place(x=170,y=200,width=70,height=30)        
        
        ttk.Label(self, text="-------------------------------------------------------").place(x=0, y=250)
        
        change_masterpass_button = tk.Button(self, text="Change Master Password", command = self.MasterPassChangeDialog)
        change_masterpass_button.place(x=66,y=280,width=150,height=30)
                
        home_button = tk.Button(self, text="Home", width=12,height=1,
                        command = self.HomeButton)
        home_button.place(x=0,y=0)              
        
    def HomeButton(self):
        '''
        Take the user back to the Menu Page
        '''
        self.controller.ShowFrame('MenuPage')      
        
    def PasswordGeneratorWarning(self):
        '''
        Notice the users that the password generator is going to generate a blank password if they leave all the buttons as "OFF"
        
        Returns:None
        '''
        alert = (self.upper_characters_state_button.config('text')[-1] == 'OFF' 
                 and self.lower_characters_state_button.config('text')[-1] == 'OFF' 
                 and self.digits_state_button.config('text')[-1] == 'OFF' 
                 and self.special_characters_button.config('text')[-1] == 'OFF')
        if alert:
            tk.messagebox.showwarning(title="No characters for Password Generator", 
                message="At least one type of characters needs to be allowed for the password generator to generate a password.")
        
    def UpperCharsStateButton(self):
        '''
        Change the state of the button for uppercase letters
        Change the state of the value in the config file accordingly
        Show warning if all password configuration buttons are left off
        '''
        if self.upper_characters_state_button.config('text')[-1] == 'ON':
            self.upper_characters_state_button.config(text='OFF')
            ChangeConfigPasterValue("PASSWORD_PREFERENCE", "upper", "False")
            self.PasswordGeneratorWarning()
        else:
            self.upper_characters_state_button.config(text='ON')
            ChangeConfigPasterValue("PASSWORD_PREFERENCE", "upper", "True")
            
    def LowerCharsStateButton(self):
        '''
        Change the state of the button for lowerrcase letters
        Change the state of the value in the config file accordingly
        Show warning if all password configuration buttons are left off
        '''
        if self.lower_characters_state_button.config('text')[-1] == 'ON':
            self.lower_characters_state_button.config(text='OFF')
            ChangeConfigPasterValue("PASSWORD_PREFERENCE", "lower", "False")
            self.PasswordGeneratorWarning()
        else:
            self.lower_characters_state_button.config(text='ON')
            ChangeConfigPasterValue("PASSWORD_PREFERENCE", "lower", "True")
            
    def DigitsStateButton(self):
        '''
        Change the state of the button for digits
        Change the state of the value in the config file accordingly
        Show warning if all password configuration buttons are left off
        '''
        if self.digits_state_button.config('text')[-1] == 'ON':
            self.digits_state_button.config(text='OFF')
            ChangeConfigPasterValue("PASSWORD_PREFERENCE", "digit", "False")
            self.PasswordGeneratorWarning()
        else:
            self.digits_state_button.config(text='ON')
            ChangeConfigPasterValue("PASSWORD_PREFERENCE", "digit", "True")
            
    def SpecialCharactersStateButton(self):
        '''
        Change the state of the button for special characters
        Change the state of the value in the config file accordingly
        Show warning if all password configuration buttons are left off
        '''
        if self.special_characters_button.config('text')[-1] == 'ON':
            self.special_characters_button.config(text='OFF')
            ChangeConfigPasterValue("PASSWORD_PREFERENCE", "special", "False")
            self.PasswordGeneratorWarning()
        else:
            self.special_characters_button.config(text='ON')
            ChangeConfigPasterValue("PASSWORD_PREFERENCE", "special", "True")
        
    def MasterPassChangeDialog(self):
        '''
        Create a dialog that asks for the new master password
        Change the saved master password according to the new master password
        '''
        new_mp = simpledialog.askstring('Change Master Password','Set a new master password:')
        ChangeConfigPasterValue("LOGIN","master_password",new_mp)          


def main():
    MainWindow = PWControlApp()
    MainWindow.geometry("280x420")
    MainWindow.resizable(False, False)  
    MainWindow.iconbitmap('logo.ico')
    MainWindow.title("PWControl")
    MainWindow.mainloop()
    
if __name__ == "__main__":
    main()