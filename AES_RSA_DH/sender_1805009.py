import socket
import diffy_hellman_1805009 as dh
import encrypt_1805009
def sender():
    host = 'localhost'
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        k=128
        p=dh.generate_p(k)
        pi=(p-1)//2
        g=dh.generate_g(2,p-1,p,pi)
        a=dh.generate_prime(k//2)
        A=dh.power(g,a,p)
        s.send((str(p)+","+str(g)+","+str(A)).encode())

        B = s.recv(1024).decode()
        key=dh.power(int(B),a,int(p))
        key=hex(key)[2:].zfill(32)
        #convert key to ascii string each 2 digits
        key=''.join([chr(int(key[i:i+2],16)) for i in range(0,len(key),2)])
        s.send("Ready".encode())
        temp=s.recv(1024).decode()
        while (temp!="Ready"):
            continue
        print ("Receiver:", temp)
        msg=input("Sender: ")
        temp=encrypt_1805009.encrypt_text(key,msg)
        # print (temp)
        s.send(temp.encode())
        #print("Receiver:", response)

    s.close()

sender()

