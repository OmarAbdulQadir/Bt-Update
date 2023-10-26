# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 03:37:30 2023

@author: Omar Abdul Qadir
"""

import Communication
import fileParse
from time import sleep

class ECU(object):
    requests = {
                "ECU Reset": [0x01, 0x11],
                "Programming session": [0x2, 0x10, 0x3],
                "Download": [0x5, 0x34, 0x1, 0x1, 0x0],
                "Transfere Data": [0x82, 0x36, 0x80],
                "Transfere exit": [0x1, 0x37]
                }
    def __init__(self, comPort, fileName):
        self.target = Communication.Comm_Start(comPort, 9600, 0.25)
        sleep(2.5)
        self.Data = fileParse.hexTolist(fileName)
        self.Dframe = []
        for i in range(0, len(self.Data), 128):
            self.Dframe.append(self.requests["Transfere Data"]+self.Data[i:i+128])
            
    def Send_ECUReset(self):
        Communication.Comm_TxFrame(self.target, self.requests["ECU Reset"])
        ECU_Respond = Communication.Comm_RxFrame(self.target)
        if(ECU_Respond == [81]):
            print("ECU Reset ok")
        elif(ECU_Respond == [127]):
            print("ECU Reset not ok")
        else:
            print("Not responding")
            return None
        return ECU_Respond
        
    def Send_ProgrammingSession(self):
        Communication.Comm_TxFrame(self.target, self.requests["Programming session"])
        ECU_Respond = Communication.Comm_RxFrame(self.target)
        if(ECU_Respond == [80]):
            print("Programming session request ok")
        elif(ECU_Respond == [127]):
            print("Programming session request not ok")
        else:
            print("Not responding")
            return None
        return ECU_Respond

    def Send_Download(self):
        Communication.Comm_TxFrame(self.target, (self.requests["Download"]+[len(self.Dframe)]))
        ECU_Respond = Communication.Comm_RxFrame(self.target)
        if(ECU_Respond == [116]):
            print("Download request ok")
        elif(ECU_Respond == [127]):
            print("Download request not ok")
        else:
            print("Not responding")
            return None
        return ECU_Respond
    
    def Send_TransfereData(self, PageData):
        Communication.Comm_TxFrame(self.target, PageData)
        ECU_Respond = Communication.Comm_RxFrame(self.target)
        if(ECU_Respond == [118]):
            print("Transfere data ok")
        elif(ECU_Respond == [127]):
            print("Transfere data not ok")
        else:
            print("Not responding")
            return None
        return ECU_Respond
    
    def Send_TransfereExit(self):
        Communication.Comm_TxFrame(self.target, self.requests["Transfere exit"])
        ECU_Respond = Communication.Comm_RxFrame(self.target)
        if(ECU_Respond == [119]):
            print("Transfere exit ok")
        elif(ECU_Respond == [127]):
            print("Transfere exit not ok")
        else:
            print("Not responding")
            return None
        return ECU_Respond
    
    def ECU_Flash(self):
        ECU_Respond = self.Send_ProgrammingSession()
        if(ECU_Respond == [80]):
            ECU_Respond = self.Send_Download()
            if(ECU_Respond == [116]):
                for frame in self.Dframe:
                    ECU_Respond = self.Send_TransfereData(frame)
                    if(ECU_Respond == [118]):
                        continue
                    else:
                       self.Send_ECUReset()
                       break;
                if(ECU_Respond == [118]):
                    ECU_Respond = self.Send_TransfereExit()
                    if(ECU_Respond == [119]):
                        print("Update Success")
                    else:
                        self.Send_ECUReset()
            else:
                self.Send_ECUReset()
        elif(ECU_Respond == [127]):
            print("Failed")
            self.ECU_Update()
            return None
        else:
            print("Failed")
            self.ECU_Flash()
            return None
            
    def ECU_Update(self):
        ECU_Respond = self.Send_Download()
        if(ECU_Respond == [116]):
            for frame in self.Dframe:
                ECU_Respond = self.Send_TransfereData(frame)
                if(ECU_Respond == [118]):
                    continue
                else:
                   self.Send_ECUReset()
                   break;
            if(ECU_Respond == [118]):
                ECU_Respond = self.Send_TransfereExit()
                if(ECU_Respond == [119]):
                    print("Update Success")
                else:
                    self.Send_ECUReset()
        else:
            print("Failed")
            self.ECU_Update()
            return None
                
    def ECU_Terminate(self):
        Communication.Comm_End(self.target)
        del(self)
