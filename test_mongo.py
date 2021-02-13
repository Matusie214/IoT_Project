import pymongo

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

mydb = myclient["mydatabase"]
mydb.create_collection("mydatabase")
print(myclient.list_database_names())

dblist = myclient.list_database_names()
if "mydatabase" in dblist:
  print("The database exists.")
