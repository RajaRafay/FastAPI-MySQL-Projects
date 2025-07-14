from fastapi import FastAPI, HTTPException, Depends, status, Query
from pydantic import BaseModel, Field,validator
from typing import Annotated
from sqlalchemy import func
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

# Initialize the FastAPI application
app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Book Schema
class BookCreate(BaseModel):
    title: str = Field(..., max_length=50)
    author: str = Field(..., max_length=50)
    pages: int = Field(..., ge=0)
    genre: str = Field(..., max_length=50)
    year: int = Field(..., ge=1900, le=2100)
    is_read: bool = Field(default=False)

    # validator - title
    @validator('title')
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title is blank. Please fill the title")
        return value.strip()

    # validator - director
    @validator('author')
    def validate_author(cls, value):
        if not value.strip():
            raise ValueError("Author cannot be blank. Please fill the author")
        return value.strip()

    # validator - pages
    @validator('pages')
    def validate_pages(cls, value):
        if value < 0:
            raise ValueError("Pages cannot be negative. Please correct the number of pages.")
        return value

    # validator - genre
    @validator('genre')
    def validate_genre(cls, value):
        if not value.strip():
            raise ValueError("Genre cannot be blank. Please fill the genre")
        return value.strip()
    
    # validator - year
    @validator('year')
    def validate_year(cls, value):
        if value < 1900:
            raise ValueError("Year must be 1900 or higher. Please correct year according to the conditions.")
        return value

class BookOut(BookCreate):
    id: int
    class Config:
        orm_mode = True

# Dependency to get the database session
def get_db():   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency Injection
db_dependency = Annotated[Session, Depends(get_db)]

# GET - List All Books
@app.get("/books/", response_model=list[BookOut])
def read_books(db: db_dependency):
    return db.query(models.Book).all()

# GET - View a single Book by ID
@app.get("/books/{book_id}", response_model=BookOut)
def read_book(book_id: int, db: db_dependency):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# POST - Add a new Book
@app.post("/books/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: db_dependency):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# PUT - Update a Book by ID
@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, book: BookCreate, db: db_dependency):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

# DELETE - Remove a Book by ID
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: db_dependency):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"detail": "Book deleted successfully"}

# GET - Search Books by Author
@app.get("/books/search/", response_model=list[BookOut])
def search_books(db: db_dependency, author: str = Query(..., min_length=1)):
    db_books = db.query(models.Book).filter(models.Book.author.ilike(f"%{author}%")).all()
    if not db_books:
        raise HTTPException(status_code=404, detail="No books found for the given author")
    return db_books

# GET - Book Stats
@app.get("/books/stats/")
def book_stats(db: db_dependency):
    query = db.query(models.Book)
    total_books = query.count()
    average_pages = query.with_entities(func.round(func.avg(models.Book.pages), 2)).scalar() or 0
    most_common_genre = db.query(models.Book.genre, func.count(models.Book.id).label('count')).group_by(models.Book.genre).order_by(func.count(models.Book.id).desc()).first()
    return {
        "total_books": total_books,
        "most_common_genre": most_common_genre[0] if most_common_genre else None,
        "average_pages": float(average_pages) if average_pages else 0.0,
    }

# GET - Books from last N years
@app.get("/books/last_n_years/", response_model=list[BookOut])
def books_from_last_n_years(db: db_dependency, n: int = Query(..., ge=1)):
    current_year = func.extract('year', func.now())
    start_year = current_year - n
    db_books = db.query(models.Book).filter(models.Book.year >= start_year).all()
    if not db_books:
        raise HTTPException(status_code=404, detail="No books found from the last N years")
    return db_books

# GET - Pagination
@app.get("/books/paginated/", response_model=list[BookOut])
def get_paginated_books(db: db_dependency, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    db_books = db.query(models.Book).offset(skip).limit(limit).all()
    if not db_books:
        raise HTTPException(status_code=404, detail="No books found")
    return db_books

# PUT - Mark a Book as Read
@app.put("/books/{book_id}/mark_read", response_model=BookOut)
def mark_book_as_read(book_id: int, db: db_dependency):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.is_read = True
    db.commit()
    db.refresh(db_book)
    return db_book

# GET - Return unread books
@app.get("/books/unread/", response_model=list[BookOut])
def get_unread_books(db: db_dependency):
    db_books = db.query(models.Book).filter(models.Book.is_read == False).all()
    if not db_books:
        raise HTTPException(status_code=404, detail="No unread books found")
    return db_books