#sandbox.py
#
# a place to test python scrips
# "will look different from time to time" <mduhain>
#
#

import PySimpleGUI as sg
import os
from rig_ghost import rig_ghost
from reward import forward, reward, reverse
#from stepper import forward, reverse
from training import training # spout lick training
from basic_handle import basic_handle #simple graspping task
from datetime import datetime


today = datetime.now()
d_now = str(today.strftime("%Y-%m-%d"))

rig_flag = 0
  
# Add some color 
# to the window 
sg.theme('SandyBeach')      
  
# Very basic window. 
# Return values using 
# automatic-numbered keys 
layout = [ 
    [sg.Text('Please enter your animals details')], 
    [sg.Text('Mouse Number', size =(15, 1)), sg.InputText()], 
    [sg.Text('Start Weight (g)', size =(15, 1)), sg.InputText()], 
    [sg.Submit(), sg.Cancel()] 
]
  
window = sg.Window('Simple data entry window', layout) 
event, values = window.read() 
window.close() 
  
# The input data looks like a simple list  
# when automatic numbered 
print('welcome mouse:' + values[0] +' weighing ' + values[1] + ' grams.')
mouse_num = values[0]
mouse_weight = values[1]

layout = [[sg.Button('Quit'), sg.Button('Run'), sg.Button('Reward'), sg.Button('Forward'), sg.Button('Reverse')]]

# Create the window
window = sg.Window('Mouse Rig v0.1', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        print('GOODBYE!')
        break

    if event == 'Run':
        print('Training script called...')
        #file_name = training()
        #file_name = rig_ghost()
        file_name = basic_handle()
        print('rig script finished...')
        #check if date file is created in mouse folder
        path = '/home/pi/Desktop/m' + str(mouse_num) +'/' + d_now + '/' #folder for todays data
        if os.path.isdir(path): #if folder for today exists
            #move data file to here
            print('Found folder for todays data...')
            print('Moving data file...')
            current_location = '/home/pi/Desktop/Rig_Control/' + file_name
            new_location = path + file_name
            os.rename(current_location, new_location)
        else:
            print('Creating folder for todays data...')
            #make directory
            os.mkdir(path)
            #move data file to here
            print('Moving data file...')
            current_location = '/home/pi/Desktop/Rig_Control/' + file_name
            new_location = path + file_name
            os.rename(current_location, new_location)

    if event == 'Forward':
        print('Moving stepper motor forwards...')
        forward()
    
    if event == 'Reward':
        print('Dispensing user initiated reward...')
        reward()

    if event == 'Reverse':
        print('Moving stepper motor backwards...')
        reverse()


# Finish up by removing from the screen
window.close()