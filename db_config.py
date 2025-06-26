from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Using SQLite for simplicity
DATABASE_URL = "sqlite:///product_reviews.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    from models import ProductReview
    Base.metadata.create_all(bind=engine)
