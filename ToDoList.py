# module required



# connecting to DB



# add ToDo
def add_task():
    task = input("Enter your task : ")
    if task.isnumeric():
        print("Task is not valid")
        add_task()
    else:
        task_list.append(task)
        status[task] = 'Not Started'


# complete ToDo
def task_status(task):
    status[task] = "Done"
    

# delete ToDo
def del_task(task):
    task_list.remove(task)
    status.pop(task)



#  save changes 




# disply tasks


# main

num = 0 # number of tasks
task_list = [] # list of tasks
status ={} # status of the task key =  task and value = status  -> status =(Done, Not Started)
add_task()
print(task_list,status)
task_status(task_list[0])
print(task_list,status)
add_task()
print(task_list,status)
del_task(task_list[0])
print(task_list,status)