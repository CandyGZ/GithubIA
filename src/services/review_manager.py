from ..integrations.github_api import GitHubAPI
from ..integrations.openai_api import OpenAIAPI
import asyncio

class ReviewManager:
    """Orquesta el proceso de revisión de código."""

    def __init__(self, github_client: GitHubAPI, openai_client: OpenAIAPI):
        self.github_client = github_client
        self.openai_client = openai_client

    async def review_pull_request(self, repo_name: str, pr_number: int):
        """
        Realiza una revisión completa de un Pull Request.
        Esta es una corutina para ser ejecutada en segundo plano.
        """
        def _blocking_io_task():
            """Función interna para agrupar todas las operaciones bloqueantes."""
            print(f"Iniciando revisión para el PR #{pr_number} en el repositorio {repo_name}...")
            
            # 1. Obtener el diff del PR desde GitHub
            diff = self.github_client.get_pr_diff(repo_name, pr_number)
            if not diff:
                print(f"No se pudo obtener el diff para el PR #{pr_number}. Abortando revisión.")
                return
            
            # 2. Enviar el diff a OpenAI para su análisis
            line_comments = self.openai_client.get_code_review(diff)
            
            if not line_comments:
                print("La IA no generó sugerencias. No se publicará ninguna revisión.")
                return
            
            # 3. Publicar la revisión como un comentario en el PR
            self.github_client.post_line_by_line_review(repo_name, pr_number, line_comments)

        # Ejecuta la función bloqueante en un hilo separado para no congelar el servidor.
        await asyncio.to_thread(_blocking_io_task)