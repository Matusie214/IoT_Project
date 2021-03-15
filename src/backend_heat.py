import sys
sys.path.append('../')
from src.termostat_con import reg_temp, grzal_con, MenageState
import threading
import time
import src.Configs.config as cfg
from src.schedule import schedule_temp
from src.MQTT_sub2 import Mongo_log
import pymongo
mongo=Mongo_log("mongodb://127.0.0.1:27017/", "smart_home_schedule_test")
collection="schedule_test"


class MenageThread():
    """
    Klasa informująca o stanie w jakim jest grzałka 
    """
    def __init__(self,mongo, collection, config=cfg) :
        self.thr=None
        self.mongo=mongo
        self.collection=collection
        self.config=config
        
        
    def new_thread(self):
        if self.thr!=None :
            self.thr.join()
        self.thr=StoppableThread(self.mongo, self.collection, config=self.config)
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

    def __init__(self, mongo, collection,  config=cfg):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
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
            constant_temp=schedule_temp(mongo, collection)
            reg_temp(constant_temp, self.state, config=self.config)
            
        self.state.change_state(False)
        
       
    
#thr = StoppableThread(constant_temp=25.0)
#thr.start()
#time.sleep(6)
#thr.join()
        
#thr2=StoppableThread(constant_temp=25.0)
#thr2.start()



def set_temp(thr_menager):
    """
    Metoda odpowiedzialna za tworzenie wątku dążącego do zalożonej temperatury
    Args:
        flag_first: określa stan początkowy wątku (powołana aby umożliwić zmianę temperatury przez użytkownika)
    """
    thr_menager.new_thread()



        
class Schedule_menager():
    
    def __init__(self) :
        self.init_temp=20.0
    
    def schedule_start():
        target_temp=schedule_temp(mongo, collection)
        set_temp(targ_temp)
    
    #def schedule_end():
        