from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    fuel_Diesel=0
    fuel_Electric=0
    fuel_LPG=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        kms_driven=int(request.form['kms_driven'])
        kms_driven2=np.log(kms_driven)
        owner=int(request.form['owner'])
        fuel_Petrol=request.form['fuel_Petrol']
        if(fuel_Petrol=='Petrol'):
                fuel_Petrol=1
                fuel_Diesel=0
                fuel_Electric=0
                fuel_LPG=0
        elif(fuel_Petrol=='Diesel'):
                fuel_Petrol=0
                fuel_Diesel=1
                fuel_Electric=0
                fuel_LPG=0
        elif(fuel_Petrol=='Electric'):
                fuel_Petrol=0
                fuel_Diesel=0  
                fuel_Electric=1
                fuel_LPG=0
        elif(fuel_Petrol=='LPG'):
                fuel_Petrol=0
                fuel_Diesel=0  
                fuel_Electric=0
                fuel_LPG=1
        else:
            fuel_Petrol=0
            fuel_Diesel=0
            fuel_Electric=0
            fuel_LPG=0
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[kms_driven2,owner,Year,fuel_Diesel,fuel_Electric,fuel_LPG,fuel_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)