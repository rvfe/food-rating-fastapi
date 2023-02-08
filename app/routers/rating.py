from app import oauth2
from ..database import get_db
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, database

router = APIRouter(
    prefix = '/avaliacoes',
    tags = ['Avaliações']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def rating(rating: schemas.Rating, db: Session = Depends(database.get_db), current_user : int = Depends(oauth2.get_current_user)):
    print(rating)
    recipe = db.query(models.Recipe).filter(models.Recipe.id == rating.recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'A receita com id {rating.recipe_id} não existe!')

    rating_query = db.query(models.Rating).filter(models.Rating.recipe_id == rating.recipe_id, models.Rating.user_id == current_user.id)
    rating_exists = rating_query.first()
    print(rating.rating)
    if 1 <= rating.rating <= 5:
        if rating_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"O usuário {current_user.id} já avaliou essa receita({rating.recipe_id})!")
        new_rating = models.Rating(recipe_id=rating.recipe_id, user_id=current_user.id, rating=rating.rating)
        print(new_rating)
        db.add(new_rating)
        db.commit()
        return {"message": "Avaliação salva com sucesso!"}
    else:
        if not rating_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Esta avaliação não existe ou pertence a outro usuário!')
        
        rating_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Deletado com sucesso!"}