from fastapi import FastAPI
from app.database import Base, engine
from app.routes import usuarios, auth_routes, protected_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticação"])
app.include_router(protected_routes.router, prefix="/protegido", tags=["Protegido"])
