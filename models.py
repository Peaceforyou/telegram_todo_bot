from database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import BIGINT,TEXT,ForeignKey,MetaData


metadata_obj = MetaData()



class people(Base):
    __tablename__ = 'people'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    users_id: Mapped[BIGINT]
    
    
class tasks(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(primary_key=True)    
    users_id: Mapped[BIGINT] = mapped_column(ForeignKey('people.id',ondelete='CASCADE'))
    description: Mapped[TEXT]
    
    
class feedbacks2(Base):
    __tablename__ = 'feedbacks2'
    
    id: Mapped[int] = mapped_column(primary_key=True)
