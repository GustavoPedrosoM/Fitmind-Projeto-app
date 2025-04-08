from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models.usuarios import Usuario
from app.schemas.auth_schemas import LoginRequest, TokenResponse

router = APIRouter()

SECRET_KEY = "sua_chave_secreta_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.nome_usuario == login_data.nome_usuario).first()
    if not usuario or usuario.senha != login_data.senha:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    
    token = create_access_token({"sub": usuario.nome_usuario})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.nome_usuario == username).first()
    if user is None:
        raise credentials_exception

    return user
