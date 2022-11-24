from os import urandom
import string 
from config_parser import MainConfigParser
import json
from encryption import EncryptPassword, DecryptPassword

DATAFILE = "data.json"
SIZE = 10
special_characters ="!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
upper_case_characters = string.ascii_uppercase
lower_case_characters = string.ascii_lowercase
digit_characters = string.digits

class Account(object):
    def __init__(self, service, username, password=''):
        '''
        Initializes an Account object

        service (string): the service where the account is signed up
        an Account object has three attribute:
            self.service (string, determined by input text)
            self.username (string, determined by input text)
            self.password (string, determined by input text)
        If the website service contains unnecessary parts, attempt to remove them
        '''
        self.service = service.strip().replace('https://','')
        self.username = username.strip()
        self.password = password.strip()
        
    def SaveAccount(self):
        '''
        Encrypt the password and save the Account into the data file.
        Create a new data file if the file is not found
        
        DATAFILE: path to where the Account(with encrypted password) is saved
        
        Returns: nothing
        '''
        new_data = {
        self.service+' '+self.username:EncryptPassword(self.password)}
        #try open the file and load the content
        try:
            with open(DATAFILE, "r") as data_file:
                data = json.load(data_file)
        #if the file is not found, create a new file and save the Account to it
        except FileNotFoundError:
            with open(DATAFILE, "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        #if the file is at the specified location, update the file by including the new_data
        else:
            data.update(new_data)
            with open(DATAFILE, "w") as data_file:
                json.dump(data, data_file, indent=4)
                
    def GetPassword(self):
        '''
        Load and decrypt the password of the Account from the datafile 
        Return None if the password or Account is not found
        
        DATAFILE: path to where the Account(with encrypted password) is saved
        
        Returns: string or None
        '''
        with open(DATAFILE) as data_file:
            data = json.load(data_file)
            if self.service+' '+self.username in data:        
                return DecryptPassword(data[self.service+' '+self.username])
            else:
                return None
            
    def DeleteAccount(self):
        '''
        Delete an account from the data file
        
        DATAFILE: path to where the Account is saved
        
        Returns: nothing
        '''
        dict_key = self.service+' '+self.username
        with open(DATAFILE) as data_file:
            data = json.load(data_file)
            for key in list(data):
                if dict_key in str(key):
                    del data[dict_key]
            with open(DATAFILE, "w") as data_file:
                json.dump(data, data_file, indent=4)

def MeetRequirements(password):
    '''
    Check if the password meetsthe standard requirements
    
    Standard requirements: password must contains
        at least one special character,
        at least one uppercase character,
        at least one lowercase character,
        at least one digit
        
    password: string
    
    Returns: bool
    '''
    specialchars = 0
    upperchars = 0
    lowerchars = 0
    digitchars = 0
    for character in password:
        if character in special_characters:
            specialchars +=1
        elif character in upper_case_characters:
            upperchars+=1
        elif character in lower_case_characters:
            lowerchars+=1
        elif character in digit_characters:
            digitchars +=1
    if specialchars > 0 and upperchars > 0 and lowerchars > 0 and digitchars > 0:
        return True
    else:
        return False  
    
def GenerateSecurePassword(size=SIZE):
    '''
    Generade a password that meets the standard requirements
        
    size(int): the number of characters in the password generated
        
    Returns: string
    '''
    chars = special_characters+upper_case_characters+lower_case_characters+digit_characters
    password =''
    while not MeetRequirements(password):
        password =  "".join(chars[c % len(chars)] for c in urandom(size))
    return password
        
def ChangeMasterPass(newMP):
    '''
    Change the master password
    
    newMP (string): the new master password
    
    Returns: nothing
    '''
    #load the config file location 
    masterkeypaster = MainConfigParser.config["LOGIN"]
    masterkeypaster["master_password"] = newMP
    #write the new master password to the config file
    with open('config.ini', 'w') as conf:
        MainConfigParser.config.write(conf)
        
def GetAccountList(service):
    '''
    Get a list of accounts registered to a specific service in the data file
    
    service (string): the service entitled with the accounts
    DATAFILE: path to where the Accounts(with encrypted password) are saved
    
    Returns: list
    '''
    account_list = []
    with open(DATAFILE) as data_file:
        data = json.load(data_file)
        for key in list(data):
            if service in str(key):
                acc = str(key).replace(service,'').strip()
                account_list.append(acc)
    return account_list
        
def DeleteAllAccounts():
    '''
    Delete all accounts saved in the data file
    
    DATAFILE: path to where the Accounts(with encrypted password) are saved
    
    Returns: nothing
    '''
    with open(DATAFILE, "w") as data_file:
        json.dump({}, data_file)

def DeleteService(service):
    '''
    Delete all accounts registered to a specific service in the data file
    
    service (string): the service entitled with the accounts that will be deleted
    DATAFILE: path to where the Accounts(with encrypted password) are saved
    
    Returns: nothing
    '''
    with open(DATAFILE) as data_file:
        data = json.load(data_file)
        for key in list(data):
            if service in str(key):
                del data[key]
        with open(DATAFILE, "w") as data_file:
            json.dump(data, data_file, indent=4)