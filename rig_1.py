 # RIG_1.py
#
# First version of the Python script designed for running the mouse
# rig v2.0, for the Tactile Synchrony Project. <mduhain>
#
# Helpful Links
# 1. Raspberry-GPIO-Python Documentation
#   https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
#
# -----------------------------------------------------------------
#
#
# 12/11/2020 <mduhain> Changing function of script for training purposes.
#  - every trial gives a reward regardless of if handle was grabbed.
#
# TODO
# From MGR (12/11/2020)
#  - for training experiment, lower reward size, and up the total number of trials 300-500.
#  - add a timed delay between the trial start and reward given.
#  - make this timed delay random (1000 - 3000 msec)

# INPUTS
tot_trials = 50 # Total Number of Trials
trial_timeout = 10 #Listen for _ seconds then proceed to next trial
reward_size = 32  #Reward size
bar_release_timeout = 5 #Time to wait for mouse to let go
#-------------------------------------------------------------
#
#
import csv
import time
import RPi.GPIO as GPIO
from datetime import datetime
from itertools import zip_longest


#create unique filename with date and time
today = datetime.now()
t_now = str(today.strftime("%Y_%m_%d_%H_%M_%S"))
new_csv = ".csv"
data = "data_"
file_name = "".join((data,t_now,new_csv))

#SET UP GPIO PINS
GPIO.setmode(GPIO.BOARD)

handle_pin = 12 # Mouse Handle
GPIO.setup(handle_pin, GPIO.IN)

lick_pin = 18 # Lick Spout
GPIO.setup(lick_pin, GPIO.IN)

manual_pin = 40 # Manual reward
GPIO.setup(manual_pin, GPIO.IN)

led_pin = 16 # LED Cue
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, 0)

control_pins = [7,11,13,15] # 4 pins for driving stepper motor
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)


#LED FLASH FUNCT
def led_flash(t):
    #led flash with t(seconds) input
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(t)
    GPIO.output(led_pin, GPIO.LOW)


# DEFINE STEP SEQUENCE
halfstep_seq = [
    [1,0,0,1],
    [0,0,0,1],
    [0,0,1,1],
    [0,0,1,0],
    [0,1,1,0],
    [0,1,0,0],
    [1,1,0,0],
    [1,0,0,0]  ]


#WATER REWARD FUNCTION
def deliver_reward():
    for i in range(reward_size):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            time.sleep(0.001)


#-----------------------------------------------------------------

#START INITIAL EVENT
events = ["Exp_Start"] #define array to hold experiment events
now = time.time() #mark time
times = [now] #define array to hold experiment event times
print('Experiment ' + t_now)

# START TRIAL LOOP
for ii in range(tot_trials):
    #Mark trial begin
    events.append("Trial_Start")
    times.append(time.time())
    print('Trial ' + str(ii) + ' Start!')

    flag = 0
    flag1 = 0
    flag2 = 0

    # Check if animal is still holding bar from last trial...
    while  GPIO.input(handle_pin) == GPIO.HIGH:
        time.sleep(0.1)
        led_flash(0.1)

    # Flash LED
    led_flash(0.2)
    time.sleep(0.2)
    led_flash(0.2)

    def handle_callback(handle_pin):
        # handle was grabbed. do stuff.
        deliver_reward()
        events.append("Reward")
        times.append(time.time())
        # wait for bar release
        GPIO.remove_event_detect(handle_pin)
        t_stamp = time.time()
        while time.time() - t_stamp < bar_release_timeout:
            if GPIO.input(handle_pin) == GPIO.HIGH:
                time.sleep(0.1)
            else:
                print("Bar Released!")
                events.append("Bar_Release")
                times.append(time.time())
                global flag
                flag = 1
                break

        if time.time() - t_stamp > bar_release_timeout:
            print("Timeout Bar Release...")
            events.append("Timeout_Bar_Release")
            times.append(time.time())


        #bar_release = GPIO.wait_for_edge(handle_pin, GPIO.FALLING, timeout=5000)
        #if bar_release is None:
        #    print("Timeout Bar Release...")
        #    events.append("Timeout_Bar_Release")
        #    times.append(time.time())
        #else:
        #    print("Bar Released!")
        #    events.append("Bar_Release")
        #    times.append(time.time())
        #    flag = 1


    #MAIN
    start = time.time()
    # Listen to input pins
    GPIO.add_event_detect(handle_pin, GPIO.RISING, callback=handle_callback, bouncetime=200)
    #GPIO.add_event_detect(lick_pin, GPIO.RISING, bouncetime=200)

    #UNCOMMENT THIS WHEN NOT IN TRAINING MODE, SEE DOC
    #print('Waiting for bar grab...')

    #TRAINING MODE
    deliver_reward()
    events.append("Reward")
    times.append(time.time())
    print('Training reward given...')


    while True:
        #UNCOMMENT THIS WHEN NOT IN TRAINING MODE, SEE DOC
        #if GPIO.event_detected(handle_pin):
        #    events.append("Touch")
        #    times.append(time.time())
        #    print("Bar Touched!")

        if GPIO.input(lick_pin) == GPIO.HIGH:
        #if GPIO.event_detected(lick_pin):
            if flag1 == 0:
                flag1 = 1
                last_lick = time.time()
                events.append("Lick")
                times.append(time.time())
                print("Spout Licked!")
            else:
                if time.time() - last_lick > 0.1:
                    flag1 = 0

        if time.time() - start > trial_timeout:
            events.append("Trial_Timeout")
            times.append(time.time())
            print("Trial Time Limit Reached!")
            break

        if GPIO.input(manual_pin) == GPIO.HIGH:
            if flag2 == 0:
                flag2 = 1
                deliver_reward()
                events.append("User_Reward")
                times.append(time.time())
                print("Reward Given!")

        if flag == 1:
            print("Successful Trial, resetting")
            events.append("Trial_Success")
            times.append(time.time())
            break

        time.sleep(0.001)

    print('Trial ' + str(ii) + ' End!')

    GPIO.remove_event_detect(handle_pin)
    GPIO.remove_event_detect(lick_pin)


#END OF TRIAL LOOP

print("maximum trials reached!")

GPIO.cleanup()

#open/create file with file_name
file_handle = open(file_name,'w+', newline ='')

#fill file with data
d = [events, times]
export_data = zip_longest(*d, fillvalue = '')
with file_handle:
    write = csv.writer(file_handle)
    write.writerow(("EVENTS", "TIMES"))
    write.writerows(export_data)

file_handle.close()

