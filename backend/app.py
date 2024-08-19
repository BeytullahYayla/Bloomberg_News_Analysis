from fastapi import FastAPI, Query, Path, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated
import uvicorn
from connect_database import engine, SessionLocal
import tables

def get_database_connection():
    """
    Dependency that provides a database session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Hagia Web Scraping")

# Allow CORS for specific origins
origins = [
    "http://localhost:4200",
    "http://localhost:8000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Ensure all tables are created
tables.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_database_connection)]

@app.get("/news/")
def get_news(db: db_dependency):
    """
    Retrieves all news records from the database.
    
    Parameters:
    -----------
    db : Session
        The database session dependency.

    Returns:
    --------
    list of tables.New
        A list of all news records.
    """
    try:
        items = db.query(tables.New).all()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while listing news: {str(e)}")

@app.get("/news_paginated/")
def get_news_paginated(db: db_dependency, limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    """
    Retrieves a paginated list of news records from the database.
    
    Parameters:
    -----------
    db : Session
        The database session dependency.
    limit : int
        The maximum number of records to retrieve.
    offset : int
        The number of records to skip before starting to retrieve.

    Returns:
    --------
    list of tables.New
        A paginated list of news records.
    """
    try:
        items = db.query(tables.New).offset(offset).limit(limit).all()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error while listing news: {str(e)}")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
