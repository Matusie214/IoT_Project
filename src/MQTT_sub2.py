import sys
sys.path.append('../')
import paho.mqtt.client as mqtt
import time
import csv
import datetime
import src.Configs.config as cfg
import pymongo

class Mongo_log():
    def __init__ (self, mongo_adress, db_name):
        self.mongo_adress=mongo_adress
        self.db_name=db_name
        self.my_client=pymongo.MongoClient(self.mongo_adress)
        self.my_db=self.my_client[self.db_name]
        
    def log_data(self, collection_name, msg, key, is_payloade=True):
        time=datetime.datetime.now()
        now=time.strftime("%d/%m/%Y %H:%M:%S")
        if is_payloade:

            print(msg.topic)
            print(str(msg.payload.decode("utf-8")))
            print(now)
            data = str(msg.payload.decode("utf-8"))
        else:
            data=str(msg)
        hum_log={
                "time": now,
                key: float(data)
                }
        #print(hum_log)
        myCol=self.my_db[collection_name]
        x=myCol.insert_one(hum_log)
        #print(myCol.find())
        #result=myCol.find()
        #for element in result:
            #print(element)


    


mongo=Mongo_log("mongodb://127.0.0.1:27017/", "smart_home_data")
# This is the Subscriber
#broker_ip = "192.168.0.171"

zapis=False
i=0
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for key in cfg.topics:
        client.subscribe(cfg.topics[key])


        
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
    
    elif msg.topic==cfg.topics["temperature_out"]:
        
        mongo.log_data(cfg.collections["temperature_out"], msg, "temperatura_zew")
        
    
    elif msg.topic==cfg.topics["temperature_in"]:
        
        mongo.log_data(cfg.collections["temperature_in"], msg, "temperatura_wew")
        
    elif msg.topic==cfg.topics["wind_str"]:
        mongo.log_data(cfg.collections["wind_str"], msg, "sila_wiatru")
    
    elif msg.topic==cfg.topics["humidity_out"]:
        mongo.log_data(cfg.collections["humidity_out"], msg, "wilgotnosc_zew")
    
    elif msg.topic==cfg.topics["humidity_in"]:
        mongo.log_data(cfg.collections["humidity_in"], msg, "wilgotnosc_wew")
  
       
    elif msg.topic==cfg.topics["wind_dir"]:
        #obróbka danych przed wysłaniem
        mongo.log_data(cfg.collections["wind_dir"], msg, "kierunek_wiatru")
        
    elif msg.topic==cfg.topics["pir_door"]:
        mongo.log_data(cfg.collections["pir_door"], msg, "pir_drzwi")
   
    elif msg.topic==cfg.topics["pir_salon"]:
        mongo.log_data(cfg.collections["pir_salon"], msg, "pir_salon")

    elif msg.topic==cfg.topics["pir_garage"]:
        mongo.log_data(cfg.collections["pir_garage"], msg, "pir_garaz")
 
    elif msg.topic==cfg.topics["co2_in"]:
        mongo.log_data(cfg.collections["co2_in"], msg, "co2_wew")

    elif msg.topic==cfg.topics["co2_out"]:
        mongo.log_data(cfg.collections["co2_out"], msg, "co2_zew")
    
    elif msg.topic==cfg.topics["gateway_rswitch"]:
        mongo.log_data(cfg.collections["gateway_rswitch"], msg, "kontaktron_bramka")
    
    elif msg.topic==cfg.topics["gate_rswitch"]:
        mongo.log_data(cfg.collections["gate_rswitch"], msg, "kontaktron_brama")
        
    elif msg.topic==cfg.topics["door_rswitch"]:
        mongo.log_data(cfg.collections["door_rswitch"], msg, "kontaktron_drzwi")
    
    elif msg.topic==cfg.topics["RFID"]:
        mongo.log_data(cfg.collections["RFID"], msg, "RFID")
    
    elif msg.topic==cfg.topics["light_out"]:
        mongo.log_data(cfg.collections["light_out"], msg, "swiatlo_zew")
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
