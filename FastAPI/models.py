from database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean


class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String)
    author = Column(String)
    date_added = Column(String)