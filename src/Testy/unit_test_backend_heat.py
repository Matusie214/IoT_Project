import sys
sys.path.append('../../')
from src.backend_heat import  StoppableThread
from src.termostat_con import temp_get
import threading
import time
from src.MQTT_sub2 import Mongo_log
import src.Configs.config_test_termostat_con 
import unittest
import paho.mqtt.client as mqtt
from datetime import datetime
import src.Configs.config_symulacja as cfg
import math
mongo=Mongo_log("mongodb://127.0.0.1:27017/", "test_database")
mongo2=Mongo_log("mongodb://127.0.0.1:27017/", "smart_home_schedule_test")
def generate_data(coll_name, temp, nb_rows=10, mongodb=mongo):
    """
    Metoda generująca wstępną temperaturę do testowania pracy grzałki
    """
    #mongodb.my_client[coll_name].drop()
    
    for i in range(nb_rows):
        mongodb.log_data(coll_name, temp, "test_temp", is_payloade=False)

def Symuluj(coll_name, state, dt=0.1, num_steps=150, init_temp=28.0, mongod=mongo):
    """
    Metoda generująca prosty symulator w celu przeprowadzenia testu na wątkach i termostacie
    
    Args:
        t_change:  zmienna odpowiedzialna za zmianę temperatury
        current:   temperatura początkowa
        num_steps: zmienna określająca ile razy odbędzie się zmiana temperatury
    """
    
    
    
    
    current=temp_get(coll_name, nb_rows=2, mongodb=mongod)
    for i in range(num_steps):
        if state.state==True:
            current+=dt
        else:
            current+=-dt
        time.sleep(0.5)
        mongod.log_data(coll_name, current, "test_temp", is_payloade=False)
        print("last state: ",state.state)
        print("temp: ", current)
        
    

    
class Set_Temp_Test(unittest.TestCase):
    '''   
    
    
    def test_watku(self):
        """
        Test sprawdzający obecność wątku w różnych scenariuszach

        Wyłączanie grzałki w celu obniżenia temperatury do pożądanej
        """
        thr = StoppableThread(mongo2,"schedule_test",config=cfg)
        
        thr.start()
        with self.subTest():
            self.assertEqual(thr.is_alive(),True)

        time.sleep(2)

        thr.join()
        with self.subTest():
            self.assertEqual(thr.is_alive(),False)
        
        """
        Włączanie grzałki w celu podniesienia temperatury
        """
        thr = StoppableThread(mongo2,"schedule_test",config=cfg)    
        thr.start()
        with self.subTest():
            self.assertEqual(thr.is_alive(),True)

        time.sleep(2)

        thr.join()
        with self.subTest():
            self.assertEqual(thr.is_alive(),False)
    '''
    def test_set_temp(self):
        cfg_sym=src.Configs.config_symulacja
        generate_data(cfg_sym.collections["temperature_in"], 24.0, mongodb=mongo)
        thr = StoppableThread(mongo2,"schedule_test",config=cfg_sym)
        thr.start()
        
        Symuluj(cfg_sym.collections["temperature_in"], thr.state ,init_temp=24.5,mongod=mongo)
        
        thr.join()
        score=temp_get(cfg_sym.collections["temperature_in"],150,mongodb=mongo)
        print(math.ceil(score))
        print(round(score))
        self.assertEqual(round(score),25.0)
        
if __name__ == '__main__':
    unittest.main()
 

        
        
       