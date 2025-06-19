from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated, List
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import uvicorn
import models

app = FastAPI()

origins = ["http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"], # well the react app works now, but this is not safe 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

class WishlistBookBase(BaseModel):
    title: str
    author: str
    date_added: str
    already_own: bool

class WishlistBookModel(WishlistBookBase):
    id: int

    class Config:
        orm_mode = True

class CompleteBookBase(BaseModel):
    title: str
    author: str
    num_pages: int
    date_started: str
    date_completed: str

class CompleteBookModel(CompleteBookBase):
    id: int

    class Config:
        orm_mode = True

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

db_dependency = Annotated[Session, Depends(get_database)]
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/wishlist", response_model=WishlistBookModel, status_code=201)
async def add_to_wishlist(wishlist_book: WishlistBookBase, db: db_dependency):
    wishlist = models.Wishlist(**wishlist_book.model_dump())
    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)

    return wishlist

@app.get("/wishlist")
async def get_wish_list(db: db_dependency, skip: int = 0, limit = 100):
    wishlist = db.query(models.Wishlist).offset(skip).limit(limit).all()
    return wishlist

@app.get("/wishlist/{book_id}")
async def get_wish_list_item(book_id, db: db_dependency):
    book = db.query(models.Wishlist).get(book_id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail=f"Book ID {book_id} not found.")
    
@app.put("/wishlist/{book_id}", response_model=WishlistBookModel)
async def edit_wish_list_item(book_id, book_dict:WishlistBookBase, db: db_dependency):
    book = db.query(models.Wishlist).filter(models.Wishlist.id == book_id).first()

    if book:
        for k, v in book_dict.model_dump(exclude_unset=True).items():
            setattr(book, k, v)

        db.add(book)
        db.commit()
        db.refresh(book)

        return book
    
    else:
        raise HTTPException(status_code=404, detail="Book not found.")

@app.delete("/wishlist/{book_id}", status_code=204)
async def delete_wish_list_item(book_id, db: db_dependency):
    book = db.query(models.Wishlist).filter(models.Wishlist.id==book_id).first()
    if book:
        db.delete(book)
        db.commit() 
    else:
        raise HTTPException(status_code=404, detail=f"Book ID {book_id} not found")
    

@app.post("/completed-books", response_model=CompleteBookModel, status_code=201)
async def add_completed_book(completed_book: CompleteBookBase, db: db_dependency):
    completed = models.Completed(**completed_book.model_dump())

    db.add(completed)
    db.commit()
    db.refresh(completed)

    return completed

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)