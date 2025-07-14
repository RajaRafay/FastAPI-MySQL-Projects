# 📘 Movie List Application & Personal Book Tracker API – FastAPI + MySQL

## 🌟 Project Overview

A mini project to build a **Movie List Application & Personal Book Tracker API** using **FastAPI** and **MySQL**. This API supports full CRUD operations, search, statistics, and optional advanced features.

---

## 📊 Tech Stack

- FastAPI
- MySQL
- SQLAlchemy ORM
- Pydantic
- Uvicorn

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/book-tracker-api.git
cd book-tracker-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv-FastAPI-MySQL
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database

```sql
CREATE DATABASE movies_list_application;
CREATE DATABASE personal_book_tracker;
```

Run the SQL schema:

```bash
mysql -u root -p movies_list_application < movies_schema.sql
mysql -u root -p personal_book_tracker < books_schema.sql
```

### 5. Update DB Config in `db.py`

```python
URL_DATABASE = "mysql+pymysql://root:rah123456asd@localhost:3306/movies_list_application"
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/personal_book_tracker"
```

### 6. Run the App

```bash
uvicorn main:app --reload
```

---

## 📁 Project Structure

```

FASTAPI-+-MYSQL-PROJECTS/
├── Movies-List-Application
├── Personal-Book-Tracker

Movies-List-Application/
├── main.py
├── models.py
├── database.py
├── movies_schema.sql

Personal-Book-Tracker/
├── main.py
├── models.py
├── database.py
├── books_schema.sql
```

---

## 📚 API Endpoints

### Movies CRUD

- `GET /movies` – List all movies
- `GET /movies/{movie_id}` – Get movie by ID
- `POST /movies` – Add a movie
- `PUT /movies/{movie_id}` – Update a movie
- `DELETE /movies/{movie_id}` – Delete a movie

### Additional Features

- `GET /movies/search?title=xyz` – Search movie by title
- `GET /movies/filter?year=1900&director=xyz` – Filter movie by year or director



### Books CRUD

- `GET /books` – List all books
- `GET /books/{book_id}` – Get book by ID
- `POST /books` – Add a book
- `PUT /books/{book_id}` – Update a book
- `DELETE /books/{book_id}` – Delete a book

### Search & Stats

- `GET /books/search?author=xyz` – Search by author
- `GET /books/stats` – Book stats (count, genre, avg pages)

### Additional Features

- `GET /books/recent?years=2` – Books from last N years
- `GET /books/unread` – Display unread books
- `GET /books?page=2&limit=5` – Pagination
- `PUT /books/{book_id}/read` – Mark books as read

---

## 📄 SQL Schema (movies\_schema.sql)

```sql
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    director VARCHAR(50) NOT NULL,
    year INT NOT NULL DEFAULT 1900
);
```

---

## 📄 SQL Schema (books\_schema.sql)

```sql
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    author VARCHAR(50) NOT NULL,
    pages INT NOT NULL DEFAULT 0,
    genre VARCHAR(50),
    year INT NOT NULL DEFAULT 1900,
    is_read BOOLEAN DEFAULT FALSE
);
```

Sample Movies Inserts:

```sql
INSERT INTO movies (title, director, year) VALUES
('Anaconda', 'A.D Adward', 2018),
('Solo-Leveling', 'Robert C. Martin', 2008);
```

Sample Books Inserts:
```sql
INSERT INTO books (title, author, pages, genre, year, is_read) VALUES
('Atomic Habits', 'James Clear', 320, 'Self-help', 2018, TRUE),
('Clean Code', 'Robert C. Martin', 464, 'Programming', 2008, FALSE);
```

---

## 🔍 API Testing

- Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📝 Research Notes

Stored in [`notes.md`](notes.md):

- JSON vs SQL
- What is an ORM
- Foreign Keys
- Indexing Best Practices
- Async in Web APIs
- Path vs Query Parameters
- SQL Operations by ORM
- Connection Pooling in FastAPI

---

## 🔗 License

Educational project for learning FastAPI + SQL.

