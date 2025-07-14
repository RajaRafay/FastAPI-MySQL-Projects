from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
URL_DATABASE = "mysql+pymysql://root:rah123456asd@localhost:3306/personal_book_tracker"

# Create the database engine
engine = create_engine(URL_DATABASE)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()