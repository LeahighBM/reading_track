from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String)
    author = Column(String)
    date_added = Column(String)
    already_own = Column(Boolean)