# -*- coding: utf-8 -*-
# Author: mihcuog@AILab
# Contatct: AI-Lab - Smart Things

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.constants import CENTER, W, NO, END
import re
import sys
import os
from classes.X_YTD import YoutubeDownloader
from threading import Thread
import random
import string
import time
from PIL import Image, ImageTk

class ProgramGUI(YoutubeDownloader):
    songID = 0
    threadQueue = []

    def centerWindow(self, width, height, window):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        window.geometry("%dx%d+%d+%d" % (width, height, x, y))
    
    def onCloseRoot(self):
        close = messagebox.askokcancel("Goodbye", "Hope see you again!!!")
        if close:
            self.root.destroy()
            sys.exit()

    def initGUI(self):
        self.root = tk.Tk()
        self.centerWindow(860, 640, self.root)
        self.root.title("X_Download @minhcuong-AILab")
        self.root.protocol("WM_DELETE_WINDOW", self.onCloseRoot)
        iconFile = "classes\icon.ico"
        self.root.iconbitmap(iconFile)
        # Lock resize window
        self.root.resizable(False, False)
        self.background_image = Image.open("asset\X_Download.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        # Tạo một label để hiển thị hình ảnh nền
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)
        # Cần giữ tham chiếu đến hình ảnh nền để tránh việc nó bị thu hồi bởi garbage collector
        self.background_label.image = self.background_photo
        self.initLabels()
        self.initEntry()
        self.initButtons()
        self.initCheckBox()
        self.initTreeView()
        self.root.mainloop()
    
    def returnHandler(self, e):
        self.addToTreeView()

    def initLabels(self):
        self.insertLabel = tk.Label(text = "LINK TO:", wraplength = 180, fg='white', background='#0E0E0E', font = ("", 12, "bold"))
        self.insertLabel.pack()
        self.insertLabel.place(relx = 0.12, rely = 0.03)

    def initEntry(self):
        self.insertVariable = tk.StringVar()
        self.insertEntry = ttk.Entry(self.root, textvariable = self.insertVariable, width = 80)
        self.insertEntry.place(relx = 0.5, rely = 0.048, anchor = CENTER)
        self.insertEntry.bind("<Return>", self.returnHandler)
        self.insertEntry.focus_set()

    def initButtons(self):
        self.buttonStyle = ttk.Style()
        self.buttonStyle.configure("W.TButton", background = "#0E0E0E", fg = "white", font = ("Open Sans", 11))
        
        self.insertTopButton = ttk.Button(self.root, style = "W.TButton", text = "Add", command = self.addToTreeView, width = 5)
        self.insertTopButton.pack()
        self.insertTopButton.place(relx = 0.796, rely = 0.029)

        self.insertBottomButton = ttk.Button(self.root, style = "W.TButton", text = "Add", command = self.addToTreeView)
        self.insertBottomButton.pack()
        self.insertBottomButton.place(relx = 0.28, rely = 0.76)

        self.removeButton = ttk.Button(self.root, style = "W.TButton", text = "Remove", command = self.removeFromTreeView)
        self.removeButton.pack()
        self.removeButton.place(relx = 0.6, rely = 0.76)

        self.downloadButton = ttk.Button(self.root, style = "W.TButton", text  = "Download", command = self.download)
        self.downloadButton.pack()
        self.downloadButton.place(relx = 0.44, rely = 0.81)

        self.openFolderButton = ttk.Button(self.root, style = "W.TButton", text = "", command = self.openFolder)
        image = tk.PhotoImage(file=r"classes\folder.png")
        self.openFolderButton.config(image = image)
        self.openFolderButton.image = image
        self.openFolderButton.pack()
        self.openFolderButton.place(relx = 0.8, rely = 0.77)

    def initCheckBox(self):
        self.convertCheckBoxVar = tk.IntVar()
        self.convertCheckBox = ttk.Checkbutton(self.root, text = "Convert to MP3", variable = self.convertCheckBoxVar, onvalue=1, offvalue=0)
        self.convertCheckBox.pack()
        self.convertCheckBox.place(relx = 0.56, rely = 0.813)

    def initTreeView(self):
        self.treeView = ttk.Treeview(self.root, height = 20)
        
        self.treeView["columns"] = ("ID", "Name", "Duration")
        self.treeView.column("#0", width = 0, stretch = NO)
        self.treeView.column("ID", anchor = CENTER, width = 40)
        self.treeView.column("Name", anchor = W, width = 500)
        self.treeView.column("Duration", anchor = CENTER, width = 120)
        
        self.treeView.heading("ID", text = "ID", anchor = CENTER)
        self.treeView.heading("Name", text = "Name", anchor = CENTER)
        self.treeView.heading("Duration", text = "Duration", anchor = CENTER)

        self.treeView.bind("<Motion>", "break")
        self.treeView.pack(pady = 50)

        self.scrollBar = ttk.Scrollbar(self.root, orient = tk.VERTICAL, command = self.treeView.yview)
        self.treeView.configure(yscrollcommand = self.scrollBar.set)

    def on_after(self):
        self.addLabel.destroy()


    def showAddingLabel(self, text, x = 0.45):
        try:
            self.addLabel.destroy()
        except:
            pass
        self.addLabel = tk.Label(text = text, wraplength = 200, font = ("", 14, "bold"))
        self.addLabel.pack()
        self.addLabel.place(relx = x, rely = 0.76)
        self.addLabel.after(5000, self.on_after)

    def showAddedLabel(self, text, x = 0.45):
        try:
            self.addLabel.destroy()
        except:
            pass
        self.addLabel = tk.Label(text = text, wraplength = 200, font = ("", 14, "bold"), fg = "green")
        self.addLabel.pack()
        self.addLabel.place(relx = x, rely = 0.76)
        self.addLabel.after(5000, self.on_after)

    def addToTreeView(self):
        Thread(target = self.insertThread).start()

    def insertThread(self):
        currentEntry = self.insertEntry.get()
        self.insertEntry.delete(0, END)
        self.insertEntry.focus()

        if re.match("^\s+$", currentEntry) or currentEntry == "":
            messagebox.showwarning(title = "Error", message = "Invalid value")
            return

        threadHash = "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
        self.threadQueue.append(threadHash)

        while self.threadQueue[0] != threadHash:
            time.sleep(1)

        self.showAddingLabel("Waiting for processing...")

        videoAttributes = self.getVideoAttributes(currentEntry)
        if videoAttributes is None:
            messagebox.showerror("Error", "Video not found or is unavailable")
            self.threadQueue.pop(0)
            return

        self.songID += 1
        self.treeView.insert("", "end", values = (self.songID, videoAttributes[0], videoAttributes[1]))

        self.threadQueue.pop(0)
        self.showAddedLabel("Added!")

    def removeFromTreeView(self):
        try:
            selectedItem = self.treeView.selection()[0]
        except:
            messagebox.showerror(title = "Error!", message = "Select at least one row to delete!")
            return
        else:
            for selectedItem in self.treeView.selection():
                for i, song in enumerate(self.songStreams):
                    if (self.treeView.item(selectedItem)["values"][1] == song["file_name"][:-4]):
                        self.songStreams.pop(i)
                        break
                self.treeView.delete(selectedItem)

    def download(self):
        if len(self.threadQueue) > 0:
            messagebox.showwarning("Atention!", "Wait for all the videos to be added")
            return
        if self.convertCheckBoxVar.get() == 1:
            convert = True
        else:
            convert = False
        self.songID = 0
        self.downloadSongs(convert)
        i = 0
        for video in self.treeView.get_children():
            self.treeView.delete(video)
            i += 1
        if i == 0:
            messagebox.showerror("Error!", "There are no videos on the list!")
            return
        self.showAddingLabel("Downloading...", 0.42)
        self.addLabel.update_idletasks()
        while len(self.downloadSongsThreadQueue) > 0:
            time.sleep(1)
        self.showAddedLabel("Downloaded!", 0.423)
    
    def openFolder(self):
        localPath = os.getcwd()
        os.startfile(os.path.join(localPath, "sounds"))
