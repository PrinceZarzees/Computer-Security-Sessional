import socket
import rsa_1805009
import decrypt_1805009
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
    temp=s.recv(1024).decode()
    temp=temp.split(",")
    public_key=(int(temp[0]),int(temp[1]))
    sign=int(temp[2])
    hash_value=hash_message(message)
    hash_value=rsa_1805009.decrypt(sign,public_key)
    if(hash_value==hash_message(message)):
        print("Message is authentic")
    else:
        print("Message is not authentic")
def receiver():
    host = 'localhost'
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    conn, addr = s.accept()
    print("Connected by:", addr)

    while True:
        bits = 512
        public_key, private_key = rsa_1805009.generate_keypair(bits)
        while(conn.recv(1024).decode()!="Ready"):
            continue
        conn.send((str(public_key[0])+","+str(public_key[1])).encode())
        temp=conn.recv(1024).decode()
        encrypted_key=int(temp)
        temp=conn.recv(1024).decode()
        encrypted_msg=temp
        key = rsa_1805009.decrypt(encrypted_key, private_key)
        key=hex(key)[2:].zfill(32)
        key=''.join([chr(int(key[i:i+2],16)) for i in range(0,len(key),2)])
        # print (key,encrypted_msg)
        msg=decrypt_1805009.decrypt_text(key,encrypted_msg)
        print("Sender:",msg)
        conn.send("Authenticate".encode())
        authenticate(msg,conn)

    conn.close()

receiver()
