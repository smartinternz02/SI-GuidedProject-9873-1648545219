import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import requests

API_KEY = "z5w_7QoNuv-PziHyHPjrv_fKcKhYzVDd_vhj4IWS2dli"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

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
    return render_template('predict.html', temp=temp, humid=humid, pressure=pressure,speed=speed, deg=degree)
    
@app.route('/y_predict',methods=['POST'])
def y_predict():
    x_test = [[float(x) for x in request.form.values()]]
    payload_scoring = {"input_data": [{"fields": [["f0","f1","f2"]], "values":x_test }]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/689614b2-8ded-4e79-aaac-49675c769d5b/predictions?version=2022-05-31', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    # print(response_scoring.json())
    pred= response_scoring.json()
    output=pred['predictions'][0]['values'][0][0]
    print(output)
    # prediction = model.predict(x_test)
    # print(prediction)
    # output=prediction[0]
    return render_template('predict.html', prediction_text='The energy predicted is {:.2f} KWh'.format(output))


if __name__ == "__main__":
    app.run(debug=False)
