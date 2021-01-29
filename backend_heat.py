from termostat_con import reg_temp, grzal_con, MenageState
import threading
import time
import config as cfg


global thr
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

flag_first=False

def set_temp(targ_temp):
    """
    Metoda odpowiedzialna za tworzenie wątku dążącego do zalożonej temperatury

    Args:
        flag_first: określa stan początkowy wątku (powołana aby umożliwić zmianę temperatury przez użytkownika)
    """
    
    global thr
    if(flag_first==False):
        thr = StoppableThread(constant_temp=targ_temp)
        thr.start()
        flag_first=True
    else:
        thr.join()
        thr = StoppableThread(constant_temp=targ_temp)
        thr.start()
        flag_first=False

def turn_off(thr_off):
    """
    Metoda kończąca życie wątku
    """
    
    global thr
    if thr_off:
        thr.join()

        
        
