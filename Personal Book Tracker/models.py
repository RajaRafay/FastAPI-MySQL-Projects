from sqlalchemy import Boolean, Column, Integer, String
from database import Base

# Movie Model
class Book(Base):
    # Table name
    __tablename__ = "books"
    
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    pages = Column(Integer, nullable=False, default=0)
    genre = Column(String(50))
    year = Column(Integer, nullable=False, default=1900)
    is_read = Column(Boolean, default=False)