# Food Calorie Prediction App

This application uses machine learning to predict the type of food in an image and estimate its calorie content. It's built with Streamlit, TensorFlow/Keras, and can be deployed using Docker or Netlify.

## Features

- Upload food images (fruits and vegetables)
- Automatic classification of food type
- Calorie estimation per 100g of the identified food
- Categorization into fruits or vegetables
- Responsive web interface

## Project Structure

```
├── App.py                 # Main Streamlit application
├── Food_Classification.py # Alternative classification script
├── Model.h5               # Pre-trained ML model
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── upload_images/         # Directory for uploaded images
├── netlify/               # Netlify deployment configuration
│   └── functions/         # Serverless functions
│       ├── server.js      # Express server for Netlify
│       └── package.json   # Node.js dependencies
└── public/                # Static assets for Netlify
```

## Local Development

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- Docker (optional, for containerization)

### Setup

1. Clone the repository

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run App.py
   ```

4. Access the app at http://localhost:8501

## Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t food-calorie-app .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 food-calorie-app
   ```

3. Access the app at http://localhost:8501

## Render Deployment

This project is configured for deployment on Render using Docker. Render allows you to deploy both the Streamlit application and the Flask API as separate web services.

### Prerequisites

- A Render account ([https://render.com/](https://render.com/))
- Your project pushed to a Git repository (GitHub, GitLab, etc.)

### Deployment Steps

1.  **Create a New Blueprint Instance on Render:**
    *   Log in to your Render dashboard.
    *   Click on "New" -> "Blueprint".
    *   Connect your Git repository where this project is hosted.
    *   Render will detect the `render.yaml` file in your repository.

2.  **Configure Services:**
    *   The `render.yaml` file defines two services:
        *   `food-calorie-app`: The Flask API.
        *   `food-calorie-streamlit`: The Streamlit application.
    *   Review the settings for each service (plan, build command, start command, environment variables).
    *   Ensure the `PYTHON_VERSION` matches your project's requirements.
    *   The `plan` is set to `free` by default. You can change this to a paid plan if needed.

3.  **Deploy:**
    *   Click "Create Blueprint Instance" (or similar button) to start the deployment process.
    *   Render will build and deploy both services based on the `Dockerfile` and `render.yaml` configuration.
    *   You will get unique URLs for both the API and the Streamlit app once deployed.

4.  **Set Environment Variables for Keep-Alive (Optional but Recommended):**
    *   After deployment, note the URLs for your API and Streamlit services.
    *   If you plan to use the `keep_alive.py` script, set the following environment variables where you run the script (e.g., locally or on another server/cron job provider):
        *   `RENDER_API_URL`: The URL of your deployed Flask API (e.g., `https://your-api-service-name.onrender.com/health`)
        *   `RENDER_STREAMLIT_URL`: The URL of your deployed Streamlit app (e.g., `https://your-streamlit-service-name.onrender.com/_stcore/health`)

### Keep-Alive Functionality

Render's free web services can spin down after a period of inactivity. To prevent this, a `keep_alive.py` script is included in this repository.

**How to use `keep_alive.py`:**

1.  **Set Environment Variables:**
    *   Ensure `RENDER_API_URL` and `RENDER_STREAMLIT_URL` are set in the environment where you will run this script.

2.  **Run the script:**
    ```bash
    python keep_alive.py
    ```
    This script will periodically send GET requests to the health check endpoints of your deployed services, keeping them active.

3.  **Alternative for Keep-Alive:**
    *   You can use a cron job service (like `cron-job.org`, GitHub Actions scheduled workflows, or a scheduler on another server) to periodically hit your service URLs.
    *   Render also offers paid plans that do not spin down services.

## How It Works

1. The application uses a pre-trained Keras model to classify food images
2. When an image is uploaded, it's preprocessed and fed to the model
3. The model predicts the food type from 36 different categories
4. The app then fetches calorie information for the predicted food
5. Results are displayed with the food category and calorie content

## API Usage

The application also includes a Flask API (`ec2_api.py`) that can be used for integration with other services:

```python
import requests

url = "http://your-api-url/predict"
files = {"file": open("path/to/image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## License

See the LICENSE file for details.
