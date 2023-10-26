# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 19:50:29 2023

@author: Omar Abdul Qadir
"""

from math import ceil

# This function takes file name and try to open it
## It returns file object if found, else retuen None
def fileObjectHandler(fileName = None):
    if(type(fileName) == str):
        try:
            file = open(fileName, "r")
            return file
        except FileNotFoundError:
            print("File not found")
            return None
    else:
        print("File name type error")
        return None


# This function takes file object fetchs a line
## It returns a list of bytes in the line or None
def fileFetchLine(file = None):
    if(file != None):
        try:
            return file.readline()
        except IOError:
            print("File type error")
            return None
    else:
        print("File object must be passed as an arrgument")
        return None


# This function takes line list
## It returns the actual data in the line
def fileParseline(Line = None):
    if(type(Line) == str):
        try:
            if(Line[:-1] == ":00000001FF"):
                print("End of file")
                return None
            else:
                data = []
                Line = Line[9:-3]
                for i in range(0, len(Line), 2):
                    data.append(int(Line[i:i+2], 16))
                return data
        except:
            print("Exception")
            return None
    else:
        print("Line Type error")
        return None


# This function takes hex filename
## It returns a list of the actual data in the file
def hexTolist(fileName = None):
    Data = []    
    hexFile = fileObjectHandler(fileName)
    hexLine = "Start"
    c=0
    while(len(hexLine) > 0):
        hexLine = fileFetchLine(hexFile)
        intLine = fileParseline(hexLine)
        try:
            Data+= intLine
        except TypeError:
            print("End of parsing")
    Data += (ceil(len(Data)/128)*128-len(Data))*[255]
    return Data





