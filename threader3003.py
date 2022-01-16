#!/usr/bin/python3
# Threader3000 - Multi-threader Port Scanner
# A project by LIII-s4ma 
# v1.0.1
# https://github.com/LIIIs4ma/threader3003
#
# Original project by The Mayor
# https://github.com/dievus/threader3000

import subprocess
import threading
import argparse
import socket
import time
import sys
import os
from queue import Queue


class color:
    default = '\033[0m'
    cyan='\033[36m'
    red='\033[31m'
    purple='\033[95m'
    lightgrey='\033[37m'
    yellow='\033[93m'
	
def parser():
    parser = argparse.ArgumentParser(description='Multi-threaded Port Scanner')
    parser.add_argument('-i', help = 'IP address of the target [ex: -i 10.10.10.10]')
    parser.add_argument('-r', help = 'Specify number of retries [ex: -r 1] [default: 1, max: 3]]' , default=1)
    parser.add_argument('-t', help = 'Specify number of thread [ex: -t 200] [default: 200, max: 250]', default=200)
    parser.add_argument('-p', help = 'Set range of ports [ex: -p 1000] It means 0 to 1000  [default: 65536]', default=65536)
    return parser.parse_args()

def banner(args=False):
    subprocess.call('clear', shell=True)
    print(color.cyan+"""  _   _                        _          _____  ___   ___ _____ 
 | |_| |__  _ __ ___  __ _  __| | ___ _ _|___ / / _ \ / _ \___ / 
 | __| '_ \| '__/ _ \/ _` |/ _` |/ _ \ '__||_ \| | | | | | ||_ \ 
 | |_| | | | | |  __/ (_| | (_| |  __/ |  ___) | |_| | |_| |__) |
  \__|_| |_|_|  \___|\__,_|\__,_|\___|_| |____/ \___/ \___/____/ 
                                                                 
 """+ color.default)
    print("                   Multi-threaded Port Scanner          ")
    print("                      A project by "+color.red+"The Mayor               "+ color.default)
    print("                       Edited by "+color.purple+"LIII-s4ma                 "+color.default)
    print()
    if(args and not args.i):
        print("You can use " + color.cyan + "threader3003 -i ip" +color.default+" for set IP also.")
        print("Check other options:" + color.cyan + "threader3003 -h" +color.default)
    print()


# Main Function
def main():
    socket.setdefaulttimeout(0.30)
    print_lock = threading.Lock()
    discovered_ports = []

    args = parser()
    banner(args)
    target = args.i if args.i else input(color.cyan+"$"+color.default+"IP: ")
    threadCount =  int(args.t) if int(args.t) <= 250 else 250
    portRange = int(args.p) if int(args.p) <= 65536 else 65536
    retryCount = int(args.r) if int(args.r) <= 3 else 3 

    def checkTarget(target):
        try:
            return socket.gethostbyname(target)
        except:
            banner(False)
            print(color.red + "[!] " + color.lightgrey + "Invalid format. Please use a correct IP or web address!")
            print()
            sys.exit()

    targetIP = checkTarget(target)

    def isPortOpen(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            portx = s.connect((targetIP, port))
            with print_lock:
                if str(port) not in discovered_ports:
                    return True
            portx.close()
        except (ConnectionRefusedError, AttributeError, OSError):
            return False

    def printOpenPort(port):
        print(color.red + "[!] " + color.lightgrey + "Port {} is open".format(port))
        discovered_ports.append(str(port))


    # Threading
    def threader():
        while True:
            worker = q.get()

            if(isPortOpen(worker)):
                printOpenPort(worker)

            q.task_done()
          
    q = Queue()
     
    def scanToIP(header=True):
        try:
            if header:
                print()
                print(color.lightgrey + "Scanning target: " +  targetIP)
                print("-" * 67)

            for r in range(retryCount):
                for i in range(threadCount):
                    t = threading.Thread(target = threader)
                    t.daemon = True
                    t.start()

                for worker in range(1, portRange):
                    q.put(worker)
                    
                time.sleep(1)
            

            q.join()
        except KeyboardInterrupt:
              print()
              print(color.red + "[!] " + color.lightgrey + "I was scanning :( Good bye!")
              quit()

    scanToIP()

    while True:
        if (not discovered_ports):
            print(color.red + "[!] " + color.default + "There is no open port.")
        print()
        
        again = input(color.yellow + "[?] " + color.default + "Would you like to try one more time (y/n): ")
        if again.lower() == 'y' or again.lower() == 'yes':
            retryCount = 1
            banner(args)
            print()
            print(color.lightgrey + "Scanning target: " +  targetIP)
            print("-" * 67)
            for i in discovered_ports:
                print(color.red + "[!] " + color.lightgrey + "Port {} is open".format(i))

            scanToIP(header=False)
        else:
            break
    
    def choices():
        print(color.cyan+"Choices:")
        if discovered_ports:
            print(color.cyan+"1: "+color.default+"sudo nmap -p{ports} -sV ".format(ports=",".join(discovered_ports))+color.red+"-sS -A"+color.default+" -T4 -Pn -oN {ip} {ip}".format(ip=target))
            print(color.cyan+"2: "+color.default+"nmap -p{ports} -sV ".format(ports=",".join(discovered_ports))+color.red+"-sC -A"+color.default+" -T4 -Pn -oN {ip} {ip}".format(ip=target))
        print(color.cyan+"3: "+color.default+"sudo nmap "+color.red+"-p- "+color.default+"-sV "+color.red+"-sS "+color.default+"-T4 -Pn -oN {ip} {ip}".format(ip=target))
        print(color.cyan+"4: "+color.default+"nmap "+color.red+"-p- "+color.default+"-sV "+color.red+"-sC "+color.default+"-T4 -Pn -oN {ip} {ip}".format(ip=target))
        print()
        print(color.cyan+"Open ports:"+color.default)
        if discovered_ports:
            print("{ports}".format(ports=",".join(discovered_ports)))
        else:
            print(color.red + "[!] " + color.default + "There is no open port. Go to Road 3 or 4.")
        print()
       
       
    def automate():
        banner(args)
        choices()
       
        nmaps = [
                '',
                "sudo nmap -p{ports} -sV -sS -A -T4 -Pn -oN {ip} {ip}".format(ports=",".join(discovered_ports), ip=target),
                "nmap -p{ports} -sV -sC -A -T4 -Pn -oN {ip} {ip}".format(ports=",".join(discovered_ports), ip=target),
                "sudo nmap -p- -sV -sS -T4 -Pn -oN {ip} {ip}".format(ports=",".join(discovered_ports), ip=target),
                "nmap -p- -sV -sC -T4 -Pn -oN {ip} {ip}".format(ports=",".join(discovered_ports), ip=target)
            ]

        def nmapper(road):
            try:
                if int(road) > 4 or 1 > int(road):
                    banner()
                    choices()
                    print(color.red + "[!] " + color.default + "Unknown road. [ex: "+color.cyan+"$"+color.default+"ROAD: 3]")
                    print()
                    return
                os.mkdir(target)
                os.chdir(target)
                banner()
                print(color.cyan+"$ "+color.default+nmaps[road])
                print()
                os.system(nmaps[road])
                return 'q'
            except FileExistsError as e:
                print()
                print(color.red + "[!] " + color.default + str(e) + ". Nmap can't write to file.")
                exit()

        while True:
            try:
                print(color.cyan+"$"+color.default+"ROAD: ",end="")
                choice = input()

                if choice.isnumeric():
                    choice = int(choice)
                else:
                    banner()
                    choices()
                    print(color.red + "[!] " + color.default + "Unknown road. [ex: "+color.cyan+"$"+color.default+"ROAD: 3]")
                    print()
                    continue

                if nmapper(choice):
                    exit()
            except KeyboardInterrupt:
                print()
                print("Goodbye!")
                quit()

    automate()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        quit()
