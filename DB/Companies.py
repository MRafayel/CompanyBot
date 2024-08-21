from sqlalchemy import Integer, Column, String
from DB.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer)
    field_id = Column(Integer)
    name = Column(String)
    photo = Column(String)
    title = Column(String)
    location = Column(String)
    employees = Column(String)
    website = Column(String)
    phone = Column(String)
    social = Column(String)


if __name__ == '__main__':
    pass
