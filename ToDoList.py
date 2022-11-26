# module required
import mysql.connector
import datetime
import psycopg2


# HELP
def helpmanual():
    print('''Enter "1"  to add a task.
      "2"  to remove a task.
      "3" to display ToDoList.
      "4" to comlpete a task.
      "5" or "q" to exit.
      to see this help just type "help" :)''')
    print() # empty line


# create DB
def create_db():
    global name
    name = input("Whats your name ? (optional) \n")
    if not name:
        name = "user"
    print("hi ", name, ".")
    print() # empty line
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
    
    
# connecting to mysql DB
def mysqlconnector():
    global mydb
    mydb = mysql.connector.connect(
    host='127.0.0.1', user='root', password='testtest', database='mysql')


# connectind to postgresql DB
def postgresconnector():
    global postcursor
    conn = psycopg2.connect(database="postgresDB",
                        host="127.0.0.1",
                        user="postgresUser",
                        password="testtest",
                        port="5455")
    postcursor =  conn.cursor()


# add ToDo
def add_task():
    task = input("Enter your task : ")
    print() # empty line
    if task.isnumeric():
        print("Task is not valid")
        add_task()
        return
    else:
        task_list.append(task)
        time.append(datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))
        status[task] = 'Not Started'
        end_time[task] = 'Not Finished'


# complete ToDo (status)
def task_status():
    try:
        taskindex = int(input("Wich Task ? (Task number) "))-1
        print() # empty line
    except ValueError:
        print("You must enter a task number! ")
        task_status()
        return
    if taskindex < 0 or taskindex >= len(task_list):
        print("number is out of range! ")
        print() # empty line
        task_status()
        return
    task = task_list[taskindex]
    if status[task] == 'Done' :
        return
    status[task] = "Done"
    end_time[task] = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
    

# delete ToDo
def del_task():
    try:
        taskindex = int(input("Wich Task ? (Task number) "))-1
        print() # empty line
    except ValueError:
        print("You must enter a task number! ")
        print() # empty line
        del_task()
        return
    if taskindex < 0 or taskindex >= len(task_list):
        print("number is out of range! ")
        print() # empty line
        del_task()
        return
    task = task_list[taskindex]
    time.remove(time[task_list.index(task)])
    task_list.remove(task)
    status.pop(task)
    end_time.pop(task)


#  save changes 
def save_task():
    mycursor = mydb.cursor()
    clstable = "TRUNCATE TABLE tasks"
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
        if "todolist" in dbname[0]:
            name = dbname[0][:-9]
            print("hi ",name)
            print() # empty line
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
    print(" ","  ",(((length)//2)-2)*' ',"task" ,(((length)//2)-2)*' ',': ', "   status   ","     Start Time     ","      End Time")
    for task in task_list:
        print() # empty line
        print(task_list.index(task)+1,". ",((length-len(task))//2)*' ',task ,((length-len(task))//2)*' ',': ',' '*3 ,status[task],"  ",time[task_list.index(task)]," ",end_time[task])
    print() # empty line


# main
def main():
    run = 1
    helpmanual()
    while run:
        cmd = input("what do you want to do ? (see help) ")
        print() # empty line
        if cmd == "help":
            helpmanual()
        elif cmd == "1":
            add_task()
        elif cmd == "2":
            del_task()
        elif cmd == "3":
            display_task()
        elif cmd == "4":
            task_status()
        elif cmd == "5" or cmd == "q" or cmd == "Q":
            run = 0 
            print("Goodbye :)")
            save_task()
            break
        else:
            print("not a valid command! :(")
            print() # empty line
            

if __name__ == "__main__":
    end_time ={}
    time = []
    task_list = [] # list of tasks
    status ={} # status of the task key =  task and value = status  -> status =(Done, Not Started)
    postgresconnector()
    #mysqlconnector()
    dataloader()
    main()

