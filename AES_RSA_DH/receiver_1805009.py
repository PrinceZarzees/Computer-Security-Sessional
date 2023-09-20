import socket
import diffy_hellman_1805009 as dh
import decrypt_1805009
def receiver():
    host = 'localhost'
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    conn, addr = s.accept()
    print("Connected by:", addr)

    while True:
        pgA= (conn.recv(1024).decode()).split(",")
        p,g,A=int(pgA[0]),int(pgA[1]),int(pgA[2])
        k=192
        b=dh.generate_prime(k//2)
        B=dh.power(int(g),b,int(p))
        conn.send(str(B).encode())
        key=dh.power(int(A),b,int(p))
        key=hex(key)[2:].zfill(32)
        key=''.join([chr(int(key[i:i+2],16)) for i in range(0,len(key),2)])
        temp=conn.recv(1024).decode()
        while (temp!="Ready"):
            continue
        conn.send("Ready".encode())
        msg=conn.recv(1024).decode()
        #print (msg)
        msg=decrypt_1805009.decrypt_text(key,msg)
        print("Sender:",msg)

    conn.close()

receiver()
