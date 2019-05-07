# -*- coding: utf-8 -*-

import random 

def main():
    string = "one two green seven"
    
    laskettu_sana = add_parity(string)
    tarkistettu, error_free = check_list(laskettu_sana)
    print("Tarkistettu viesti: {}, No errors found: {}".format(tarkistettu, error_free))
        
def add_parity(n):
    """
    Adds parity bit to chractors and returns list of numbers
    """
    list = []
    
    for letter in n:     
        #Calculate the parity bit of the numeric value of the character
        value = ord(letter)
        
        #Left shift the charcater value by one bit
        value <<= 1
        
        #Add the parity bit to the character value
        value += get_parity(value)
        
        #add to a list
        list.append(chr(value))
        
    return list
    
def get_parity(n):
    while n > 1:
        n = (n >> 1) ^ (n & 1)
    return n
    
def check_list(list):
    error_free = True
    checked = []
    for value in list:
        num, bool = check_parity(ord(value))
        if(bool == False):
            error_free = False
        checked.append(num)
        
    return changeToString(checked), error_free
        
    
def check_parity(n):
    """
    Checks given values parity and returns boolean value depending on its status 
    and number value of character.
    True -> everything is good, False -> something went wrong.
    """
    parity_bit = 0
    #Read the parity bit from the numeric value of the character
    parity_bit = int((bin(n)[-1:]))
    
    #Right shift the character value by one bit
    n >>= 1
    
    #add random errrors
    if(random.randrange(10) > 8):
        n = n + 3
        
    #Calculate the parity of the character value and compare to received parity
    if((countSetBits(n)%2) != parity_bit):
        return n, False
        
    return n, True
        
def countSetBits(value):
    """
    Function calculates number of ones from given numbers binary and returns 
    calculated mount.
    """
    # convert given number into binary  
    binary = bin(value) 
    # now separate out all 1's from binary string 
    # skips two starting characters of binary string i.e; 0b
    setBits = [ones for ones in binary[2:] if ones=='1'] 

    return int(len(setBits))

def changeToString(list):
    """
    Creates a string from numbers in a list.
    """
    string = ""
    for i in list:
        string += chr(i)
           
    return string
     
if __name__ == '__main__':
    # Call the main function when this script is executed
    main()
    
