import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("E_USERNAME")
password = os.getenv(("E_PASSWORD"))
basic = HTTPBasicAuth(username, password)

SHEETY_APP_ID = os.getenv("E_SHEETY_APP_ID")
SHEETY_API_KEY = os.getenv("E_SHEETY_API_KEY")

AMADEUS_API = os.getenv("E_AMADEUS_API")
AMADEUS_API_SECRET = os.getenv("E_AMADEUS_API_SECRET")


class DataManager:
    def __init__(self):
        self.access_token = None
        self.row_id = 2
        self.sheety_headers = {
            "x-app-id": SHEETY_APP_ID,
            "x-app-key": SHEETY_API_KEY,
        }
        self.cities = None
        self.flight_data = None
        # self.get_city_name()
        # self.get_iata_codes()

    def get_token(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials",
            "client_id": AMADEUS_API,
            "client_secret": AMADEUS_API_SECRET,
        }

        response = requests.post(os.getenv("AMADEUS_ENDPOINT_TOKEN"), headers=header, data=data)
        self.access_token = response.json()["access_token"]

    def get_city_name(self):
        response = requests.get(os.getenv("SHEETY_GET_ENDPOINT"), auth=basic, headers=self.sheety_headers)
        self.cities = response.json()["prices"]

    def get_iata_codes(self):
        auth_parameter = {
            "Authorization": f"Bearer {self.access_token}"
        }

        for city in self.cities:
            city_param = {
                "keyword": city["city"].upper(),
            }

            response1 = requests.get(os.getenv("AMADEUS_CITY_ENDPOINT"), params=city_param, headers=auth_parameter)
            city_code = response1.json()["data"][0]["iataCode"]

            sheety_put_param = {
                "price": {
                    "iataCode": city_code  # sheety uses camelCase
                }
            }

            # populate the spreadsheet with iata codes from amadeus
            requests.put(url=f"{os.getenv("SHEETY_GET_ENDPOINT")}/{self.row_id}", auth=basic,headers=self.sheety_headers,
                         json=sheety_put_param)

            self.row_id += 1  # to change rows in sheety spreadsheet it starts with row 2

    def get_data(self):
        response = requests.get(os.getenv("SHEETY_GET_ENDPOINT"), auth=basic, headers=self.sheety_headers)
        self.flight_data = response.json()["prices"]

        # gets all data from spreadsheet then inserted into list using list comprehension
        flight_deals = [data for data in self.flight_data]

        return flight_deals









