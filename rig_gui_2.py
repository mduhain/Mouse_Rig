#sandbox.py
#
# a place to test python scrips
# "will look different from time to time" <mduhain>
#
#

import PySimpleGUI as sg 
from rig_ghost import rig_ghost

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
print(event, values[0], values[1]) 

layout = [[sg.Button('Quit'), sg.Button('Run'), sg.Button('Forward'), sg.Button('Reverse')]]

# Create the window
window = sg.Window('Mouse Rig v0.1', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    if event == 'Run':
        print('Rig_1.py Called')
        rig_ghost()
        #if rig_flag == 0:
        #    import rig_ghost 
        #    rig_flag = 1
        #else:
        #    rig_ghost()

    if event == 'Forward':
        print('test_stepper.py Called')

    if event == 'Reverse':
        print('rev_stepper.py Called')


# Finish up by removing from the screen
window.close()
