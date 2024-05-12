import wave
import shutil

def encode_data(oldwav, newwav, data): 
    frame_bytes = bytearray(list(oldwav.readframes(oldwav.getnframes()))) # creates an array of bytes from the data within the audio file
    
    data = data + int((len(frame_bytes)-(len(data)*8*8))/8)*'#' #adding dummy data
    
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0')for i in data]))) #converts text to bit array
    
    for i, bit in enumerate(bits): #replace lsb of each byte with one bit of the text bit array
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    
    frame_modified = bytes(frame_bytes) #get the modified bytes
    newwav.writeframesraw(frame_modified) #writes modified data to the output file



def encode():
    wav = input("Please enter the name of the .wav you wish to encode (with extension) : ")
    wavv = wave.open(wav, 'r') #reads input file
 
    data = input("Please enter your secret message : ")
    if (len(data) == 0):
        raise ValueError('no message?!?!?! You didnt write anything!?!??!')
 
    new_wav_name = input("Please enter the name of your new .wav (with extension) : ") 
    newwav = shutil.copyfile(wav, new_wav_name) #creates a copy where the output will be stored

    # lines 31 to 37 - reads the output file and stores audio file parameters to be used when writing to it later
    with wave.open(new_wav_name, "rb") as handle:
        params = handle.getparams()
        frames = handle.readframes(44100)
       

    params = list(params)
    params[3] = len(frames) 

    newwav = wave.open(new_wav_name, "w") #opens output file to be written to
    newwav.setparams(params) #sets output file parameters

    encode_data(wavv, newwav, data) #runs encode data function with variables stored from earlier
 


def decode(): 
    wav = input("Please enter the name of the .wav you wish to decode (with extension) : ")
    wav = wave.open(wav,'r') #reads file
    frame_bytes = bytearray(list(wav.readframes(wav.getnframes()))) #converts read file to bytes

    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))] #extract lsb of each byte

    string = "".join(chr(int("".join(map(str, extracted[i:i+8])),2)) # convert byte array to string
    for i in range(0, len(extracted),8))

    decoded = string.split("###")[0] #remove dummy data

    print(f"Your decoded message: {decoded}") #outputs the message left over
    wav.close()



def main():
   running = True
   print ("Bonsoir, Welcome to Ezra's audio steganography practical!\n")
   while running == True:
        a = int(input("1. Encode\n2. Decode\n3. Exit\n"))
        if (a == 1):
            encode()
    
        elif (a == 2):
            decode()
        elif (a == 3):
            running = False
        else:
            raise Exception("Please enter a valid input")
    #menue system


main()