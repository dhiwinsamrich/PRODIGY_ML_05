# Deployment Guide for Food Calorie Prediction App on Render

This guide provides detailed instructions for deploying the Food Calorie Prediction Streamlit application and its associated Flask API to Render using Docker and the `render.yaml` blueprint.

## Prerequisites

Before you begin, ensure you have the following:

*   A Git repository (e.g., GitHub, GitLab, Bitbucket) with your project code pushed. This repository should include:
    *   `App.py`: Your main Streamlit application file.
    *   `ec2_api.py`: Your Flask API file.
    *   `requirements.txt`: Lists all Python dependencies (including `streamlit`, `flask`, `gunicorn`, `tensorflow`, `keras`, etc.).
    *   `Model.h5`: Your trained machine learning model.
    *   `Dockerfile`: Defines the Docker image for your application.
    *   `render.yaml`: The Render blueprint configuration file.
    *   `keep_alive.py` (Optional): Script to keep free-tier services active.
*   A Render account ([https://render.com/](https://render.com/)).
*   Docker installed locally if you wish to test the Docker build locally first.

## Project Structure for Render Deployment

Your project root directory should ideally look like this for Render deployment:

```
FoodCalorie/
├── App.py
├── Dockerfile
├── Food_Classification.py
├── LICENSE
├── Model.h5
├── README.md
├── Scripts/                 # (Virtual environment, not deployed)
├── deploy.md                # (This file)
├── ec2_api.py
├── keep_alive.py
├── pyvenv.cfg               # (Virtual environment, not deployed)
├── render.yaml              # Key for Render deployment
├── requirements.txt
└── upload_images/
    └── .gitkeep
```

## Understanding `render.yaml`

The `render.yaml` file is crucial for deploying to Render. It defines the services, build commands, start commands, environment variables, and other configurations. Here's a breakdown of the one we created:

```yaml
services:
  - type: web
    name: food-calorie-api # Service for the Flask API
    env: docker
    repo: https://github.com/your-username/your-repo-name # Replace with your actual repo URL
    region: oregon # Or your preferred region
    plan: free # Or your preferred plan
    healthCheckPath: /health
    dockerfilePath: ./Dockerfile
    dockerContext: .
    dockerCommand: "gunicorn --bind 0.0.0.0:$PORT ec2_api:app" # How to start the Flask API
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.19 # Or your desired Python version
      - key: PORT
        value: 5000 # Port Gunicorn will listen on (Render maps this)

  - type: web
    name: food-calorie-streamlit # Service for the Streamlit App
    env: docker
    repo: https://github.com/your-username/your-repo-name # Replace with your actual repo URL
    region: oregon # Or your preferred region
    plan: free # Or your preferred plan
    healthCheckPath: /_stcore/health # Streamlit's default health check
    dockerfilePath: ./Dockerfile
    dockerContext: .
    dockerCommand: "streamlit run App.py --server.port $PORT --server.address 0.0.0.0" # How to start Streamlit
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.19 # Or your desired Python version
      - key: PORT
        value: 8501 # Port Streamlit will listen on (Render maps this)
```

**Key points in `render.yaml`:**

*   **`services`**: Defines a list of services to be deployed.
*   **`type: web`**: Indicates a web service.
*   **`name`**: A unique name for your service on Render.
*   **`env: docker`**: Specifies that the deployment environment is Docker.
*   **`repo`**: **IMPORTANT!** You MUST replace `https://github.com/your-username/your-repo-name` with the actual URL of your Git repository.
*   **`region`**: The geographical region where your service will be hosted.
*   **`plan`**: Render's pricing plan (e.g., `free`, `starter`).
*   **`healthCheckPath`**: An endpoint Render pings to check if your service is healthy.
    *   For Flask: `/health` (which we added to `ec2_api.py`).
    *   For Streamlit: `/_stcore/health` (Streamlit's built-in health check).
*   **`dockerfilePath`**: Path to your `Dockerfile`.
*   **`dockerContext`**: The directory context for the Docker build.
*   **`dockerCommand`**: The command to run when the Docker container starts.
    *   For Flask API: `gunicorn --bind 0.0.0.0:$PORT ec2_api:app` (uses Gunicorn to serve the Flask app).
    *   For Streamlit: `streamlit run App.py --server.port $PORT --server.address 0.0.0.0`.
*   **`envVars`**: Environment variables for your service.
    *   `PYTHON_VERSION`: Specifies the Python version for the build environment.
    *   `PORT`: The port your application inside the container should listen on. Render automatically assigns an external URL and routes traffic to this internal port.

## Understanding the `Dockerfile`

The `Dockerfile` defines how your application is packaged into a Docker image. The one we are using is generic enough for both the Flask API and Streamlit app:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Make port 8501 available to the world outside this container (for Streamlit)
# Make port 5000 available (for Flask/Gunicorn)
# Render will use the $PORT environment variable, so these EXPOSE lines are more for documentation/local testing.
EXPOSE 8501
EXPOSE 5000

# The command to run the application will be specified in render.yaml (dockerCommand)
# For local testing, you might add a CMD here, e.g.:
# CMD ["streamlit", "run", "App.py", "--server.port=8501", "--server.address=0.0.0.0"]
# Or for the API:
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "ec2_api:app"]
```

**Key points in `Dockerfile`:**

*   `FROM python:3.9-slim`: Starts with a slim Python 3.9 base image.
*   `WORKDIR /app`: Sets the working directory inside the container.
*   `COPY requirements.txt .` and `RUN pip install ...`: Copies and installs dependencies.
*   `COPY . .`: Copies all your project files into the `/app` directory in the image.
*   `EXPOSE 8501` and `EXPOSE 5000`: Informs Docker that the application might listen on these ports. Render uses the `PORT` environment variable specified in `render.yaml` to tell your app which port to listen on, and then maps external traffic to it.
*   The actual start command is provided by `dockerCommand` in `render.yaml`, making this `Dockerfile` reusable for both services.

## Deployment Steps to Render

1.  **Ensure `render.yaml` is Correct:**
    *   **Crucially, update the `repo` URL in `render.yaml` to point to YOUR Git repository.**
    *   Verify Python versions, regions, and plans as needed.

2.  **Push to Git:**
    *   Commit all your files (`App.py`, `ec2_api.py`, `requirements.txt`, `Model.h5`, `Dockerfile`, `render.yaml`) to your Git repository.
    ```bash
    git add .
    git commit -m "Configure project for Render deployment"
    git push origin main # Or your default branch
    ```

3.  **Create a New Blueprint Instance on Render:**
    *   Log in to your Render dashboard ([https://dashboard.render.com/](https://dashboard.render.com/)).
    *   Click on **"New"** (usually a blue button) and select **"Blueprint"**.
    *   Connect your Git provider (GitHub, GitLab) if you haven't already.
    *   Select the repository containing your project.
    *   Render will automatically detect the `render.yaml` file.

4.  **Review and Deploy:**
    *   Render will parse `render.yaml` and show you the services it plans to create (e.g., `food-calorie-api` and `food-calorie-streamlit`).
    *   You might be prompted to give Render permission to access the repository if it's the first time.
    *   Review the service names, plans, regions, and environment variables.
    *   Click **"Create Blueprint Instance"** (or a similar button like "Apply" or "Deploy").

5.  **Monitor Build and Deployment:**
    *   Render will start the build process for each service. This involves:
        *   Cloning your repository.
        *   Building the Docker image using your `Dockerfile` (this happens once if both services use the same Docker image from the same commit, or separately if configurations differ significantly or they are treated as distinct builds).
        *   Pushing the image to Render's internal registry.
        *   Starting the container with the `dockerCommand` specified in `render.yaml`.
    *   You can view the logs for each service in the Render dashboard to monitor progress and troubleshoot any issues.

6.  **Access Your Deployed Services:**
    *   Once deployed, Render will provide unique URLs for each service (e.g., `food-calorie-api.onrender.com` and `food-calorie-streamlit.onrender.com`).
    *   You can find these URLs in the service dashboard on Render.

## Build Command (Handled by Docker)

With `env: docker` in `render.yaml`, Render doesn't use a separate "build command" field in the UI in the same way it does for native environments. Instead, the Docker build process itself is the "build command":

*   Render executes `docker build -f Dockerfile .` (or equivalent) using the specified `dockerfilePath` and `dockerContext`.
*   The `RUN pip install ...` line within your `Dockerfile` handles the installation of Python dependencies.

There isn't a separate build command you need to enter in the Render UI if you are using a `render.yaml` with `env: docker`.

## Keep-Alive for Free Tier Services (Optional)

Render's free web services spin down after 15 minutes of inactivity. To keep them alive:

1.  **Use `keep_alive.py`:**
    *   After deployment, get the URLs for your API's `/health` endpoint and Streamlit's `/_stcore/health` endpoint.
    *   Set these as environment variables where you plan to run `keep_alive.py`:
        ```bash
        export RENDER_API_URL="https://your-api-service-name.onrender.com/health"
        export RENDER_STREAMLIT_URL="https://your-streamlit-service-name.onrender.com/_stcore/health"
        ```
    *   Run the script:
        ```bash
        python keep_alive.py
        ```
    *   This script can be run on your local machine, a Raspberry Pi, or any always-on server. You can also adapt it for services like GitHub Actions scheduled workflows or `cron-job.org`.

2.  **Upgrade to a Paid Plan:** Render's paid plans do not spin down services.

## Troubleshooting

*   **Check Build Logs:** The first place to look for errors is the build logs for each service on the Render dashboard.
*   **Check Runtime Logs:** After a successful build, check the runtime logs for any application errors.
*   **`render.yaml` Syntax:** Ensure `render.yaml` is correctly formatted (YAML is sensitive to indentation).
*   **`Dockerfile` Issues:** Test your `Dockerfile` build locally: `docker build -t test-app .`
*   **Dependency Conflicts:** Ensure `requirements.txt` is accurate and there are no conflicting packages.
*   **Model File Size:** If `Model.h5` is very large, it might cause issues with free tier limits or slow down deployments. Consider optimizing or hosting it externally if needed.
*   **Port Configuration:** Ensure `dockerCommand` in `render.yaml` uses `$PORT` (e.g., `streamlit run App.py --server.port $PORT`) and that your application inside the container correctly listens on this port.

This comprehensive guide should help you successfully deploy your Food Calorie Prediction application to Render. Good luck!