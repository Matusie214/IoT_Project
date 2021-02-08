from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import sys 
sys.path.append("../")
from src.termostat_con import temp_get

app = Flask(__name__)



@app.route('/')
def index():
"""
metoda tworząca stronę główną webowej aplikacji 
    
    Args:
    temp -> zmienna przetrzymująca temperaturę dla pierwszego uruchomienia strony
    hum -> zmienna przetrzymująca wilgotność dla pierwszego uruchomienia strony
    move -> zmienna przetrzymująca stan czujnika ruchu dla pierwszego uruchomienia strony
"""
    temp = temp_get("../Data/Temperature.csv")
    hum= temp_get("../Data/Wilgotnosc.csv")
    move=temp_get("../Data/Entrance.csv")
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
    return render_template('index.html', temp = temp, hum=hum,move=move )

@app.route('/termostat')
def index2():
    return render_template('termostat/index2.html')

@app.route('/interactive/')
def interactive():
	return render_template('interactive.html')

@app.route('/background_process')
def background_process():
    """
    Metoda używana do ciągłej aktualizacji informacji na stronie 
    
    jsonify(nazwa zmiennej na stronie= wartość,....)
    """
    if temp_get("../Data/Entrance.csv",nb_rows=1)==1:
        return jsonify(temperature=temp_get("../Data/Temperature.csv"),humidity= temp_get("../Data/Wilgotnosc.csv"),
                       movement="wykryto aktywność")
    elif temp_get("../Data/Entrance.csv",nb_rows=1)==0:
        return jsonify(temperature=temp_get("../Data/Temperature.csv"),humidity= temp_get("../Data/Wilgotnosc.csv"),
                       movement="brak aktywności")
    else:
        return jsonify(temperature=temp_get("../Data/Temperature.csv"),humidity= temp_get("../Data/Wilgotnosc.csv"),
                       movement=temp_get("../Data/Entrance.csv",nb_rows=1))
   
    
    #return jsonify(temperature=temp_get("../Data/Temperature.csv"),humidity= temp_get("../Data/Wilgotnosc.csv"))


if __name__ == '__main__':
    app.run(host = '0.0.0.0')





