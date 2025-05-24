# Deployment Guide for Car Diagnostics Assistant

This guide will help you deploy your Car Diagnostics Assistant web application to various hosting platforms. We've prepared the necessary deployment files for you.

## Prerequisites

1. Make sure you have Git installed and your code is committed to a GitHub repository
2. Create accounts on the deployment platform of your choice (see options below)
3. Ensure your `.env` file contains the necessary environment variables:
   - `GROQ_API_KEY` - Your Groq API key (if using the Groq API)

## Deployment Options

### Option 1: Heroku Deployment

Heroku is a cloud platform that lets you deploy, run, and manage applications.

1. **Create a Heroku account** at [heroku.com](https://heroku.com) if you don't have one
2. **Install the Heroku CLI** from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Login to Heroku CLI**:
   ```bash
   heroku login
   ```
4. **Create a new Heroku app**:
   ```bash
   heroku create car-diagnostics-assistant
   ```
5. **Set up environment variables**:
   ```bash
   heroku config:set GROQ_API_KEY=your_groq_api_key_here
   ```
6. **Deploy to Heroku**:
   ```bash
   git push heroku main
   ```
7. **Open your application**:
   ```bash
   heroku open
   ```

### Option 2: Python Anywhere Deployment

PythonAnywhere is a cloud-based Python development and hosting environment.

1. **Create a PythonAnywhere account** at [pythonanywhere.com](https://pythonanywhere.com)
2. **Go to the Web tab** and create a new web app, selecting "Flask" and the latest Python version
3. **Clone your repository**:
   ```bash
   git clone https://github.com/yourusername/car-diagnostics-assistant.git
   ```
4. **Set up a virtual environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 car-diagnostics-env
   pip install -r requirements.txt
   ```
5. **Configure your web app**:
   - WSGI configuration file: Edit to point to your Flask app
   - Set environment variables in the web app configuration

### Option 3: Railway Deployment

Railway is a deployment platform where you can provision infrastructure, develop with that infrastructure locally, and then deploy to the cloud.

1. **Sign up for Railway** at [railway.app](https://railway.app)
2. **Install the Railway CLI**:
   ```bash
   npm i -g @railway/cli
   ```
3. **Login to Railway**:
   ```bash
   railway login
   ```
4. **Initialize a new project**:
   ```bash
   railway init
   ```
5. **Deploy your application**:
   ```bash
   railway up
   ```

## File Structure for Deployment

The following files have been prepared for deployment:

- `requirements.txt`: Lists all Python dependencies
- `Procfile`: Tells Heroku (or other platforms) how to run your application
- `wsgi.py`: Entry point for WSGI servers like Gunicorn
- `runtime.txt`: Specifies the Python version

## Post-Deployment Tasks

1. **Test your application** thoroughly after deployment
2. **Set up monitoring** to track application performance
3. **Configure custom domain** (optional) if you want to use your own domain name

## Troubleshooting

- **Application crashes**: Check the logs on your hosting platform
- **Missing dependencies**: Ensure all required packages are listed in `requirements.txt`
- **Environment variables**: Verify all required environment variables are set correctly

For further assistance, refer to the documentation of your chosen hosting platform.
