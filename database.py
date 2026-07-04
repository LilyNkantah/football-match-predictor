# Import necessary libraries for:
#   building a FastAPI application, 
#   interacting with a database using SQLAlchemy, 
#   and defining data models with Pydantic.

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Create a FastAPI application instance and configure the database connection using SQLAlchemy.
app = FastAPI()
DATABASE_URL = "sqlite:///./test.db"  # SQLite database URL for local development
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

# Define the database model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Define dependency to get a database session - gives db session to be used and ensures it is closed after use.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define Pydantic models for request and response data validation
class ItemCreate(BaseModel):
    name: str
    description: str

class ItemResponse(ItemCreate):
    id: int
    name: str
    description: str

# Define API endpoint to create a new item in the database
@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())  # Create a new Item instance from the request data
    db.add(db_item)  # Add the new item to the database session
    db.commit()  # Commit the changes to the database
    db.refresh(db_item)  # Refresh the instance with the committed changes
    return db_item  # Return the created item

# Define API endpoint to read an Item by ID from the database
@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()  # Query the database for the item by ID
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item 

# Run the FastAPI application using Uvicorn if the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)