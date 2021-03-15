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
import src.schedule as schedule
mongo=Mongo_log("mongodb://127.0.0.1:27017/", "test_database")
mongo2=Mongo_log("mongodb://127.0.0.1:27017/", "smart_home_schedule_test")
collection="schedule_test"

mongo2.show_data(collection)
print("witam")
#print(schedule.getPeriods(mongo2,collection,"Friday"))
print(schedule.schedule_temp(mongo2,collection))  
#class Schedule_Temp_Test(unittest.TestCase):
    
            
    #def x(self):
        