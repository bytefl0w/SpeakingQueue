import tkinter as tk
from tkinter import ttk
import time
import logging
import os
 

class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        print("Main Class")
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.label = ttk.Label(parent, text="Hello world")
        self.label.grid(row = 0, column = 2 )
        
 
class Navbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        print("Navbar Class")
        tk.Frame.__init__(self, parent, *args, **kwargs)
 
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.navbar = Navbar(self)
        self.main = Main(self)
       
        self.main.grid(row = 0)
        self.navbar.grid(row = 1)
 
    # def checkForModuleUpdates(self):
    #     <check for updates>
    #     self.after(100, self.checkForModuleUpdates)
       
if __name__ == "__main__":
    root = tk.Tk()
    print("Starting up application...")
    root.title("Speaking Queue")
    root.geometry("480x220")
    mw = MainApplication(root)
    mw.grid()
    #root.after_idle(wm.checkForModuleUpdates)
    root.mainloop()
    print("Closing applicaton...")
