#!/usr/bin/python
# -*- coding: utf-8 -*-

# The modules required
import sys
import socket
import struct


def send_and_receive_tcp(address, port, message):
    print("---This is the TCP part---")
    print("")
    print("You gave arguments: {} {} {}".format(address, port, message))
    BUFFER_SIZE = 1024
    # create TCP socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()
        
        
    # connect socket to given address and port
    s.connect((address, port))

    # python3 sendall() requires bytes like object. encode the message with str.encode() command
    encoded_message = message.encode()

    # send given message to socket
    s.sendall(encoded_message)

    # receive data from socket
    data = s.recv(BUFFER_SIZE)

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
    content_length = sys.getsizeof(encoded_str)
    
    #check lengths
    print("message length: {}".format(sys.getsizeof(encoded_str)))
    print("Boolian length: {}".format(sys.getsizeof(True)))
    print("cid length: {}".format(sys.getsizeof(b_cid)))


    #Pack message as binary data, Byte order is big-endian ">"
    #Note that in python3 struct.pack takes bytes objects instead of strings.
    data = struct.pack('>8s??HH128s', b_cid, True, False, data_remaining, content_length, encoded_str)

    #Send message to server  
    s.sendto(data, addr)

    # Loop the following
    while(1):
        # receive data from socket
        data, server = s.recvfrom(BUFFER_SIZE)

        #Unpack recieved data
        r_cid, bool1, bool2, a, b, string2 = struct.unpack('>8s??HH128s', data)

        # Data you receive is in bytes format. Turn it to string with .decode() command
        recieved = (string2.decode()).rstrip("\x00")
        print(recieved)

        #Reverse list
        list = recieved.split(" ")
        list.reverse()

        #Turn list to string
        string = ""
        for i in list:
            string += i + " " 
        print(string)
        string.encode()

        # if received data contains the word 'Bye' break the loop
        if('Bye' in string):
            break

        #send reversed list
        encoded_str = string
        content_length = sys.getsizeof(encoded_str)
        data = struct.pack('>8s??HH128s', b_cid, True, False, data_remaining, content_length, encoded_str)
        s.sendto(data, addr)

    return


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

