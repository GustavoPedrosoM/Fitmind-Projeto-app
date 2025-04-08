from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = "sua_chave_super_secreta"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nome_usuario: str = payload.get("sub")
        if nome_usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return nome_usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
