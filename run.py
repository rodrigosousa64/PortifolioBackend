import os
from app import create_app # Importa a fábrica de dentro do seu pacote 'app'
from waitress import serve
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")



if __name__ == "__main__":
 app = create_app()   # ← cria a instância da aplicação
 port = int(os.environ.get("PORT", 7000))

 serve(app, host="0.0.0.0", port=port)
