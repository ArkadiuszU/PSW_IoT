import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
import time
import threading


input_names = []
output_names = []
inputs = []
outputs = []
temp_run = True
temp_measurements = [0,0,0]

def pi_controler_setup(outputs_, inputs_, output_names_, input_names_):
    global output_names, input_names, inputs, outputs
    output_names = output_names_
    input_names = input_names_
    inputs = inputs_
    outputs = outputs_
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for pin in outputs:
        GPIO.setup(pin, GPIO.OUT)  # ten pin bedzie wyjsciem
    for pin in inputs:
        GPIO.setup(pin, GPIO.IN)  # ten pin bedzie wejsciem

    temp_sensor_thread = threading.Thread(target=temp_sensor_loop)
    temp_sensor_thread.start()

def set_output(name):
    GPIO.output(outputs[output_names.index(name)] ,GPIO.LOW)

def clear_output(name):
    GPIO.output(outputs[output_names.index(name)] ,GPIO.HIGH)

def check_input(name):
    return GPIO.input(inputs[input_names.index(name)])

def get_measurment():
    return temp_measurements

def temp_measurement_stop():
    global temp_run
    temp_run = False


def temp_sensor_loop():
    while (temp_run):
        index = 0
        for sensor in W1ThermSensor.get_available_sensors():
            #print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
            temp_measurements[index] = round(sensor.get_temperature(),1)
            index +=1

