# module required
import mysql.connector
import datetime

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
    sql = r"CREATE TABLE tasks (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255), add_time DATETIME,status VARCHAR(255),end_time DATETIME)"
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
        time.append(datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))
        status[task] = 'Not Started'


# complete ToDo (status)
def task_status(task):
    status[task] = "Done"
    end_time[task] = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
    

# delete ToDo
def del_task(task):
    time.remove(time[task_list.index(task)])
    task_list.remove(task)
    status.pop(task)
    end_time.pop(task)


#  save changes 
def save_task():
    mycursor = mydb.cursor()
    clstable = "TRUNCATE TABLE tasks"
    print(clstable)
    mycursor.execute(clstable)
    mydb.commit()
    for i in range(len(task_list)):
        if status[task_list[i]] == "Done":
            End_Time = end_time[task_list[i]]
            save_end_time = r",STR_TO_DATE('{}','%Y-%m-%d %H:%i:%S'))".format(End_Time)
        else:
            save_end_time = ",NULL)"
        sql = r"INSERT INTO tasks (task,add_time,status,end_time) values ('{}',STR_TO_DATE('{}','%Y-%m-%d %H:%i:%S'),'{}'".format(task_list[i],time[i],status[task_list[i]]) + save_end_time
        mycursor.execute(sql)
        mydb.commit()


# init DB
def init():
    create_db()
    create_table()

# data loader
def dataloader():
    global name
    mycursor = mydb.cursor()
    sql_name = "show databases"
    # extracting databases name from database
    mycursor.execute(sql_name)
    db_names = mycursor.fetchall()
    for dbname in db_names:
        print(db_names)
        if "todolist" in dbname[0]:
            name = dbname[0][:-9]
            print("hi ",name)
            usedb = "USE " + dbname[0]
            mycursor.execute(usedb)
            mydb.commit()
            break
    else:
        return init()
    sql = "SELECT * FROM tasks"
    mycursor.execute(sql)
    global myresult
    myresult = mycursor.fetchall()
    extractor()
    

# data extractor
def extractor():
    global task_list,time,status,end_time
    for record in myresult:
        task_list.append(record[1])
        time.append(record[2].strftime(r"%Y-%m-%d %H:%M:%S"))
        status[record[1]] = record[3]
        if record[4] == None:
            end_time[record[1]] = "Not Started"
        else:
            end_time[record[1]] = record[4].strftime(r"%Y-%m-%d %H:%M:%S")


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
end_time ={}
time = []
task_list = [] # list of tasks
status ={} # status of the task key =  task and value = status  -> status =(Done, Not Started)
connector()

dataloader()
# add_task()
# print(task_list,status,time,end_time)
# task_status(task_list[0])
# print(task_list,status,time,end_time)
# add_task()
# print(task_list,status,time,end_time)
# del_task(task_list[0])
# print(task_list,status,time,end_time)
# add_task()
# print(task_list,status,time,end_time)
# add_task()
# print(task_list,status,time,end_time)
# task_status(task_list[2])
display_task()
print(task_list,status,time,end_time)
save_task()