from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(Integer)  # 0 - текущее, 1 - желаемое
    tags = Column(String)   # "деньги, переезд"