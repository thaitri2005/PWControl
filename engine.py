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
    def __init__(self, username, website, password=''):
        '''
        Initializes an Account object

        website (string): the website where the account is signed up
        an Account object has three attribute:
            self.website (string, determined by input text)
            self.username (string, determined by input text)
            self.password (string, generated) through the randomizer
        If the website is invalid, attempt to fix or raise a ValueError
        '''
        self.website = website.strip().replace('https://','')
        self.username = username
        self.password = password
            
    @property
    def password(self):
        '''
        return the account's password
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
        If the password is blank, generate a password
        '''   
        password = password.strip()     
        if password == "":
            self._password = pw_gen()
        else:
            self._password = password
        
def pw_gen():
    '''
    Generate a string of password that contains at least one special character, one uppercase character, one lowercase character, and one digit
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
    

def save_pass(username, website, password=''):
    '''
    Used to save passwords into the data file
    '''
    acc = Account(str(username), str(website), EncryptPassword(str(password)))
    new_data = {
    acc.website+' '+acc.username:acc.password}
    try:
        with open("data.json", "r") as data_file:
            # reading old data
            data = json.load(data_file)
    except FileNotFoundError:
        with open("data.json", "w") as data_file:
            json.dump(new_data, data_file, indent=4)
    else:
        data.update(new_data)

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
    
        
def get_pass(username, website):
    '''
    Used to get passwords from the data file
    '''

    with open("data.json") as data_file:
        data = json.load(data_file)        
        if website+' '+username in data:        
            return DecryptPassword(data[website+' '+username])

def ChangeMainPass(newMP):
    #Get the LOGIN section
    loginkey = StaticConfigParser.config["LOGIN"]

    #Update the password
    loginkey["master_password"] = newMP

    #Write changes back to file
    with open('config.ini', 'w') as conf:
        StaticConfigParser.config.write(conf)
        
