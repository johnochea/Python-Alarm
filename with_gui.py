import time
from datetime import datetime
import PySimpleGUI as sg
from plyer import notification
import winsound
import time

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
     
    
def startAlarm(times:int,task:str,description:str, window): #This function starts the alarm process which takes in time, task name, and description
    notifyUser(task,description)
    window.Hide()
    if times > 0:
        time.sleep(times)
        triggeralarm(task)
        window.UnHide()
        
def triggeralarm(task:str):
    winsound.PlaySound('sound', winsound.SND_ASYNC)
    
    alarm_window = make_alarmWindow(task)
    while True:
        alarm_window.read()
        break
    alarm_window.close()
    winsound.PlaySound(None, winsound.SND_PURGE)

    

def make_mainWindow(): #This creates the Window or the main GUI of the alarm "app"
    sg.theme('Dark2')
    layout = [  [sg.Text('taskAlert: Deadline Reminder',justification='center',size=(43,1),font=("Arial",18))],
                [sg.Text('Task:',justification='center',size=(75,1),key = '_text1_')],
                [sg.InputText(pad=(150,0),key = '_task_')],
                [sg.Text('Due Date (mm/dd/yyyy):',justification='center',size=(75,1),key = '_text2_')],
                [sg.InputText(pad=(150,0),key = '_date_')],
                [sg.Text('Time (24-hr format) (hr:min:sec) (00:00:00):',justification='center',size=(75,1),key = '_text3_')],
                [sg.InputText(pad=(150,0),key = '_time_')],
                [sg.Text(' ')],
                [sg.Button('Set Alarm',pad=(270,0))],
                [sg.Text(' ')]  ]

    return sg.Window('taskAlert!', layout, finalize=True)

def make_alarmWindow(taskName:str): #This creates the Window for the alarm notification
    sg.theme('Dark2')
    alarmLayout = [  [sg.Text('Deadline Alarm Clock',justification='center',size=(43,1),font=("Arial",18))],
                [sg.Text(' ')],
                [sg.Text(taskName,justification='center',size=(75,1))],
                [sg.Text('has reached its deadline',justification='center',size=(75,1))],
                [sg.Text(' ')],
                [sg.Button('Stop Alarm',pad=(270,0))]   ]

    return sg.Window('Deadline!', alarmLayout, finalize=True) 

window = make_mainWindow()


while True:
    event, values = window.read()
    
    if event == "Set Alarm":
        dateNow = datetime.now()
        deadline = datetime(int(getYear(values['_date_'])),int(getMonth(values['_date_'])),int(getDay(values['_date_'])),int(getHour(values['_time_'])),int(getMinute(values['_time_'])),int(getSecond(values['_time_'])))
        timeDiff = (deadline - dateNow)
        totalWait = timeDiff.total_seconds()
        if totalWait <= 0:
            sg.popup("Error: Cannot make alarm to the past! Set alarm again!")
        else:
            window['_text1_'].Update(visible = False)
            window['_task_'].Update(visible = False)
            window['_text2_'].Update('Alarm successfully set!')
            window['_date_'].Update(visible = False)
            window['_text3_'].Update(visible = False)
            window['_time_'].Update(visible = False)
            window.refresh()
            
            time.sleep(2)

            window['_text1_'].Update(visible = True)
            window['_task_'].Update(visible = True)
            window['_text2_'].Update('Due Date (mm/dd/yyyy):')
            window['_date_'].Update(visible = True)
            window['_text3_'].Update(visible = True)
            window['_time_'].Update(visible = True)
            window.refresh()

            startAlarm(totalWait,values['_task_'],"alarm has been set!", window)
            
    if event == sg.WIN_CLOSED:
        break
window.close()
