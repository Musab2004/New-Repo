# Project Title

This app is a simple predictor of House price based on house median income , total rooms and total bedrooms

## Project Setup

```python

git clone https://github.com/Musab2004/House_Predict_App
cd House_Predict_App
pip install -r requirements.txt
```

## Run House Prediction APP

```python
 python3 app.py
```

#### http://127.0.0.1:5000/predict

Payload
```python 
{
    "median_income": your value here,
    "total_rooms": your value here,
    "total_bedrooms": Your value here 
}
```
Response

```python
{
    "predicted_house_price: Predicted value
}
```
