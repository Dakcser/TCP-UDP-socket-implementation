def main():        
    text = """This is the first line. This is the second line. The line below is true. The line above is false.  A short line. A very very very very very very very very very long line. A self-referential line. The last line."""
    
    
    #Tulosta viestin pituus   
    remain = len(text)
    #Käy läpi vieti palat
    for piece in pieces(text):
        #Tulosta kuinka paljon viestiä on jäljellä
        print(remain)
        #Vähennä jo lähetettty määrä
        remain -= len(piece)
        #Tulosta lähetettävä pala
        print(piece)
        #Pakkaa pala, data pitäisi olla jo encrypted ja pariteetti lisätty
        # data = pack(piece)
        #LÄHETÄ
        # send(piece)
        
def pieces(string, length=64):
    #Paloittele annettu viesti määriteltyyn pituuteen.
    return (string[0+i:length+i] for i in range(0, len(string), length))
  
if __name__ == '__main__':
    # Call the main function when this script is executed
    main()