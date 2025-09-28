# Asistente de Código con IA para GitHub

Este proyecto es un asistente de software automatizado que se integra con GitHub y utiliza la API de OpenAI para realizar tareas de desarrollo, como revisiones de código y generación de documentación.

## ¿Qué hace?

El asistente funciona como un servicio web que escucha eventos de GitHub (webhooks) y actúa en consecuencia:

1.  **Revisión Automática de Pull Requests**:
    *   Cuando se crea o actualiza un Pull Request, el asistente obtiene automáticamente los cambios en el código.
    *   Envía estos cambios a un modelo de IA (GPT-4o) para un análisis detallado.
    *   Publica las sugerencias de la IA como comentarios directamente en las líneas de código correspondientes dentro del Pull Request, facilitando una revisión rápida y eficiente.

2.  **Generador de Documentación bajo Demanda**:
    *   Al publicar un comentario con el comando `/document` en cualquier Pull Request o Issue, el asistente se activa.
    *   Analiza la estructura de archivos completa del repositorio.
    *   Utiliza la IA para generar un archivo `README.md` profesional y detallado.
    *   Crea o actualiza automáticamente el `README.md` en la rama principal del repositorio.

## Cómo Ponerlo en Marcha

Sigue estos pasos para configurar y ejecutar el asistente en tu propio repositorio.

### 1. Prerrequisitos

*   Python 3.10 o superior.
*   Git.
*   Una cuenta de GitHub y una de OpenAI.
*   ngrok para exponer tu servidor local a internet.

### 2. Instalación

Primero, clona el repositorio y navega al directorio del proyecto.

```bash
# Clona tu repositorio (reemplaza la URL)
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

Se recomienda crear un entorno virtual para gestionar las dependencias.

```bash
# Crear un entorno virtual
python -m venv venv

# Activar el entorno
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

Instala las dependencias necesarias desde `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 3. Configuración de API Keys

1.  Renombra el archivo `.env.example` a `.env`.
2.  Abre el archivo `.env` y añade tus claves de API:
    *   `GITHUB_TOKEN`: Genera un **Fine-grained personal access token** en GitHub. Necesita los siguientes permisos para el repositorio que quieres que gestione:
        *   **Contents**: `Read and write`
        *   **Pull requests**: `Read and write`
        *   **Issues**: `Read and write`
    *   `OPENAI_API_KEY`: Tu clave secreta de la API de OpenAI.

### 4. Ejecución del Servidor

Inicia el servidor web FastAPI con `uvicorn`. Este comando debe ejecutarse desde la raíz del proyecto.

```bash
uvicorn src.main:app --reload
```

El servidor estará disponible localmente en `http://127.0.0.1:8000`.

### 5. Exposición con ngrok

Abre una **nueva terminal** y ejecuta `ngrok` para crear un túnel público hacia tu servidor local.

```bash
ngrok http 8000
```

Copia la URL `https` que te proporciona ngrok (ej. `https://<id-aleatorio>.ngrok-free.app`).

### 6. Configuración del Webhook en GitHub

1.  Ve a tu repositorio en GitHub y navega a **Settings > Webhooks**.
2.  Haz clic en **"Add webhook"**.
3.  **Payload URL**: Pega la URL de ngrok seguida de `/webhook`.
4.  **Content type**: Selecciona `application/json`.
5.  **Secret**: (Opcional, pero recomendado) Añade una clave secreta para asegurar tus webhooks.
6.  **Which events would you like to trigger this webhook?**:
    *   Selecciona "Let me select individual events".
    *   Marca las casillas **"Pull requests"** y **"Issue comments"**.
7.  Haz clic en **"Add webhook"**.

¡Listo! Tu asistente está configurado. Ahora puedes probar su funcionalidad creando un Pull Request o usando el comando `/document`.