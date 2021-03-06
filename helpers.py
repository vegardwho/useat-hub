from operator import sub
import requests
from datetime import timedelta

def convert_two_bytes_to_celsius(first_byte, second_byte):
    return (first_byte + 256 * second_byte) * 0.1


def pretty_print_pixels(temperature_data):
    result_str = ""
    for i in range(len(temperature_data)):
        result_str += "%0.1f" % temperature_data[i]
        result_str += "\n" if i % 4 == 3 else " "
    print result_str


def convert_to_image(temperature_data):
    img = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    min_temp = min(min(temperature_data), 28)
    for i in range(len(temperature_data)):
        x = i % 4
        y = i / 4
        temperature = temperature_data[i]
        temperature -= min_temp
        temperature /= 10
        temperature *= 255
        temperature = int(min(temperature, 255))
        img[y][x] = temperature
    return img


def median(x):
    if len(x) % 2 != 0:
        return sorted(x)[len(x) / 2]
    else:
        midavg = (sorted(x)[len(x) / 2] + sorted(x)[len(x) / 2 - 1]) / 2.0
        return midavg


def get_six_lowest_values(x):
    return sorted(x)[:6]


def absolute_diff(former_list, current_list):
    diff = map(sub, current_list, former_list)
    return map(abs, diff)


def is_max_larger_than(pixel_list, number):
    return max(pixel_list) > number


def is_stationary_human(celsius_data):
    max_temp = max(celsius_data)
    lowest_values = get_six_lowest_values(celsius_data)
    median_of_lowest_values = median(lowest_values)
    diff_median_max = max_temp - median_of_lowest_values

    result = diff_median_max >= 2.2
    #print 'is stationary human detected:', result
    return result


def is_moving_human(celsius_data, previous_celsius_data):
    result = False

    if len(previous_celsius_data) == 16:
        abs_diff_between_frames = absolute_diff(previous_celsius_data, celsius_data)
        max_abs_diff_between_frames = max(abs_diff_between_frames)
        if max_abs_diff_between_frames >= 0.4:
            result = True

    #print 'is moving human detected:', result
    return result


def report_availability(room_id, is_available, hub_token):
    url = 'http://useat-api.iver.io/rooms/' + str(room_id) + '/report_availability/'
    payload = {'is_available': 1 if is_available else 0, 'hub_token': hub_token}
    response = requests.post(url, payload)
    #print response


def get_frequency():
    return timedelta(seconds=60)
