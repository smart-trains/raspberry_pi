import struct


def parse_temperature_matrix(data):
    message = {}

    for i, datum in enumerate(data):
        if i == 0:
            message['thermistor__c'] = datum * 0.0625
        else:
            message['cell_{index}__c'.format(index=(i - 1))] = datum * 0.25

    return message


def parse_temperature(data):
    return {'temperature__c': struct.unpack('f', data)[0]}


def parse_humidity(data):
    return {'humidity__c': struct.unpack('f', data)[0]}


def parse_vibration(data):
    acceleration_factor = 16384
    gyro_factor = 131

    keys = [
        'acceleration_x__c',
        'acceleration_y__c',
        'acceleration_z__c',
        'gyro_x__c',
        'gyro_y__c',
        'gyro_z__c',
    ]
    message = {}

    print(data)

    for i in range(0, len(data), 2):
        number = int.from_bytes(data[i:i + 2], byteorder='big', signed=True)

        if i < 6:
            number /= acceleration_factor
        else:
            number /= gyro_factor

        message[keys[int(i / 2)]] = number

    return message
