from collections import deque
import paho.mqtt.client as mqtt
import numpy as np
import math 
import config as cfg


topic_grzalka = cfg.topic_grzalka

#metoda odczytująca z pliku temp
def temp_get(file_name, nb_rows=10):
    """
    Metoda ustalająca temperaturę poprzez odczytanie 10 rekordów temperatury do wyciągnięcia średniej wyniku

    Args:
        rows:      tablica zwierająca n linii z pliku odczytów
        temps:     tablica odczytanych n elementów
        file_name: ścieżka do pliku zawierającego odczyty
    
    Return:
        Zwraca sumę elementów tablicy rekordów temperatury
    """
    with open(file_name) as temp_file:
        rows=deque(temp_file,nb_rows)
#    print(list(rows))

    temps=[]
    for row in list(rows):
        try:
            record=float(row.split(',')[1].strip('\n'))
            if not math.isnan(record):
                temps.append(record)
        except ValueError:
            pass      
#   print(temps)
        
    
#   print(np.mean(temps))
    """ obsługa wyjątków -> w pliku znajdują się same odczyty nan"""   
    if math.isnan(np.mean(temps)):
        raise ValueError("wszystkie wartosci nan")
    else:
        return np.mean(temps)
    

def grzal_con(flag_on, config=cfg):
    """metoda sterująca włączeniem i wyłączeniem grzałki

    Args:
        flag_on: typ boolean - określa aktualny stan grzałki 
        config:  określenie który plik zawiera konfgiurację

    """
    client_mobile = mqtt.Client()
    client_mobile.connect(config.broker_ip, config.broker_port)
    
    if flag_on and config.last_state == False:
        client_mobile.publish(config.topic_grzalka,config.dic["on"])
        #print(1)
        change_state(True)
        
    elif flag_on == False and config.last_state ==True:
        client_mobile.publish(config.topic_grzalka,config.dic["off"])
        #print(0)
        change_state(False)
        

        
def change_state(new_state):
    """
    metoda zajmująca się zmianą flagi oznaczającą aktualny stan grzałki

    Args:
        new_state: nowy oczekiwany stan grzałki zapisywany do pliku konfiguracyjnego
    """
    #import config_test_termostat_con
    #config_test_termostat_con.last_state = new_state
    import config_symulacja
    config_symulacja.last_state = new_state
    
    
    
#pętla zwrotna utrzymująca temp
# to do : obsługa wyjątku - w momencie otrzymania z czujnika nan
def reg_temp(target_temp,config=cfg):
    """
    Metoda określająca który komunikat pracy grzałki nadać do borkera

    Args:
        target_temp:  temperatura którą chcemy osiągnąć poprzez odczyt z czujnika
        current_temp: temperatura aktualnie odczytywana z czujnika
    """
    current_temp = temp_get(config.path_data)
    
    if target_temp > current_temp:
        #grzałka włącz
        grzal_con(True,config=config)
        #print("true")
    else:
        grzal_con(False,config=config)
        #print("false")
        #grzałka wyłącz
        
reg_temp(2.0)        
