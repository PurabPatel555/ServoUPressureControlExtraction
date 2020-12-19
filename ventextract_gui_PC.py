# -*- coding: utf-8 -*-
"""
VentExtract.ipynb
Purab Patel

"""
import numpy as np
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
from matplotlib.pyplot import ion
ion()
import os
import sys
from Tkinter import *
import tkFileDialog as filedialog 

def browse(): 
    OUT_PATH = filedialog.askdirectory(initialdir = "/", title = "Select Output Folder")
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select ASC File", 
                                          filetypes = (("ASC files", 
                                                        "*.ASC*"), 
                                                       ("all files", 
                                                        "*.*"))) 
    
    RAW_DATA = filename
    RAW_DATA_NAME = os.path.splitext(os.path.basename(RAW_DATA))[0]
    
    x_extract = np.genfromtxt(RAW_DATA, dtype=str, deletechars="b'")
    
    
    x = np.transpose(x_extract)
    x = x[:,1:]
    
    x = x.astype(float)
    id = 0 
    plotnum = 0
    fig = plt.figure(figsize=(100, 100))
    xx = x[3,:]
    peaks, properties = find_peaks(xx, height=(2,5), distance=5, prominence=1)
    print(peaks)
    print(properties["peak_heights"])
    id_extract = [0]
    id_extract2 = [peaks[0]]
    amax=0
    i = -1
    while True:
        i = i+1
        if(i>(len(peaks)-1)):
            break
        if(np.amax(xx[id_extract[-1]:peaks[i]])<amax):
            print(np.amax(xx[id_extract[-1]:peaks[i]]))
            break
        else:
            if(i == (len(peaks)-1)):
                id_extract.append(peaks[i])
                amax = np.amax(xx[id_extract[-2]:id_extract[-1]])
                print(amax)
            else:
                if((peaks[i+1]-peaks[i])>1000):
                    id_extract.append(peaks[i])
                    id_extract2.append(peaks[i+1])
                    amax = np.amax(xx[id_extract[-2]:id_extract[-1]])
                    print(amax)

    #plt.plot(xx)
    #plt.plot(peaks, xx[peaks])
    #plt.scatter(id_extract, xx[id_extract]+10, s=50, c="red")
    #plt.scatter(id_extract2, xx[id_extract2]+10, s=50, c="green")
    print(id_extract2[-10:-1])
    print(id_extract[-10:-1])
    print(peaks[-10:-1])

    lowerupper = []

    for i in range(len(id_extract2)):
        plotnum = plotnum+1
        plt.subplot(25,1,plotnum)
        endpeak, _ = find_peaks((5-xx[id_extract2[i]-75:id_extract2[i]]), height=(-1,5), distance=5, prominence=0.2)
        endpeak = endpeak[-1]
        print(endpeak)
        lower = id_extract[i]-50
        upper = id_extract2[i]-(75-endpeak)
        lowerupper.append([lower, upper])
        plt.plot(xx[lower:upper+35])
    
    run = np.genfromtxt(RAW_DATA, dtype=str, deletechars="b'")
    run = np.transpose(run)
    
    for i, segment in enumerate(lowerupper):
      run_sample = np.hstack((np.transpose([run[:,0]]), run[:,segment[0]:segment[1]]))
      run_sample = np.vstack((run_sample[0:6,:], run_sample[14,:]))
    
      np.savetxt((OUT_PATH + "/" + "PC" + str(i+6) + '.ASC'), np.transpose(run_sample), fmt='%s', delimiter = '\t')
       
                                                                                                      
window = Tk() 
   
window.title('NVR') 
   
window.geometry("500x250") 
   
window.config(background = "white") 
   
title = Label(window,  
                            text = "ZAM Breath Extraction Program", 
                            width = 50, height = 4,  
                            fg = "blue") 
   
       
button_start = Button(window,  
                        text = "Start", 
                        command = browse)  
   
button_exit = Button(window,  
                     text = "Exit", 
                     command = exit)  
   
title.grid(column = 1, row = 1) 
   
button_start.grid(column = 1, row = 2) 
   
button_exit.grid(column = 1,row = 3) 
   
window.mainloop() 
