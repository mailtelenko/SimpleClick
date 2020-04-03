# Imports
from os import system, name 
import pyautogui

#
# Variable Declaration/Config
#

# Pyautogui config
pyautogui.FAIL_SAFE = True
pyautogui.PAUSE = .6    

# Modifiers:
mouse_duration = .15
key_duration = .2

# Fun & games (at work?!)
counter = 0
animation_display_count = 3

# Events list:
events = [[1632, 89], "click", "INPUT", [1600,369], "click", "click", ["9", "enter", "enter", "right", "1", "enter", "right", "2","0","2","0", "enter"], [1632, 89], "click", [1609,136,1537,138]]

# Clear screen
def clear():
    # Clear screen
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 

# Properly space and display messages
def prompt(message):

    clear()

    # Display and get information
    return input(message + "\n==> ")

# Print stats to console
def display_stats():  
    print("Display information: ", pyautogui.size())
    print(counter, " edits completed.")

# Edit script variables
def config():
    global mouse_duration
    global key_duration

    # Get failsalfe
    if(prompt("Enable failsafe (y/n) [" + str(pyautogui.FAIL_SAFE) + "]") == "y"):
        pyautogui.FAIL_SAFE = True
    else:
        pyautogui.FAIL_SAFE = False

    # Get pause speed
    pyautogui.PAUSE = float(prompt("Duration between actions (number) [" + str(pyautogui.PAUSE) + "]"))

    # Get pause speed
    mouse_duration = float(prompt("Mouse speed (number) [" + str(mouse_duration) + "]"))

    # Get keyboard speed
    key_duration = float(prompt("Mouse speed (number) [" + str(key_duration) + "]"))


# Update events list with user actions
def program_events():    
    # Display instructions for how to program

    # Create local events list
    events = []

    # Loop until exit command ('exit') is recieved
    while(True):
        # Prompt for input
        choice = prompt("Available commands:\n'finish' --> Saves sequence and returns to main menu\n'click' --> Registers a click at the current pointer location (alt-tab to reselect widow without moving cursor)\n")
        
        # Add current mouse position and "click"
        if (choice == 'click'):
            events.append([pyautogui.position().x, pyautogui.position().y])
            events.append("click")
        
        # Click and drag
        if (choice == "drag"):
            # Create initial two points
            drag = [pyautogui.position().x, pyautogui.position().y]

            # Prompt to move mouse
            prompt("Move the mouse to the second point and then press enter.")

            # Add second point to drag
            drag.append(pyautogui.position().x)
            drag.append(pyautogui.position().y)

            events.append(drag)

        # Stop accepting events
        elif (choice == "finish"):
            break
    
    return events

# Run events stored in events variable
def perform_events():
    # Global variable declaration
    global counter 

    # Iterate counter
    counter += 1

    # Initialize event anim list
    anim_events = 0

    # Iterate over each command in 
    for command in events:
        # Animate events in console
        perform_event_anim(events, anim_events)
        anim_events += 1

        # Confirmation event --> ask for input
        if (command == "INPUT"):
            input("Press enter to confirm edit...")

        # Click event --> left click mouse
        elif (command == "click"):
            pyautogui.click()

        # Array parsing
        else:
            # Check if first element is string --> type in as key input
            if (type(command[0]) is str):
                pyautogui.typewrite(command, interval=key_duration)
            
            # Check if list and length is 4 --> click and drag
            elif (type(command) is list and len(command) == 4):
                pyautogui.moveTo(command[0], command[1], mouse_duration)
                pyautogui.dragTo(command[2], command[3], mouse_duration)
            
            # Anything else (list) --> move mouse
            else:
                pyautogui.moveTo(command[0], command[1], mouse_duration)

# Console "animation" while performing
def perform_event_anim(anim_events, pos):
    # Clear screen
    clear()

    # Iterate over x times to display x events
    for i in range(animation_display_count):
        event = ""

        # Print tab & -->
        print("\t" * i, "--> ", end="")
        
        # Check if there are enough events left to update var
        if (len(anim_events) - pos >= (i + 1)):
            event = anim_events[i + pos]
        
        # Parse event
        if (event == "click"):
            event = "Left click"
        
        # List parsing
        elif (type(event) == list):
            # Keyboard type (string)
            if (type(event[0]) == str):
                event = " ".join(event)
            
            # Click drag
            elif (len(event) == 4):
                event = "Click from [" + str(event[0]) + ", " + str(event[1]) + "] to [" + str(event[2]) + ", " + str(event[3]) + "]"
        
            else:
                event = "Move to [" + str(event[0]) + ", " + str(event[1]) + "]"

        print(event + "\n")

# Main method
def main():
    # Get global variable
    global events

    # Prompt for menu choice
    choice = prompt("Main Menu:\n --> Enter 'run' to start the set/preset events.\n --> Enter 'program' to create an event set to follow\n --> Enter 'export' to export your event set to file\n --> Enter 'load' to load your exported event from the current directory\n --> Enter 'stats' to get the current statistics\n --> Enter 'exit' to stop the script\n")

    # Default proceed to perform_event
    if (choice == 'run'):
        perform_events()
    
    # Run event programmer
    elif (choice == 'program'):
        # Confirm deletion of events variable
        if (prompt("*** By continuing the current events sequence will be erased. If you want to proceed type 'continue'.***\n") == 'continue'):
            events = program_events() 

    # Display current stats
    elif (choice == 'stats'):
        display_stats()

    # Run conifg
    elif (choice == "config"):
        config()

    if (choice != 'exit'):
        main()

# Start main loop
main()