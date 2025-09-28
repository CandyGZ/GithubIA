import openai
import json

class OpenAIAPI:
    """Cliente para interactuar con la API de OpenAI."""

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("La clave de API de OpenAI no puede estar vacía.")
        openai.api_key = api_key

    def get_code_review(self, diff: str) -> list[dict]:
        """
        Envía un diff de código a OpenAI para obtener una revisión.

        Args:
            diff: Una cadena de texto con los cambios de código.

        Returns:
            Una lista de diccionarios, donde cada uno es un comentario de revisión.
        """
        prompt = f"""
        Actúa como un revisor de código senior. Revisa los siguientes cambios de código (diff) y proporciona sugerencias de mejora.
        Devuelve tus sugerencias en un formato JSON. El JSON debe ser una lista de objetos, donde cada objeto representa un comentario y tiene las siguientes claves:
        - "file_path": (string) La ruta del archivo que se está comentando.
        - "line_number": (integer) El número de línea dentro del diff donde se debe colocar el comentario.
        - "comment": (string) El texto del comentario de revisión.

        Si no tienes sugerencias, devuelve una lista vacía [].

        Ejemplo de respuesta JSON:
        [
          {{
            "file_path": "src/main.py",
            "line_number": 15,
            "comment": "Considera usar una variable de entorno para este valor en lugar de tenerlo hardcodeado."
          }}
        ]

        Cambios de código (diff):
        {diff}
        """
        response = openai.chat.completions.create(
            model="gpt-5-nano", # Usamos un modelo con mejor soporte para JSON
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            # El modelo puede devolver el JSON dentro de una clave, ej. {"comments": [...]}.
            # Buscamos la primera lista que encontremos en el JSON.
            json_response = json.loads(response.choices[0].message.content)
            for value in json_response.values():
                if isinstance(value, list):
                    return value
            return [] # Si no se encuentra una lista
        except (json.JSONDecodeError, IndexError):
            return []

    def get_documentation(self, file_tree: list[str]) -> str:
        """
        Genera un archivo README.md a partir de la estructura de archivos de un proyecto.

        Args:
            file_tree: Una lista de rutas de archivo del proyecto.

        Returns:
            El contenido del README.md generado en formato Markdown.
        """
        file_list = "\n".join(f"- `{path}`" for path in file_tree)
        prompt = f"""
        Actúa como un desarrollador de software escribiendo la documentación para un nuevo proyecto.
        Basado en la siguiente estructura de archivos, genera un archivo README.md completo y profesional en formato Markdown.
        El README debe incluir secciones como: "Acerca del Proyecto", "Estructura de Archivos", "Cómo Empezar" (con instrucciones genéricas de instalación y ejecución), y "Uso".

        Estructura de archivos del proyecto:
        {file_list}
        """
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content