from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, Numeric, String
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    name = Column(String, nullable=False, unique=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Rating(Base):
    __tablename__ = "ratings"

    # id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key = True)
    recipe_id = Column(Integer, ForeignKey("recipes.id",ondelete="CASCADE"), primary_key = True)
    rating = Column(Numeric(precision=3, scale=2),nullable=True)
