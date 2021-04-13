from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import sys 
sys.path.append("../")
from src.termostat_con import temp_get
from src.MQTT_pub import send_MSG
app = Flask(__name__)
import requests
import pymongo
from src.MQTT_sub2 import Mongo_log
mongo=Mongo_log("mongodb://127.0.0.1:27017/", "smart_home_schedule_test")
collection="schedule_test"
from src.schedule import getPeriods, changeDefalut, restoreDefalut, addHarmonogram, changePeriod


import logging

log_format = '%(asctime)s %(filename)s: %(message)s'
logging.basicConfig(filename='test.log', format=log_format,
                    level=logging.DEBUG)

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')







@app.route('/', methods=["GET","POST"])
def index():
    """
    metoda tworząca stronę główną webowej aplikacji 
    
    Args:
    temp -> zmienna przetrzymująca temperaturę dla pierwszego uruchomienia strony
    hum -> zmienna przetrzymująca wilgotność dla pierwszego uruchomienia strony
    move -> zmienna przetrzymująca stan czujnika ruchu dla pierwszego uruchomienia strony
    """
    try:
        temp_out = temp_get("temperatura_zew")
        temp_in= temp_get("temperatura_wew")
        hum_out= temp_get("wilgotnosc_zew")
        hum_in=temp_get("wilgotnosc_wew")
        move=temp_get("kontaktron_brama")
        move2=temp_get("kontaktron_bramka")
        move3=temp_get("kontaktron_drzwi")
        co2_out=temp_get("co2_zew")
        co2_in=temp_get("co2_wew")
        pir=temp_get("pir_drzwi")
        pir2=temp_get("pir_salon")
        pir3=temp_get("pir_garaz")
        rfid=temp_get("RFID")
        windd=temp_get("wiatr_kierunek")
        winds=temp_get("wiatr_sila")
        light=temp_get("swiatlo_zew")
        level=temp_get("poziom")
        """ if request.method == 'POST':

            if request.form['submit_button'] == 'Do Something':
                print("włącz termostat", file=sys.stderr) 
                pass
        # do something

            elif request.form['submit_button'] == 'Do Something Else':
                print("wyłącz termostat", file=sys.stderr)
                pass# do something else

            else:
                pass # unknown
        """
        
            
        if request.method == 'POST':
            #response = requests.get('')
            temp=request.form['temp']
            if float(temp)<40 and float(temp)>=0:
                print("włącz termostat",temp) 
            pass
        return render_template('index.html', temp_out=temp_out, temp_in=temp_in, hum_out=hum_out, hum_in=hum_in, move=move, move2=move2, move3=move3, co2_out=co2_out, co2_in=co2_in, pi=pir, pir2=pir2, pir3=pir3, rfid=rfid, windd=windd, winds=winds, level=level, light=light)
    except Exception as e:
        return(str(e))
    
    
@app.route('/termostat/')
def index2():
    return render_template('termostat/index2.html')


@app.route('/dash/')
def dash():
    send_MSG("test","elo")
    return redirect("http://108.59.81.89:5000/", code=302)

@app.route('/dash2/', methods=["GET","POST"])
def dash2():
    logging.debug("POST")
    try:
        if request.method == 'POST':
                #response = requests.get('')
                
                temp=request.form['temp']
                
                day=request.form['day']
                logging.info(temp)
                logging.info(day)
                logging.debug(temp)
                if float(temp)<40 and float(temp)>=0:
                    print("włącz termostat",temp)
                    changeDefalut(mongo, "schedule_test", str(day), temp)
                pass
    except Exception as e:
        return(str(e))
    ''' 
    print("#######")
    print("#######")
    if request.method=='POST':
            defalut=request.form['def']
            print(defalut)
            changeDefalut(mongo, "schedule_test", "Saturday", defalut)
    '''
    #redirect("http://108.59.81.89:5000/", code=302)

    return redirect("http://108.59.81.89:5000/", code=302)
@app.route('/dash3/', methods=["GET","POST"])
def dash3():
    logging.debug("POST")
    try:
        if request.method == 'POST':
                #response = requests.get('')
                
                temp=request.form['temp']
                
                day=request.form['day']
                start=request.form['start']
                end=request.form['end']
                logging.info(temp)
                logging.info(day)
                logging.debug(temp)
                if float(temp)<40 and float(temp)>=0:
                    print("włącz termostat",temp)
                    addHarmonogram(mongo, "schedule_test", temp, str(day), str(start), str(end) )
                pass
    except Exception as e:
        return(str(e))
    ''' 
    print("#######")
    print("#######")
    if request.method=='POST':
            defalut=request.form['def']
            print(defalut)
            changeDefalut(mongo, "schedule_test", "Saturday", defalut)
    '''
    return redirect("http://108.59.81.89:5000/", code=302)

    #return render_template('404.html')

@app.route('/interactive/')
def interactive():
	return render_template('interactive.html')

@app.route('/background_process/')
def background_process():
    """
    Metoda używana do ciągłej aktualizacji informacji na stronie 
    
    jsonify(nazwa zmiennej na stronie= wartość,....)
    
    """
    movement=temp_get("kontaktron_brama")
    movement2=temp_get("kontaktron_bramka")
    movement3=temp_get("kontaktron_drzwi")
    #if temp_get("kontaktron_brama",nb_rows=1)==1:
    return jsonify(
        temperature_out=temp_get("temperatura_zew"),
        temperature_in=temp_get("temperatura_wew"),
        humidity_out= temp_get("wilgotnosc_zew"),
        humidity_in= temp_get("wilgotnosc_wew"),
        light=temp_get("swiatlo_zew"),
        movement=movement,
        movement2=movement2,
        movement3=movement3,
        co2_out=temp_get("co2_zew",nb_rows=1),
        co2_in=temp_get("co2_wew",nb_rows=1),
        rfid=temp_get("RFID"),
        pir=temp_get("pir_drzwi"),
        pir2=temp_get("pir_salon"),
        pir3=temp_get("pir_garaz"),
        level=temp_get("poziom"),
        windd=temp_get("wiatr_kierunek"),
        winds=temp_get("wiatr_sila")
    )
    """elif temp_get("kontaktron_brama",nb_rows=1)==0:
        return jsonify(temperature=temp_get("temperatura_zew"),humidity= temp_get("wilgotnosc_zew"),
                       movement="brak aktywności",co2=temp_get("co2_zew",nb_rows=1))
    else:
        return jsonify(temperature=temp_get("temperatura_zew"),humidity= temp_get("wilgotnosc_zew"),
                       movement=temp_get("kontaktron_brama",nb_rows=1),Co2=temp_get("co2_zew",nb_rows=1))
   """
    
    #return jsonify(temperature=temp_get("../Data/Temperature.csv"),humidity= temp_get("../Data/Wilgotnosc.csv"))

@app.errorhandler(404)
def page_not_found(e):
        return render_template("404.html")
    
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0')





