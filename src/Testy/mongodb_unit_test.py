import sys
sys.path.append('../../')
import time
import unittest
import pymongo
from src.MQTT_sub2 import Mongo_log

mongo=Mongo_log("mongodb://127.0.0.1:27017/", "test_database")

class collection_create(unittest.TestCase):
    
    def test_x(self):
        
        myCol=mongo.my_db["test_collection"]
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
        self.assertEqual(1,1)
        
    def log_data_test(self):
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