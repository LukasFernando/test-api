import os
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import unpad

class DecryptManager:
    def __init__(self):
        path_to_project = os.getcwd() + '\\'
        self.path_to_private_key = path_to_project + 'private_key.pem'
        self.path_to_public_key = path_to_project + 'public_key.pem'
        private_key = os.path.exists(self.path_to_private_key)
        public_key = os.path.exists(self.path_to_public_key)

        if not (private_key and public_key):
            self.generate_keys()

    def decrypt_data(self, cipher_text):
        cipher_data = base64.b64decode(cipher_text)
        iv = cipher_data[:16]
        encrypted_key = cipher_data[16:16 + 256]
        encrypted_text = cipher_data[16 + 256:]
        asymmetric_key = self.get_key(self.path_to_private_key)
        cipher_rsa = PKCS1_OAEP.new(asymmetric_key)
        symmetric_key = cipher_rsa.decrypt(encrypted_key)
        cipher_aes = AES.new(symmetric_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher_aes.decrypt(encrypted_text), AES.block_size)

        return json.loads(decrypted_data.decode('utf-8'))

    def generate_keys(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        with open('private_key.pem', 'wb') as private_file:
            private_file.write(private_key)
        with open('public_key.pem', 'wb') as public_file:
            public_file.write(public_key)

    def get_key(self, file_path:str, key_str:bool=False):
        with open(file_path, 'rb') as file:
            key_file = file.read()
            if key_str:
                return key_file
            else:
                return RSA.import_key(key_file)
