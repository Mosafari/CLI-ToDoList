# module required
import mysql.connector

# create DB
def create_db():
    global name
    name = input("Whats your name ? (optional)\n")
    if not name:
        name = "user"
    print("hi ", name, ".")
    mycursor = mydb.cursor()
    sql = "CREATE DATABASE {}_todolist".format(name)
    mycursor.execute(sql)
    mydb.commit()
    
    
# create table
def create_table():
    mycursor = mydb.cursor()
    s= "USE {}_todolist".format(name)
    mycursor.execute(s)
    mydb.commit()
    sql = "CREATE TABLE tasks (id INTEGER PRIMARY KEY, task VARCHAR(255), add_time TIMESTAMP,status VARCHAR(255),end_time TIMESTAMP)"
    mycursor.execute(sql)
    mydb.commit()
    
    
# connecting to DB
def connector():
    global mydb
    mydb = mysql.connector.connect(
    host='127.0.0.1', user='root', password='testtest', database='mysql')


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




# display tasks
def display_task():
    length = 0
    for i in task_list:
        if len(i)> length:
            length = len(i)
    for task in task_list:
        print() # empty line
        print(task ,(length-len(task))*' ',': ', status[task])

# main

num = 0 # number of tasks
task_list = [] # list of tasks
status ={} # status of the task key =  task and value = status  -> status =(Done, Not Started)
connector()
create_db()
create_table()
add_task()
print(task_list,status)
task_status(task_list[0])
print(task_list,status)
add_task()
print(task_list,status)
del_task(task_list[0])
print(task_list,status)
add_task()
print(task_list,status)
add_task()
print(task_list,status)
task_status(task_list[2])
display_task()
