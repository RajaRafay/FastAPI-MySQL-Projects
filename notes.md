# 📓 Research Notes: FastAPI + SQL Project

## 1. What is the difference between JSON files and SQL databases?

- **JSON files** store data in a plain text, key-value format, useful for simple or small applications.
- **SQL databases** store structured data in tables with relationships, indexes, and constraints.
- SQL databases offer better performance, integrity, and querying capabilities for large-scale or multi-user applications.

## 2. What is an ORM, and why is it useful?

- ORM stands for **Object-Relational Mapping**.
- It allows developers to interact with the database using Python classes instead of raw SQL queries.
- ORMs improve productivity, reduce boilerplate code, and make code easier to maintain and debug.

## 3. How do foreign keys work in SQL?

- A **foreign key** is a column that creates a relationship between two tables.
- It references the primary key of another table.
- Ensures **referential integrity**: data in one table must correspond to data in another.

## 4. What are best practices for database indexing?

- Use indexes on columns frequently used in `WHERE`, `JOIN`, or `ORDER BY` clauses.
- Don’t over-index: too many indexes slow down inserts/updates.
- Use **composite indexes** when filtering by multiple columns.
- Always index **foreign keys**.

## 5. Why is async important in modern web APIs?

- Async enables **non-blocking** I/O operations.
- It helps handle many requests efficiently, especially during database or network delays.
- In FastAPI, async routes allow better performance for high-concurrency apps.

## 6. What are Query Parameters vs Path Parameters?

- **Path Parameters** are part of the URL path (e.g., `/books/5` → id=5).
- **Query Parameters** appear after `?` in the URL (e.g., `/books/search?author=xyz`).
- Use path params for specific resources and query params for filtering or searching.

## 7. What SQL operations are used under the hood by ORM libraries?

ORM libraries use SQL operations like:

- `SELECT` – for reading data
- `INSERT INTO` – for adding records
- `UPDATE` – for modifying records
- `DELETE` – for removing records
- `JOIN`, `WHERE`, `ORDER BY`, etc. – for advanced queries ORMs translate Python method calls into optimized SQL queries.

## 8. How does FastAPI support connection pooling with databases?

- FastAPI can use **SQLAlchemy** with `SessionLocal()` and connection pooling features.
- Pooling keeps a set of active DB connections ready for reuse, improving performance.
- The engine configuration (via `create_engine`) controls pooling size, timeout, etc.

Example:

```python
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
```

