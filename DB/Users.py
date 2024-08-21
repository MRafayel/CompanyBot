import datetime

from sqlalchemy import Integer, Column, DateTime, String, Float
from DB.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    field_id = Column(Integer)
    last_comp_id = Column(Integer)
    term = Column(DateTime, default=datetime.datetime.now())


if __name__ == '__main__':
    pass
