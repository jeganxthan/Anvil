from app.db.database import engine
from sqlalchemy.orm import Session

session = Session(engine)