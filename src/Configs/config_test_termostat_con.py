broker_ip="34.123.208.229"
broker_port=1883
db_name="test_database"
path_data_heating="temperature_in"
topic_grzalka="grzalka_test"
topic_grzalka2="grzalka_test2"
dic={"on":"1","off":"0"}
path_data_temperature="temperature_in"
path_data_wiatr_sila="./../../Data/WindS.csv"
path_data_wiatr_kierunek="./../../Data/WindD.csv"
path_data_entrance="./../../Data/Entrance.csv"
topic ={ "harmonogram_new":"harmonogram_new",
        "light_salon":"light_salon",
        "heating_switch":"heating_switch",
        "grzalka":"grzalka",
        "temperatura":"temperatura"}

collections={
 "temperature_in":"symulated_temp"
    
}