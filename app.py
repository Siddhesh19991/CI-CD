import numpy as np
from flask import Flask, request, jsonify
import pickle
import joblib


# The model was created using scikit-learn==1.4.1.post1 so we import this version here to avoid warnings.
app = Flask(__name__)


# model = pickle.load(open("model.pkl", "rb"))  # Loading the model
model = joblib.load('model.joblib')
encoding = pickle.load(open("encoding_dict.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))


@app.route("/predict", methods=["POST"])
def predict():
    json_dic = request.get_json()

    # Getting the input data from the user
    house_type = json_dic.get("House_Type")
    municipality = json_dic.get("Municipality")
    living_Area = json_dic.get("Living_Area")
    built_On = json_dic.get("Built_On")
    rooms = json_dic.get("Rooms")
    lift = (1 if json_dic.get("Lift") == "Yes" else 0)
    balcony = (1 if json_dic.get("Balcony") == "Yes" else 0)
    plot_Area = json_dic.get("Plot_Area")
    other_Area = json_dic.get("Other_Area")

    municipality_encode = encoding[municipality]

    # Altering the user data to fit for the input to the model
    value1 = []
    if (built_On == "1900-1950"):
        value1 = [1, 0, 0, 0, 0]
    elif (built_On == "1951-2000"):
        value1 = [0, 1, 0, 0, 0]
    elif (built_On == "2001-2010"):
        value1 = [0, 0, 1, 0, 0]
    elif (built_On == "2011-present"):
        value1 = [0, 0, 0, 1, 0]
    elif (built_On == "Before 1900s"):
        value1 = [0, 0, 0, 0, 1]

    value2 = []
    if (house_type == "Fritidshus"):
        value2 = [1, 0, 0, 0, 0, 0]
    elif (house_type == "Kedjehus"):
        value2 = [0, 1, 0, 0, 0, 0]
    elif (house_type == "Lägenhet"):
        value2 = [0, 0, 1, 0, 0, 0]
    elif (house_type == "Parhus"):
        value2 = [0, 0, 0, 1, 0, 0]
    elif (house_type == "Tomt"):
        value2 = [0, 0, 0, 0, 1, 0]
    elif (house_type == "Villa"):
        value2 = [0, 0, 0, 0, 0, 1]

    value3 = []

    if (house_type == "Lägenhet"):
        value3 = [municipality_encode, rooms,
                  lift, balcony, living_Area, 0, 0]
    else:
        value3 = [municipality_encode, 0, 0,
                  0, living_Area, plot_Area, other_Area]

    final_values = value3 + value1 + value2

    final_values = np.array(final_values)

    final_values_matrix = final_values.reshape(1, -1)

    final_values_matrix[:, (1, 4, 5, 6)] = scaler.transform(
        final_values_matrix[:, (1, 4, 5, 6)])

    prediction = model.predict(final_values_matrix)

    return jsonify({"value": np.array2string(round(prediction[0], 3))})


@app.route("/")
def root():
    app = Flask(__name__, static_url_path='/static')
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
