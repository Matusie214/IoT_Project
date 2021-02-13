import pymongo

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

mydb = myclient["smart_home_data"]
mydb.create_collection("smart_home_data")
print(myclient.list_database_names())

dblist = myclient.list_database_names()
if "smart_home_data" in dblist:
  print("The database exists.")
