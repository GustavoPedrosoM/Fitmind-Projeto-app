from fastapi import FastAPI
from app.database import Base, engine
from app.routes import usuarios, auth_routes, protected_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ou ["*"] para testes abertos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticação"])
app.include_router(protected_routes.router, prefix="/protegido", tags=["Protegido"])
