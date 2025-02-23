#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
from lib import LCD_2inch
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import cv2 as cv
cap = cap = cv.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)
# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
try:
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_2inch.LCD_2inch(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_2inch.LCD_2inch()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    while True:
        
        # Capture frame-by-frame
        ret, rawframe = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        rawframe = cv.cvtColor(rawframe,cv.COLOR_BGR2RGB)
        frame = Image.fromarray(rawframe)
        # if frame is read correctly ret is True
        
        image = frame.rotate(180)
        disp.ShowImage(image)
        if cv.waitKey(1) == ord('q'):
            disp.module_exit()
            cap.release()
            logging.info("quit:")
            break
        
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    cap.release()
    logging.info("quit:")
    exit()