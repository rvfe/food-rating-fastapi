from fastapi import FastAPI
from .routers import user, recipe, auth, rating
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipe.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(rating.router)

@app.get("/")
def root():
    return {"mensagem": "Opa!"}
