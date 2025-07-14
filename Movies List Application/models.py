from sqlalchemy import Column, Integer, String
from database import Base

# Movie Model
class Movie(Base):
    # Table name
    __tablename__ = "movies"
    
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    director = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False, default=1900) 
