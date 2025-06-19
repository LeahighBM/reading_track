from fastapi import FastAPI, Depends
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

@app.post("/wishlist", response_model=WishlistBookModel)
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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)