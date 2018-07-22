# -----------------------------
# speakingQueue.py
# developed by Erik Mortimer
# Description: This python application is used to keep track of a speaking queue used throughout meetings
# -----------------------------

import tkinter as tk
from tkinter import ttk
from tkinter import font
import time
import logging
import os

class Name():
    def __init__(self, canvas, y, stringInput):
        self.tag = "n-%d" % id(self)
        self.canvas = canvas
        self.obj = canvas.create_text((0, y), text=stringInput[0], font=FONT, anchor="nw", tags=("name", self.tag))
    def moveUp(self):
        self.canvas.move(self.tag, 0, -TEXTSPACING)


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        print("Main Class")
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.y = 0
        self.queue = tk.Canvas(parent, width = 400, height = DIMENSIONS[0])
        self.queueList = list()
        self.queue.pack(side=tk.RIGHT)
        
    def addName(self, stringInput):
        # obj = self.queueList.append(self.queue.create_text((0,self.y), anchor="nw", text=stringInput[0]))
        obj = Name(self.queue, self.y, stringInput)
        self.queueList.append(obj)
        self.y += TEXTSPACING 

    def nextName(self):
        if self.queueList:
            self.queue.delete(self.queueList[0].obj)
            self.queueList.pop(0)
            for items in self.queueList:
                items.moveUp()
            self.y -= TEXTSPACING

        

# TODO: Add more to comment when features are implemented 
# Left side of the GUI, includes namelist 
class Tools(Main):
    def __init__(self, parent, _main, *args, **kwargs):
        print("Tools Class")

        # Init vars
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.nameList = []
        self.parseFile()
        self.nlVar = tk.StringVar(value=self.nameList)

        self.initFrames()

        self.scrollBar = ttk.Scrollbar(self.searchFrame, orient=tk.VERTICAL)
        self.guiNameList = tk.Listbox(self.searchFrame, listvariable=self.nlVar, height=10, yscrollcommand=self.scrollBar.set)
        self.buttons = [tk.Button(self.buttonFrame, padx = 5) for count in range(2)]
        self.buttons[0].config(text="Add", command=lambda: _main.addName(self.getCurselection()))
        self.buttons[1].config(text="Next", command=lambda: _main.nextName())
        self.scrollBar.config(command=self.guiNameList.yview)

        self.packMe()

    def initFrames(self):
        self.buttonFrame = tk.Frame(self)
        self.searchFrame = tk.Frame(self)
        
    def packMe(self):
        self.searchFrame.pack(side=tk.LEFT, anchor="nw")
        self.scrollBar.pack(side=tk.LEFT, anchor="nw", fill=tk.Y)
        self.guiNameList.pack(side=tk.LEFT, anchor="nw")
        self.buttonFrame.pack(side=tk.LEFT, anchor="nw")
        self.buttons[0].pack()
        self.buttons[1].pack()


    def parseFile(self):
        print("Start parsing file...")
        with open("names.txt", "r") as file:
           line = next(file, None)
           while line:
               self.nameList.append(line) 
               line = next(file, None)

    def getCurselection(self):
        items = self.guiNameList.curselection()
        items = [self.nameList[int(item)] for item in items]
        return items
            
# tk.Frame of the whole app 
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.main = Main(self)
        self.tools = Tools(self, self.main)
       
        self.main.pack()
        self.tools.pack()
 
    # def checkForModuleUpdates(self):
    #     <check for updates>
    #     self.after(100, self.checkForModuleUpdates)
       
if __name__ == "__main__":
    root = tk.Tk()
    print("Starting up application...")
    root.title("Speaking Queue")
    DIMENSIONS = [800, 600]
    FONT = font.Font(family='Helvetica', size='18', weight='bold')
    TEXTSPACING = 40
    root.geometry("{}x{}".format(DIMENSIONS[0],DIMENSIONS[1]))
    mw = MainApplication(root)
    mw.pack(padx=10, pady=10)
    #root.after_idle(wm.checkForModuleUpdates)
    root.mainloop()
    print("Closing applicaton...")
