from Crypto.Cipher import AES
from Crypto import Random
import base64
import hashlib
from static_config_parser import StaticConfigParser

config = StaticConfigParser()
KEY = config.get('KEY', 'key')

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
    
def EncryptPassword(plain_text):
    MSG = AESCipher(KEY)
    return MSG.encrypt(plain_text).decode()

def DecryptPassword(encrypted_text):
    MSG = AESCipher(KEY)
    return MSG.decrypt(str.encode(encrypted_text))