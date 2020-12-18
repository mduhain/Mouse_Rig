# basic_handle.py
#
# First version of the Python script designed for running the mouse
# rig v2.0, for the Tactile Synchrony Project. <mduhain>
#
# This Version Requires The Mouse TO Grab The Bar, and Recieve reward.
#
# Helpful Links
# 1. Raspberry-GPIO-Python Documentation
#   https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
#
# ----------------------------------------------------------------------------------------------------------
# <NOTES>
# 2020-12-18 <mduhain>
#   "This is a copy from rig_1.py which currently lives on the Desktop. This function is wrapped
#   in a local function with the same name "basic_handle.py / basic_handle()". This way we can 
#   import the module (from basic_handle import basic_handle) into the rig_gui.
#
#
#-----------------------------------------------------------------------------------------------------------
# <TODO> ( - marks an item, + marks a completed item)
#
#  + Touch bar, Flash light, give reward.
#  + Remove their hand manually with a tooth pick if they dont get it.
#  - then add to the gui, a raster plot for visualizing when the animal grabbed the bar.
#  - And a user input to change the reward size, and trial delay duration.
#
#
#
# INPUTS

def basic_handle():
    tot_trials = 10            # Total Number of Trials
    trial_timeout = 7           # Listen for _ seconds then proceed to next trial
    reward_size = 56            # Reward size
    bar_release_timeout = 5     # Time to wait for mouse to let go
    uninitiated_trial_limit = 20 # uninitiated trials before experiment termination
    #
    #
    #
    import csv
    import time
    import math
    import random
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
    GPIO.cleanup()
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
        GPIO.output(led_pin, GPIO.HIGH) # turn LED on
        time.sleep(t)
        GPIO.output(led_pin, GPIO.LOW) # LED off


    # DEFINE STEP SEQUENCE
    # this is the pattern of on/off signals to send the stepper motor magnets
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


    # CREATE INITIAL EVENT
    events = ["Exp_Start"] #define array to hold experiment events
    now = time.time() #mark time
    times = [now] #define array to hold experiment event times
    print('Experiment ' + t_now)

    last_lick_trial = 0

    #--------------------------------------------------------------------------------------------------------
    # START TRIAL LOOP
    for ii in range(tot_trials):
            #Mark trial begin
            events.append("Trial_Start")
            times.append(time.time())
            print('Trial ' + str(ii) + ' Start!')

            #per trial variables / flags
            flag = 0
            flag1 = 0 # for tracking speed of licks
            flag2 = 0 # for delivering manual licks with external button

            # Check if animal is still holding bar from last trial...
            while  GPIO.input(handle_pin) == GPIO.HIGH:
                time.sleep(0.5)
                print('Animal needs to let go...')

            # Flash LED
            #led_flash(0.2)
            #time.sleep(0.2)
            #led_flash(0.2)

            def handle_callback(handle_pin):
                # handle was grabbed. do stuff.
                events.append("Touch")
                times.append(time.time())
                print("Bar Touched!")
                led_flash(0.5)
                deliver_reward()
                events.append("Reward")
                times.append(time.time())
                print("Reward Given!")
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

            #MAIN
            start = time.time()
            # Listen to input pins
            GPIO.add_event_detect(handle_pin, GPIO.RISING, callback=handle_callback, bouncetime=200)
            #GPIO.add_event_detect(lick_pin, GPIO.RISING, bouncetime=200)

            #UNCOMMENT THIS WHEN NOT IN TRAINING MODE, SEE DOC
            #print('Waiting for bar grab...')

            #TRAINING MODE CODE
            #delay for random time of 1-3 seconds
            #T_delay = math.floor((2000*random.random())+1000)/1000
            #time.sleep(T_delay)
            #print('Trial ' + str(ii) + ', delay = ' + str(T_delay) + ' seconds...')

            #deliver_reward()
            #events.append("Reward")
            #times.append(time.time())
            #print('Training reward given...')

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # MAIN LOOP FOR SENSING PINS AND RESPONDING
            while True:
            #Uncomment this block of code (4 lines) when not in training mode
                if GPIO.event_detected(handle_pin):
                    #call back
                    useless_var = 1

                if GPIO.input(lick_pin) == GPIO.HIGH: #if GPIO.event_detected(lick_pin):
                    if flag1 == 0:
                        flag1 = 1
                        last_lick = time.time()
                        events.append("Lick")
                        times.append(time.time())
                        print("Spout Licked!")
                        last_lick_trial = ii
                    else: #this flag makes sure licks dont occur more than every 80ms (10 HZ max lick speed)
                        # especially if the sensor is stuck on, TODO, fix this logic <mduhain, 2020-12-15>
                        if time.time() - last_lick > 0.08:
                            flag1 = 0 #reset lick flag

                if time.time() - start > trial_timeout:
                    events.append("Trial_Timeout")
                    times.append(time.time())
                    print("Trial Time Limit Reached!")
                    break

                if flag == 1:
                    print("Successful Trial, resetting")
                    events.append("Trial_Success")
                    times.append(time.time())
                    break

                time.sleep(0.001)

            print('Trial ' + str(ii) + ' End!')
            print('.....')

            GPIO.remove_event_detect(handle_pin)
            GPIO.remove_event_detect(lick_pin)

            #check if the animal has stopped licking
            if (ii - last_lick_trial) >= uninitiated_trial_limit:
                events.append("Animal_on_strike")
                times.append(time.time())
                print('This animal has stopped working...')
                break

    #END OF TRIAL LOOP

    print("Experiment " + t_now + " has concluded!")
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
    
    return file_name
