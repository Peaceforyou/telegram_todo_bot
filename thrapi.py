from conserv import connect_to_server
from  fastapi import FastAPI,Response
from pydantic import BaseModel
from datetime import date,datetime
from orm import take_data_orm


app = FastAPI()



# Get feedback database
@app.get("/get/feedbacks",tags=["Get methods"])
def getfeedback():
    # Connect to the server
    con, cursor = connect_to_server()
    try:
        cursor.execute("SELECT * FROM feedbacks2")
        rows = cursor.fetchall()
        result = '\n'.join([f'{str(row[0])}.  {str(row[1])}, {str(row[2])}' for row in rows])
        return Response(content=result, media_type="text/plain")
    except Exception as e:
        return {"error": str(e)}
    finally:
        con.close()



#Get all tasks
@app.get("/get/tasks/",tags=["Get methods"])
def gettasks(userid:int):
    try:
        tasks = take_data_orm(userid)
        if tasks:
            result = '\n'.join([f'{index + 1}. {task.description}' for index,task in enumerate(tasks)])
            return Response(content=result, media_type="text/plain")
        else:
            return Response(status_code=404)
    except Exception as e:
        return {"error": str(e)}




#Creating BaseModel to add tasks

class Task(BaseModel):
    user_id: int
    message: str
    date_received: None
    
# Add task    
@app.post("/add/tasks")
def addtask(task: Task):
    # Connect to the server
    con, cursor = connect_to_server()
    try:
        cursor.execute("INSERT INTO tasks (users_id,description, time) VALUES (%s,%s,%s)", (task.user_id,task.message,task.date_received))
        con.commit()
        return Response(content='Все успешно добавилось', media_type="text/plain")
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        con.close()




# Delete task
@app.post("/delete/tasks")
def deletetask(task: Task):
    # Connect to the server
    con, cursor = connect_to_server()
    try:
        task_index = int(task.message) - 1
        cursor.execute("SELECT id FROM tasks WHERE users_id = %s", (task.user_id,))
        rows = cursor.fetchall()
        if rows:
            real_task_id = rows[task_index]  
            cursor.execute("DELETE FROM tasks WHERE users_id = %s AND id = %s", (task.user_id, real_task_id))
            con.commit()
            return Response(content='Успешно удалено!', media_type="text/plain")
        
        else:
            return Response(content='Нет задач для удаления!', media_type="text/plain")
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        con.close()