# Import necessary libraries for:
#   building a FastAPI application, 
#   interacting with a database using SQLAlchemy, 
#   and defining data models with Pydantic.

from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import DateTime, create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Create a FastAPI application instance and configure the database connection using SQLAlchemy.
app = FastAPI()
DATABASE_URL = "sqlite:///./football_predictor.db"  # SQLite database URL for local development
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

# Define the database model

# TEAMS
class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, unique=True, index=True)
    team_name = Column(String, index=True)

# SEASONS
class Season(Base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True, index=True)
    start_year = Column(Integer, index=True)
    end_year = Column(Integer, index=True)

# SEASONS PLAYED
class SeasonPlayed(Base):
    __tablename__ = "seasons_played"
    team_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"), primary_key=True)
    season_id = Column(Integer, sqlalchemy.ForeignKey("seasons.id"), primary_key=True)

# FIXTURES
class Fixture(Base):
    __tablename__ = "fixtures"
    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, sqlalchemy.ForeignKey("seasons.id"))
    date = Column(DateTime, index=True)
    home_team_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"))
    away_team_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"))
    winner_team_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"), nullable=True)  # Nullable to allow for draws or unplayed matches
    home_goals_scored = Column(Integer, nullable=True)  # Nullable to allow for unplayed matches
    away_goals_scored = Column(Integer, nullable=True)  # Nullable to allow for unplayed matches

# HEAD TO HEADS
class HeadToHead(Base):
    __tablename__ = "head_to_heads"
    id = Column(Integer, primary_key=True, index=True)
    current_fixture_id = Column(Integer, sqlalchemy.ForeignKey("fixtures.id"))
    past_fixture_date = Column(DateTime, index=True)
    team1_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"))
    team2_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"))
    season_id = Column(Integer, sqlalchemy.ForeignKey("seasons.id"))
    winner_team_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"), nullable=True) 
    team1_goals_scored = Column(Integer, nullable=True) 
    team2_goals_scored = Column(Integer, nullable=True)

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

# TEAMS
class TeamCreate(BaseModel):
    team_id: int
    team_name: str

class TeamResponse(TeamCreate):
    id: int
    team_id: int
    team_name: str

# SEASONS
class SeasonCreate(BaseModel):
    start_year: int
    end_year: int

class SeasonResponse(SeasonCreate):
    id: int
    start_year: int
    end_year: int

# SEASONS PLAYED
class SeasonPlayedCreate(BaseModel):
    team_id: int
    season_id: int

class SeasonPlayedResponse(SeasonPlayedCreate):
    team_id: int
    season_id: int

# FIXTURES
class FixtureCreate(BaseModel):
    season_id: int
    date: datetime
    home_team_id: int
    away_team_id: int
    winner_team_id: int | None = None  # Optional field to allow for draws or unplayed matches
    home_goals_scored: int | None = None  # Optional field to allow for unplayed matches
    away_goals_scored: int | None = None

class FixtureResponse(FixtureCreate):
    id: int
    season_id: int
    date: datetime
    home_team_id: int
    away_team_id: int
    winner_team_id: int | None = None
    home_goals_scored: int | None = None
    away_goals_scored: int | None = None

# HEAD TO HEADS
class HeadToHeadCreate(BaseModel):
    current_fixture_id: int
    past_fixture_date: datetime
    team1_id: int
    team2_id: int
    season_id: int
    winner_team_id: int | None = None
    team1_goals_scored: int | None = None
    team2_goals_scored: int | None = None

class HeadToHeadResponse(HeadToHeadCreate):
    id: int
    current_fixture_id: int
    past_fixture_date: datetime
    team1_id: int
    team2_id: int
    season_id: int
    winner_team_id: int | None = None
    team1_goals_scored: int | None = None
    team2_goals_scored: int | None = None


# Define API endpoint to create a new team in the database
@app.post("/teams/", response_model=TeamResponse)
async def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    db_team = Team(**team.model_dump())  # Create a new Team instance from the request data
    db.add(db_team)  # Add the new team to the database session
    db.commit()  # Commit the changes to the database
    db.refresh(db_team)  # Refresh the instance with the committed changes
    return db_team  # Return the created team

# Define API endpoint to read a Team by ID from the database
@app.get("/teams/{team_id}", response_model=TeamResponse)
async def read_team(team_id: int, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.team_id == team_id).first()  # Query the database for the team by ID
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


# Define API endpoint to delete a Team by ID from the database
@app.delete("/teams/{team_id}", response_model=TeamResponse)
async def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.team_id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(db_team)
    db.commit()
    return db_team

# Run the FastAPI application using Uvicorn if the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)