from database import sesison_factory
from models import tasks_orm
from sqlalchemy import select



#ADD TASK TO SERV
def insert_data_orm(userid,desc):
    with sesison_factory() as session:
        task = tasks_orm(users_id=userid,description= desc)
        session.add(task)
        session.commit()



#GET TASKS FROM SERV
def take_data_orm():
    with sesison_factory() as session:
        # query = session.Select(tasks_orm)
        query = select(tasks_orm)
        result = session.execute(query)
        print(result.scalars().all())
        for id,task in result.scalars():
            print(f'Айди: {id}, Задача {task}\n')
## пофиксить обработку запроса плюс попробовать поймать это через фастапи, то есть закоментировать
## весь код и оставить только функцию для возврата данных
        
        

take_data_orm()        