from os import urandom
import string
from config_parser import GetConfigPaster
from encryption import EncryptPassword, DecryptPassword
import sqlite3

DATAFILE = "database.db"
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
        Encrypt the password and save the Account into the database.
        Update the password if there is an existing account with the same service and username.
        Create a new database if the file is not found.
        Create a new table if the Table is not found.
        
        DATAFILE: path to where the Account(with encrypted password) is saved
        
        Returns: nothing
        '''
        new_acc = (self.service,self.username,EncryptPassword(self.password))
        try:
            connection = sqlite3.connect(DATAFILE)
            cur = connection.cursor()
            
            cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='ACCOUNT' ''')
            if cur.fetchone()[0]==1 : 
                pass
            else:
                cur.execute("""CREATE TABLE ACCOUNT(
                    service text,
                    username text,
                    password text)
                            """)

            if self.GetPassword() == None:
                cur.executemany("INSERT INTO ACCOUNT (service, username, password) VALUES (?,?,?)", [new_acc])
            else:
                cur.execute("""UPDATE ACCOUNT SET password=(?) WHERE (service, username)=(?,?)""",[EncryptPassword(self.password),self.service,self.username])
            connection.commit()
            cur.close()

        except sqlite3.Error as error:
            print("Failed to save account. ", error)
        finally:
            if connection:
                connection.close()
        
                
    def GetPassword(self):
        '''
        Load and decrypt the password of the Account from the database 
        Return None if the password or Account is not found
        
        DATAFILE: path to where the Account(with encrypted password) is saved
        
        Returns: string or None
        '''
        try:
            connection = sqlite3.connect(DATAFILE)
            cursor = connection.cursor()

            cursor.execute("""SELECT * FROM ACCOUNT WHERE (service,username) = (?,?)""", [self.service,self.username])
            records = cursor.fetchall()
            if len(records) == 1:
                for row in records:
                    return DecryptPassword(row[2])
            else:
                return None
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data. ", error)
        finally:
            if connection:
                connection.close()
                        
    def DeleteAccount(self):
        '''
        Delete an account from the database
        
        DATAFILE: path to where the Account is saved
        
        Returns: nothing
        '''
        try:
            connection = sqlite3.connect(DATAFILE)
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM ACCOUNT WHERE (service,username) = (?,?)""", [self.service,self.username])
            connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to delete from database. ", error)
        finally:
            if connection:
                connection.close()


def MeetRequirements(password):
    '''
    Check if the password meets the requirements in the configuration
        
    password: string
    
    Returns: bool
    '''
    specialchars = eval(GetConfigPaster('PASSWORD_PREFERENCE', 'special'))
    upperchars = eval(GetConfigPaster('PASSWORD_PREFERENCE', 'upper'))
    lowerchars = eval(GetConfigPaster('PASSWORD_PREFERENCE', 'lower'))
    digitchars = eval(GetConfigPaster('PASSWORD_PREFERENCE', 'digit'))
    
    specialcharscount = 0
    uppercharscount = 0
    lowercharscount = 0
    digitcharscount = 0
    for character in password:
        if character in special_characters:
            specialcharscount +=1
        elif character in upper_case_characters:
            uppercharscount +=1
        elif character in lower_case_characters:
            lowercharscount +=1
        elif character in digit_characters:
            digitcharscount +=1
    if ((specialcharscount > 0 or specialchars == False) 
        and (uppercharscount > 0 or upperchars == False) 
        and (lowercharscount > 0 or lowerchars == False) 
        and (digitcharscount > 0 or digitchars == False)):
        return True
    else:
        return False  
    
def MeetStandardRequirements(password):
    '''
    Check if the password meets the standard requirements
    
    Standard requirements: password contains
        at least one special character,
        at least one uppercase character,
        at least one lowercase character,
        at least one digit
    Length of at least 6
        
    password: string
    
    Returns: bool
    '''
    specialcharscount = 0
    uppercharscount = 0
    lowercharscount = 0
    digitcharscount = 0
    for character in password:
        if character in special_characters:
            specialcharscount +=1
        elif character in upper_case_characters:
            uppercharscount +=1
        elif character in lower_case_characters:
            lowercharscount +=1
        elif character in digit_characters:
            digitcharscount +=1
    if specialcharscount > 0 and uppercharscount > 0 and lowercharscount > 0 and digitcharscount > 0 and len(password)>=6:
        return True
    else:
        return False  
    
def GeneratePassword():
    '''
    Generade a password that meets the requirements in the configuration
        
    Returns: string
    '''
    specialchars = eval(GetConfigPaster('PASSWORD_PREFERENCE', 'special'))
    upperchars = eval(GetConfigPaster('PASSWORD_PREFERENCE', 'upper'))
    lowerchars = eval(GetConfigPaster('PASSWORD_PREFERENCE', 'lower'))
    digitchars = eval(GetConfigPaster('PASSWORD_PREFERENCE', 'digit'))
    size = int(GetConfigPaster('PASSWORD_PREFERENCE', 'pass_length'))
    chars = ''
    if specialchars == True:
        chars += special_characters
    if upperchars == True:
        chars += upper_case_characters
    if lowerchars == True:
        chars += lower_case_characters
    if digitchars == True:
        chars += digit_characters
    password =''
    while not MeetRequirements(password):
        password =  "".join(chars[c % len(chars)] for c in urandom(size))
    return password

def GetAccountList(service):
    '''
    Get a list of accounts registered to a specific service in the database
    
    service (string): the service entitled with the accounts
    DATAFILE: path to where the Accounts(with encrypted password) are saved
    
    Returns: list
    '''
    acc_list = []
    try:
        connection = sqlite3.connect(DATAFILE)
        cursor = connection.cursor()

        cursor.execute("""SELECT * FROM ACCOUNT WHERE (service) = (?)""", [service])
        records = cursor.fetchall()
        for row in records:
            acc_list.append(row[1])
        cursor.close()
        return acc_list

    except sqlite3.Error as error:
        print("Failed to read data. ", error)
    finally:
        if connection:
            connection.close()
        
def DeleteAllAccounts():
    '''
    Delete all accounts saved in the database
    
    DATAFILE: path to where the Accounts(with encrypted password) are saved
    
    Returns: nothing
    '''
    connection = sqlite3.connect(DATAFILE)
    connection.cursor().execute('DELETE FROM ACCOUNT;');		
    connection.commit()
    connection.close()

def DeleteService(service):
    '''
    Delete all accounts registered to a specific service in the database
    
    service (string): the service entitled with the accounts that will be deleted
    DATAFILE: path to where the Accounts(with encrypted password) are saved
    
    Returns: nothing
    '''
    connection = sqlite3.connect(DATAFILE)
    connection.cursor().execute("""DELETE FROM ACCOUNT WHERE (service)=(?);""",[service]);		
    connection.commit()
    connection.close()
