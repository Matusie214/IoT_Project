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
    
    elif msg.topic==cfg.topic["sila_wiatru"]:
        time=datetime.datetime.now()

        now=time.strftime("%d/%m/%Y %H:%M:%S")


        data = str(msg.payload.decode("utf-8"))

        print(data+" "+now)
        print(userdata)
        print(msg.topic)
        plik=open(cfg.path_data_wiatr_sila,'a')
        plik.write(now+","+data)
        plik.write("\n")
        plik.close()
        
    elif msg.topic==cfg.topic["wilgotnosc"]:
        log_data(cfg.collections["humidity"], msg, "wilgotnosc")
      
       
    elif msg.topic==cfg.topic["kierunek_wiatru"]:
        time=datetime.datetime.now()

        now=time.strftime("%d/%m/%Y %H:%M:%S")


        data = str(msg.payload.decode("utf-8"))

        print(data+" "+now)
        print(userdata)
        print(msg.topic)
        plik=open(cfg.path_data_wiatr_kierunek,'a')
        plik.write(now+","+data)
        plik.write("\n")
        plik.close()
        
    elif msg.topic==cfg.topic["pir_stairs_1"]:
        time=datetime.datetime.now()

        now=time.strftime("%d/%m/%Y %H:%M:%S")


        data = str(msg.payload.decode("utf-8"))

        print(data+" "+now)
        print(userdata)
        print(msg.topic)
        plik=open(cfg.path_data_entrance,'a')
        plik.write(now+","+data)
        plik.write("\n")
        plik.close()
    elif msg.topic==cfg.topic["co2"]:
        time=datetime.datetime.now()

        now=time.strftime("%d/%m/%Y %H:%M:%S")


        data = str(msg.payload.decode("utf-8"))

        print(data+" "+now)
        print(userdata)
        print(msg.topic)
        plik=open(cfg.path_data_co2,'a')
        plik.write(now+","+data)
        plik.write("\n")
        plik.close()

    elif msg.topic==cfg.topic["gateway_rswitch"]:
        time=datetime.datetime.now()

        now=time.strftime("%d/%m/%Y %H:%M:%S")


        data = str(msg.payload.decode("utf-8"))

        print(data+" "+now)
        print(userdata)
        print(msg.topic)
        plik=open(cfg.path_data_gate,'a')
        plik.write(now+","+data)
        plik.write("\n")
        plik.close()

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
