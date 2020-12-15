# rig_gui.py
#
# version 0.1
# <mduhain> an interactive GUI for working with the mouse rig.
#  - will rely on the previous script rig_1.py, test_stepper.py, and rev_stepper.py
#
#

# Import GUI sandbox
import PySimpleGUI as sg

# Define the window's contents
layout = [[sg.Text("Which mouse are we working with?")],
          [sg.Input(key='-INPUT-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('Ok'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Mouse Rig v0.1', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    window['-OUTPUT-'].update('Welcome ' + values['-INPUT-'] + "! Thanks for trying Mouse Rig v0.1", text_color='yellow')

# Finish up by removing from the screen
window.close()