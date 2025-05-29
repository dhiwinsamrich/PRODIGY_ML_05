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

## Netlify Deployment

This project is configured for Netlify deployment, but note that Netlify doesn't directly support running Streamlit applications. The Netlify configuration provides an informational page about how to run the app locally.

### Deployment Steps

1. Push your code to a Git repository (GitHub, GitLab, etc.)

2. Sign up or log in to [Netlify](https://www.netlify.com/)

3. Create a new site from Git:
   - Click "Add new site" → "Import an existing project"
   - Connect to your Git provider and select your repository

4. Netlify will automatically detect the configuration in `netlify.toml`

5. Deploy the site

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
