from os import urandom
import string 
from static_config_parser import StaticConfigParser
import json
from encryption import EncryptPassword, DecryptPassword

size = 10
special_characters ="!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
upper_case_characters = string.ascii_uppercase
lower_case_characters = string.ascii_lowercase
digit_characters = string.digits

class Account(object):
    def __init__(self, username, service, password=''):
        '''
        Initializes an Account object

        service (string): the service where the account is signed up
        an Account object has three attribute:
            self.service (string, determined by input text)
            self.username (string, determined by input text)
            self.password (string, generated) through the randomizer
        If the website service contains unnecessary parts, attempt to remove them
        '''
        self.service = service.strip().replace('https://','')
        self.username = username
        self.password = password
            
    @property
    def password(self):
        '''
        Return the account's password
        '''
        return self._password    
    @property
    def username(self):
        '''
        return the account's username
        '''
        return str(self._username)

    @username.setter
    def username(self, username):
        '''
        If the username is blank, raise a ValueError
        '''   
        username = username.strip()     
        if username == "":
            raise ValueError
        else:
            self._username = username            
    @password.setter
    def password(self, password):
        '''
        If the password is blank, generate a random password
        '''   
        password = password.strip()     
        if password == "":
            self._password = GenerateSecurePassword()
        else:
            self._password = password
        
def GenerateSecurePassword():
    '''
    Generate a string of password that contains:
        at least one special character
        at least one uppercase character
        at least one lowercase character
        at least one digit
    '''
    chars = special_characters+upper_case_characters+lower_case_characters+digit_characters
    MeetExpectation = False
    specialchars = 0
    upperchars = 0
    lowerchars = 0
    digitchars = 0
    while not MeetExpectation:
        password =  "".join(chars[c % len(chars)] for c in urandom(size))
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
            MeetExpectation = True
    return password
    
def SavePassword(username, service, password=''):
    '''
    Used to save passwords into the data file
    '''
    acc = Account(str(username), str(service), EncryptPassword(str(password)))
    new_data = {
    acc.service+' '+acc.username:acc.password}
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        with open("data.json", "w") as data_file:
            json.dump(new_data, data_file, indent=4)
    else:
        data.update(new_data)
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
     
def GetPassword(username, service):
    '''
    Used to get passwords from the data file
    '''
    with open("data.json") as data_file:
        data = json.load(data_file)        
        if service+' '+username in data:        
            return DecryptPassword(data[service+' '+username])

def ChangeMasterPass(newMP):
    loginkey = StaticConfigParser.config["LOGIN"]
    loginkey["master_password"] = newMP
    with open('config.ini', 'w') as conf:
        StaticConfigParser.config.write(conf)
        
