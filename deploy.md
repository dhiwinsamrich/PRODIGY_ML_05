# Deployment Guide for Food Calorie Prediction App

This guide provides instructions for deploying the Food Calorie Prediction Streamlit application to various cloud platforms.

## Prerequisites

Before you begin, ensure you have the following:

*   A Git repository (e.g., GitHub, GitLab, Bitbucket) with your project code pushed.
*   Accounts on the respective cloud platforms you intend to use.
*   Docker installed locally if you plan to use Docker-based deployments.

## Project Structure for Deployment

Ensure your project includes the following files, which were created in previous steps:

*   `App.py`: Your main Streamlit application file.
*   `requirements.txt`: Lists all Python dependencies.
*   `Model.h5`: Your trained machine learning model.
*   `Dockerfile`: Defines the Docker image for your application.
*   `netlify.toml` (Optional, for Netlify): Netlify-specific configuration.

## Option 1: Deploying to Netlify (Using Docker)

Netlify can deploy services from Docker images. We've already configured this.

**Steps:**

1.  **Push your code to a Git provider** (GitHub, GitLab, Bitbucket).
    Make sure `Dockerfile` and `netlify.toml` are in the root of your repository.

2.  **Sign up or Log in to Netlify.**

3.  **Create a new site from Git:**
    *   Click on "Add new site" -> "Import an existing project".
    *   Connect to your Git provider and select your repository.

4.  **Configure Build Settings (Netlify should pick this up from `netlify.toml`):
    *   Netlify will use the `netlify.toml` file for build commands and publish directory. The current `netlify.toml` is set up to build and run your Docker container.
    *   The command in `netlify.toml` is: `docker build -t prodigy-ml-05 . && docker run -d -p 8501:8501 prodigy-ml-05`
    *   The publish directory is set to `.` (root), as Netlify will serve the app from the running Docker container.

5.  **Deploy your site.**
    Netlify will build the Docker image and deploy your Streamlit application. You'll get a URL once the deployment is successful.

**Note on `netlify.toml`:**
The `netlify.toml` provided earlier includes a basic setup:
```toml
[build]
  command = "docker build -t prodigy-ml-05 . && docker run -d -p 8501:8501 prodigy-ml-05"
  publish = "."

[[plugins]]
  package = "@netlify/plugin-functions-core"

[[redirects]]
  from = "/*"
  to = "/.netlify/functions/server"
  status = 200

[functions]
  directory = "netlify/functions"
  node_bundler = "esbuild"
  included_files = ["!node_modules/**"]
```
This configuration tells Netlify to build a Docker image named `prodigy-ml-05` and then run it, exposing port 8501. The redirects and functions part might be more relevant if you were serving a static site with serverless functions, but for a pure Docker deployment, the `[build]` section is key.

## Option 2: Deploying with Docker on Other Platforms (Heroku, AWS, Google Cloud, Azure)

Most modern cloud platforms support deploying Docker containers. The general steps are similar:

1.  **Build your Docker Image:**
    ```bash
    docker build -t your-image-name:latest .
    ```

2.  **Push your Docker Image to a Container Registry:**
    *   **Docker Hub:** `docker push your-dockerhub-username/your-image-name:latest`
    *   **AWS ECR (Elastic Container Registry):** Follow AWS ECR instructions to create a repository and push your image.
    *   **Google Container Registry (GCR):** Follow Google Cloud instructions to push your image.
    *   **Azure Container Registry (ACR):** Follow Azure instructions to push your image.

3.  **Deploy the Image on the Cloud Platform:**

    *   **Heroku:**
        *   Log in to Heroku: `heroku login`
        *   Log in to Heroku Container Registry: `heroku container:login`
        *   Push your image: `heroku container:push web -a your-heroku-app-name`
        *   Release the image: `heroku container:release web -a your-heroku-app-name`
        *   Ensure your `Dockerfile` exposes the correct port (8501 for Streamlit) and uses `CMD ["streamlit", "run", "App.py"]`.

    *   **AWS (e.g., using Elastic Beanstalk, ECS, or App Runner):**
        *   **AWS App Runner:** This is often the simplest for containerized web apps. Point App Runner to your image in ECR.
        *   **AWS Elastic Beanstalk:** Create an application and environment, choosing Docker as the platform. You can upload your `Dockerfile` or a `Dockerrun.aws.json` file, or point to an image in ECR.
        *   **AWS ECS (Elastic Container Service):** More control, but more complex. Define a task definition with your container image and run it as a service.

    *   **Google Cloud (e.g., using Cloud Run, GKE, or App Engine Flex):**
        *   **Google Cloud Run:** Ideal for stateless containers. Deploy directly from an image in GCR. Configure the port to 8501.
        *   **Google Kubernetes Engine (GKE):** For more complex, orchestrated deployments.
        *   **App Engine Flexible Environment:** Define a `app.yaml` that specifies a custom runtime with your Docker image.

    *   **Azure (e.g., using Azure App Service, Azure Kubernetes Service, or Azure Container Instances):**
        *   **Azure App Service for Containers:** Deploy web apps using Docker containers. Point it to your image in ACR.
        *   **Azure Container Instances (ACI):** A simple way to run a Docker container without orchestration.
        *   **Azure Kubernetes Service (AKS):** For full Kubernetes orchestration.

**General Docker Deployment Considerations:**

*   **Port Mapping:** Ensure the platform maps an external port (usually 80 or 443 for HTTP/S) to your container's exposed port (8501 for Streamlit).
*   **Environment Variables:** Configure any necessary environment variables on the platform.
*   **Model File:** Your `Model.h5` is copied into the Docker image by the `COPY . .` command in the `Dockerfile`. Ensure it's not too large for the platform's limits or consider loading it from cloud storage if it's very big.
*   **Persistent Storage:** Streamlit apps that save files (like the `upload_images` directory in your `App.py`) will lose those files if the container restarts, as Docker containers are typically stateless. For persistent storage, you'd need to integrate with platform-specific storage solutions (e.g., AWS S3, Google Cloud Storage, Azure Blob Storage) or mount persistent volumes if the platform supports it.

## Option 3: Platform-Specific Python Deployments (Without Docker, if applicable)

Some platforms allow direct Python app deployments. However, for apps with specific dependencies and ML models, Docker is often more reliable.

*   **Heroku (using Python buildpack):**
    *   Create a `Procfile`: `web: streamlit run App.py`
    *   Ensure `requirements.txt` is accurate.
    *   `git push heroku main`
    *   This might require additional system-level dependencies for TensorFlow/Keras, which can be harder to manage without Docker.

*   **Google App Engine Standard (Python):**
    *   Requires an `app.yaml` file.
    *   May have limitations on native C libraries, which can be an issue for some ML packages. App Engine Flexible (with Docker) is often preferred for ML apps.

## Final Checks and Troubleshooting

*   **Logs:** Always check the deployment logs on your chosen platform for errors.
*   **Dependencies:** Double-check that all necessary packages are in `requirements.txt`.
*   **Model Path:** Ensure `App.py` correctly loads `Model.h5` (e.g., `model = load_model('Model.h5')`). The `Dockerfile` copies it to the working directory.
*   **Resource Limits:** Be mindful of memory and CPU limits on free or lower-tier plans, especially for ML models.

This guide provides a starting point. Always refer to the official documentation of the cloud platform you choose for the most up-to-date and detailed instructions. Good luck!