# 22 wins per 5 min (1 SA round), 264 wins per hour and 6336 wins per day (24 hours) with only 1 kill per win.

import os
os.system('cls')
import time
import socks
import socket
import struct
import threading
from configparser import ConfigParser
from xml.dom import minidom
import requests
import getpass
 
class WinBot:
    def __init__(self, Username, Password, ServerIP, ServerPort, mainAlt = '', startedNow = True, startPt = 0):
        self.NullByte = struct.pack("B", 0)
        self.BufSize = 4096
        self.mainUsername = mainAlt
        self.Username = Username
        self.Password = Password
        self.altVar = True
        self.startedNow = startedNow
        self.startPt = startPt

        self.connectToServer(ServerIP, ServerPort)
 
    def sendPacket(self, PacketData, Receive = False):
        Packet = bytes(PacketData, "utf-8")
 
        try:
            self.SocketConn.send(Packet + self.NullByte)
 
            if Receive:
                return self.SocketConn.recv(self.BufSize).decode("utf-8")
        except:
            return

    def startKeepAlive(self, TimerSeconds = 15):
        if hasattr(self, "SocketConn"):
            KeepAliveTimer = threading.Timer(TimerSeconds, self.startKeepAlive)
            KeepAliveTimer.daemon = True
            KeepAliveTimer.start()

            self.sendPacket("0")
 
    def connectionHandler(self):
        Buffer = b""
 
        while hasattr(self, "SocketConn"):
            try:
                Buffer += self.SocketConn.recv(self.BufSize)
            except Exception as e:
                print('\a')
                print(self.Username + " - BUFFER ERROR OCCURED")
                break
 
            if len(Buffer) == 0:
                print('\a')
                print(self.Username + " disconnected")
                if hasattr(self, "SocketConn"):
                    self.SocketConn.close()
                    del self.SocketConn
                break
            elif Buffer.endswith(self.NullByte):
                Receive = Buffer.split(self.NullByte)
                Buffer = b""

                if self.Username != self.mainUsername:
                    for Data in Receive:
                        Data = Data.decode("utf-8")

                        if Data.startswith("U"):
                            config_object = ConfigParser()
                            config_object.read("config.ini")
                            botalt = config_object["WIN"]

                            theId = botalt['bot_id']
                            easyOut = ["509", "804500700", "6807000"]
                            for packet in easyOut:
                                self.sendPacket(packet)
                            self.sendPacket("7{}7000".format(theId))
 
    def connectToServer(self, ServerIP, ServerPort):
        start = time.time()
        try:
            self.SocketConn = socket.create_connection((ServerIP, ServerPort), timeout=5)
            self.SocketConn.settimeout(None)
        except Exception as Error:
            print(self.Username + " : " + Error)
            return
 
        Handshake = self.sendPacket("08HxO9TdCC62Nwln1P", True).strip(self.NullByte.decode("utf-8"))
 
        if Handshake == "08":
            Credentials = "09{};{}".format(self.Username, self.Password)
            RawData = self.sendPacket(Credentials, True).split(self.NullByte.decode("utf-8"))
 
            for Data in RawData:
                if Data.startswith("A"):
                    self.UserID = Data[1:][:3]
                    self.Username = Data[4:][:20].replace("#", "")
                    EntryPackets = ["02Z900_", "03_"]
                    if self.Username != self.mainUsername:
                        for Packet in EntryPackets:
                            self.sendPacket(Packet)

                    colored = ""
                    if time.time() - start > 2 and time.time() - start < 4:
                        colored = "\u001b[33;1m"
                    elif time.time() - start > 4:
                        colored = "\u001b[31;1m"
                        print("\a")
                    else:
                        colored = "\u001b[32;1m"

                    print(colored+self.Username + " has been logged in. [" + str(time.time() - start) + "]\033[0m")
 
                    self.startKeepAlive()
 
                    ConnectionThread = threading.Thread(target=self.connectionHandler)
                    ConnectionThread.start()

                    WinningThread = threading.Thread(target=self.startWinning)
                    WinningThread.daemon = True
                    WinningThread.start()
 
                    break
                elif Data == "09":
                    print("Incorrect password")
                    break
                elif Data == "091":
                    print("Currently banned.")
 
                    break

    def getWins(self):
        try:
            APIURL = 'http://api.xgenstudios.com/?method=xgen.stickarena.stats.get&username={}'.format(self.Username)
            APIData = minidom.parseString(requests.get(APIURL).text)
            StatTag = APIData.getElementsByTagName('stat')
            Wins = StatTag[0].firstChild.nodeValue
            return Wins
        except:
            print("Couldnt get wins")
            pass
                    
    def collect(self):
        time.sleep(5.5)
        rooms = ["1v1 revenge", "i want vip", "noobs welcome", "xgen hq", "brawles", "not vip game", "katana vs glock", 
        "wow", "chit chat", "samurai", "good game", "drake", "versus", "oblock", 
        "1v1 game", "rocket science", "putin sucks", "the pit", "black hole", "stickarena", "ballistick", "gpack"]

        parser = ConfigParser()
        parser.read('config.ini')
        parser.set('WIN', 'bot_id', self.UserID)

        with open('config.ini', 'w') as configfile:
            parser.write(configfile)

        roomNr = self.startPt
        added = False
        lastWins = self.getWins()
        newWins = ''
        st = ''
        start = ''

        while roomNr < 23: #23
            st = time.time()
            if(roomNr == 4 and self.startedNow != True):
                WinNext(self.Username, self.Password, 'ballistick7.xgenstudios.com', 1138, self.Username, True, 4)
                break
            elif(roomNr == 8 and self.startedNow != True):
                WinNext(self.Username, self.Password, 'ballistick8.xgenstudios.com', 1138, self.Username, True, 8)
                break
            elif(roomNr == 12 and self.startedNow != True):
                WinNext(self.Username, self.Password, 'ballistick9.xgenstudios.com', 1138, self.Username, True, 12)
                break
            elif(roomNr == 16 and self.startedNow != True):
                WinNext(self.Username, self.Password, 'ballistick4.xgenstudios.com', 1138, self.Username, True, 16)
                break
            elif(roomNr == 20 and self.startedNow != True):
                WinNext(self.Username, self.Password, 'ballistick1.xgenstudios.com', 80, self.Username, True, 20)
                break
            elif(roomNr == 0 and self.startedNow != True):
                WinNext(self.Username, self.Password, 'ballistick6.xgenstudios.com', 1138, self.Username, True, 0)
                break

            self.sendPacket('03'+rooms[roomNr])
            self.startedNow = False
            while added == False:
                newWins = self.getWins()
                if(newWins != lastWins):
                    added = True
                    lastWins = newWins
                    timePassed = time.time() - st
                    mins, secs = divmod(timePassed, 60)
                    timeMinutes = "%02d:%02d" % (mins, secs)
                    print(lastWins + " ["+str(roomNr+1)+"] | " + timeMinutes)

            if(roomNr == 21): #21
                roomNr = 0
            else:
                roomNr += 1
            added = False

    def startWinning(self):
        if(self.Username == self.mainUsername):
            print("")
            self.collect()
        else:
            time.sleep(5.5)

            RoomNames = {"copiummachine1": "1v1 revenge", "copiummachine2": "i want vip", "copiummachine3": "noobs welcome", 
            "copiummachine4": "xgen hq", "copiummachine5": "brawles", "copiummachine6": "not vip game", 
            "copiummachine7": "katana vs glock", "copiummachine8": "wow", "copiummachine9": "chit chat",
            "copiummachine10": "samurai", "copiummachine11": "good game", "copiummachine12": "drake",
            "copiummachine13": "versus", "copiummachine14": "oblock",
            "copiummachine15": "1v1 game", "copiummachine16": "rocket science", "copiummachine17": "putin sucks",
            "copiummachine18": "the pit", "copiummachine19": "black hole", "copiummachine20": "stickarena", 
            "copiummachine21": "ballistick", "copiummachine22": "gpack"}#, "copiummachine23": "real combat", "copiummachine24": "slayin"}

            RoomName = RoomNames[self.Username] 
            
            self.sendPacket("027200{}".format(RoomName))
            self.sendPacket("05mp=**") # ** Unjoinable map for normies

class WinNext:
    def __init__(self, Username, Password, ServerIP, ServerPort, mainAlt = '', startedNow = True, startPt = 0):
        WinBot(Username, Password, ServerIP, ServerPort, mainAlt, startedNow, startPt)

class AltKing:
    def __init__(self):
        self.NullByte = struct.pack("B", 0)
        self.BufSize = 4096
        self.deathAlt = "copiummachine"
        self.deathPW = ""
        self.mainAccount = input("Account to alt: ")
        self.mainPW = getpass.getpass()
        print("")
 
        WinBot(self.deathAlt+"1", self.deathPW, 'ballistick6.xgenstudios.com', 1138) # 45.32.193.38
        time.sleep(14.5) # potential for 24 games - 13,2916666667 (14,5 x 22 = 319)
        WinBot(self.deathAlt+"2", self.deathPW, 'ballistick6.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"3", self.deathPW, 'ballistick6.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"4", self.deathPW, 'ballistick6.xgenstudios.com', 1138)
        time.sleep(14.5)


        WinBot(self.deathAlt+"5", self.deathPW, 'ballistick7.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"6", self.deathPW, 'ballistick7.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"7", self.deathPW, 'ballistick7.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"8", self.deathPW, 'ballistick7.xgenstudios.com', 1138)


        time.sleep(14.5)
        WinBot(self.deathAlt+"9", self.deathPW, 'ballistick8.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"10", self.deathPW, 'ballistick8.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"11", self.deathPW, 'ballistick8.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"12", self.deathPW, 'ballistick8.xgenstudios.com', 1138)


        time.sleep(14.5)
        WinBot(self.deathAlt+"13", self.deathPW, 'ballistick9.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"14", self.deathPW, 'ballistick9.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"15", self.deathPW, 'ballistick9.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"16", self.deathPW, 'ballistick9.xgenstudios.com', 1138)
    
        time.sleep(14.5)
        WinBot(self.deathAlt+"17", self.deathPW, 'ballistick4.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"18", self.deathPW, 'ballistick4.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"19", self.deathPW, 'ballistick4.xgenstudios.com', 1138)
        time.sleep(14.5)
        WinBot(self.deathAlt+"20", self.deathPW, 'ballistick4.xgenstudios.com', 1138)


        time.sleep(14.5)
        WinBot(self.deathAlt+"21", self.deathPW, 'ballistick1.xgenstudios.com', 80)
        time.sleep(14.5)
        WinBot(self.deathAlt+"22", self.deathPW, 'ballistick1.xgenstudios.com', 80)
        
        WinBot(self.mainAccount, self.mainPW, 'ballistick6.xgenstudios.com', 1138, self.mainAccount)
 
if __name__ == "__main__":
    AltKing()
