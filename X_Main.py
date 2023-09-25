# -*- coding: utf-8 -*-
# Author: mihcuog@AILab
# Contatct: AI-Lab - Smart Things

import tkinter as tk
from tkinter import Message ,Text
from PIL import Image, ImageTk
import pandas as pd
#import datetime
from tkinter import font as tkFont
from tkinter import PhotoImage 
import time
import tkinter.ttk as ttk
import subprocess
import logging
from playsound import playsound


class X_Main():
    def __init__(self):
        # Create info ui
        #self.master = master
        self.play_x_main = playsound(r'alerts\xmain.wav')
        self.xmain = tk.Tk()  
        self.xmain.title("X_Main - @minhcuong-AILab")
        self.xmain.geometry("1300x800")
        self.xmain.resizable(False, False)
        # Background main x
        self.background_image = PhotoImage(file="asset/main_ui.png")
        self.background_label = tk.Label(self.xmain, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        # Main gui
        #self.xmain.attributes('-fullscreen', True) setting fullscreen image
        self.button_X_Download = tk.Button(self.xmain, text="DOWNLOAD",command=self.open_X_Download,anchor='w',justify='left' ,fg="white",borderwidth=0    ,width=10  ,height=1, activebackground = "Red" ,font=('Helvetica', 15, ' bold '), background="#07080A")#.grid(row=8, column=2, padx=5)
        self.button_X_Download.place(x=310, y=310)
        self.button_X_Subtrans = tk.Button(self.xmain, text="SUBTRANS",command=self.open_X_Subtrans,fg="white",anchor='w',justify='left',borderwidth=0  ,width=11  ,height=1 , activebackground = "Red" ,font=('Helvetica', 15, ' bold '), background="#07080A")#.grid(row=8, column=2, padx=5)
        self.button_X_Subtrans.place(x=310, y=395)
        self.button_X_Real_Time = tk.Button(self.xmain, text="REAL-TIME",command=self.open_X_Real_Time,anchor='w',justify='left' ,fg="white",borderwidth=0    ,width=9  ,height=1, activebackground = "Red" ,font=('Helvetica', 15, ' bold '), background="#07080A")
        self.button_X_Real_Time.place(x=310, y=480)
        self.button_X_Out = tk.Button(self.xmain, text="EXIT",command=self.out_X_Main,anchor='w',justify='left' ,fg="white",borderwidth=0    ,width=4 ,height=1, activebackground = "Red" ,font=('Helvetica', 15, ' bold '), background="#07080A")
        self.button_X_Out.place(x=330, y=565)

    # Open X_Download Part---
    def open_X_Download(self):
        playsound(r'alerts\alert.wav')
        print("******      X_Download @minhcuong-AILab Already!")
        self.X_Download_Path = "X_Download.py"
        subprocess.call(['python', self.X_Download_Path], shell=True)
    # Open X_Subtrans Part---
    def open_X_Subtrans(self):
        playsound(r'alerts\xstream.wav')
        print("******      X_Subtrans @minhcuong-AILab Already!")
        self.X_Subtrans_Path = "X_Subtrans.py"
        subprocess.call(['python', self.X_Subtrans_Path], shell=True)
    def open_X_Real_Time(self):
        playsound(r'alerts\xstream.wav')
        print("******      X_Real_Time @minhcuong-AILab Already!")
        self.X_Real_Time_Path = "X_Real_Time.py"
        subprocess.call(['python', self.X_Real_Time_Path], shell=True)    
    # Out X_Main Program---
    def out_X_Main(self):
        playsound(r'alerts\xclose.wav')
        print("******      X_Main - @minhcuong-AILab ~.~ Hope you enjoy that!!!")
        self.xmain.destroy()
    def run(self):
        self.xmain.mainloop()

def main():
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.debug("Nhớ debug nha!!!")
    logging.info("Check kĩ thông tin đi")
    logging.warning("Đây là cảnh báo cho bạn nè!!!")
    logging.error("Lỗi chương trình rồi bạn ơi!!!")
    logging.critical("Bạn đã làm cái gì vậy?")
    running = X_Main()
    running.run()

if __name__ == "__main__":
    main()






