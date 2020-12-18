def rig_ghost():
    import csv
    import time
    #import RPi.GPIO as GPIO
    from datetime import datetime
    from itertools import zip_longest
    import random
    import os

    #create unique filename with date and time
    today = datetime.now()
    t_now = str(today.strftime("%Y_%m_%d_%H_%M_%S"))
    new_csv = ".csv"
    data = "data_"
    file_name = "".join((data,t_now,new_csv))

    time.sleep(0.2)

    #START INITIAL EVENT
    events = ["Exp_Start"] #define array to hold experiment events
    now = time.time() #mark time
    times = [now] #define array to hold experiment event times
    print('Experiment ' + t_now)

    time.sleep(0.2)

    #STRT TRIAL LOOP
    for n in range(3):
        print('Trial ' + str(n+1) + ' start!')
        events.append("Trial_Start")
        times.append(time.time())
        time.sleep(0.2)
        print('Reward given!')
        events.append("Reward")
        times.append(time.time())
        time.sleep(2)
        for nn in range(10):
            num = random.random()
            if num > 0.75:
                print('Spout Licked!')
                time.sleep(0.1)
        print('Trial ' + str(n+1) + ' end!')
        events.append("Trial_End")
        times.append(time.time())
        print('...')
        time.sleep(0.5)

    #end experiment
    print('Experiment ' + t_now + ' has finished.')
    
    #open/create file with file_name
    print('writing data file...')
    file_handle = open(file_name,'w+', newline ='')

    #fill file with data
    d = [events, times]
    export_data = zip_longest(*d, fillvalue = '')
    with file_handle:
        write = csv.writer(file_handle)
        write.writerow(("EVENTS", "TIMES"))
        write.writerows(export_data)

    file_handle.close()
    print('Datafile: ' + file_name + ' wrote.')
    
    return file_name