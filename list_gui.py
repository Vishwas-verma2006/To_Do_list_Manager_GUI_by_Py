# Final to do list manager with GUI 
file = "D:\CODING\python language\Projects\Task.txt"

import PySimpleGUI as sg

def load_task():
    tasks = []
    try:
        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("[#] "):
                    tasks.append({'task': line[4:], 'completed':True})
                elif "[ ] " in line:
                    tasks.append({'task': line[4:], 'completed':False})
    except FileNotFoundError:
        open(file, "w").close()
    return tasks

def save_task(tasks):
    with open(file, "w") as f:
        for task in tasks:
            status = "[#]" if task['completed'] else "[ ]"
            f.write(f"{status} {task['task']}\n")

def display(win,tasks):
    display = []
    for i,task in enumerate(tasks):
        if task['completed']:
            display.append(f"{i+1}.✅ {task['task']}\n")
        else:
            display.append(f"{i+1}.❎ {task['task']}\n")
    win['list'].update(display)

sg.theme("DarkGrey13")  # theme of window 
 
sg.set_options(font=('Segoe UI', 12, "bold"), button_color=('white', '#007ACC')) # set up of colors of all things in windows 

layout = [ [sg.Text('📝 Your To-Do List', font=('Segoe UI', 16, 'bold'), justification='center', expand_x=True)],
          
           [sg.Text("Enter the task:"), sg.InputText(key=('task'),size=(35,2)),
            sg.Button("Add",bind_return_key=True,size=(12,1),pad=((10, 10), (10, 10)))],

           [sg.Listbox(values = [], size=(40,10), key= ('list'))],

           [sg.Button("Mark Task",size=(12,1),pad=((10, 10), (10, 10))), 
            sg.Button("Delete",size=(12,1),pad=((10, 10), (10, 10))),
            sg.Button('Edit',size=(12,1),pad=((10, 10), (10, 10))),
            sg.Button("Exit",size=(12,1),pad=((10, 10), (10, 10))) ]
]

win = sg.Window("TO DO LIST MANAGER", layout, size= (600,400), element_justification='center',resizable=True, finalize=True)

# make the list and call the file functions 
tasks = load_task()
display(win,tasks)

while True:
    event ,value = win.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    elif event == 'Add':
        data = value['task'].strip()
        if data:
            tasks.append({'task':data, 'completed':False})
            save_task(tasks)
            display(win,tasks) # GUI function to display task on list_box
            win['task'].update("")
        else:
            sg.popup("Please Enter a Task.")
        
    elif event == 'Mark Task':
        selected = value['list']
        if selected:
            for t in tasks:
                if t['task'] in selected[0]:
                    if t['completed'] == True:
                        t['completed'] = False
                    else:
                        t['completed'] = True
            save_task(tasks)
            display(win,tasks)
    
    elif event == 'Delete':
        selected = value['list']
        if selected:
            for i,t in enumerate(tasks):
                if t['task'] in selected[0]:
                    tasks.pop(i)
            save_task(tasks)
            display(win,tasks)

    elif event == 'Edit':
        selected = value["list"]
        if selected:
            for t in tasks:
                if t['task'] in selected[0]:
                    new = sg.popup_get_text("Enter the new task:- ")
                    if new is not None: # check if the user click cancle on popup 
                        t['task'] = new
            save_task(tasks)
            display(win,tasks)
    
win.close()