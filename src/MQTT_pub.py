import sys
sys.path.append('../')
import paho.mqtt.client as mqtt
import time
import csv
import datetime
import src.Configs.config as cfg
import pymongo

def send_MSG(topic, msg):
    """Metoda obsługująca wysyłanie wiadomości przez MQTT do urządzeń wyjściowych"
    
    Args:
        topic - temat wiadomości
        msg   - treść wiadomości
    
    """
    client = mqtt.Client()
    client.connect(cfg.broker_ip, cfg.broker_port)
    client.publish(topic,msg)
    
    #client.publish("dioda","zgas")
    
    
send_MSG("test_switch","1")
time.sleep(10)
send_MSG("test_switch","0")