from database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import BIGINT,TEXT,ForeignKey,MetaData,DATE


metadata_obj = MetaData()



class people(Base):
    __tablename__ = 'people'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    users_id: Mapped[int]
    
    
class tasks_orm(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(primary_key=True)    
    users_id: Mapped[int] = mapped_column(ForeignKey('people.id',ondelete='CASCADE'))
    description: Mapped[str]
    
    
class feedbacks2_orm(Base):
    __tablename__ = 'feedbacks2'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
class completed_orm(Base):
    __tablename__ = 'completed'
    
    users_id: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]
    # date: Mapped[DATE]
