from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioResponse
from app.auth.auth_handler import get_current_user
from app.auth.auth_bearer import JWTBearer


router = APIRouter(prefix="/usuarios", tags=["Usuários"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.nome_usuario == usuario.nome_usuario).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    novo_usuario = Usuario(**usuario.dict())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/me", dependencies=[Depends(JWTBearer())])
def get_usuario_logado(current_user: Usuario = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "nome_usuario": current_user.nome_usuario
    }
