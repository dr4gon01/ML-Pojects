
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os


#initialize flask app
app = Flask(__name__)

# Get the absolute path of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the correct path to the model file
model_path = os.path.join(BASE_DIR, "../output/fraud_detection_model_rf.pkl")

# Load the model, but the downside of joblibs & pickles: Insecure, vulnerable to attacks
model = joblib.load(model_path)


# Print the expected feature names
print("Expected Features:", model.feature_names_in_)

@app.route("/predict", methods=['POST'])
def predict():
    try:
        #get json data from the request
        data = request.get_json()

        #convert the data into a df for easier processing
        df = pd.DataFrame([data])

        #check if head of the df
        print("Received Data:\n", df.head())

        #print the value of the first element
        print("First Row Values:\n", df.iloc[0])

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

        print(f"Error: {e}")  # Print error to console

        return jsonify({'error': str(e)})


#run it automatically
if __name__ == "__main__":
    #check the local http://127.0.0.1:5000/predict

    #for local testing use
    # run the code from test.txt
    app.run(debug=True)
