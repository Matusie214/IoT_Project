import sys
sys.path.append('../../')
from src.backend_heat import turn_off, set_temp, StoppableThread
from src.termostat_con import temp_get
import threading
import time
import src.Configs.config_test_termostat_con as cfg
import unittest
import paho.mqtt.client as mqtt
import src.Configs.config_symulacja 
import math

def generate_data(path , temp):
    """
    Metoda generująca wstępną temperaturę do testowania pracy grzałki
    """
    
    fileVariable = open(path, 'r+')
    fileVariable.truncate(0)
    fileVariable.close()
    
    for i in range(10):
        plik=open(path,'a')
        plik.write(","+str(temp))
        plik.write("\n")
        plik.close()

def Symuluj(state, dt=0.1, num_steps=150, init_temp=28.0, config=cfg):
    """
    Metoda generująca prosty symulator w celu przeprowadzenia testu na wątkach i termostacie
    
    Args:
        t_change:  zmienna odpowiedzialna za zmianę temperatury
        current:   temperatura początkowa
        num_steps: zmienna określająca ile razy odbędzie się zmiana temperatury
    """
    
    
    
    
    current=temp_get(config.path_data_temperature)
    for i in range(num_steps):
        if state.state==True:
            current+=dt
        else:
            current+=-dt
        time.sleep(0.5)
        plik=open(config.path_data_temperature,'a')
        plik.write(","+str(current))
        plik.write("\n")
        plik.close()
        print("last state: ",state.state)
        print("temp: ", current)
        
    

    
class Set_Temp_Test(unittest.TestCase):
    
    
    
    def test_watku(self):
        """
        Test sprawdzający obecność wątku w różnych scenariuszach

        Wyłączanie grzałki w celu obniżenia temperatury do pożądanej
        """
        thr = StoppableThread(constant_temp=25.0,config=cfg)
        
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
        thr = StoppableThread(constant_temp=35.0,config=cfg)    
        thr.start()
        with self.subTest():
            self.assertEqual(thr.is_alive(),True)

        time.sleep(2)

        thr.join()
        with self.subTest():
            self.assertEqual(thr.is_alive(),False)
    
    def test_set_temp(self):
        generate_data(src.Configs.config_symulacja.path_data_temperature,24.0)
        thr = StoppableThread(constant_temp=25.0,config=src.Configs.config_symulacja)
        thr.start()
        
        Symuluj(thr.state ,init_temp=24.5,config=src.Configs.config_symulacja)
        
        thr.join()
        score=temp_get(src.Configs.config_symulacja.path_data_temperature,1000)
        print(math.ceil(score))
        print(round(score))
        self.assertEqual(round(score),25.0)
        
if __name__ == '__main__':
    unittest.main()
 

        
        
       