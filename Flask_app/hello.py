from flask import Flask, render_template, request, redirect, url_for
import sys 
sys.path.append("/home/mcezary97/")
from termostat_con import temp_get

app = Flask(__name__)



@app.route('/')
def index():

    temp = temp_get("/home/g2pawel_urbanski/Mess.csv")
    
    if request.method == 'POST':

        if request.form['submit_button'] == 'Do Something':
            print("włącz termostat", file=sys.stderr) 
            pass
    # do something
    
        elif request.form['submit_button'] == 'Do Something Else':
            print("wyłącz termostat", file=sys.stderr)
            pass# do something else
    
        else:
            pass # unknown

    return render_template('index.html', temp = temp)

@app.route('/termostat')
def index2():
    return render_template('termostat/index2.html')
   
if __name__ == '__main__':
    app.run(host = '0.0.0.0')





