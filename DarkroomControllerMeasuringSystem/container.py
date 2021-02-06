import time
import threading
from pi_controller import *
from API_client import *

class Container:
    def __init__(self, name, set_time = 5 , set_max_counter = 10):
        self.name = name
        self.set_time = set_time
        self.actual_time = 0.0
        self.in_proces = False
        self.max_counter = set_max_counter
        self.counter_warning = False
        self.counter_fault = False
        self.t = threading.Thread()
        self.program_run=True

    def start_proces(self):
        if ((not self.in_proces) and ( not self.counter_fault)):
            self.in_proces = True
            self.t = threading.Thread(target= self.start)
            self.t.start()
            print("PROCES: start "+ self.name)

    def block_process(self, command):
        if(command):
            self.counter_fault = True
        else:
            self.counter_fault = False


    def counter_reset(self):
        self.actual_counter = 0
        self.cycle_end()


    def start(self):
        start = time.time()
        while (self.program_run):
            time.sleep(0.1)
            dt = time.time() - start
            self.actual_time = round(dt, 1)
            if (dt > self.set_time):
                self.in_proces = False
                self.actual_time = 0.0
                print("PROCES: stop {}".format(self.name))
                break
    
