import time
from plyer import notification
import os

clear = lambda: os.system("cls")
MINUTE = int(60)
sameInitialTimer = False
initialTimer = 0

def main():
    global sameInitialTimer
    global initialTimer
    clear()
    stopwatchStart = 0
    totalTime = 0
    restartChoice = ""

    if not sameInitialTimer:
        initialTimer = 0
    #input initial timer lenght
        initialTimer = int(input("Initial timer duration (minutes): ")) * MINUTE
    print("Started timer for", initialTimer//60, "minute(s).")
    sameInitialTimer = False
    #run timer
    time.sleep(initialTimer)
    #notify on timer end
    notification.notify(
    title="Minimum Pomo",
    message="Minimum time's up.",
    app_icon=None,
    timeout=5,
    )
    #start a stopwatch
    stopwatchStart = time.time()
    #display total time upon stopwatch stop
    input("Enter to stop work period, Ctrl+C to exit.\n")
    totalTime = time.time() - stopwatchStart + initialTimer
    print("Focused for", totalTime//60, "minute(s).")
    #start another one if wanted
    restartChoice = input("Would you like to start another pomo?(Y/n/s(ame initial timer)): ").lower()
    if restartChoice == "s":
        sameInitialTimer = True
    elif restartChoice == "n":
        exit()

while True:
	try:
		main()
	except KeyboardInterrupt:
		exit()