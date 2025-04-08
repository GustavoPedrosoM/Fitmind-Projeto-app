from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome_usuario: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome_usuario: str

    model_config = {
        "from_attributes": True
    }
