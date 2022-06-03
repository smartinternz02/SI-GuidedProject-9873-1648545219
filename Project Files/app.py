import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import requests

app = Flask(__name__)
model = joblib.load('Wind_RFR')

@app.route('/')
def home():
    return render_template('intro.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/windapi',methods=['POST'])
def windapi():
    city=request.form.get('city')
    apikey="cc61a6050a8315e1fcc1e845ff687c50"
    url="http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+apikey
    resp = requests.get(url)
    resp=resp.json()
    te = resp["main"]["temp"]-273
    tem = "{:.2f}".format(te)
    temp = str(tem)+" °C"
    humid = str(resp["main"]["humidity"])+" %"
    pressure = str(resp["main"]["pressure"])+" mmHG"
    speed = str(resp["wind"]["speed"])+" m/s"
    degree = str(resp["wind"]["deg"])+" °"
    return render_template('predict.html', temp=temp, humid=humid, pressure=pressure,speed=speed, deg = degree)
    
@app.route('/y_predict',methods=['POST'])
def y_predict():
    x_test = [[float(x) for x in request.form.values()]]
    
    prediction = model.predict(x_test)
    print(prediction)
    output=prediction[0]
    return render_template('predict.html', prediction_text='The energy predicted is {:.2f} KWh'.format(output))
 

if __name__ == "__main__":
    app.run(debug=True)
