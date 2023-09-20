import socket
import rsa_1805009
import encrypt_1805009
import random
import hashlib

def hash_message(message):
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    message=message.rstrip('\0')
    message=message.encode('utf-8')
    # Hash the message
    hash_object.update(message)

    # Get the hexadecimal representation of the hash
    hash_value = hash_object.hexdigest()

    return int(hash_value,16)
def authenticate(message,s):
    public_key,private_key=rsa_1805009.generate_keypair(512)
    hash_value=hash_message(message)
    sign=rsa_1805009.encrypt(hash_value,private_key)
    s.send((str(public_key[0])+","+str(public_key[1])+","+str(sign)).encode())

def sender():
    host = 'localhost'
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        key=random.randrange(2**127,2**128)
        s.send("Ready".encode())
        public_key=s.recv(1024).decode()
        public_key=public_key.split(",")
        public_key=(int(public_key[0]),int(public_key[1]))
        encrypted_key=rsa_1805009.encrypt(key,public_key)
        msg=input("Sender: ")
        key=hex(key)[2:].zfill(32)
        key=''.join([chr(int(key[i:i+2],16)) for i in range(0,len(key),2)])
        temp=encrypt_1805009.encrypt_text(key,msg)
        # print (key,temp)
        s.send(str(encrypted_key).encode())
        s.send(temp.encode())
        while(s.recv(1024).decode()!="Authenticate"):
            continue

        authenticate(msg,s)

    s.close()

sender()

