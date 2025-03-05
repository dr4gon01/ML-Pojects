
from flask import Flask, request, jsonify
import joblib
import pandas as pd


#initialize flask app
app = Flask(__name__)


#load the trained fraud detection model
model = joblib.load("../output/fraud_detection_model_rf.pkl")

@app.route("/predict", methods=['POST'])
def predict():
    try:
        #get json data from the request
        data = request.get_json()

        #convert the data into a df for easier processing
        df = pd.DataFrame([data])

        #check if head of the df
        print(df.head())

        #print the value of the first element
        print(df[0])

        #make predictions for the first item
        prediction = model.predict(df)[0]

        prediction_int = int(prediction)

        if prediction_int == 0 :
            print("Non Fraud transaction")
        else:
            print("Fraud detected")

        #return result
        return jsonify({'fraud': prediction_int})

    except Exception as e:
        return jsonify({'error': str(e)})

#run it automatically
if __name__ == "__main__":
    app.run(debug=True)
