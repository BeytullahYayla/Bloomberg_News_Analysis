from fastapi import FastAPI,Query,Path
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from connect_database import engine, SessionLocal
from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
import tables
from models import *
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import tables
import uvicorn
from constants import *

def get_database_connection():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

app=FastAPI(title="Hagia Web Scapping")
    
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

tables.Base.metadata.create_all(bind=engine)
    
db_dependency = Annotated[Session, Depends(get_database_connection)]


# GET fonksiyonu
@app.get("/news/")
def get_news(db: Session = Depends(get_database_connection)):
    
    try:
        items = db.query(tables.New).all()
    except AttributeError:
        raise HTTPException("There is an error occurred while listing news")

    return items
# GET function with pagination
@app.get("/news_paginated/")
def get_news(db: Session = Depends(get_database_connection), limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    try:
        # Querying the database with limit and offset for pagination
        items = db.query(tables.New).offset(offset).limit(limit).all()
    except AttributeError:
        raise HTTPException(status_code=500, detail="There was an error while listing news")
    
    return items
        

        
if __name__=='__main__':
    uvicorn.run(app,host="127.0.0.1",port=8000)