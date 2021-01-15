#!/usr/bin/env python

import PySimpleGUI as sg
from os import system
from time import sleep
from threading import Thread


# Read Saved Theme
with open("theme.txt") as theme:
    theme = theme.read()



# Variables
timer_goal = 5
timer = 0
start_loops = True
clicks = 0
running = True
final = 0
cps = 0
round_finished = False
off = True
record = ""
file = ""
saved_rec = ""
write_rec = ""


# Window Theme
sg.theme(theme)



#··Window Elements··#

# Upper menu
menu =  [["File", ["Themes", ["Default", "Lite_Theme", "Light_Blue", "Dark_Blue", "Navy_Blue", 
                             "Blue_Night", "Blue_Purple", "Light_Purple", "Dark_Purple",
                             "Black_and_Red", "Grey_and_Green", "Cob_Green", "Garnet", "Berry", "Green",]]], 
                             ["Time", ["1 Second", "3 Seconds", "5 Seconds", "10 Seconds", "15 Seconds", "30 Seconds", "1 Minute"]]]


# Themes Dictionary, to be able to write a custom name to the themes and not have the theme name that uses PySimpleGui
themes = dict(Default="DarkAmber", Lite_Theme="SystemDefault1", Light_Blue="BlueMono", Navy_Blue="DarkBlue13", Dark_Blue="DarkBlue12",
              Blue_Night="DarkBlue14", Blue_Purple="DarkBlue5", Light_Purple="DarkBlue4", Dark_Purple="DarkBlue6",
              Grey_and_Green="DarkGrey", Cob_Green="DarkGreen1", Black_and_Red="DarkBrown4", Berry="DarkPurple3", Garnet="DarkRed", Green="Green")


# The theme List of the Upper Menu
them_list = ["Default", "Lite_Theme", "Light_Blue", "Dark_Blue", "Navy_Blue",
             "Blue_Night", "Blue_Purple", "Light_Purple", "Dark_Purple",
             "Grey_and_Green", "Cob_Green", "Black_and_Red", "Berry", "Garnet", "Green"]


# Score table
scores = [  [sg.Text("0.0 CPS in 0s", justification='c', size=(30,1), font='Mambo 20', pad=(None, (0, 20)), key='-R-')],
            [sg.Text("Timer: 0", justification='c', size=(30,1), font='Mambo 35', pad=(None, (0, 20)), key='-T-')],
            [sg.Text("CPS: 0.0", justification='c', size=(30,1), font='Mambo 35', key='-CPS-')],
            [sg.Text("Clicks: 0", justification='c', size=(30,1), font='Mambo 35', pad=(None, (20, 20)), key='-C-')]]

# Exit Button
close_but = [   [sg.Column(scores, pad=(0, (15, 1)),  key='-CL-')],
                [sg.Column([[sg.Button('Close', size=(12, 1))]], justification='right')]]


# Window construction
layout = [  [sg.Menu(menu, background_color="White", text_color="Black", key="-M-")],
            [sg.Button('Press to Start', size=(60, 15), font='Arial 15', key='-B-'),
             sg.Column(close_but, expand_y=True)]]

# Window Features
window = sg.Window('G-CPS', layout, size=(1000, 375), finalize=True, grab_anywhere=True, icon="ico.ico")

# Tkinter code required to position the close button
window['-CL-'].Widget.pack(expand=True)
window['-CL-'].Widget.master.pack(fill='y', expand=True)

# Display the record of the default open time mode when opening the program. If file doesn't exist a new one will be created
create_f = open("record_5.txt", "a")
create_f.close()
with open("record_5.txt", "r") as saved:
    saved_rec = saved.read()

    if saved_rec == "":
        saved_rec = 0.0
        
    record = str(saved_rec) + " CPS in 5s"
    window["-R-"].update(record)



# Function to disable the Button for 3s to prevent extra clicks
def disable():
    global timer, off, file, timer_goal, saved_rec, write_rec, cps, record



    window["-B-"].update(disabled=True)
    window['-T-'].update("Timer: " + str(timer))
    window["-B-"].update("Done!")
    sleep(1.5)
    window.grab_any_where_on()
    window["-B-"].update("Press to Start")
    window["-B-"].update(disabled=False)
    off = False

    file = "record_" + str(timer_goal) + ".txt"
    with open(file, "r") as saved:
        saved_rec = saved.read()
    saved.close()

    if saved_rec == "" or float(saved_rec) < cps:
        write_rec = open(file, "w+")
        write_rec.write(str(cps))
        write_rec.close()
        record = str(cps) + " CPS in " + str(timer_goal) + "s"
        window["-R-"].update(record)


# Creating the thread for the disable function
dis = Thread(target=disable)




# Main loop where the timer gets updated
def timer_loop():
    global timer, round_finished, clicks
    try:
        
        while running:
            if round_finished == False:
                sleep(1)
                timer += 1

                # Stopping the timer
                if timer == timer_goal and off == True:
                    round_finished = True
                    disable()
                
                if round_finished == True:
                    timer = timer_goal
                window['-T-'].update("Timer: " + str(timer))
                

                if timer == 0 and clicks == 0:
                    window['-B-'].update("Press to Start") 
                
                
            else:
                sleep(0.05)

            
    except:
        pass

# Creating the thread for the timer_loop() function
start_loop = Thread(target=timer_loop)


# Function where the CPS calculation is done
def calculation():
    global clicks, cps, timer, round_finished, running

    while running:
        
        try:
            if round_finished == True:
                sleep(0.1)
                pass

            else:
                sleep(0.3)
                cps = clicks / timer
                cps = round(cps, 1)
                window["-CPS-"].update("CPS: " + str(cps)) 

        except:
            pass

# Creating the thread for the calculation() function
start_calc = Thread(target=calculation)


#···Main PySimpleGui event loop···#
while running:
    window["-C-"].update("Clicks: " + str(clicks))
    # This first if will only run the first time the user clicks the Button
    if clicks == 1 and start_loops == True:
        start_loop.start()
        start_calc.start()
        start_loops = False

    event, values = window.read()

    # Window closing event
    if event == sg.WINDOW_CLOSED or event == "Close":
        running = False

    # Reset values when round is finished
    if round_finished == True:
            clicks = 0
            timer = 0

    
    # Restart the scores hen first click is pressed
    if event == '-B-':
        if off == False:
            off = True
            round_finished = False
        clicks += 1
        window['-C-'].update("Clicks: " + str(clicks))


        # Empty the Button when the user is spamming clicks
        if clicks != 0:
            window.grab_any_where_off()
            window['-B-'].Update("")




    #Theme Saving
    if event in them_list:
        set_theme= open("theme.txt","w+")
        set_theme.write(themes[event])
        set_theme.close()
        running = False
        system("hide.vbs")




    # Change the timer goal
    if event == "1 Second" and clicks == 0:
        if timer >= 1:
            pass
        else:
            timer_goal = 1

    if event == "3 Seconds" and clicks == 0:
        if timer >= 3:
            pass
        else:
            timer_goal =3

    if event == "5 Seconds" and clicks == 0:
        if timer >= 5:
            pass
        else:
            timer_goal = 5

    if event == "10 Seconds" and clicks == 0:
        if timer >= 10:
            pass
        else:
            timer_goal = 10

    if event == "15 Seconds" and clicks == 0:
        if timer >= 15:
            pass
        else:
            timer_goal = 15

    if event == "30 Seconds" and clicks == 0:
        if timer >=30:
            pass
        else:
            timer_goal = 30

    if event == "1 Minute" and clicks == 0:
        if timer >= 60:
            pass
        else:
            timer_goal = 60

    # Saving of the record
    if event in ("1 Second", "3 Seconds", "5 Seconds", "10 Seconds", "15 Seconds", "30 Seconds", "1 Minute") and clicks == 0:
        if event == "1 Minute":
            event = "60"
        event = int(''.join(filter(str.isdigit, event)))


        file = "record_" + str(event) + ".txt"

        # Create file inc ase doesn't exist
        create = open(file, "a")
        create.close()

        with open(file, "r") as saved:
            saved_rec = saved.read()

            if saved_rec == "":
                saved_rec = 0.0

            record = str(saved_rec) + " CPS in " + str(event) + "s"
            window["-R-"].update(record)
        saved.close()

# Closing the window
window.close()

# Made By PETEROLO 291©