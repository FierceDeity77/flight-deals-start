import requests
from datetime import timedelta, datetime
from data_manager import DataManager  # imported the data_manager module
from flight_data import FlightData

amadeus_endpoint_flights = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class FlightSearch:
    def __init__(self, user_data: DataManager):  # : DataManager class to identify the data type
        self.user_flight_data = user_data  # gets the object data manager
        self.city_name = None
        self.departure = None
        self.currency = None
        self.grand_total = None
        self.discounted_flights = []
        self.deal_search()

    def deal_search(self):
        tom = datetime.now() + timedelta(5)  # adds the current date 1 day to get the date tomorrow
        # two_weeks = tom + timedelta(13)
        # six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

        date_tomorrow = datetime.strftime(tom, '%Y-%m-%d')

        auth_parameter = {
            "Authorization": f"Bearer {self.user_flight_data.access_token}"
        }

        user_flight_list = self.user_flight_data.get_data()  # list from data_manager module
        # user_flight_list = [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 40000, 'id': 2},
        #                     {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 40000, 'id': 4}]
        for data in user_flight_list:
            self.city_name = data["city"]
            city = data["iataCode"]
            user_price = data["lowestPrice"]

            flight_parameters = {
                "originLocationCode": "MNL",
                "destinationLocationCode": city,
                "departureDate": date_tomorrow,
                "adults": 1,
                "currencyCode": "PHP",
                "maxPrice": user_price,
                "travelClass": "ECONOMY"
            }

            response = requests.get(amadeus_endpoint_flights, params=flight_parameters, headers=auth_parameter)
            response.raise_for_status()

            raw_data = response.json()["data"]
            for raw in raw_data:  # loops through the api data then gets the cheapest price
                price = float(raw["price"]["grandTotal"])
                if price < user_price:
                    user_price = price
                    try:
                        self.departure = response.json()["data"][0]["itineraries"][0]["segments"][0]["departure"]
                        self.currency = response.json()["data"][0]["price"]["currency"]
                        self.grand_total = user_price

                        # object created from FlightData class
                        # inserted into a list with the flight data pulled from the api
                        sorted_flight_data = FlightData(self.city_name, self.departure, self.currency, self.grand_total)
                        self.discounted_flights.append(sorted_flight_data)

                    except:
                        pass

    def deal_found(self):
        if len(self.discounted_flights) > 0:
            return True
        else:
            return False








             # for flight in data["data"]:
             #        price = float(flight["price"]["grandTotal"])
             #        if price < lowest_price:
             #            lowest_price = price
             #            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
             #            destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
             #            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
             #            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
             #            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
             #            print(f"Lowest price to {destination} is £{lowest_price}")











