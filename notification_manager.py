from flight_search import FlightSearch
from twilio.rest import Client
from dotenv import load_dotenv
import smtplib
import os

load_dotenv()


class NotificationManager:
    def __init__(self, flight_s: FlightSearch):
        self.found_flight = flight_s
        self.dc_flight_list = self.found_flight.discounted_flights
        self.city = None
        self.departure = None
        self.currency = None
        self.total = None

    def send_sms(self):
        client = Client(os.getenv("E_twilio_account_sid"), os.getenv("E_twilio_auth_token"))
        message = client.messages.create(
            from_='+12406812118',
            body=f"Subject:Low price alert!\n\nCheapest price for {self.city} from: {self.departure} to "
                 f"{self.city} Only {self.currency}{self.total}",
            to=''
        )

        print(message.status)
        print("SMS sent!")

    def send_email(self):

        for deal in range(len(self.dc_flight_list)):
            self.city = self.dc_flight_list[deal].city
            self.departure = self.dc_flight_list[deal].departure
            self.currency = self.dc_flight_list[deal].currency
            self.total = self.dc_flight_list[deal].total

            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()  # Transport layer security - makes connection secure
                connection.login(user=os.getenv("E_my_email"), password=os.getenv("E_mail_pw"))
                connection.sendmail(from_addr=os.getenv("E_my_email"),
                                    to_addrs=os.getenv("E_my_email"),
                                    msg=f"Subject:Low price alert!\n\nCheapest price for {self.city} "
                                        f"from: {self.departure} to {self.city} Only {self.currency}{self.total}")

        print("Email Sent!")
