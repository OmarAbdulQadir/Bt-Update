# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 15:58:09 2023

@author: Omar Abdul Qadir
"""

from Boot import *

Filename = input("Enter file name: ")
ComPort = input("Enter Communication port: ")

Target = ECU(ComPort, Filename)
Target.ECU_Flash()
Target.ECU_Terminate()
