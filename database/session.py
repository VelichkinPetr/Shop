from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test_database.db')
session = sessionmaker(bind=engine)

async def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()