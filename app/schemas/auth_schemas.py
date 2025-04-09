from pydantic import BaseModel

class RegisterRequest(BaseModel):
    nome_usuario: str
    senha: str

class LoginRequest(BaseModel):
    nome_usuario: str
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

