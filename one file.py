#!/usr/bin/python
# -*- coding: utf-8 -*-

# The modules required
import sys
import socket
import struct
import time
import random

def send_and_receive_tcp(address, port, message):
    print("")
    print("---This is the TCP part---")

    print("You gave arguments: {} {} {}".format(address, port, message))
    BUFFER_SIZE = 1024

    # create TCP socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    #create key list
    keys = create_keys()


    # connect socket to given address and port
    s.connect((address, port))

    # python3 sendall() requires bytes like object. encode the message with str.encode() command
    encoded_message = message.encode()

    # send given message to socket
    s.sendall(encoded_message)

    # receive data from socket
    data = s.recv(BUFFER_SIZE)
    print(data)
    # data you received is in bytes format. turn it to string with .decode() command
    message = data.decode()

    # print received data
    print("Server answered: {}".format(message))


    #Seperate CID and UDP port from recieved message
    list = message.split(" ")
    cid = list[1][:8]
    udp_port = int(list[2][:5])

    #print saved info
    print("CID: {}, Port: {}\n".format(cid, udp_port))

    # close the socket
    s.close()

    # Get your CID and UDP port from the message

    # Continue to UDP messaging. You might want to give the function some other parameters 
    # like the above mentioned cid and port.
    send_and_receive_udp(address, udp_port, cid)
    return


def send_and_receive_udp(address, port, cid):
    '''
    Implement UDP part here.
    '''

    BUFFER_SIZE = 1024
    print("---This is the UDP part---")

    #Create UDP socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    #Define address
    addr = (address, port)

    #Encode message to byte object
    string = ("Hello from {}".format(cid))
    print("You are sending to server: {}".format(string))

    encoded_str = string.encode()
    b_cid = cid.encode()
    data_remaining = 0
    content_length = len(encoded_str)

    #Pack message as binary data, Byte order is big-endian ">"
    #Note that in python3 struct.pack takes bytes objects instead of strings.
    data = struct.pack('>8s??HH128s', b_cid, True, False, data_remaining, content_length, encoded_str)

    #Send message to server  
    s.sendto(data, addr)

    # Loop the following
    while(1):

        data_left = 1
        message = ""

        while(data_left != 0):
            # receive data from socket
            data, server = s.recvfrom(BUFFER_SIZE)

            #Unpack recieved data
            r_cid, bool1, bool2, data_left, b, string2 = struct.unpack('>8s??HH128s', data)
            #print(r_cid, bool1, bool2, data_left, b, string2)
            #Data you receive is in bytes format. Turn it to string with .decode() command
            recieved = (string2.decode()).rstrip("\x00")
            recieved = recieved.strip()
            print(recieved)
            message += recieved


        # if received data contains the word 'Bye' break the loop
        if('Bye' in message):
            break


        #Reverse list
        list = message.split(" ")
        list.reverse()

        #Turn list to string
        string = ""
        for i in list:
            string += i + " " 
        string = string[:-1]

        print(string)
        print("")
        #print(len(string))

        #send reversed list
        packets = chunking(string)
        for pack in packets:
            piece, data_remaining = pack
            data_remaining = int(data_remaining)
            if data_remaining == 0:
                EOM = True
            else:
                EOM = False

            encoded_str = piece.encode()
            content_length = len(encoded_str)
            data = struct.pack('>8s??HH128s', b_cid, True, EOM, data_remaining, content_length, encoded_str)
            s.sendto(data, addr)
            #print(EOM)
            #print("Data remaining: {}".format(data_remaining))
            #print("content length: {}".format(content_length))
            time.sleep(0.5)


    return

def chunking(text):
    """
    Takes in full message and returns list<tuple>. Which contains 64byte string and how 
    much of message is remaining in other tuples.
    """        
    list = []  
    remain = len(text)

    #Go trough packets
    for piece in pieces(text):
        #Subtract sended message length
        remain -= len(piece)

        #Add to list packet and remain as a tuple
        list.append(tuple((piece, remain)))

    return list        

def pieces(string, length=64):
    """
    Cuts strind down to 64 byte long pieces.
    """
    #Split to defiant length
    return (string[0+i:length+i] for i in range(0, len(string), length))

def encrypt(string, key):
    """
    Encrypts message by XORing the numeric calue of each character in the message with the 
    numeric value of the correspanding character in the key. Return encrypted string.
    """
    encrypted_str = ""
    for i, a in zip(string, key):
        encrypted_str += (str(ord(i) ^ ord(a)))

    return encrypted_str

def decrypt(encrypted_string, key):
    """
    Decrypts message by adding key and encrypted characters values toghetter. 
    Returns decrypted string.
    """
    decrypted_str = ""
    for i, a in zip(string, key):
        encrypted_str += (str(ord(i) + ord(a)))

    return decrypted_str

def create_keys():
    """
    Creates list of 20 keys. Each key contains 64 hexivalues as a string.
    """
    keys = []
    for number in range(20):
        ran = random.randrange(10**80)
        my_hex = "%064x" % ran
        keys.append(my_hex)
    return keys

def main():
    USAGE = 'usage: %s <server address> <server port> <message>' % sys.argv[0]

    try:
        # Get the server address, port and message from command line arguments
        server_address = str(sys.argv[1])
        server_tcpport = int(sys.argv[2])
        message = str(sys.argv[3])
    except IndexError:
        print("Index Error")
    except ValueError:
        print("Value Error")
    # Print usage instructions and exit if we didn't get proper arguments
        sys.exit(USAGE)

    send_and_receive_tcp(server_address, server_tcpport, message)


if __name__ == '__main__':
    # Call the main function when this script is executed
        main()