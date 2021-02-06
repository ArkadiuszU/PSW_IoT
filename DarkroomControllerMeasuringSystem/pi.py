
from time import sleep
import time
from container import Container
from pi_controller import *
import threading
from API_client import *
from lcd import lcddriver

values = ["developer", "stop bath" , "fixer"]
setTimes = [20,15,10]
cols = [" actual_time ", " actual_temp ", " proces ", " counter_val ", " counter_status "]
outputs = [40, 38, 36 , 32]
output_names = ["dioda_Y" , "dioda_G", "dioda_B", "dioda_R"]
inputs = [37, 35, 33, 31, 29]
input_names = ["btt_Y" , "btt_G", "btt_B", "btt_R", "btt_4"]
containers = []
temp_measurements = [0,0,0]
screen= 0
screen_change = False 
run = True 
process_guard = 0
global_counter = 5
max_counter_value= 30
global_name = "oczekiwanie"
global_time = 0.0
global_status= "ok"


def lcd_loop():
    global screen_change, screen, global_counter
    display = lcddriver.lcd()
    display.lcd_display_string("Darkroom control", 1)
    progress="#"
    titles= []
    for c in containers:
        titles.append(c.name)
        titles.append(c.name)
    for i in range(16):
        display.lcd_display_string(progress, 2)
        progress = progress + "#" 
        
    display.lcd_display_string("{}                   ".format(titles[0]), 1)
    while(run):
        if(screen_change):
            screen = screen + 1
            if(screen>(len(containers))*2-1):
                screen=0
            display.lcd_display_string("{}                   ".format(titles[screen]), 1)
            screen_change = False

        while(not screen_change and run):
            if(screen %2 == 0):
                display.lcd_display_string("t:{} c:{}           ".format(containers[screen/2].actual_time, global_counter), 2)
            else:
                display.lcd_display_string("temp:{} *C             ".format(temp_measurements[2-int(screen/2)]), 2)  
            if(not check_input("btt_4")):
                print("end status loop")
                break
        if(not check_input("btt_4")):
                print("end status loop")
                break
    display.lcd_display_string("                   ", 1)
    display.lcd_display_string("                   ", 2)
    print("end of lcd")

def refresh_app_loop_2():
    global global_name, global_time, global_status
    is_fault = False
    work = False
    for i in range(len(containers)):
        if (containers[i].in_proces):
            global_name = values[i]
            global_status = "work"
            global_time = containers[i].actual_time
            set_output(output_names[i])
            work = True
        else:
            clear_output(output_names[i])

        for m in temp_measurements:
            if(m > 27):
                is_fault = True
                for c in containers:
                    c.block_process(True)
            else:
                for c in containers:
                    c.block_process(False)

        if(global_counter>=max_counter_value):
            is_fault= True
            containers[0].block_process(True)
        else:
            containers[0].block_process(False)
        if (is_fault):
            set_output("dioda_R")
            global_status = "fault"
        else:
            clear_output("dioda_R")
            if(not work):
                global_status = "ok"
            
    if(not work):
        global_name = "oczekiwanie"
        global_time = 0
   
def API_client_loop():
    global temp_measurements, global_counter, global_name, global_time, global_status
    while(run):
        response = Post_IoT(global_name, temp_measurements, global_time, global_counter, global_status)
        if(response.status_code == 200): 
            print("API: success in send measurements")
        else:
            print("API: fault in send measurements")
        #global_counter = Get_counter()
        #Get_settings()
    print("end API")
#Get_settings()

def get_measurement_loop():
    global temp_measurements
    while(run):
        temp_measurements = get_measurment()
    print("temp end")


for x in range(len(values)):
    containers.append(Container(values[x],setTimes[x]))

pi_controler_setup(outputs, inputs, output_names, input_names)
clear_output("dioda_Y")
clear_output("dioda_G")
clear_output("dioda_B")
clear_output("dioda_R")


refresh_lcd_thread = threading.Thread(target=lcd_loop)
API_client_loop_thread = threading.Thread(target=API_client_loop)
measurment_thread = threading.Thread(target=get_measurement_loop)

refresh_lcd_thread.start()
API_client_loop_thread.start()
measurment_thread.start()

btt_pressed = False
try:
    while (True):
        for i in range(len(values)):
            if (not check_input(input_names[i])):
                if(i == process_guard):
                    if(process_guard == 0):
                        #PostCounter("counter_up")
                        global_counter+=1
                    containers[i].start_proces()
                    process_guard+=1
                if(process_guard>2):
                    process_guard=0

        if (not check_input("btt_R") and (not btt_pressed)):
            start = time.time()
            while(not check_input("btt_R")):
                dt = time.time() - start
                if (dt > 0.1):
                    btt_pressed=True
                    screen_change = True
                    break

        if(btt_pressed and (check_input("btt_R"))):
            btt_pressed=False

        refresh_app_loop_2()
        
except KeyboardInterrupt:
    print('')
    run=False
    temp_measurement_stop()
    for container in containers:
        container.program_run = False
        try:
            container.t.join()
            refresh_lcd_thread.join()
            measurment_thread.join()
        except:
            print("end of {}".format(container.name))
    clear_output("dioda_Y")
    clear_output("dioda_G")
    clear_output("dioda_B")
    clear_output("dioda_R")
    print('end of program')


                   
    









