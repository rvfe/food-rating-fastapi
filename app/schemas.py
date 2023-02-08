from datetime import datetime
from pickletools import float8
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint

class UserBase(BaseModel):
    email:EmailStr
    password:str
    name:str

class UserCreate(UserBase):
    pass

class UserCustom(BaseModel):
    id: int
    email:EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class RecipeBase(BaseModel):
    title: str
    content: str
    # owner_id: int

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    title: str
    content: str
    created_at: datetime
    owner_id: int
    owner: UserCustom
    
    class Config:
        orm_mode = True

class Rating(BaseModel):
    recipe_id: int
    rating: conint(le=5)

class RecipesCustom(BaseModel):
    Recipe: Recipe
    rating_votes: int
    rating_average: Optional[float] = None

    class Config:
        orm_mode = True

class Upvotes(BaseModel):
    recipe_id: int
    user_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

