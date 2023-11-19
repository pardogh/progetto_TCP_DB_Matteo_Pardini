import socket
import Facilities as F

def manage_list(s):
    s.send(' '.encode())
    data=s.recv(2048)
    data=F.bytes_to_list(data)
    for i in data:
        print(i)
    s.send(' '.encode())

def manage_input(s):
    s.send(' '.encode())
    data = s.recv(1024).decode()
    data = input(data)
    s.send(data.encode())


HOST = 'localhost'    # Il nodo remoto, qui metti il tuo indirizzo IP per provare connessione server e client dalla tua macchina alla tua macchina
PORT = 50010             # La stessa porta usata dal server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    data = s.recv(1024)
    if(data.decode()=='#777'):
        manage_list(s)
    elif(data.decode()=='#111'):
        manage_input(s)
    else:
        print('\n', data.decode())
        s.send(' '.encode())

s.close()


