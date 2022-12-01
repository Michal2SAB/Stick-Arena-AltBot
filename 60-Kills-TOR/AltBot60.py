# This worked with the labpass server as the kills limit was set to 60. Using TOR proxies we could bypass the IP limitations for one server and load 22 bots.
# Capable of making 1320 kills per 5 min (1 SA round) and 380160 kills in a day (24 hours)

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
 
class AltBot:
    def __init__(self, Username, Password, ServerIP, ServerPort, socka, mainAlt = ''):
        self.NullByte = struct.pack("B", 0)
        self.BufSize = 4096
        self.mainUsername = mainAlt
        self.Username = Username
        self.Password = Password
        self.altVar = True
        socket.socket = socka

        self.connectToServer(ServerIP, ServerPort)
 
    def sendPacket(self, PacketData, Receive = False):
        Packet = bytes(PacketData, "utf-8")
 
        try:
            self.SocketConn.send(Packet + self.NullByte)
 
            if Receive:
                return self.SocketConn.recv(self.BufSize).decode("utf-8")
        except:
            return

    def startKeepAlive(self, TimerSeconds = 20):
        if self.Username == self.mainUsername:
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
                print(self.Username + " - BUFFER EXCEPTION OCCURED or TOR ERROR")
                break
 
            if len(Buffer) == 0:
                print('\a')
                print(self.Username + " disconnected")
                if hasattr(self, "SocketConn"):
                    self.SocketConn.close()
                    del self.SocketConn
 
                break
 
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

                    AltingThread = threading.Thread(target=self.startAlt)
                    AltingThread.daemon = True
                    AltingThread.start()
 
                    break
                elif Data == "09":
                    print("Incorrect password")
                    break
                elif Data == "091":
                    print("Currently banned.")
 
                    break

    def getKills(self):
        try:
            APIURL = 'http://api.xgenstudios.com/?method=xgen.stickarena.stats.get&username={}'.format(self.Username)
            APIData = minidom.parseString(requests.get(APIURL).text)
            StatTag = APIData.getElementsByTagName('stat')
            Kills = StatTag[2].firstChild.nodeValue
            return Kills
        except:
            print("Couldnt get kills")
            pass
                    
    def collect(self):
        rooms = ["1v1 revenge", "i want vip", "noobs welcome", "xgen hq", "brawles", "not vip game", "katana vs glock", 
        "wow", "chit chat", "samurai", "good game", "drake", "versus", "oblock", 
        "1v1 game", "rocket science", "putin sucks", "the pit", "black hole", "stickarena", "ballistick", "gpack"]

        parser = ConfigParser()
        parser.read('config.ini')
        parser.set('ALT', 'bot_id', self.UserID)

        with open('config.ini', 'w') as configfile:
            parser.write(configfile)

        roomNr = 0
        added = False
        lastKills = self.getKills()
        newKills = ''
        st = ''
        start = ''

        while roomNr < 23:
            st = time.time()
            self.sendPacket('03'+rooms[roomNr])
            while added == False:
                newKills = self.getKills()
                if(newKills != lastKills): #newKills != lastKills
                    added = True
                    lastKills = newKills
                    timePassed = time.time() - st
                    mins, secs = divmod(timePassed, 60)
                    timeMinutes = "%02d:%02d" % (mins, secs)
                    print(lastKills + " ["+str(roomNr+1)+"] | " + timeMinutes)

            if(roomNr == 21):
                roomNr = 0
            else:
                roomNr += 1
            added = False

    def startAlt(self):
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
            "copiummachine21": "ballistick", "copiummachine22": "gpack"}

            RoomName = RoomNames[self.Username]
            CreateRoom = ["020200{}".format(RoomName)] # "04{}".format(RoomName) IF ALTBOT DONT WORK PUT THIS IN
            JoinRoom = ["04{}".format(RoomName), "03{}".format(RoomName)]
            easyOut = ["509", "804500700", "6807000"]

            for Packet in CreateRoom:
                self.sendPacket(Packet)
            self.sendPacket("05mp=**") # ** Unjoinable map for normies
                
            while self.altVar:
                config_object = ConfigParser()
                config_object.read("config.ini")
                botalt = config_object["ALT"]

                theId = botalt['bot_id']

                time.sleep(0.5)
                for packet in easyOut:
                    self.sendPacket(packet)
                self.sendPacket("7{}7000".format(theId))
 
class AltKing:
    def __init__(self):
        self.NullByte = struct.pack("B", 0)
        self.BufSize = 4096
        self.deathAlt = "copiummachine"
        self.deathPW = ""
        self.mainAccount = input("Account to alt: ")
        self.mainPW = getpass.getpass()
        print("")

        self.temp = socket.socket

        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1",9150)
        socket.socket = socks.socksocket

        sockeT = socket.socket
 
        AltBot(self.deathAlt+"1", self.deathPW, 'ballistick5.xgenstudios.com', 1138, self.temp) # 45.32.193.38
        time.sleep(14) # 14
        AltBot(self.deathAlt+"2", self.deathPW, 'ballistick5.xgenstudios.com', 1138, self.temp)
        time.sleep(14)
        AltBot(self.deathAlt+"3", self.deathPW, 'ballistick5.xgenstudios.com', 1138, self.temp)
        time.sleep(14)
        AltBot(self.deathAlt+"4", self.deathPW, 'ballistick5.xgenstudios.com', 1138, self.temp)
        time.sleep(14)
        AltBot(self.deathAlt+"5", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sockeT)
        time.sleep(14)
        AltBot(self.deathAlt+"6", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sockeT)
        time.sleep(14)
        AltBot(self.deathAlt+"7", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sockeT)
        time.sleep(14)
        AltBot(self.deathAlt+"8", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sockeT)
        time.sleep(14)
        AltBot(self.deathAlt+"9", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sockeT)

        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1",9152)
        socket.socket = socks.socksocket
        sockEt = socket.socket

        time.sleep(14)
        AltBot(self.deathAlt+"10", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sockEt)
        time.sleep(14)
        AltBot(self.deathAlt+"11", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sockEt)
        time.sleep(14)
        AltBot(self.deathAlt+"12", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sockEt)
        time.sleep(14)
        AltBot(self.deathAlt+"13", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sockEt)
        time.sleep(14)
        AltBot(self.deathAlt+"14", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sockEt)

        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1",9153)
        socket.socket = socks.socksocket
        soCket = socket.socket

        time.sleep(14)
        AltBot(self.deathAlt+"15", self.deathPW, 'ballistick5.xgenstudios.com', 1138, soCket)
        time.sleep(14)
        AltBot(self.deathAlt+"16", self.deathPW, 'ballistick5.xgenstudios.com', 1138, soCket)
        time.sleep(14)
        AltBot(self.deathAlt+"17", self.deathPW, 'ballistick5.xgenstudios.com', 1138, soCket)
        time.sleep(14)
        AltBot(self.deathAlt+"18", self.deathPW, 'ballistick5.xgenstudios.com', 1138, soCket)
        time.sleep(14)
        AltBot(self.deathAlt+"19", self.deathPW, 'ballistick5.xgenstudios.com', 1138, soCket)

        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1",9154)
        socket.socket = socks.socksocket
        sOcket = socket.socket

        time.sleep(14)
        AltBot(self.deathAlt+"20", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sOcket)
        time.sleep(14)
        AltBot(self.deathAlt+"21", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sOcket)
        time.sleep(14)
        AltBot(self.deathAlt+"22", self.deathPW, 'ballistick5.xgenstudios.com', 1138, sOcket)
        
        AltBot(self.mainAccount, self.mainPW, 'ballistick5.xgenstudios.com', 1138, self.temp, self.mainAccount)
 
if __name__ == "__main__":
    AltKing()
