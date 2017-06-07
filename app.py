import sys
import os
import prettytable
import requests
from bs4 import BeautifulSoup
import urllib.request

class TutorialPoint():
    menu = []
    chapters = []
    option = -1

    def __init__(self):
            print ("TutorialPoint")
            print ("---------------")
            self.url = 'https://www.tutorialspoint.com/'
            self.url1 ='https://www.tutorialspoint.com'

    def Menu(self):
        notinclue = []
        r = requests.get(self.url)
        html =r.content
        soup = BeautifulSoup(html, "html.parser")
        divs = soup.findAll('div', {'class': 'row featured-boxes'})
        for atag in divs:
            a = atag.findAll('a')
        i = 1
        l = []
        self.menuTable = prettytable.PrettyTable(["Option", "Topic"])
        for atag in a:
            if atag.text not in notinclue:
                l.append(i)
                l.append(atag.text)
                self.menuTable.add_row(l)
                l.append(atag.get('href'))
                self.menu.append(l)
                i = i + 1
                l = []
    
        print(self.menuTable[:290])
        self.a = int(input("Enter 0 to load more options or 1 to download topics: "))
        if self.a == 0:
            print(self.menuTable[290:580])
            self.a = int(input("enter 0 to load more or 1 to download topics: "))
            if self.a == 0:
                print(self.menuTable[580:850])
                self.getMenu()
            else:
                self.getMenu()
    
        else:   
            self.getMenu()

    def getMenu(self):
        self.option = -1
        while(self.option < 0 or self.option > len(self.menu)):
            self.option = int(input("Enter an option to download: "))

        self.directory = self.menu[self.option - 1][1]
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.getTopic() 

    def getTopic(self):

        self.url = self.menu[self.option - 1][2]
        r = requests.get(self.url1+self.url)
        soup = BeautifulSoup(r.text, "html.parser")

        
        divs = soup.findAll('aside', {'class': 'sidebar'})
        for atag in divs:
            a = atag.findAll('a')

       
        chapterTable = prettytable.PrettyTable(["Option", "Topic"])
        i = 1
        l = []
        for atag in a:
            l.append(i)
            l.append(atag.text)
            chapterTable.add_row(l)
            l.append(atag.get('href'))
            self.chapters.append(l)
            i = i + 1
            l = []
        print (chapterTable)
        option = -1
        while(option < 0 or option > len(self.chapters)):
            option = int(input("Enter an option to download (Enter '0' to download all): "))

        print ("Downloading file(s) ........")
        if(option == 0):
            for x in self.chapters:
                rq = urllib.request.Request(self.url1+x[2])
                res = urllib.request.urlopen(rq)
                f = open(self.directory + "/" + x[1] + ".html", 'wb')
                f.write(res.read())
                print ("File saved to " +  self.directory + "/" + x[1] + ".html")
                f.close()
        else:
            rq = self.chapters[option - 1][2]
            res = urllib.request.urlopen(self.url1+rq)
            f = open(self.directory + "/" + self.chapters[option - 1][1] + ".html", 'wb')
            f.write(res.read())
            print ("File saved to " +  self.directory + "/" + self.chapters[option - 1][1] + ".html")
            f.close()

        self.chapters = []
        opt = -1
        print ("1. Menu")
        print ("2. Topics")
        print ("3. Exit")
        while(opt != 1 and opt != 2 and opt != 3):
            opt = int(input("Enter your option: "))
        if(opt == 1):
            self.getMenu()
        elif(opt == 2):
            self.getTopic()
        else:
            sys.exit();        

     
obj = TutorialPoint()
obj.Menu()