# GEMINI.md

## Project Overview

This project is a Gemini API proxy built with FastAPI. It provides a simple, secure, and configurable way to access Google's Gemini models. The proxy supports API key rotation, model listing, and chat completion interfaces that are compatible with the OpenAI API format. This allows it to be integrated with tools that expect an OpenAI-compatible backend. The project also includes two Vue.js frontends for configuration and interaction.

The application is designed to be deployed on platforms like Hugging Face Spaces, Claw Cloud, and Render, and it can also be run locally or in a Docker container.

## Building and Running

### Local Development

To run the project locally, follow these steps:

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure the application:**
    Create a `.env` file in the root directory and set the required environment variables. The most important one is `GEMINI_API_KEYS`. You can find all available configuration options in `app/config/settings.py`.

3.  **Run the application:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 7860
    ```

The application will be available at `http://localhost:7860`.

### Docker

The project includes a `Dockerfile` for building a container image. The CI/CD pipeline in `.github/workflows/main.yml` automatically builds and pushes the image to the GitHub Container Registry.

To build the Docker image locally:

```bash
docker build -t hajimi .
```

To run the Docker container:

```bash
docker run -p 7860:7860 -e GEMINI_API_KEYS="your_api_keys" hajimi
```

## Development Conventions

*   **Configuration:** The application is configured using environment variables. A comprehensive list of these variables can be found in `app/config/settings.py`.
*   **Backend:** The backend is built with Python and FastAPI. The main application logic is in `app/main.py`, and the API routes are defined in `app/api/routes.py`.
*   **Frontend:** The project has two frontends, `hajimiUI` and `page`, both built with Vue.js. The source code for these is in the `hajimiUI` and `page` directories, respectively.
*   **CI/CD:** The project uses GitHub Actions for CI/CD. The workflow in `.github/workflows/main.yml` builds and pushes a Docker image to the GitHub Container Registry on every push to the `main` branch.
*   **Documentation:** The `wiki` directory contains documentation for deployment, troubleshooting, and other aspects of the project.
