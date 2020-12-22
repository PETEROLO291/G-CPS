# Made By PETEROLO 291©
import PySimpleGUI as sg
from time import sleep
from threading import Thread



sg.theme('DarkAmber')



# Varialbes
timer = 0
start_check = True
clicks = 0
running = True
final = 0
cps = 0
round_finished = False



# Window Elements
scores = [  [sg.Text("Timer: 0", justification='c', size=(30,1), font='Mambo 30',  key='-T-')],
            [sg.Text("CPS: 0", justification='c', size=(30,1), font='Mambo 30', key='-CPS-')],
            [sg.Text("Clicks: 0", justification='c', size=(30,1), font='Mambo 30', key='-C-')]]


layout = [  [sg.Button('Press to Start', size=(60, 15), font='Arial 15', key='-B-'),
            sg.Column(scores, vertical_alignment='start_loop')]]


window = sg.Window('G-CPS', layout, size=(1000, 375), icon="ico.ico")





# Function to disable the Button for 3s to prevent extra clicks
def disable():
    global clicks
    window["-B-"].update(disabled=True)

    window['-T-'].update("Timer: " + str(timer))
    window["-B-"].update("Done!")
    sleep(3)
    window["-B-"].update("Press to Start")
    window["-B-"].update(disabled=False)

# Creating the thread for the disable() function
dis = Thread(target=disable)




# Main loop where the timer gets updated
def timer_loop():
    global dis, timer, clicks, round_finished
    try:
        timer = 0
        while running:
            if round_finished == True:
                timer = 5
            window['-T-'].update("Timer: " + str(timer)) 
            timer += 1
            sleep(1)

            # Stopping the timer
            if timer == 5:
                round_finished = True
                disable()
                timer = 0
    except:
        pass



# Creating the thread for the timer_loop() function
start_loop = Thread(target=timer_loop)



# Fix to prevent the timer running until there is no click event
def check():
    global timer
    while running:
        sleep(1)

        if clicks == 0:
            timer = 0



# Creation and execution of the check thread
st_ceck = Thread(target=check)
st_ceck.start()



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


start_calc = Thread(target=calculation)


# Main PySimpleGui event loop
while True:

    # This first if will only run the first time the user clicks the Button
    if clicks == 1 and start_check == True:
        start_loop.start()
        start_calc.start()
        start_check = False

    event, values = window.read()

    # Window closing event
    if event == sg.WINDOW_CLOSED:
        running = False
        break
    
    # Restart the scores hen first click is pressed
    elif event == '-B-':
        if round_finished == True:
            round_finished = False
            timer = 0
            clicks = 0
        # Empty the Button when the user is spamming clicks
        if clicks < 1:
            window['-B-'].Update("")
        clicks += 1
        window['-C-'].update("Clicks: " + str(clicks))

# Closing the window
window.close()