__author__ = 'Peder'

#
import requests



# params: int, int, string
# (room_id, number of seats available, hub password)
def report_availability(room_id, num_available, token):

    url = 'http://useat-api.iver.io/rooms/' + str(room_id) + '/report_availability/'

    payload = {'is_available': num_available, 'hub_token': token}

    response = requests.post(url, payload)

    print(response.text)



''' TESTING '''

report_availability(3, 1, 'hemmelig')