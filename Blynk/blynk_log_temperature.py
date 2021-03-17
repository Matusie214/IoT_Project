import sys
sys.path.append('../')
import numpy as np
import _thread
import paho.mqtt.client as mqtt
import time
import datetime
import csv
from datetime import datetime
import BlynkLib
import blynklib
import random
from collections import deque
import math 
from src.termostat_con import temp_get
from src.backend_heat import  set_temp, StoppableThread ,MenageThread
from src.MQTT_pub import send_MSG
global blynk
import requests
global thr
BLYNK_AUTH  = "iDP2biz4a0erZXDaMpuJaSLvbhc3mcon"
BLYNK_AUTH2 = "QOAJk6CMlkI6v6MmU6Juu2cq8g72l62-"

blynk = BlynkLib.Blynk(BLYNK_AUTH,
                       server="34.123.208.229",        # set server address
                       port=8080,                       # set server port
                       heartbeat=30,                    # set heartbeat to 30 secs
                       #log=print                       # use print function for debug logging
                       )

blynk2 =BlynkLib.Blynk(BLYNK_AUTH2,
                       server="34.123.208.229",        # set server address
                       port=8080,                       # set server port
                       heartbeat=30,                    # set heartbeat to 30 secs
                       #log=print                       # use print function for debug logging
                       )
print("end")


global slider_temp
def displayTemp():
    """
    metoda przygotowująca dane do przesłania na aplikację mobilną
    
    structure:
        blynk.virtual_write(nr pinu,'format'.format(zmienna z danymi))
    """
    while True:
        time.sleep(1)
    
        """
        Przypisanie pinów:
        pin |     czujnik
        ----+--------------------------
        V0  |     TEMPERATURA WEWNATRZ
        V1  |     WILGOTNOŚĆ  WEWNĄTRZ
        V2  |     TEMPERATURA ZEWNĄTRZ
        V3  |     WILGOTNOŚĆ  ZEWNĄTRZ
        V4  |     Co2         WEWNĄTRZ
        V5  |     Co2         ZEWNĄTRZ
        V6  |     PIR         DRZWI
        V7  |     PIR         SALON
        V8  |     PIR         GARAŻ
        V9  |     KONTAKTRON  BRAMA
        V10 |     KONTAKTRON  FURTKA
        V11 |     KONTAKTRON  DRZWI
        V12 |     MAGNETOMETR
        V13 |     TRANSOPTOR
        V14 |     ULTRADŹWIĘKOWY
        V15 |     FOTODIODA
        V16 |     RFID
        V17 |     
        V18 |     
        V19 |     
        V20 |     BRAMA
        V21 |     ALARM
        V22 |     GRZAŁKA
        V23 |     WENTYLATOR
        
        """

    
    
        
        #temp = temp_get("temperatura_wew")
        edge_detect(0,"temperatura_wew")
        edge_detect(1,"wilgotnosc_wew")
        edge_detect(2,"temperatura_zew")
        edge_detect(3,"wilgotnosc_zew")
        edge_detect(4,"co2_wew")
        edge_detect(5,"co2_zew")


        pir_drzwi= temp_get("pir_drzwi",nb_rows=1)
        if pir_drzwi==1:
            icon_change(6, 1, BLYNK_AUTH)
        elif pir_drzwi==0:
            icon_change(6, 2, BLYNK_AUTH)
            
        pir_salon= temp_get("pir_salon",nb_rows=1)
        if pir_salon==1:
            icon_change(7, 1, BLYNK_AUTH)
        elif pir_salon==0:
            icon_change(7, 2, BLYNK_AUTH)
        
        pir_garaz= temp_get("pir_garaz",nb_rows=1)
        if pir_garaz==1:
            icon_change(8, 1, BLYNK_AUTH)
        elif pir_garaz==0:
            icon_change(8, 2, BLYNK_AUTH)
        
        kontaktron_brama= temp_get("kontaktron_brama",nb_rows=1)
        if kontaktron_brama==1:
            icon_change(9, 1, BLYNK_AUTH)
        elif kontaktron_brama==0:
            icon_change(9, 2, BLYNK_AUTH)
        elif kontaktron_brama!=1 and kontaktron_brama!=0:
            icon_change(9, 3, BLYNK_AUTH)
        
        kontr_bramka = temp_get("kontaktron_bramka",nb_rows=1)
        if kontr_bramka==1:
            icon_change(10, 1, BLYNK_AUTH)
        elif kontr_bramka==0:
            icon_change(10, 2, BLYNK_AUTH)
            
        kontr_drzwi = temp_get("kontaktron_drzwi",nb_rows=1)
        if kontr_drzwi==1:
            icon_change(11, 1, BLYNK_AUTH)
        elif kontr_drzwi==0:
            icon_change(11, 2, BLYNK_AUTH)
            
        edge_detect(13,"wiatr_sila")
        edge_detect(14,"poziom")
        edge_detect(15,"swiatlo_zew")
        #edge_detect(16,"RFID")
        blynk.virtual_write(19,"ostatni tag:")
        blynk.virtual_write(18,temp_get("RFID",nb_rows=1))
        
        """
  
        #wiatr_kier = temp_get("wiatr_kierunek")
        
       
        
        """
        #print(temp)
        #blynk.virtual_write(0,'{:.2f}'.format(temp))
        
        
        
 
        #blynk2.virtual_write(0,'{:.2f}'.format(temp))
        #blynk2.virtual_write(1,'{:.2f}'.format(hum))
        
        #notifyier()
          
@blynk.VIRTUAL_WRITE(56)
def my_write_handler(value):
    """
    metoda obsługująca akcje z wirtualnego pinu 2
    """
   
    print(value)
    
    if value[0] == '1':
        send_MSG("test_switch","1")
    elif value[0] == '0':
        send_MSG("test_switch","0")
        
        
        
        
@blynk.VIRTUAL_WRITE(30)        
def my_write_handler(value):
    if value[0] == '1':
        send_MSG("gateway_switch","1")
    elif value[0] == '0':
        send_MSG("gateway_switch","0")

@blynk.VIRTUAL_WRITE(31)        
def my_write_handler(value):
    if value[0] == '1':
        send_MSG("gate_switch","1")
    elif value[0] == '2':
        send_MSG("gate_switch","0")
    elif value[0] == '3':
        send_MSG("gate_switch","2")
        
@blynk.VIRTUAL_WRITE(32)        
def my_write_handler(value):
    if value[0] == '1':
        send_MSG("door_switch","1")
    elif value[0] == '0':
        send_MSG("door_switch","0")
@blynk.VIRTUAL_WRITE(27)        
def my_write_handler(value):
    if value[0] == '1':
        send_MSG("gate_switch","1")
    elif value[0] == '2':
        send_MSG("gate_switch","0")
    elif value[0] == '3':
        send_MSG("gate_switch","2")
    
    



@blynk.VIRTUAL_WRITE(24)
def my_write_handler(value):
    """
    metoda obsługująca akcje z wirtualnego pinu 2
    """
    global thr
    global slider_temp
    print(value)
    
    if value[0] == '1':
        thr = StoppableThread(constant_temp=slider_temp)
        thr.start()
        print(thr.state.state," ",str(slider_temp))
        blynk.virtual_write(25,255)
        
        blynk2.virtual_write(25,255)
        pass
    elif value[0] == '0':
        try:
            thr.join()
            print(thr.state.state)
            blynk.virtual_write(25,0)
            
            blynk2.virtual_write(25,0)
        except:
            pass
@blynk.VIRTUAL_WRITE(26)
def my_write_handler(value):
    """
    metoda obsługująca akcje z wirtualnego pinu 3
    """
    global slider_temp
    slider_temp=float(value[0])
    print(value)
    blynk.notify("wartość: ",value)
    blynk2.notify("wartość: ",value)
@blynk.VIRTUAL_WRITE(27)
def my_write_handler(value):
    
    
        blynk.notify("something")
def notifyier():
    while(True):
        time.sleep(20)
        #blynk.notify("something")
        print("time up")
        
def icon_change(pin, value, token):
    new=value
    print("icon")
    print("new",new)
    request_old="http://34.123.208.229:8080/"+str(token)+"/get/V"+str(pin)
    old=requests.get(request_old)
    
    oldF=float(old.json()[0])
    print("old",oldF)
    print(new!=oldF)
    if new!=oldF:
        #print("old",old)
        #print("new",new)
        request="http://34.123.208.229:8080/"+str(token)+"/update/V"+str(pin)+"?value="+str(new)
        val=requests.get(request)
        print("wysłano",request)

    
def edge_detect(pin,collection):
    new= temp_get(collection)

    token="iDP2biz4a0erZXDaMpuJaSLvbhc3mcon"
    #http://34.123.208.229:8080/iDP2biz4a0erZXDaMpuJaSLvbhc3mcon/get/V
    request="http://34.123.208.229:8080/"+str(token)+"/get/V"+str(pin)
    old=requests.get(request)
    oldF=float(old.json()[0])
    #print(round(np.mean(oldF),1))
    #print(new!=oldF)
    if new!=oldF:
        blynk.virtual_write(pin,'{:.2f}'.format(new))
        #print("old",old)
        #print("new",new)
        
_thread.start_new_thread(displayTemp,() )










while True:
    blynk.run()