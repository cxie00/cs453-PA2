#!/usr/bin/env python3
# Last updated: Oct, 2021

import sys
from socket import *
import datetime
from checksum import checksum, checksum_verifier

CONNECTION_TIMEOUT = 60 # timeout when the sender cannot find the receiver within 60 seconds
FIRST_NAME = "Chloe"
LAST_NAME = "Xie"

# python PA2_sender.py 128.119.245.12 20000 2003 0.0 0.0 0 2 C:/Users/chloe/cs453/PA2/PA2_template/declaration.txt
# python PA2_sender.py 128.119.245.12 20000 1123 0.0 0.3 0 2 C:/Users/chloe/cs453/PA2/PA2_template/declaration.txt
# python PA2_sender.py 128.119.245.12 20000 1123 0.3 0.0 0 2 C:/Users/chloe/cs453/PA2/PA2_template/declaration.txt
# python PA2_sender.py 128.119.245.12 20000 1123 0.3 0.3 0 2 C:/Users/chloe/cs453/PA2/PA2_template/declaration.txt
# python PA2_sender.py 128.119.245.12 20000 1123 0.0 0.0 4 2 C:/Users/chloe/cs453/PA2/PA2_template/declaration.txt
def start_sender(server_ip, server_port, connection_ID, loss_rate=0, corrupt_rate=0, max_delay=0, transmission_timeout=60, filename="declaration.txt"):
    """
     This function runs the sender, connnect to the server, and send a file to the receiver.
     The function will print the checksum, number of packet sent/recv/corrupt recv/timeout at the end. 
     The checksum is expected to be the same as the checksum that the receiver prints at the end.

     Input: 
        server_ip - IP of the server (String)
        server_port - Port to connect on the server (int)
        connection_ID - your sender and receiver should specify the same connection ID (String)
        loss_rate - the probabilities that a message will be lost (float - default is 0, the value should be between 0 to 1)
        corrupt_rate - the probabilities that a message will be corrupted (float - default is 0, the value should be between 0 to 1)
        max_delay - maximum delay for your packet at the server (int - default is 0, the value should be between 0 to 5)
        tranmission_timeout - waiting time until the sender resends the packet again (int - default is 60 seconds and cannot be 0)
        filename - the path + filename to send (String)

     Output: 
        checksum_val - the checksum value of the file sent (String that always has 5 digits)
        total_packet_sent - the total number of packet sent (int)
        total_packet_recv - the total number of packet received, including corrupted (int)
        total_corrupted_pkt_recv - the total number of corrupted packet receieved (int)
        total_timeout - the total number of timeout (int)

    """

    print("Student name: {} {}".format(FIRST_NAME, LAST_NAME))
    print("Start running sender: {}".format(datetime.datetime.now()))

    checksum_val = "00000"
    total_packet_sent = 0
    total_packet_recv = 0
    total_corrupted_pkt_recv = 0
    total_timeout =  0

    print("Connecting to server: {}, {}, {}".format(server_ip, server_port, connection_ID))

    # have to implement hello properly on sender...
    """
    if you get 
    waiting, then get other side to connect, 

    or if you get ok, 
    then it is ready to send, 

    and then third is error: other side doesnt show up: just terminate

    """
    ##### START YOUR IMPLEMENTATION HERE #####
    try:
        msg = f"HELLO S {loss_rate} {corrupt_rate} {max_delay} {connection_ID}"
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
        total_file = ""
        if ok:
            with open(filename, "r") as f: # NOTE: SHOULD IT BE rb or r
                # print("line 64")
                seq_num = 0
                ack_num = 0
                bytes = f.read(20)
                bytes_read = 0
                while bytes_read < 200:
                    bytes_read += 20
                    total_file += bytes
                    prefix = f"{seq_num} {ack_num} {bytes} "
                    checksum_text = checksum(prefix)
                    packet = f"{seq_num} {ack_num} {bytes} {checksum_text}" 
                    answer = ""
                    ack_received = -1 
                    while ack_received != str(seq_num) or not checksum_verifier(answer):
                        try:
                            # print(f'packet: {packet}')
                            clientSocket.send(packet.encode())
                            clientSocket.settimeout(transmission_timeout)
                            # print("86: sent packet. starting timer.")
                            total_packet_sent += 1
                            while (ack_received != str(seq_num) or not checksum_verifier(answer)):
                                if (ack_received != -1 and answer != ""): 
                                    total_corrupted_pkt_recv += 1
                                answer = clientSocket.recv(1024).decode()   
                                total_packet_recv += 1
                                # print(f'answer: {answer} RECEIVED')
                                if not answer:
                                    continue
                                ack_received = answer[2]
                        except timeout:
                            # print("TIMEOUT OCCURRED") 
                            total_timeout += 1
                    seq_num = 1 - seq_num
                    bytes = f.read(20)

    except KeyboardInterrupt:
        clientSocket.close()
    clientSocket.close() 
    # print(total_file) # NOTE: remove when done
    checksum_val = checksum(total_file)
    ##### END YOUR IMPLEMENTATION HERE #####

    print("Finish running sender: {}".format(datetime.datetime.now()))

    # PRINT STATISTICS
    # PLEASE DON'T ADD ANY ADDITIONAL PRINT() AFTER THIS LINE
    print("File checksum: {}".format(checksum_val))
    print("Total packet sent: {}".format(total_packet_sent))
    print("Total packet recv: {}".format(total_packet_recv))
    print("Total corrupted packet recv: {}".format(total_corrupted_pkt_recv))
    print("Total timeout: {}".format(total_timeout))

    return (checksum_val, total_packet_sent, total_packet_recv, total_corrupted_pkt_recv, total_timeout)
 
if __name__ == '__main__':
    # CHECK INPUT ARGUMENTS
    if len(sys.argv) != 9:
        print("Expected \"python3 PA2_sender.py <server_ip> <server_port> <connection_id> <loss_rate> <corrupt_rate> <max_delay> <transmission_timeout> <filename>\"")
        exit()

    # ASSIGN ARGUMENTS TO VARIABLES
    server_ip, server_port, connection_ID, loss_rate, corrupt_rate, max_delay, transmission_timeout, filename = sys.argv[1:]
    
    # RUN SENDER
    start_sender(server_ip, int(server_port), connection_ID, loss_rate, corrupt_rate, max_delay, float(transmission_timeout), filename)
