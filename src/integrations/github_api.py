from github import Github, GithubException

class GitHubAPI:
    """Cliente para interactuar con la API de GitHub."""

    def __init__(self, token: str):
        if not token:
            raise ValueError("El token de GitHub no puede estar vacío.")
        self.client = Github(token)

    def get_pr_diff(self, repo_name: str, pr_number: int) -> str:
        """
        Obtiene los cambios (diff) de un Pull Request específico.

        Args:
            repo_name: El nombre del repositorio (ej. 'owner/repo').
            pr_number: El número del Pull Request.

        Returns:
            Una cadena de texto con el diff del PR.
        """
        try:
            repo = self.client.get_repo(repo_name)
            pull_request = repo.get_pull(pr_number)
            
            # Itera sobre todos los archivos en el PR para construir el diff completo.
            full_diff = []
            for file in pull_request.get_files():
                # El atributo 'patch' contiene el diff del archivo.
                if file.patch:
                    full_diff.append(f"--- a/{file.filename}\n+++ b/{file.filename}\n{file.patch}")
            
            return "\n".join(full_diff)
        except GithubException as e:
            print(f"Error al obtener el PR de GitHub: {e}")
            return ""

    def post_review_comment(self, repo_name: str, pr_number: int, comment: str):
        """
        Publica un comentario en un Pull Request.

        Args:
            repo_name: El nombre del repositorio (ej. 'owner/repo').
            pr_number: El número del Pull Request.
            comment: El texto del comentario a publicar.
        """
        try:
            repo = self.client.get_repo(repo_name)
            pull_request = repo.get_pull(pr_number)
            pull_request.create_issue_comment(comment)
            print(f"Comentario publicado exitosamente en el PR #{pr_number}.")
        except GithubException as e:
            print(f"Error al publicar el comentario en GitHub: {e}")

    def post_line_by_line_review(self, repo_name: str, pr_number: int, comments: list[dict]):
        """
        Publica una revisión completa con comentarios en líneas específicas.

        Args:
            repo_name: El nombre del repositorio.
            pr_number: El número del Pull Request.
            comments: Una lista de comentarios, cada uno un dict con 'file_path', 'line_number', 'comment'.
        """
        try:
            repo = self.client.get_repo(repo_name)
            pull_request = repo.get_pull(pr_number)

            review_comments = []
            for comment in comments:
                review_comments.append({
                    "path": comment["file_path"],
                    "body": comment["comment"],
                    "position": comment["line_number"] # La IA nos da la posición en el diff
                })
            
            pull_request.create_review(body="Revisión automática completada por el asistente de IA.", comments=review_comments)
            print(f"Revisión por línea publicada exitosamente en el PR #{pr_number}.")
        except GithubException as e:
            print(f"Error al publicar la revisión por línea en GitHub: {e}")

    def get_repo_file_tree(self, repo_name: str) -> list[str]:
        """
        Obtiene una lista de las rutas de todos los archivos en la rama principal.
        """
        try:
            repo = self.client.get_repo(repo_name)
            tree = repo.get_git_tree(repo.default_branch, recursive=True).tree
            # Filtramos solo los archivos (type='blob')
            return [element.path for element in tree if element.type == 'blob']
        except GithubException as e:
            print(f"Error al obtener el árbol de archivos de GitHub: {e}")
            return []

    def update_readme(self, repo_name: str, content: str):
        """
        Crea o actualiza el archivo README.md en la rama principal.
        """
        try:
            repo = self.client.get_repo(repo_name)
            readme_path = "README.md"
            commit_message = "docs: Generar README.md con asistente de IA"

            try:
                # Intenta obtener el archivo para ver si existe
                file = repo.get_contents(readme_path, ref=repo.default_branch)
                # Si existe, lo actualiza
                repo.update_file(file.path, commit_message, content, file.sha, branch=repo.default_branch)
                print("README.md actualizado exitosamente.")
            except GithubException as e:
                if e.status == 404:
                    # Si no existe (404), lo crea
                    repo.create_file(readme_path, commit_message, content, branch=repo.default_branch)
                    print("README.md creado exitosamente.")
                else:
                    raise e
        except GithubException as e:
            print(f"Error al actualizar/crear README.md: {e}")