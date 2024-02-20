from flask import Flask, render_template
from flask import jsonify
import pickle
from flask import request
import joblib
from flask_cors import CORS
from werkzeug.routing import Rule
import json
from flask import redirect

app = Flask(__name__)
CORS(app)
filename = "linear_model_1.pkl"
HOUSE_PRICE_PREDICTING__MODEL = joblib.load(filename)
app.url_map.add(Rule("/", endpoint="homepage"))
app.url_map.add(Rule("/predict", endpoint="index"))


@app.before_request
def before_request_func():
    print("request.endpoint : ", request.endpoint)
    if request.endpoint not in ["homepage", "index"]:
        return jsonify({"error": "Only / or /predict endpoints are allowed"})


def predict(house_median_income, total_rooms, total_bedrooms):
    predicted_house_price = HOUSE_PRICE_PREDICTING__MODEL.predict(
        [[float(house_median_income), int(total_rooms), int(total_bedrooms)]]
    )
    return predicted_house_price[0][0]


def check_format(data):
    if len(data) != 3:
        return jsonify({"error": "Argument error"})
    if (
        "median_income" not in data
        or "total_bedrooms" not in data
        or "total_rooms" not in data
    ):
        return jsonify({"error": "Bad Arguments error"})


def check_input(house_median_income, total_bedrooms, total_rooms):
    if house_median_income <= 0 or total_bedrooms <= 0 or total_rooms <= 0:
        return jsonify({"error": "Bad input error"})
    if total_bedrooms >= total_rooms:
        return jsonify(
            {
                "error": "Bad input error. total bedrooms should be smaller or equal to total rooms"
            }
        )

@app.endpoint("homepage")
def homepage():
    return render_template("homepage.html")


@app.endpoint("index")
def predict_house_price():
    print("request to get json is here : ", request.data)
    try:
        print(request.data)
        json_object = json.loads(request.data)
        print("Is valid json? true")
    except ValueError as e:
        print("Is valid json? false")
        return jsonify({"error": "Only json format is allowed"})

    if request.method == "POST":
        if request.get_json():
            data = request.get_json()
            error = check_format(data)
            if error:
                return error
            try:
                house_median_income = float(data.get("median_income"))
                print("house_median_income : ", house_median_income)
                total_bedrooms = int(data.get("total_bedrooms"))
                print("total_bedrooms : ", total_bedrooms)
                total_rooms = int(data.get("total_rooms"))
                print("total_rooms : ", total_rooms)
            except:
                return jsonify({"error": "Bad Arguments error"})
            error = check_input(
                house_median_income,
                total_rooms=total_rooms,
                total_bedrooms=total_bedrooms,
            )
            if error:
                return error
            predicted_house_price = predict(
                house_median_income, total_rooms, total_bedrooms
            )
            response = {
                "house_median_income": float(house_median_income),
                "total_rooms": int(total_rooms),
                "total_bedrooms": int(total_bedrooms),
                "predicted_house_price": predicted_house_price,
            }
        else:
            response = {
                "error": "You need to give house median income to predict the price. Example: House=7 in json format"
            }

        return jsonify(response)
    else:
        return jsonify({"error": "Only GET methode is allowed"})


if __name__ == "__main__":
    app.run(debug=True)
