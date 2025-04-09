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
def take_data_orm(userid):
    with sesison_factory() as session:
        query = (
            select(tasks_orm).where(tasks_orm.users_id == userid)
        )
        result = session.execute(query)
        tasks = result.scalars().all()  
        return tasks


        
           