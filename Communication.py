# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 19:50:14 2023

@author: Omar Abdul Qadir
"""

import serial
import time

# This function takes target's port, baudrate, timeout
## return serial object ready to communicate with or null if operation failed
def Comm_Start(serial_target_port, serial_target_baudrate = 9600, serial_target_timeout = None):
    serial_target = serial.Serial(port= serial_target_port, baudrate = serial_target_baudrate, timeout= serial_target_timeout)
    print("Coneccted")
    return serial_target



# This function disconnect the serial port
def Comm_End(serial_target = None):
    if(serial_target != None):
        serial_target.close()



# This function takes serial port object and receive one byte data only
## return one byte data or null if nothing received
def Comm_RxByte(serial_target = None):
    if( type(serial_target) == serial.serialwin32.Serial ):
        c = 0
        while(serial_target.in_waiting == 0):
            time.sleep(0.5)
            c+=1
            if( c == 4 ):
                return None
        return list(serial_target.readall())[0]
    else:
        return None



# This function takes serial port object and receive data frame
## return size and list of the received data or null if nothing received
def Comm_RxFrame(serial_target = None):
    if( type(serial_target) == serial.serialwin32.Serial ):
        c = 0
        while(serial_target.in_waiting == 0):
            time.sleep(0.5)
            c+=1
            if( c == 4 ):
                return None
        return list(serial_target.readall())
    else:
        return None



# This function takes serial port object and one byte data to transmit
def Comm_TxByte(serial_target = None, TxByte = None):
    if( (type(TxByte) == int) and (type(serial_target) == serial.serialwin32.Serial) and (serial_target.is_open == True) ):
        serial_target.write([TxByte])
    else:
        return None



# This function takes serial port object and list of data to transmit
def Comm_TxFrame(serial_target = None, TxList = None):
    if( (type(TxList) == list) and (type(serial_target) == serial.serialwin32.Serial) ):
        serial_target.write(TxList)
    else:
        return None



