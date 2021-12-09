import os 
import threading

scriptpath = "C:/Users/..." 
exepath = "C:/Users/..." 
backupexe = "C:/Users/..." 

def front():
    os.startfile(exepath)

def back():
    os.startfile(scriptpath)
    

def main():
    os.startfile(backupexe)

    bThread = threading.Thread(target = back)
    bThread.daemon = True
    bThread.start()

    front()


if __name__ == "__main__":
    main()