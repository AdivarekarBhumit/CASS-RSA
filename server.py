import socket
import rsa
from base64 import b64encode, b64decode

public, private = rsa.newkeys()
public2, private2 = rsa.newkeys()

server = socket.socket()
server.bind(('localhost',5050))
server.listen(10)

conn, address = server.accept()
choice = int(conn.recv(1024))
#send public key
conn.send(public.exportKey())
if choice == 1:
    print('Encryption Decryption')
    #Receive encrypted message
    msg = conn.recv(1024)
    print(rsa.decrypt(b64decode(msg), private))
elif choice == 2:
    print('Digital Signature')
    #Sending message
    msg = input('Enter Message:').encode()
    conn.send(msg)
    #Sending signature
    signature = b64encode(rsa.sign(msg, private))
    conn.send(signature)
elif choice == 3:
    print('Encryption Decryption With Digital Signature')
    msg = input('Enter Message:').encode()
    conn.send(msg)
    #Sending signature
    signature = b64encode(rsa.sign(msg, private))
    conn.send(signature)
    if bool(conn.recv(1024)):
        print('Connection Cannot be Established')
    else:
        msg = conn.recv(1024)
        print(rsa.decrypt(b64decode(msg), private))
else:
    conn.close()