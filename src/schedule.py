"""
CONFIG Z KLUCZAMI WARTOSCI HARMONOGRAMU!!!!!


metoda/klasa pobierająca harmonogramy (głównie informacje)

metoda tworząca nowe harmonogramy ( temperatura do, przedział czasowy, dzień tygodnia, temperatura domyślna, czas trwania, priorytet  ) half-done
metoda do pobierania przedziałów czasowych i temperatury DONE
metoda do update przedzialu czasowego (pobranie przedziału, wybranie który zmienić/usunąć, dzień , zapisać cały słownik ze zmianami) Done
metoda do zmiany temperatury domyślnej danego dnia/dni DONE
metoda powrotu do ustawień fabrycznych/czyszczenia harmonogramu DONE
metoda dodająca nowy przedział DONE

"""
from MQTT_sub2 import Mongo_log
import pymongo
from datetime import datetime
mongo=Mongo_log("mongodb://127.0.0.1:27017/", "smart_home_schedule_test")

#                                     v Config,
def initHarmonogram(mongo, collection,  temp=21, days=["Saturday","Sunday","Monday","Tuesday"],  trigger="defalut"):
    """
    Metoda tworząca harmonogramy od zera - może być wykorzystana do przywracania ustawień domyślnych
        
        Args:
            mongo      - połaczenie z bazą danych
            collection - kolekcja (powinna być schedule)
            temp       - temperatura domyślna w podstawowym harmonogramie
            days       - dzień w którym obowiązuje harmonogram
            trigger    - ustalenie priorytetu
            
            
            Przykładowy harmonogram

            
            "day":"Saturday",
            "trigger":"defalut",
            "defalut_temp":24.0,
            "periods":[
            {
                "start":"17:00",
                "end":"18:00",
                "temp":30
            },
            {
                "start":"19:00",
                "end":"20:00",
                "temp":32
            }
            ]

        

    """
    
    
    myCol=mongo.my_db[collection]
    
    for day in days:
        schedule={
        "day":day,
        "trigger":trigger,
        "defalut_temp":temp,
        "periods":[]
        }
        x=myCol.insert_one(schedule)
#initHarmonogram(mongo,"schedule_test")

def addHarmonogram(mongo, collection, temp, day, start, end):
    """
    Metoda dodająca harmonogram w danym dniu
        
        Args:
            mongo      - połaczenie z bazą danych
            collection - kolekcja (powinna być schedule)
            temp       - temperatura w przedziale czasowym w harmonogramie
            day        - dzień w którym obowiązywać będzie harmonogram
            start      - początek działania harmonu
            end        - koniec działania harmonogramu
    
    """
    
    myCol=mongo.my_db[collection]
    myquery = { "$and":[{"day":{"$eq":day}},{"periods":{'$exists': 1}}] }
    periods=getPeriods(mongo,collection,day)
    newharmonogram={"start":start,
            "end":end,
            "temp":temp}
    periods.append(newharmonogram)
    newvalues = { "$set": { "periods":periods}}
    
    myCol.update_one(myquery, newvalues)


def getPeriods(mongo,collection,day,defalut_temp=False):
    """
    Metoda pobierająca przedziały czasowe harmonogramów w danym dniu
        
        Args:
            mongo      - połaczenie z bazą danych
            collection - kolekcja (powinna być schedule)
            day        - dzień w którym obowiązuje harmonogram
    
    """
    myCol=mongo.my_db[collection]
    myquery = { "$and":[{"day":{"$eq":day}},{"periods":{'$exists': 1}}] }
    schedule=list(myCol.find(myquery))
    periods=schedule[0]["periods"]
    print(list(periods))
    if defalut_temp:
        temp=schedule[0]["defalut_temp"]
        return list(periods),temp
    else:
        return list(periods)
#addHarmonogram(mongo, "schedule_test", 22.0, "Saturday", "10:30", "10:35")
 
def changeDefalut(mongo, collection, day, temp):
    """
    Metoda zmieniająca temperaturę domyślną w danym dniu
        
        Args:
            mongo      - połaczenie z bazą danych
            collection - kolekcja (powinna być schedule)
            temp       - temperatura domyślna w podstawowym harmonogramie
            day        - dzień w którym obowiązuje harmonogram
            temp       - temperatura która będzie ustawiona domyślnie w danym dniu
    
    """
    myCol=mongo.my_db[collection]
    myquery = { "$and":[{"day":{"$eq":day}},{"periods":{'$exists': 1}}] }
    newvalues = { "$set": { "defalut_temp":temp}}
    myCol.update_one(myquery, newvalues)
    
#changeDefalut(mongo, "schedule_test", "Saturday", 22.0)

def changePeriod(mongo, collection, day, start_old, end_old, start_new, end_new, temp=None):
    """
    Metoda godziny trwania harmonogramu w danym dniu
        
        Args:
            mongo      - połaczenie z bazą danych
            collection - kolekcja (powinna być schedule)
            temp       - temperatura podczas trwania w przedziale czasowym w harmonogramie
            day       - dzień w którym obowiązuje harmonogram
            start_old  - początek działania harmonu którego chcemy zmienić
            end_old    - koniec działania harmonogramu którego chcemy zmienić
            start_new  - początek działania harmonu na jaki chcemy zmienić
            end_new    - koniec działania harmonogramu na jaki chcemy zmienić
    
    """
    myCol=mongo.my_db[collection]
    myquery = { "$and":[{"day":{"$eq":day}},{"periods":{'$exists': 1}}] }
    periods=getPeriods(mongo,collection,day)
    newPeriods=[]
    
    for period in periods:
        if period["start"]==start_old and period["end"]==end_old:
            if temp!=None:
                newtemp=temp
            else:
                newtemp=period["temp"]
            newPeriod={
                "start":start_new,
                "end":end_new,
                "temp":newtemp
            }
            newPeriods.append(newPeriod)
        else:
            newPeriods.append(period)
        
    myquery = { "$and":[{"day":{"$eq":day}},{"periods":{'$exists': 1}}] }    
    newvalues = { "$set": { "periods":newPeriods}}
    
    myCol.update_one(myquery, newvalues)
#changePeriod(mongo, "schedule_test", "Saturday", "11:30","11:35","11:30","11:35",temp=21.0)

def dropSchedule(mongo, collection):
    """
    Metoda usuwająca harmonogramy
        
        Args:
            mongo      - połaczenie z bazą danych
            collection - kolekcja (powinna być schedule)
           
    
    """
    
    myCol=mongo.my_db[collection]
    myCol.drop()
    
def restoreDefalut(mongo, collection="schedule_test", days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
    """
    Metoda usuwająca harmonogramy i przywracająca harmonogramy domyślne
        
        Args:
            mongo      - połaczenie z bazą danych
            collection - kolekcja (powinna być schedule)
            day        - dzień w którym obowiązuje harmonogram
    
    """
    myCol=mongo.my_db[collection]
    dropSchedule(mongo, collection)
    initHarmonogram(mongo,collection,days)

def schedule_temp(mongo, collection, day=None, hour=None, minute=None):
    if day==None and hour==None and minute==None:
        now = datetime.now() # current date and time

        Day = now.strftime("%d")
        minute_current = now.strftime("%M")
        hour_current=now.strftime("%H")
        minute=minute_current
        hour=hour_current
        day=day_current
    
    string_now=hour+":"+minute
    
    element = datetime.datetime.strptime(string_now,"%H:%M")
    timestamp = datetime.datetime.timestamp(element)  
    myCol=mongo.my_db[collection]
    myquery = { "$and":[{"day":{"$eq":day}},{"periods":{'$exists': 1}}] }
    periods, final_temp=getPeriods(mongo,collection,day,defalut_temp=True)
    
    for period in periods:
        
        string_start=period["start"]
        element2 = datetime.datetime.strptime(string_start,"%H:%M")
        timestamp_start = datetime.datetime.timestamp(element2)
        
        string_end=period["end"]
        element3 = datetime.datetime.strptime(string_end,"%H:%M")
        timestamp_end = datetime.datetime.timestamp(element3)
        
        if timestamp_start<timestamp and timestamp_end>timestamp:
            final_temp=period["temp"]
            return final_temp
    return final_temp
        
    