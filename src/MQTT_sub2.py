import sys
sys.path.append('../')
import paho.mqtt.client as mqtt
import time
import csv
import datetime
import src.Configs.config as cfg
import pymongo
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

mydb = myclient["smart_home_data"]
# This is the Subscriber
#broker_ip = "192.168.0.171"

zapis=False
i=0
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for key in cfg.topic:
        client.subscribe(cfg.topic[key])

def log_data(collection_name, msg, key):
    time=datetime.datetime.now()
    now=time.strftime("%d/%m/%Y %H:%M:%S")
    data = str(msg.payload.decode("utf-8"))
    hum_log={
            "time": now,
            key: float(data)
            }
    myCol=mydb[collection_name]
    x=myCol.insert_one(hum_log)
    print(data)
    print(hum_log)
        
def on_message(client, userdata, msg):
    """
    Metoda uruchamiana w momencie odebrania wiadomości - zajmuje się zapisem wiadmości zawierającej odczyt z czujników
    
    """
    
    if msg.topic==cfg.topic["temperatura"]:
    
        time=datetime.datetime.now()

        now=time.strftime("%d/%m/%Y %H:%M:%S")
        
        data = str(msg.payload.decode("utf-8"))
       
            
        print(data+" "+now)
        print(userdata)
        print(msg.topic)
        #print(i+" "+tab[i])
        plik=open(cfg.path_data_temperature,'a')
        plik.write(now+","+data)
        plik.write("\n")
        plik.close()
    
    elif msg.topic==cfg.topics["tempterature_out"]:
        data=str(msg.payload.decode("utf-8"))
        print(data)
        log_data(cfg.collections["tempterature_out"], data, "temperatura_zew")
        
    
    elif msg.topic==cfg.topics["temperature_in"]:
        log_data(cfg.collections["temperature_in"], msg, "temperatura_wew")
        
    elif msg.topic==cfg.topics["wind_str"]:
        log_data(cfg.collections["wind_str"], msg, "sila_wiatru")
    
    elif msg.topic==cfg.topics["humidity_out"]:
        log_data(cfg.collections["humidity_out"], msg, "wilgotnosc_zew")
    
    elif msg.topic==cfg.topics["humidity_in"]:
        log_data(cfg.collections["humidity_in"], msg, "wilgotnosc_wew")
  
       
    elif msg.topic==cfg.topics["kierunek_wiatru"]:
        #obróbka danych przed wysłaniem
        log_data(cfg.collections["wind_dir"], msg, "kierunek_wiatru")
        
    elif msg.topic==cfg.topics["pir_door"]:
        log_data(cfg.collections["pir_door"], msg, "pir_drzwi")
   
    elif msg.topic==cfg.topics["pir_salon"]:
        log_data(cfg.collections["pir_salon"], msg, "pir_salon")

    elif msg.topic==cfg.topics["pir_garage"]:
        log_data(cfg.collections["pir_garage"], msg, "pir_garaz")
 
    elif msg.topic==cfg.topics["co2_in"]:
        log_data(cfg.collections["co2_in"], msg, "co2_wew")

    elif msg.topic==cfg.topics["co2_out"]:
        log_data(cfg.collections["co2_out"], msg, "co2_zew")
    
    elif msg.topic==cfg.topics["gateway_rswitch"]:
        log_data(cfg.collections["gateway_rswitch"], msg, "kontaktron_brama")
        
    elif msg.topic==cfg.topics["door_rswitch"]:
        log_data(cfg.collections["door_rswitch"], msg, "kontaktron_drzwi")
    
    elif msg.topic==cfg.topics["RFID"]:
        log_data(cfg.collections["RFID"], msg, "RFID")
    
    elif msg.topic==cfg.topics["light_out"]:
        log_data(cfg.collections["light_out"], msg, "swiatlo_zew")
        print(data+" "+now)


def save_climate_data():
    client = mqtt.Client()
    client.connect(cfg.broker_ip, cfg.broker_port)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()


    
def client_mobile():
    client_mobile = mqtt.Client()
    client_mobile.connect(cfg.broker_ip, cfg.broker_port)
    client_mobile.publish("dioda","zapal")
    time.sleep(0.10)
    client_mobile.publish("dioda","zgas")

if __name__ == "__main__":
    save_climate_data()
