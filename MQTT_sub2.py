import paho.mqtt.client as mqtt
import time
import csv
import datetime



# This is the Subscriber
broker_ip = "192.168.0.171"
topic =[ "harmonogram_new","light_salon","heating_switch","grzalka"]

def on_connect(client, userdata, flags, rc):
  print("Connected with result code " + str(rc))
  client.subscribe(topic[0])
  client.subscribe(topic[1])
  client.subscribe(topic[2])
  client.subscribe(topic[3])

def on_message(client, userdata, msg):
    time=datetime.datetime.now()
    
    now=time.strftime("%d/%m/%Y %H:%M:%S")
    
    
    data = str(msg.payload.decode("utf-8"))
    
    print(data+" "+now)
    print(userdata)
    print(msg.topic)
    plik=open('Mess.csv','a')
    plik.write(now+","+data)
    plik.write("\n")
    plik.close()

def save_climate_data():
    client = mqtt.Client()
    client.connect(broker_ip, 1883)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()
def client_mobile():
    client_mobile = mqtt.Client()
    client_mobile.connect(broker_ip, 1883)
    client_mobile.publish("dioda","zapal")
    time.sleep(0.10)
    client_mobile.publish("dioda","zgas")

if __name__ == "__main__":
    save_climate_data()
