from datetime import datetime
import threading
from plyer import notification
import winsound
import keyboard
def getYear(date:str) -> str: #This function extracts the 'year (yyyy)' portion of the Date input
    return date[6:10]

def getMonth(date:str) -> str: #This function extracts the 'month (mm)' portion of the Date input
    return date[0:2]

def getDay(date:str) -> str: #This function extracts the 'day (dd)' portion of the Date input
    return date[3:5]

def getHour(time:str) -> str: #This function extracts the 'hour' portion of the Time input
    return time[0:2]

def getMinute(time:str) -> str: #This function extracts the 'minute' portion of the Time input
    return time[3:5]

def getSecond(time:str) -> str: #This function extracts the 'seconds' portion of the Time input
    return time[6:8]

def notifyUser(taskName:str,description:str): #This function is responsible for the notifications that pop up
    notification.notify(
        title = taskName,
        message = description,
        timeout = 5
        )
        
def startAlarm(times:int,task:str,description:str): #This function starts the alarm process which takes in time, task name, and description
    notifyUser(task,description)

    if times > 86400:
        dayBefore = times - 86400
        dayNotif = threading.Timer(dayBefore, startAlarm,[86400,task,"is due in 1 day!"])
        dayNotif.start()

    elif times > 3600 and times <= 86400:
        hourBefore = times - 3600
        hourNotif = threading.Timer(hourBefore, startAlarm,[3600,task,"is due in 1 hour!"])
        hourNotif.start()
            
    elif times > 600 and times <= 3600:
        minutesBefore = times - 600
        minuteNotif = threading.Timer(minutesBefore, startAlarm,[600,task,"is due in 10 minutes!"])
        minuteNotif.start()

    elif times > 60 and times <= 600:
        secondsBefore = times - 60
        secondsNotif =  threading.Timer(secondsBefore, startAlarm, [60, task, "is due in 60 seconds"])
        secondsNotif.start()
    
    elif times < 0:
        print("Error cannot create alarm to the past")
        return False
    
    else:
        timer = threading.Timer(times, triggeralarm, [task])
        timer.start()
        
def triggeralarm(task:str):
    winsound.PlaySound('sound', winsound.SND_ASYNC)
    print("Deadline of " + task +"\nPress a key to turn off alarm.")
    while True:
        if keyboard.is_pressed("space") or keyboard.is_pressed("enter") or keyboard.is_pressed("esc"):
            winsound.PlaySound(None, winsound.SND_PURGE)
            break
        
def alarm_maker(date:str, times:str, task:str):
    dateNow = datetime.now()
    deadline = datetime(int(getYear(date)),int(getMonth(date)),int(getDay(date)),int(getHour(times)),int(getMinute(times)),int(getSecond(times)))
    timeDiff = (deadline - dateNow)
    totalWait = timeDiff.total_seconds()
    check = startAlarm(totalWait,task,"alarm has been set!")
    if check == False:
        return check
    else:
        return "Task: %s and Deadline: %s" %(task, str(deadline))

def set_alarm():
    print("Enter task name:")
    task = str(input())
    print("Enter date (mm/dd/yyyy):")
    date = str(input())
    print("Enter time of alarm (hh:mm:ss):")
    times = str(input())
    data = alarm_maker(date, times, task)
    return data

def confirm():
    print("Set another alarm? Y/N")
    set = str(input())
    if set == "Y" or set == "y":
        return True
    elif set == "N" or set == "n":
        return False
    else:
        print("Wrong input, try again:")
        confirm()
    
arr = []



while True:
    data = set_alarm()
    if data == False:
        pass
    else:
        arr.append(data)
    set = confirm()
    if set == True:
        continue
    elif set == False:
        break

for elements in arr:
    print(elements)
