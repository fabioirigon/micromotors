#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:35:05 2022

@author: fip
"""

import tkinter as tk
from tkinter import Frame, Label, filedialog
from PIL import ImageTk, Image

WIDTH, HEIGHT = 600, 400

#main class
class Gui():
    def __init__(self, root):
        self.root=root
        self.entry = tk.Entry(root)

        #dynamic strings (select button and average result)
        self.stvar=tk.StringVar()
        self.stvar.set("center_line")
        self.labtxt=tk.StringVar()
        self.labtxt.set("avg:")

        # image holder, binded to mouse click and movement        
        self.canvas=tk.Canvas(root, width=WIDTH, height=HEIGHT, background='white')
        self.canvas.grid(row=0,column=0)
        self.canvas.bind("<Button 1>", self.onCanvasClick)
        self.canvas.bind("<Motion>", self.onCanvasHover)

        # frame on the right, to host buttons and labels
        frame = Frame(self.root)
        frame.grid(row=0,column=1, sticky="n")

        # buttons and labels on the right side
        self.Button1=tk.Button(frame,text="Open File", bg="blue", 
                               command=self.onOpenFile).grid(row = 0,column = 1, 
                                                             sticky = "we")
        self.option=tk.OptionMenu(frame, self.stvar, "center_line", "points")
        self.option.grid(row=1,column=1,sticky="nwe")
        self.label1=Label(frame, text="op").grid(row=1,column=0, sticky="nw")
        self.label2=Label(frame, textvariable=self.labtxt).grid(row=2,column=0, sticky="w")
        self.clear_pts_butt=tk.Button(frame,text="clear points", command=self.onClear)
        self.clear_pts_butt.grid(row = 3,  column = 1, sticky = "we")

        # then some internal data (image, points and vertical line position)
        self.img = None
        self.points=[]
        self.c_line = 0
        self.c_line_color = "yellow"
        self.temp_pt = [0, 0]

    # when mouse hovering the image, show line or point position        
    def onCanvasHover(self, event):
        if self.img is not None:
            if self.stvar.get() == "center_line":
                self.c_line = event.x
                self.c_line_color = "yellow"
            else:
                if len(self.points) == 0 or self.points[-1][2] != 0:
                    self.temp_pt = [event.x, event.y]
                else:
                    self.temp_pt = [event.x, self.points[-1][1]]
        self.refresh()

    # on image click, mark line or point        
    def onCanvasClick(self, event):
        if self.stvar.get() == "center_line":
            self.stvar.set("points")
            self.c_line = event.x
            self.c_line_color = "green"
        else:
            if len(self.points) == 0 or self.points[-1][2] != 0:
                self.points.append([event.x,event.y, 0])
            else:
                self.points[-1][2]=event.x
        self.refresh()
        
    def onClear(self):
        self.points=[]
        self.refresh()        

    # draw all stuff
    def refresh(self):
        self.canvas.create_image(0,0,image=self.img,anchor="nw")
        self.canvas.create_line(self.c_line, 0, self.c_line, 400, fill=self.c_line_color)
        
        avg, cnt = 0, 0
        r = 5
        for x, y, z in self.points:
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='green')
            self.canvas.create_text(x-2*r, y-2*r, fill='green', text='1.0')
            self.canvas.create_line(x, y, self.c_line, y, fill="blue")
            if z != 0:
                self.canvas.create_oval(z-r, y-r, z+r, y+r, fill='green')
                self.canvas.create_line(z, y, self.c_line, y, fill="red")
                
                #avoid div by zero
                if x-self.c_line != 0: 
                    rat = (self.c_line-z)/(x-self.c_line)
                else:
                    rat = (self.c_line-z)
                txt = "%.2f"%(rat)
                avg += rat
                cnt += 1
                self.canvas.create_text(z+2*r, y-2*r, fill='red', text=txt)

        x, y = self.temp_pt
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='yellow')

        if cnt>0:
            self.labtxt.set("avg: %.2f"%(avg/cnt))

    # open image file
    def onOpenFile(self):
        filetypes = (
                ('image files', ['*.png', '*.jpg', '*.jpeg']),
                ('All files', '*.*')
            )

        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='.',
            filetypes=filetypes)

        img = Image.open(filename)
        width, height = img.size
        fac = max(width/WIDTH, height/HEIGHT)
        width, height = int(width/fac), int(height/fac)
        img = img.resize((width, height))  

        self.img = ImageTk.PhotoImage(img)
        self.canvas.config(width=img.width, height=img.height)
        self.refresh()

# main app        
if __name__== '__main__':
    root=tk.Tk()
    gui=Gui(root)
    root.mainloop()
    
