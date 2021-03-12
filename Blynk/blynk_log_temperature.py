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
        V15 |     ELEKTROZACZEP DRZWI
        V16 |     ELEKTROZACZEP FURTKA
        V17 |     FOTODIODA
        V18 |     LAMPA
        V19 |     RFID
        V20 |     BRAMA
        V21 |     ALARM
        V22 |     GRZAŁKA
        V23 |     WENTYLATOR
        
        """
    
    
    
    
        temp = temp_get("temperatura_wew")
        temp2 = temp_get("temperatura_zew")
        
        hum = temp_get("wilgotnosc_wew")
        hum2 = temp_get("wilgotnosc_zew")
        
        co2 = temp_get("co2_zew")
        co22 = temp_get("co2_wew")
        
        kontr_bramka = temp_get("kontaktron_bramka")
        
        """
        
        kontr_brama = temp_get("kontaktron_brama")
        kontr_drzwi = temp_get("kontaktron_drzwi")
        
        pir_drzwi  = temp_get("pir_drzwi")
        pir2_salon = temp_get("pir_salon")
        pir3_garaz = temp_get("pir_garaz")
        
        #RFID = temp_get("RFID")
        
        wiatr_predkosc = temp_get("wiatr_kierunek")
        #wiatr_kier = temp_get("wiatr_sila")
        
        fotodioda = temp_get("swiatlo_zew")
        
        ultradzwiekowy = temp_get("poziom")
        """
        #print(temp)
        blynk.virtual_write(0,'{:.2f}'.format(temp))
        blynk.virtual_write(1,'{:.2f}'.format(hum))
        blynk.virtual_write(2,'{:.2f}'.format(temp2))
        blynk.virtual_write(3,'{:.2f}'.format(hum2))
        blynk.virtual_write(4,'{:.2f}'.format(co22))
        blynk.virtual_write(5,'{:.2f}'.format(co2))
        blynk.virtual_write(10,'{:.2f}'.format(kontr_bramka))
        """blynk.virtual_write(6,'{:.2f}'.format(pir_drzwi))
        blynk.virtual_write(7,'{:.2f}'.format(pir2_salon))
        blynk.virtual_write(8,'{:.2f}'.format(pir3_garaz))
        blynk.virtual_write(9,'{:.2f}'.format(kontr_brama))
        
        blynk.virtual_write(11,'{:.2f}'.format(kontr_drzwi))
        #blynk.virtual_write(12,'{:.2f}'.format(wiatr_kier))
        blynk.virtual_write(13,'{:.2f}'.format(wiatr_predkosc))
        blynk.virtual_write(14,'{:.2f}'.format(ultradzwiekowy))
        blynk.virtual_write(17,'{:.2f}'.format(fotodioda))
        #blynk.virtual_write(19,'{:.2f}'.format(RFID))
        """
        blynk2.virtual_write(0,'{:.2f}'.format(temp))
        blynk2.virtual_write(1,'{:.2f}'.format(hum))
        
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
    wartosc=value[0]
    otwarte=0
    while(wartosc!=0):
        kontr_bramka = temp_get("kontaktron_bramka",nb_rows=1)
        if wartosc == '1' and (kontr_bramka==1.0 and otwarte==0) :
            print("nacisnieto")
            
            
            blynk.virtual_write(27,2) # Show image 1 - Widget on V3
            while kontr_bramka!=0.0:
                kontr_bramka = temp_get("kontaktron_bramka",nb_rows=1)
                time.sleep(0.5)
        elif kontr_bramka==0.0 :
            print("otwarto")
            
            otwarte=1
            blynk.virtual_write(27,1) # Show image 2 - Widget on V3
            while kontr_bramka!=1.0:
                kontr_bramka = temp_get("kontaktron_bramka",nb_rows=1)
                time.sleep(0.5)
        elif otwarte==1 and kontr_bramka==1.0 :
            print("zamknieto")
            blynk.virtual_write(27,2)
            time.sleep(0.5)
            wartosc=0
        else:
            otwarte=1
            time.sleep(0.5)
            
@blynk.VIRTUAL_WRITE(32)        
def my_write_handler(value):
    wartosc=value[0]
    otwarte=0
    while(wartosc!=0):
        kontr_bramka = temp_get("kontaktron_bramka",nb_rows=1)
        if wartosc == '1' and (kontr_bramka==1.0 and otwarte==0) :
            print("nacisnieto")
            
            
            blynk.virtual_write(29,2) # Show image 1 - Widget on V3
            while kontr_bramka!=0.0:
                kontr_bramka = temp_get("kontaktron_bramka",nb_rows=1)
                time.sleep(0.5)
        elif kontr_bramka==0.0 :
            print("otwarto")
            
            otwarte=1
            blynk.virtual_write(29,1) # Show image 2 - Widget on V3
            while kontr_bramka!=1.0:
                kontr_bramka = temp_get("kontaktron_bramka",nb_rows=1)
                time.sleep(0.5)
        elif otwarte==1 and kontr_bramka==1.0 :
            print("zamknieto")
            blynk.virtual_write(29,2)
            time.sleep(0.5)
            wartosc=0
        else:
            otwarte=1
            time.sleep(0.5)

    
@blynk.VIRTUAL_READ(10)
def my_read_handler():
    kontr_bramka = temp_get("kontaktron_bramka",nb_rows=1)
    # this widget will show some time in seconds..
    blynk.virtual_write(10, kontr_bramka)


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
_thread.start_new_thread(displayTemp,() )
while True:
    blynk.run()