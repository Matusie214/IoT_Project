import sys
sys.path.append('../../')
from collections import deque
import paho.mqtt.client as mqtt
import numpy as np
import math 
import src.Configs.config as cfg
from src.MQTT_sub2 import Mongo_log
import pymongo

mongo=Mongo_log("mongodb://127.0.0.1:27017/", "smart_home_data")
topic_grzalka = cfg.topic["temperatura"]

class MenageState():
    """
    Klasa informująca o stanie w jakim jest grzałka
    """
    def __init__(self) :
        self.state=True
    
    def change_state(self, new_state):
        self.state=new_state



#metoda odczytująca z pliku temp
def temp_get(coll_name, nb_rows=2, mongodb=mongo):
    """
    Metoda ustalająca temperaturę poprzez odczytanie 10 rekordów temperatury do wyciągnięcia średniej wyniku

    Args:
        mongo:     połaczenie z bazą
        rows:      tablica zwierająca n rekordów z bazy
        temps:     tablica odczytanych n elementów
        coll_name: nazwa kolekcji z odczytami
    
    Return:
        Zwraca średnią z sumy elementów tablicy rekordów temperatury
    """
    myCol=mongodb.my_db[coll_name]
    
    rows=list(myCol.find().sort("_id",-1).limit(nb_rows))
    temps=[]
    if coll_name=="RFID" or "wiatr_kierunek":
        for row in rows:
            record=row[list(row.keys())[2]]
            print(record)
        return record
            
    else:
        for row in rows:
            try:
                record=float(row[list(row.keys())[2]])
                #print(row.keys(),record)
                if not math.isnan(record):
                    temps.append(record)
            except ValueError:
                pass      
        """
        obsługa wyjątków
        """
        if math.isnan(np.mean(temps)):
            raise ValueError("wszystkie wartosci nan")
        else:
            return round(np.mean(temps),nb_rows) 

        
    

def grzal_con(flag_on, state, config=cfg):
    """metoda sterująca włączeniem i wyłączeniem grzałki

    Args:
        flag_on: typ boolean - określa aktualny stan grzałki 
        config:  plik z konfiguracją metod

    """
    client_mobile = mqtt.Client()
    client_mobile.connect(config.broker_ip, config.broker_port)
    
    if flag_on and state.state == False:
        client_mobile.publish(config.topic["temperatura"],config.dic["on"])
        #print(1)
        state.change_state(True)
        
    elif flag_on == False and state.state ==True:
        client_mobile.publish(config.topic["temperatura"],config.dic["off"])
        #print(0)
        state.change_state(False)
        

        
 
        
        
#pętla zwrotna utrzymująca temp
# to do : obsługa wyjątku - w momencie otrzymania z czujnika nan
def reg_temp(target_temp, state, config=cfg):
    """
    Metoda określająca który komunikat pracy grzałki nadać do borkera

    Args:
        mongod:       połączenie z bazą danych
        target_temp:  temperatura którą chcemy osiągnąć poprzez odczyt z czujnika
        current_temp: temperatura aktualnie odczytywana z czujnika
    """
    mongod=Mongo_log("mongodb://127.0.0.1:27017/", config.db_name)
    current_temp = temp_get(config.collections["temperature_in"], nb_rows=2, mongodb=mongod)
    if target_temp > current_temp:
        #grzałka włącz
        grzal_con(True, state, config=config)
        #print("true")
    else:
        grzal_con(False, state, config=config)
        #print("false")
        #grzałka wyłącz
        
#reg_temp(2.0)        
