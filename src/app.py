from src.config import Config
from src.integrations.github_api import GitHubAPI
from src.integrations.openai_api import OpenAIAPI
from src.services.review_manager import ReviewManager

def main():
    """Punto de entrada principal de la aplicación."""
    
    # Inicializar clientes con las claves de configuración
    github_client = GitHubAPI(token=Config.GITHUB_TOKEN)
    openai_client = OpenAIAPI(api_key=Config.OPENAI_API_KEY)
    
    # Inicializar el gestor de revisiones
    review_manager = ReviewManager(github_client, openai_client)
    
    # --- Ejemplo de uso ---
    # Reemplaza con un repositorio y PR reales para probar
    repo_name = "CandyGZ/ShapeCalculator" # Debe ser una cadena "owner/repo"
    pr_number = 1  # Número de identificación único del Pull Request con el que comienza el conteo

    
    review_manager.review_pull_request(repo_name, pr_number)

if __name__ == "__main__":
    main()