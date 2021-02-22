import sys
sys.path.append('../../')
from src.termostat_con import reg_temp, grzal_con, temp_get, MenageState
import threading
import time
#from backend_heat import *
#import backend_heat.StoppableThread
import src.Configs.config_test_termostat_con as cfg
import unittest
import paho.mqtt.client as mqtt


state=MenageState()
class Temp_Get_Test(unittest.TestCase):
    
   
    def test_x(self):
        """ test z plikiem posiadającym same wartości typu String """        
        self.assertRaises(ValueError, temp_get, "./../../Data/test_temp3.csv")
        
    def test_y(self):
        """ test sprawdzający poprawność działania funkcji odczytu metody """        
        avg_temp = temp_get(coll_name="test_temp_coll_1",nb_rows=3)
        self.assertEqual(avg_temp,28.5)
        
    def test_z(self):
        """ test z plikiem posiadającym wartości nan """        
        avg_temp = temp_get(coll_name="test_temp_coll_4",nb_rows=10)
        self.assertEqual(avg_temp,30.0)
        

    def test_zx(self):
        """ test z plikiem posiadającym mniej rekordów niż wymagana liczba podana w żądaniu """        
        avg_temp = temp_get(coll_name="test_temp_coll_5",nb_rows=2)
        self.assertEqual(avg_temp,30.0)


class Termostat_con_test(unittest.TestCase):
    

    
    def test_grzal_con(self):
        """ Test sprawdzający poprawność wysyłanych sygnałów do brokera przez metodę grzal_con (włączenie grzałki """
        
        
        
        def on_message(client, userdata, message):
                with self.subTest():
                    self.assertEqual(str(message.payload.decode("utf-8")),"1")
                with self.subTest():
                    self.assertEqual(message.topic,cfg.topic_grzalka)
                
                
        client = mqtt.Client() #create new instance
        client.on_message=on_message #attach function to callback

        client.connect(cfg.broker_ip) #connect to broker
        client.loop_start() #start the loop

        client.subscribe(cfg.topic_grzalka)
        state.change_state(False)
        grzal_con(True, state, config=cfg)
        
        #client.publish(cfg.topic_grzalka,cfg.dic["on"])
        time.sleep(4) # wait
        client.loop_stop() #stop the loop
        
        
    
    def test_grzal_con2(self):
        """ Test sprawdzający poprawność wysyłanych sygnałów do brokera przez metodę grzal_con (wyłączenie grzałki) """
        
        
        def on_message(client, userdata, message):
                with self.subTest():
                    self.assertEqual(str(message.payload.decode("utf-8")),"0")
                with self.subTest():
                    self.assertEqual(message.topic,cfg.topic_grzalka)
                
                
        client = mqtt.Client() #create new instance
        client.on_message=on_message #attach function to callback

        client.connect(cfg.broker_ip) #connect to broker
        client.loop_start() #start the loop

        client.subscribe(cfg.topic_grzalka)
        state.change_state(True)
        grzal_con(False, state, config=cfg)
        
        #client.publish(cfg.topic_grzalka,cfg.dic["on"])
        time.sleep(4) # wait
        client.loop_stop() #stop the loop
   
    def test_grzal_con3(self):
        """ Test sprawdzający wystąpienie przypadów zabronionych """
        
        
        def on_message(client, userdata, message):
                with self.subTest():
                    self.assertEqual(str(message.payload.decode("utf-8")),"0","Ten przypadek nie powinien nastąpić")
                with self.subTest():
                    self.assertEqual(str(message.payload.decode("utf-8")),"1","Ten przypadek nie powinien nastąpić")
                
                
        client = mqtt.Client() #create new instance
        client.on_message=on_message #attach function to callback

        client.connect(cfg.broker_ip) #connect to broker
        client.loop_start() #start the loop

        client.subscribe(cfg.topic_grzalka)
        state.change_state(True)
        grzal_con(True, state, config=cfg)
        state.change_state(False)
        grzal_con(False, state, config=cfg)
        #client.publish(cfg.topic_grzalka,cfg.dic["on"])
        time.sleep(4) # wait
        client.loop_stop() #stop the loop

    
    
    
    
    
    
class Termostat_con_test2(unittest.TestCase):
       
    #dodać 2 testy (wył grzałka -> wył, wł grzałka -> wł)
    
    def test_reg_temp(self):
        """ Test sprawdzający poprawność określania porządanego stanu grzałki -> włączenie w celu podniesienia temperatury """
        def on_message(client, userdata, message):
            self.assertEqual(str(message.payload.decode("utf-8")),"1")
                
    
            
        client = mqtt.Client() #create new instance
        client.on_message=on_message #attach function to callback

        client.connect(cfg.broker_ip) #connect to broker
        client.loop_start() #start the loop

        client.subscribe(cfg.topic_grzalka)
        state.change_state(False)
        reg_temp(35.6, state, config=cfg)
        time.sleep(4) # wait
        client.loop_stop() #stop the loop
    
    def test_reg_temp2(self):
        """ Test sprawdzający poprawność określania porządanego stanu grzałki -> wyłączenie w celu obniżenia temperatury """
        def on_message(client, userdata, message):
            self.assertEqual(str(message.payload.decode("utf-8")),"0")
                
    
            
        client = mqtt.Client() #create new instance
        client.on_message=on_message #attach function to callback

        client.connect(cfg.broker_ip) #connect to broker
        client.loop_start() #start the loop

        client.subscribe(cfg.topic_grzalka2)
        state.change_state(True)
        reg_temp(22.0, state, config=cfg)
        time.sleep(4) # wait
        client.loop_stop() #stop the loop
        
        
if __name__ == '__main__':
    unittest.main()
    
    
    


