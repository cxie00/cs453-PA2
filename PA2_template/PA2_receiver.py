#!/usr/bin/env python3
# Last updated: Oct, 2021

import sys
import time
from socket import *
import datetime 
from checksum import checksum, checksum_verifier

"""
format of packet between sender and receiver 
<integer sequence number> <space> <integer ACK number> <space>  
<20 bytes of characters – payload> <space>  
<integer checksum represented as characters> 
"""
"""
python PA2_receiver.py 127.0.0.1 65432 1123 0.0 0.0 0 
"""
CONNECTION_TIMEOUT = 60 # timeout when the receiver cannot find the sender within 60 seconds
FIRST_NAME = "Chloe"
LAST_NAME = "Xie"

# python PA2_receiver.py 128.119.245.12 20000 2003 0.0 0.0 0
# python PA2_receiver.py 128.119.245.12 20000 1123 0.0 0.3 0
# python PA2_receiver.py 128.119.245.12 20000 1123 0.3 0.0 0
# python PA2_receiver.py 128.119.245.12 20000 1123 0.3 0.3 0
# python PA2_receiver.py 128.119.245.12 20000 1123 0.0 0.0 4
def start_receiver(server_ip, server_port, connection_ID, loss_rate=0.0, corrupt_rate=0.0, max_delay=0.0):
    """
     This function runs the receiver, connnect to the server, and receiver file from the sender.
     The function will print the checksum of the received file at the end. 
     The checksum is expected to be the same as the checksum that the sender prints at the end.

     Input: 
        server_ip - IP of the server (String)
        server_port - Port to connect on the server (int)
        connection_ID - your sender and receiver should specify the same connection ID (String)
        loss_rate - the probabilities that a message will be lost (float - default is 0, the value should be between 0 to 1)
        corrupt_rate - the probabilities that a message will be corrupted (float - default is 0, the value should be between 0 to 1)
        max_delay - maximum delay for your packet at the server (int - default is 0, the value should be between 0 to 5)

     Output: 
        checksum_val - the checksum value of the file sent (String that always has 5 digits)
    """

    print("Student name: {} {}".format(FIRST_NAME, LAST_NAME))
    print("Start running receiver: {}".format(datetime.datetime.now()))

    checksum_val = "00000"

    ##### START YOUR IMPLEMENTATION HERE #####
    try: 
        msg = f"HELLO R {loss_rate} {corrupt_rate} {max_delay} {connection_ID}"
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((server_ip, server_port))
        clientSocket.send(msg.encode())
        answer = "" 
        ok = False
        while "OK" not in answer:
            if "ERROR" in answer:
                break
            answer = clientSocket.recv(1024).decode()
            print(answer)
        ok = True
        if ok:
            total_file = ""
            expected_seq_num = 0
            while True:
                msg = clientSocket.recv(1024).decode() 
                if not msg:
                    break
                # print(f'msg: {msg}')
                seq_num = msg[0] # sender's seq num is 1st 
                ack = seq_num
                
                if checksum_verifier(msg) and seq_num == str(expected_seq_num):
                    # swap expected num bc now we expect the next number
                    text_content = msg[4:-6]
                    total_file += text_content
                    expected_seq_num = 1 - expected_seq_num
                else: 
                    # swap the opposite ack num bc message got corrupted or has wrong seq num
                    ack = 1 - expected_seq_num
                prefix = f'  {ack}                      '
                msg_checksum = checksum(prefix)
                packet = f'  {ack}                      {msg_checksum}'
                clientSocket.send(packet.encode())
                # print(f'pac: {packet} SENT')
    except KeyboardInterrupt:
        clientSocket.close()
    finally:
        clientSocket.close()
    # print(total_file)
    checksum_val = checksum(total_file)
    ##### END YOUR IMPLEMENTATION HERE #####

    print("Finish running receiver: {}".format(datetime.datetime.now()))

    # PRINT STATISTICS
    # PLEASE DON'T ADD ANY ADDITIONAL PRINT() AFTER THIS LINE
    print("File checksum: {}".format(checksum_val))

    return checksum_val

 
if __name__ == '__main__':
    # CHECK INPUT ARGUMENTS
    if len(sys.argv) != 7:
        print("Expected \"python PA2_receiver.py <server_ip> <server_port> <connection_id> <loss_rate> <corrupt_rate> <max_delay>\"")
        exit()
    server_ip, server_port, connection_ID, loss_rate, corrupt_rate, max_delay = sys.argv[1:]
    # START RECEIVER
    start_receiver(server_ip, int(server_port), connection_ID, loss_rate, corrupt_rate, max_delay)
