'''
Created on 01.08.2019

@author: Joshua
'''
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

class UserDB(object):
    '''
    classdocs
    '''
    Users = [0]*20;
    PWs = [0]*20;


    def __init__(self):
        '''
        Constructor
        '''
    
    def genPubKey(self):
        secret_code="Chaosprojekt"
        key = RSA.generate(2048)
        encrypted_key = key.export_key(passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC")
        file_out = open("rsa_key.bin", "wb")
        file_out.write(encrypted_key)
        file_out.close()
        print("Finished generating RSA key")
        
        
        
    def generatePEM(self):
        secret_code = "Chaosprojekt"
        encoded_key = open("rsa_key.bin","rb").read() 
        key = RSA.import_key(encoded_key, passphrase=secret_code)
        
        public_key = key.publickey().export_key()
        file_out = open("public.pem", "wb")
        file_out.write(public_key)
        file_out.close()
        
        private_key = key.export_key()
        file_out = open("private.pem", "wb")
        file_out.write(private_key)
        file_out.close()
        print("Finished generating .pem's...")
    def encryptData(self, receiver):
        print("Start Encrypting...")
        data = open('pinf.passwd', 'r').read().encode("utf-8");
        file_out = open("encrypted_data.bin", "wb")
        recipient_key = RSA.import_key(open("public.pem").read())
        session_key = get_random_bytes(16)
        
        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)
         
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        
        [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
        print("Stop Encrypting...")
    def decryptData(self):
        file_in = open("encrypted_data.bin","rb")
        
        private_key = RSA.import_key(open("private.pem").read())
        
        enc_session_key, nonce, tag, ciphertext = \
            [file_in.read(x)for x in (private_key.size_in_bytes(), 16, 16, -1)]

        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        temp = open("pinf.passwd",'w')
        temp.write(data.decode("utf-8"))
        temp.close()