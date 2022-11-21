from socket import *
import sys

def TCP_sender():
    try: 
        serverName = "128.119.245.12" # IP of "http://gaia.cs.umass.edu/" found with pinging
        serverPort = 20000
        loss_rate = 0.0
        corruption_rate = 0.0
        max_delay = 0
        id = "1123"
        msg = f"HELLO S {loss_rate} {corruption_rate} {max_delay} {id}"
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        clientSocket.send(msg.encode())
        answer = clientSocket.recv(1024).decode()
        print(answer)
        answer = clientSocket.recv(1024).decode()
        print(answer)
        clientSocket.close()    
    except KeyboardInterrupt:
        clientSocket.close()

TCP_sender()