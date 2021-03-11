import sys
sys.path.append('../')
from src.termostat_con import reg_temp, grzal_con, MenageState
import threading
import time
import src.Configs.config as cfg
import src.schedule
from MQTT_sub2 import Mongo_log
import pymongo
mongo=Mongo_log("mongodb://127.0.0.1:27017/", "smart_home_schedule_test")

class MenageThread():
    """
    Klasa informująca o stanie w jakim jest grzałka
    """
    def __init__(self, temp) :
        self.thr=None
        
    def new_thread(self,new_temp):
        if self.thr!=None :
            self.thr.join()
        self.thr=StoppableThread(constant_temp=new_temp)
        self.thr.start()
        
    def turn_off(self):
    """
    Metoda kończąca życie wątku
    """
        if self.thr!=None :
            self.thr.join()


class StoppableThread(threading.Thread):
    """
        Definicja pracy, inicjacji oraz zatrzymania wątków
    """

    def __init__(self, constant_temp=21.0, config=cfg):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
        self.constant_temp = constant_temp
        self.config = config
        self.state = MenageState()

    def stop(self):
        self._stop_event.set()
        "zatrzymanie wątku"

    def join(self, *args, **kwargs):
        self.stop()
        super(StoppableThread,self).join(*args, **kwargs)
        
    def run(self):
        while not self._stop_event.is_set():
            reg_temp(self.constant_temp, self.state, config=self.config)
            
        self.state.change_state(False)
        
       
    
#thr = StoppableThread(constant_temp=25.0)
#thr.start()
#time.sleep(6)
#thr.join()
        
#thr2=StoppableThread(constant_temp=25.0)
#thr2.start()



def set_temp(targ_temp,thr_menager):
    """
    Metoda odpowiedzialna za tworzenie wątku dążącego do zalożonej temperatury
    Args:
        flag_first: określa stan początkowy wątku (powołana aby umożliwić zmianę temperatury przez użytkownika)
    """
        thr_menager.new_thread(targ_temp)



        
class Schedule_menager():
    
    def schedule_start():
        target_temp=schedule_temp(mongo, collection)
        set_temp(targ_temp)
    
    def schedule_end():
        