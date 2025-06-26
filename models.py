from sqlalchemy import Column, Integer, String, Float
from db_config import Base

class ProductReview(Base):
    __tablename__ = "product_reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    product_name = Column(String)
    review = Column(String)
    sentiment = Column(String)
    polarity = Column(Float)
    sales = Column(Integer)
    region = Column(String)
