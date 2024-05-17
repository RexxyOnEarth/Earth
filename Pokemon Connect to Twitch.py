import socket 
import pyautogui #Ensure pyautogui is downloaded to your terminal (To do this ensure python is installed then -m pip install pyautogui)

SERVER = "irc.twitch.tv"
PORT = 6667
PASS = "" #OAuth Code
BOT = "TwitchBot"
CHANNEL = "" #twitch name all lowercase
OWNER = "" #twitch name all lowercase

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(("PASS " + PASS + "\n" +
          "NICK " + BOT + "\n" +
          "JOIN #" + CHANNEL + "\n").encode())

def gamecontrol(message):   #To Change keybounds change after keyDown or keyUp to responding Keyboard button
    if "up" in message.lower():
        pyautogui.keyDown('w')
        pyautogui.keyUp('w')
    elif "down" in message.lower():
        pyautogui.keyDown('s')
        pyautogui.keyUp('s')
    if "right" in message.lower():
        pyautogui.keyDown('d')
        pyautogui.keyUp('d')
    elif "left" in message.lower():
        pyautogui.keyDown('a')
        pyautogui.keyUp('a')
    elif message.lower() == "abut" or message.lower() == "a": #To Ensure when someone is speaking in a sentence that 'a' isn't called for
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
    elif message.lower() == "bbut" or message.lower() == "b":
        pyautogui.keyDown('backspace')
        pyautogui.keyUp('backspace')
    elif "start" in message.lower():
        pyautogui.keyDown('esc') 
        pyautogui.keyUp('esc')
    elif "enter" in message.lower():
        pyautogui.keyDown('enter') 
        pyautogui.keyUp('enter')
    elif "shift" in message.lower():
        pyautogui.keyDown('shift') 
        pyautogui.keyUp('shift')    
    elif "select" in message.lower():
        pyautogui.keyDown('1') 
        pyautogui.keyUp('1')     
    else:
        pass 
 
def joinchat(): 
    while True:
        try:
            readbuffer_join = irc.recv(1024).decode()
            for line in readbuffer_join.split("\n"):
                print(line)
                if "End of /NAMES list" in line:
                    print("Bot has joined " + CHANNEL + "'s Channel!")
                    sendMessage("Chat Room Joined")
                    return
        except Exception as e:
            print("Error reading from server:", e)
            return

def sendMessage(message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    irc.send((messageTemp + "\n").encode())

def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user

def getMessage(line):
    try:
        message = (line.split(":", 2))[2]
    except:
        message = ""
    return message

def Console(line):
    return "PRIVMSG" not in line

def twitch():
    joinchat()
    while True:
        try:
            readbuffer = irc.recv(1024).decode() 
        except Exception as e:
            print("Error reading from server:", e)
            continue
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            elif "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n"
                irc.send(msgg.encode())
                print(msgg)
                continue
            else:
                print(line)
                user = getUser(line)
                message = getMessage(line)
                gamecontrol(message)

if __name__ == '__main__':
    twitch()
