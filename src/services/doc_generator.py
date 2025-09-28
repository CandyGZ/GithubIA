from ..integrations.github_api import GitHubAPI
from ..integrations.openai_api import OpenAIAPI
import asyncio

class DocGenerator:
    """Orquesta la generación de documentación."""

    def __init__(self, github_client: GitHubAPI, openai_client: OpenAIAPI):
        self.github_client = github_client
        self.openai_client = openai_client

    async def generate_project_readme(self, repo_name: str):
        """
        Genera y publica un README.md para todo el proyecto.
        """
        def _blocking_io_task():
            print(f"Iniciando generación de README para el repositorio {repo_name}...")
            
            # 1. Obtener la estructura de archivos del repositorio
            file_tree = self.github_client.get_repo_file_tree(repo_name)
            
            # 2. Enviar la estructura a OpenAI para generar el README
            readme_content = self.openai_client.get_documentation(file_tree)
            
            # 3. Publicar el nuevo README.md en el repositorio
            self.github_client.update_readme(repo_name, readme_content)

        await asyncio.to_thread(_blocking_io_task)