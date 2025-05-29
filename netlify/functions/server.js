// netlify/functions/server.js
const serverless = require('serverless-http');
const express = require('express');
const path = require('path');

const app = express();

// Serve static assets if available
app.use(express.static(path.join(__dirname, '../../public')));

// Add middleware to parse JSON and URL-encoded data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/.netlify/functions/server/health', (req, res) => {
  res.status(200).json({ status: 'ok', message: 'Food Calorie Prediction API is running' });
});

// Redirect root to the deployed Streamlit app URL
app.get('/', (req, res) => {
  // Since Netlify doesn't directly support running Streamlit apps,
  // we'll redirect users to a page explaining how to access the app
  res.send(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>Food Calorie Prediction App</title>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
          h1 { color: #333; }
          .container { border: 1px solid #ddd; padding: 20px; border-radius: 5px; }
          .info { background-color: #f8f9fa; padding: 15px; border-left: 4px solid #17a2b8; margin-bottom: 20px; }
          .button { display: inline-block; background-color: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; }
        </style>
      </head>
      <body>
        <h1>Food Calorie Prediction App</h1>
        <div class="container">
          <div class="info">
            <p>This application is a Streamlit-based ML app for predicting calories in food items from images.</p>
            <p>The app is containerized with Docker and needs to be run in an environment that supports Docker containers.</p>
          </div>
          <p>To run this application:</p>
          <ol>
            <li>Clone the repository from GitHub</li>
            <li>Make sure Docker is installed on your system</li>
            <li>Run <code>docker build -t food-calorie-app .</code> to build the Docker image</li>
            <li>Run <code>docker run -p 8501:8501 food-calorie-app</code> to start the container</li>
            <li>Access the app at <code>http://localhost:8501</code></li>
          </ol>
          <p>For more information, please refer to the README and deployment documentation in the repository.</p>
        </div>
      </body>
    </html>
  `);
});

// Catch-all handler
app.all('*', (req, res) => {
  res.status(404).json({
    status: 'error',
    message: 'This endpoint does not exist. The Streamlit app needs to be run via Docker as described in the documentation.'
  });
});

module.exports.handler = serverless(app);