import sys
import struct

def main():
    string = "Hello"
    key = "abcde"
    message = encrypt(string, key)
    print(message)


def encrypt(string, key):
    encrypted_str = ""
    for i, a in zip(string, key):
        encrypted_str += (str(ord(i) ^ ord(a)) + " ")
            
    return encrypted_str
    
    
if __name__ == '__main__':
    # Call the main function when this script is executed
    main()