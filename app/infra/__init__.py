

from .database import SessionLocal, engine

# Exporta os principais componentes para facilitar imports
__all__ = [
    'SessionLocal',
    'engine', 
    'Base',
    # Adicione outros componentes que queira exportar
]

# Inicialização do pacote (opcional)
print("Infra package initialized") 



