from fastapi import APIRouter, Depends
from app.auth.auth_dependencies import verificar_token

router = APIRouter()

@router.get("/protegido")
def rota_protegida(usuario: str = Depends(verificar_token)):
    return {"mensagem": f"Bem-vindo, {usuario}! Você acessou uma rota protegida."}
