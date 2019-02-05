# -----------------------------
# speakingQueue.py
# developed by Erik Mortimer
# Description: This python application is used to keep track of a speaking queue used throughout meetings
# -----------------------------

import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog

import time
import logging
import os
import threading
import sqlite3

class TopFont(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Font")
        self.msg = tk.Message(self, text="This is where changing the font will go")
        self.msg.pack()

class TopAbout(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("About")
        self.msg = tk.Message(self, text="Speaking Queue application\nMade by: Erik Mortimer\nVersion: 0.8")
        self.msg.pack()


class Name():
    def __init__(self, canvas, y, stringInput):
        self.tag = stringInput
        self.canvas = canvas
        self.obj = canvas.create_text((40, y), text=stringInput[0], font=FONT, anchor="nw", tags=("name", self.tag))
        self.getText = self.canvas.itemcget(self.obj, 'text')
    def moveUp(self):
        self.canvas.move(self.tag, 0, -TEXTSPACING)


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        print("Main Class")
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.y = 0
        self.queue = tk.Canvas(parent, width = 450, height = DIMENSIONS[0], relief=tk.RAISED, background="white")

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

    def deleteName(self):
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
        self.main = _main
        self.nameList = []
        self.parseFile("names.txt")
        self.timesSpoken = {}

        for self.x in self.nameList:
            self.timesSpoken[self.x] = 0
        #print(self.timesSpoken)
        self.nlVar = tk.StringVar(value=self.nameList)
        self.searchTerm = tk.StringVar()
        self.searchTerm.trace("w", lambda name, index, mode: self.update_list())

        self.initFrames()

        self.scrollBar = ttk.Scrollbar(self.searchFrame, orient=tk.VERTICAL)
        self.scrollBarSpoken = ttk.Scrollbar(self.spokenFrame, orient=tk.VERTICAL)
        self.guiNameList = tk.Listbox(self.searchFrame, listvariable=self.nlVar, height=15, width=35, yscrollcommand=self.scrollBar.set, selectmode=tk.SINGLE, activestyle="none")
        self.selection = 0
        self.guiNameList.select_set(self.selection)

        self.buttons = [tk.Button(self.buttonFrame, padx = 7, pady = 3) for count in range(4)]
        self.buttons[0].config(text="Add", command=lambda: _main.addName(self.getCurselection()), takefocus=False, width=7)
        self.buttons[1].config(text="Next", command=lambda: self.nextNameClick(_main.queueList[0].getText), takefocus=False, width=7)
        self.buttons[2].config(text="Delete", command=lambda: _main.deleteName(), takefocus=False, width=7)
        self.buttons[3].config(text="Clear", command=lambda: self.clearSpoken(), takefocus=False, width=7)
        self.scrollBar.config(command=self.guiNameList.yview)
        self.searchBar = tk.Entry(self.searchFrame, textvariable=self.searchTerm, takefocus=True)
        
        self.tree = ttk.Treeview(self.spokenFrame, yscrollcommand=self.scrollBarSpoken.set, selectmode=tk.BROWSE)

        self.tree["columns"]=("spoken")
        self.tree.column("spoken", width=100)
        self.tree.heading("spoken", text="Spoken")
        self.treeList = []
        for self.nameListIdx in range(len(self.nameList)-1):
            #print(self.nameListIdx)
            self.treeList.append(self.tree.insert("", int(self.nameListIdx), text=str(self.nameList[self.nameListIdx]), values=(str(self.timesSpoken[self.nameList[self.nameListIdx]]))))

        #self.tree.insert("", 0, text="Line 1", values=("1A","1b"))
        #self.id2 = self.tree.insert("", 1, "dir2", text="Dir 2")
        #self.tree.insert(self.id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))
        self.scrollBarSpoken.config(command=self.tree.yview)
        self.packMe()
        

        self.update_list()
    
    def nextNameClick(self, stringInput):
        self.timesSpoken[stringInput] += 1
        self.z = 0
        while self.nameList[self.z] != stringInput:
            self.z += 1
        self.tree.set(self.treeList[self.z],column="spoken",value=(str(self.timesSpoken[stringInput])))
        self.main.nextName()

    def clearSpoken(self):
        for item in self.treeList:
            self.tree.set(item, column="spoken", value="0")
        for self.x in self.nameList:
            self.timesSpoken[self.x] = 0

    def OnEntryDown(self, event):
        if self.selection < self.guiNameList.size()-1:
            self.guiNameList.select_clear(self.selection)
            self.selection += 1
            self.guiNameList.select_set(self.selection)

    def OnEntryUp(self, event):
        if self.selection > 0:
            self.guiNameList.select_clear(self.selection)
            self.selection -= 1
            self.guiNameList.select_set(self.selection)

    def update_list(self):
        term = self.searchTerm.get()

        self.guiNameList.delete(0, tk.END)

        for item in self.nameList:
            if len(term) == 0:
                self.guiNameList.insert(tk.END, item)
            elif term.isupper():
                if len(term) == 1:
                    if item.split()[0][0] == term[0]:
                        self.guiNameList.insert(tk.END, item)
                elif len(term) == 2:
                    if item.split()[0][0] == term[0] and item.split()[1][0] == term[1]:
                        self.guiNameList.insert(tk.END, item)
                elif term in item:
                    self.guiNameList.insert(tk.END, item)
            elif term.islower():
                if term in item.lower():
                    self.guiNameList.insert(tk.END, item)
            elif term in item:
                self.guiNameList.insert(tk.END, item)
                    
        self.guiNameList.select_set(0)
        self.selection = 0

    def initFrames(self):
        self.buttonFrame = tk.Frame(self)
        self.searchFrame = tk.Frame(self, height=400)
        self.spokenFrame = tk.Frame(self, height=300)
        
    def packMe(self):
        self.searchBar.pack(side=tk.BOTTOM, anchor="e", fill=tk.X)
        self.spokenFrame.pack(side=tk.BOTTOM, anchor="s")
        self.scrollBar.pack(side=tk.LEFT, anchor="e", fill=tk.Y)
        self.scrollBarSpoken.pack(side=tk.LEFT, anchor="e", fill=tk.Y)
        self.guiNameList.pack(side=tk.LEFT, anchor="e", fill=tk.X)
        self.searchFrame.pack(side=tk.LEFT, anchor="e", fill=tk.X)

        self.buttonFrame.pack(side=tk.LEFT, anchor="n")
        self.buttons[0].pack()
        self.buttons[1].pack()
        self.buttons[2].pack()
        self.buttons[3].pack()
        
        self.tree.pack()
        
        
    def parseFile(self, fileName):
        print("Start parsing file...")
        self.nameList = []
        if (os.path.exists(str(fileName))):
            with open(str(fileName), "r") as file:
                line = next(file, None)
                while line:
                    self.nameList.append(line.strip("\n")) 
                    line = next(file, None)
        else:
            print("WARNING: can't find names.txt file in directory!")

    def getCurselection(self):
        items = self.guiNameList.curselection()
        tempList = self.guiNameList.get(0,tk.END)
        items = [tempList[int(item)] for item in items]
        return items
            
# tk.Frame of the whole app 
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.main = Main(self)
        self.tools = Tools(self, self.main)
        self.menubar = tk.Menu(self)
        self.addToMenuBar()
        
        self.main.pack(side=tk.RIGHT)
        self.tools.pack(side=tk.LEFT, anchor="nw")

    def addToMenuBar(self):
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Import", command=self.load_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Exit", command=self.parent.destroy, accelerator="Alt+F4")
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label="Font", command=lambda: TopFont(self))
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)

        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Overview", command=lambda: print("Overview command"), accelerator="F1")
        self.help_menu.add_command(label="About", command=lambda: TopAbout(self), accelerator="F2")
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

    def load_file(self):
        fname = filedialog.askopenfilename(initialdir=os.getcwd(),title="Import file",filetypes=(("Text files","*.txt"),("All files","*.*")), multiple=False)

        if fname:
            print("Import " + fname)
            fileName = str(fname)
            mw.tools.parseFile(fileName)
            mw.tools.update_list()
        return

    # def checkForModuleUpdates(self):
    #     <check for updates>
    #     self.after(100, self.checkForModuleUpdates)
       
if __name__ == "__main__":
    root = tk.Tk()
    print("Starting up application...")
    root.title("Speaking Queue")
    DIMENSIONS = [1280, 720]
    FONT = font.Font(family='Courier New', size='24', weight='bold')
    FILENAME = "names.txt"
    TEXTSPACING = 50
    root.geometry("{}x{}".format(DIMENSIONS[0],DIMENSIONS[1]))
    mw = MainApplication(root)
    root.config(menu=mw.menubar)
    root.bind('<Return>',lambda e: mw.main.addName(mw.tools.getCurselection()))
    root.bind('<Delete>',lambda e: mw.main.deleteName())
    root.bind("<Down>", mw.tools.OnEntryDown)
    root.bind("<Up>", mw.tools.OnEntryUp)
    root.bind('<Shift-Return>',lambda e:  mw.tools.nextNameClick(mw.main.queueList[0].getText))
    root.bind('<Control-Alt-Return>', lambda e: mw.tools.clearSpoken())
    # root.bind('<BackSpace>',lambda e: mw.main.nextName())
    mw.pack(padx=10, pady=10)
    #root.after_idle(wm.checkForModuleUpdates)
    root.mainloop()
    print("Closing applicaton...")

