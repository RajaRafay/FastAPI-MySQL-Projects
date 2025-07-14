from fastapi import FastAPI, HTTPException, Depends, status, Query
from pydantic import BaseModel, Field, validator
from typing import Annotated  
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

# Create FastAPI instance
app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Pydantic - BaseModel
class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Title is required")
    director: str = Field(..., min_length=1, description="Director is required")
    year: Annotated[int, Field(ge=1900, le=2100)] = Field(..., description="Year must be between 1900 and 2100")

    # validator - title
    @validator('title')
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title is blank. Please fill the title")
        return value.strip()

    # validator - director
    @validator('director')
    def validate_director(cls, value):
        if not value.strip():
            raise ValueError("Director cannot be blank. Please fill the director")
        return value.strip()

    # validator - year
    @validator('year')
    def validate_year(cls, value):
        if value < 1900:
            raise ValueError("Year must be 1900 or higher. Please correct year according to the conditions.")
        return value

class MovieOut(MovieCreate):
    id: int
    class Config:
        orm_mode = True

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency Injection
db_dependancy = Annotated[Session, Depends(get_db)]

# GET - Display ALL Movies
@app.get("/movies/", response_model=list[MovieOut])
def read_movies(db: db_dependancy):
    return db.query(models.Movie).all()

# GET - Display a specific movie by ID
@app.get("/movies/{movie_id}", response_model=MovieOut)
def read_movie(movie_id: int, db: db_dependancy):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

# POST - Add a new movie
@app.post("/movies/", response_model=MovieOut, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: db_dependancy):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie 

# PUT - Update an existing movie
@app.put("/movies/{movie_id}", response_model=MovieOut)
def update_movie(movie_id: int, movie: MovieCreate, db: db_dependancy):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in movie.dict().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# DELETE - Remove a movie
@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: db_dependancy):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(db_movie)
    db.commit()

# GET - Search Movies by Title
@app.get("/movies/search/", response_model=list[MovieOut])
def search_movies(db: db_dependancy, q: str = Query(..., min_length=1, description="Title search query")):
    db_movies = db.query(models.Movie).filter(models.Movie.title.ilike(f"%{q}%")).all()
    if db_movies is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found matching search criteria")
    return db_movies

# GET - Filter Movies by Year and Director
@app.get("/movies/filter/", response_model=list[MovieOut])
def filter_movies(db: db_dependancy, year: Annotated[int | None, Query(ge=1900, le=2100)] = None, director: Annotated[str | None, Query(min_length=1)] = None):
    query = db.query(models.Movie)
    if year is not None:
        query = query.filter(models.Movie.year == year)
    if director is not None:
        query = query.filter(models.Movie.director.ilike(f"%{director}%"))
    results = query.all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No movies match the filter criteria")
    return results