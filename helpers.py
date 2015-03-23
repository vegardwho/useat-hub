from operator import sub


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

def larger_than(pixel_list,number):
    if (max(pixel_list) > number):
        return True
    else
        return False