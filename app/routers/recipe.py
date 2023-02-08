from app import oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas

router = APIRouter(
    prefix='/receitas',
    tags=['Receitas']
)

@router.get("/",response_model= List[schemas.RecipesCustom])
def get_recipes(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit: int=10, skip: int = 0, search: Optional[str] = ""):
    results = db.query(models.Recipe, func.count(models.Rating.recipe_id).label("rating_votes"),func.round(func.avg(models.Rating.rating),2).label('rating_average')).join(models.Rating,models.Rating.recipe_id == models.Recipe.id, isouter=True).group_by(models.Recipe.id).all()

    return results

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Recipe)
def create_recipes(recipe: schemas.RecipeCreate, db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    new_recipe = models.Recipe(owner_id = current_user.id,**recipe.dict())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


@router.get("/{id}",response_model=schemas.RecipesCustom)
def  get_recipe(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    recipe = db.query(models.Recipe, func.count(models.Rating.recipe_id).label("rating_votes"),func.round(func.avg(models.Rating.rating),2).label('rating_average')).join(models.Rating,models.Rating.recipe_id == models.Recipe.id, isouter=True).group_by(models.Recipe.id).filter(models.Recipe.id == id).first()

    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"receita com id: {id} não foi encontrada!")
    return recipe


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),):
    recipe_query = db.query(models.Recipe).filter(models.Recipe.id == id, models.Recipe.owner_id == current_user.id)
    deleted_recipe = recipe_query.first()

    if deleted_recipe == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Receita não encontrada")
    if deleted_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Receita pertence à outro usuário. Só pode ser atualizada pelo criador")

    recipe_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}", response_model=schemas.Recipe)
def update_recipe(id:int,updated_recipe: schemas.RecipeCreate,  db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    recipe_query = db.query(models.Recipe).filter(models.Recipe.id == id, models.Recipe.owner_id == current_user.id)
    recipe_rs = recipe_query.first()

    if recipe_rs == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Receita não existe ou pertence a outro usuário")
    if recipe_rs.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Receita pertence à outro usuário. Só pode ser atualizada pelo criador")

    recipe_query.update(updated_recipe.dict(), synchronize_session=False)
    db.commit()
    return recipe_query.first()