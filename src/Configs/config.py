broker_ip="108.59.81.89"
broker_port=1883
db_name="smart_home_data"
path_data_temperature="./../Data/Temperature.csv"
path_data_wiatr_sila="./../Data/WindS.csv"
path_data_wiatr_kierunek="./../Data/WindD.csv"
path_data_entrance="./../Data/Entrance.csv"
path_data_wilgotnosc="./../Data/Wilgotnosc.csv"
path_data_co2="./../Data/Co2.csv"
path_data_level="./../Data/Wypelnienie.csv"
path_data_gate="./../Data/Gate.csv"
path_data_rfid="./../Data/RFID.csv"
path_data_entrance2="./../Data/Entrance2.csv"
path_data_stairs="./../Data/Stairs.csv"
path_data_light="./../Data/Light.csv"
topic_grzalka="grzalka"
dic={"on":"1","off":"0"}
topic ={ "harmonogram_new":"harmonogram_new",
        "light_salon":"light_salon",
        "heating_switch":"heating_switch",
        "grzalka":"grzalka",
        "temperatura":"temperatura",
       "sila_wiatru":"sila_wiatru",
       "kierunek_wiatru":"kierunek_wiatru",
       "wejście":"wejście",
       "wilgotnosc":"wilgotnosc",
       "pir_stairs_1":"pir_stairs_1",
       "co2":"co2",
       "gateway_rswitch":"gateway_rswitch"}


topics={
    "humidity_out":"humidity_out",
    "humidity_in":"humidity_in",
    "temperature_out":"temperature_out",
    "temperature_in":"temperature_in",
    "co2_out":"co2_out",
    "co2_in":"co2_in",
    "gateway_rswitch":"gateway_rswitch",
    "gate_rswitch":"gate_rswitch",
    "door_rswitch":"door_rswitch",
    "light_out":"light_out",
    "pir_door":"pir_door",
    "pir_salon":"pir_salon",
    "pir_garage":"pir_garage",
    "RFID":"RFID",
    "wind_dir":"wind_dir",
    "wind_str":"wind_str",
    "heating_switch":"heating_switch",
    "level":"level"
}

collections={
    "humidity_out":"wilgotnosc_zew",
    "humidity_in":"wilgotnosc_wew",
    "temperature_out":"temperatura_zew",
    "temperature_in":"temperatura_wew",
    "co2_out":"co2_zew",
    "co2_in":"co2_wew",
    "gateway_rswitch":"kontaktron_bramka",
    "gate_rswitch":"kontaktron_brama",
    "door_rswitch":"kontaktron_drzwi",
    "light_out":"swiatlo_zew",
    "pir_door":"pir_drzwi",
    "pir_salon":"pir_salon",
    "pir_garage":"pir_garaz",
    "RFID":"RFID",
    "wind_dir":"wiatr_kierunek",
    "wind_str":"wiatr_sila",
    "level":"poziom"
    
}





path2_data_temperature="./../Data/Temperature.csv"
path2_data_wiatr_sila="./../Data/WindS.csv"
path2_data_wiatr_kierunek="./../Data/WindD.csv"
path2_data_wilgotnosc="./../Data/Wilgotnosc.csv"
path2_data_co2="./../Data/Co2.csv"
path2_data_level="./../Data/Wypelnienie.csv"
path2_data_rfid="./../Data/RFID.csv"
path2_data_light="./../Data/Light.csv"
path2_data_entrance="./../Data/Pir3.csv"
path2_data_stairs="./../Data/Stairs.csv"
path2_data_entrance2="./../Data/Pir2.csv"