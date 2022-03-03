import requests
import datetime
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

APP_ID = os.getenv("APP_NUTR_ID")
APP_KEY = os.getenv('APP_NUTR_KEY')
API_AUTH = os.getenv('API_AUTH_HEADER')
sheet_endpoint = os.getenv('SHEET_ENDPOINT')

AGE = 27
WEIGHT = 76
HEIGHT = 173

today = datetime.datetime.today().date().strftime("%d/%m/%Y")
time = datetime.datetime.today().time().strftime("%H:%M:%S")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

sports = input("Specify exercises that you completed today: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY
}

header_sheety = {
    "authorization": API_AUTH
}

exercise_params = {
    "query": sports,
    "gender": "male",
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

response = requests.post(url=exercise_endpoint, json=exercise_params, headers=headers)
response.raise_for_status()
data = response.json()

sheet_data = {
    "workoutSheet":
    {
        "date": today,
        "time": time,
        "exercise": data["exercises"][0]["user_input"],
        "duration": f'{data["exercises"][0]["duration_min"]}',
        "calories": data["exercises"][0]["nf_calories"]
    }
}

response_writing = requests.post(url=sheet_endpoint, json=sheet_data, headers=header_sheety)
response_writing.raise_for_status()

