from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager


d_manager = DataManager()
d_manager.get_token()
f_search = FlightSearch(d_manager)  # passes the d_manager object
notify = NotificationManager(f_search)

if f_search.deal_found:
    notify.send_sms()
    notify.send_email()






# TODO 1 - set when ideal departure flight date
# TODO 2 - get the cheapest flight * done
# TODO 3 - return date/ set number of days/weeks of vacation
# TODO 4 - multiple emails

