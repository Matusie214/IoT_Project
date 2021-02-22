import sys
sys.path.append('../')
import numpy as np
import _thread
import paho.mqtt.client as mqtt
import time
import datetime
import csv
import BlynkLib
from collections import deque
import math 
from src.termostat_con import temp_get
from src.backend_heat import turn_off, set_temp, StoppableThread
global blynk
global thr
BLYNK_AUTH = "iDP2biz4a0erZXDaMpuJaSLvbhc3mcon"

blynk = BlynkLib.Blynk(BLYNK_AUTH,
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
    
        temp = temp_get("temperatura_zew")
        hum = temp_get("wilgotnosc_zew")
        move = temp_get("kontaktron_bramka")
        print(temp)
        blynk.virtual_write(0,'{:.2f}'.format(temp))
        blynk.virtual_write(1,'{:.2f}'.format(hum))

@blynk.VIRTUAL_WRITE(2)
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
        blynk.virtual_write(4,255)
        pass
    elif value[0] == '0':
        try:
            thr.join()
            print(thr.state.state)
            blynk.virtual_write(4,0)
        except:
            pass
@blynk.VIRTUAL_WRITE(3)
def my_write_handler(value):
    """
    metoda obsługująca akcje z wirtualnego pinu 3
    """
    global slider_temp
    slider_temp=float(value[0])
    print(value)
_thread.start_new_thread(displayTemp,() )
while True:
    blynk.run()