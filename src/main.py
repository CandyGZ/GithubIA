from fastapi import FastAPI, Request, HTTPException
from .config import Config
from .integrations.github_api import GitHubAPI
from .integrations.openai_api import OpenAIAPI
from .services.review_manager import ReviewManager
from .services.doc_generator import DocGenerator
import asyncio

# --- Inicialización de la Aplicación y Clientes ---
# Se inicializan una sola vez cuando la aplicación arranca
app = FastAPI()

github_client = GitHubAPI(token=Config.GITHUB_TOKEN)
openai_client = OpenAIAPI(api_key=Config.OPENAI_API_KEY)
review_manager = ReviewManager(github_client, openai_client)
doc_generator = DocGenerator(github_client, openai_client)


@app.post("/webhook")
async def github_webhook(request: Request):
    """
    Endpoint que recibe notificaciones (webhooks) de GitHub.
    """
    payload = await request.json()

    # Verificamos si el evento es un Pull Request abierto o actualizado
    action = payload.get("action")
    if "pull_request" in payload and action in ["opened", "synchronize"]:
        repo_name = payload["repository"]["full_name"]
        pr_number = payload["pull_request"]["number"]
        
        print(f"Webhook recibido para PR #{pr_number} en {repo_name} (Acción: {action})")
        
        # Ejecutamos la revisión en segundo plano para no bloquear la respuesta a GitHub
        asyncio.create_task(review_manager.review_pull_request(repo_name, pr_number))
        
        return {"status": "Revisión de PR iniciada"}

    # Verificamos si el evento es un comentario con el comando /document
    if "comment" in payload and payload.get("action") == "created":
        comment_body = payload.get("comment", {}).get("body", "").strip()
        if comment_body == "/document":
            repo_name = payload["repository"]["full_name"]
            print(f"Comando '/document' recibido para el repositorio {repo_name}")

            asyncio.create_task(doc_generator.generate_project_readme(repo_name))

            return {"status": "Generación de documentación iniciada"}

    return {"status": "Evento no procesado"}

@app.get("/")
def read_root():
    return {"message": "El asistente de revisión de código está en línea."}