import sys
sys.path.append('../../')
import time
import unittest
import pymongo
from src.MQTT_sub2 import Mongo_log

mongo=Mongo_log("mongodb://127.0.0.1:27017/", "test_database")

class collection_create(unittest.TestCase):
    
    def test_x(self):
        """
        Test sprawdzający poprawność tworzenia kolekcji wraz zapisem
        """
        #myCol=mongo.my_db["wilgotnosc_zew"]
        myCol=mongo.my_db["test_collection"]
        #myCol.drop()
        print(mongo.my_client.list_database_names())
        test_log={
        "time":"10/02/2021 13:52:11",
        "record": "25.50"
        }
        myCol.insert_one(test_log)
        dblist=mongo.my_client.list_database_names()
        if "test_database" in dblist:
            print("The database exists.")
        cols = mongo.my_db.collection_names()
        for c in cols:
            print (c)
        print(myCol.find().limit(5))
        for x in myCol.find().sort("time",-1).limit(5):
            print(x)
        print(list(myCol.find({},{ "record": 25.5 }))[0]["record"])
        self.assertEqual(list(myCol.find({},{ "record": 25.5 }))[0]["record"],"25.50")
        
        
    def log_data_test(self):
        """
        to do:
        wysyłać wiadomość przez mqtt i nasłuchiwać tamtau w celach testowych
        muk
        """
        print("test")
        mongo.log_data("test_collection3","10.0","test_key")
        cols = mongo.my_db.collection_names()
        for c in cols:
            print (c)
        myCol=mongo.my_db["test_collection3"]
        print(myCol.find().limit(5))
        self.assertEqual(1,1)
        
        """time=datetime.datetime.now()
        now=time.strftime("%d/%m/%Y %H:%M:%S")
        data = str(msg.payload.decode("utf-8"))
        hum_log={
                "time": now,
                key: float(data)
                }
        myCol=mydb[collection_name]
        x=myCol.insert_one(hum_log)
        print(data)
        print(hum_log)"""


if __name__ == '__main__':
    unittest.main()