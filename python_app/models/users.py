from sqlalchemy.orm import relationship,Mapped,mapped_column
from sqlalchemy import Index
from typing import Annotated
from .base import Base
import datetime

fcx = Annotated[int,mapped_column(primary_key= True)]

class UsersOrm(Base):
    __tablename__ = "users"
    id : Mapped[fcx]
    username : Mapped[str] = mapped_column(unique= True)
    password : Mapped[bytes] 
    email : Mapped[str] = mapped_column(unique= True)
    created_at : Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow())
    is_admin : Mapped[bool] = mapped_column(default=False) 

    
