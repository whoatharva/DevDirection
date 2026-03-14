# Hosting DevDirection

This guide covers deploying the DevDirection project to reliable cloud platforms like **Railway.app** or **Render.com**. DevDirection is built on `FastAPI` (Python) utilizing `uvicorn` and serving static frontend files. 

## Project Architecture (Deployment Specs)
* **Framework**: FastAPI (Python 3.10+) 
* **Entry Point**: `app.main:app`
* **Static Assets**: All frontend HTML/JS/CSS served via FastAPI `StaticFiles` from `/static`
* **Required Secrets**: `GOOGLE_API_KEY` (or `GEMINI_API_KEY`)

---

## Required Environment Variables
You must set these exactly as written in your host's environment settings panel:
* `GOOGLE_API_KEY` : *Your Gemini api key from Google AI Studio*

*(Optional fallback: `GEMINI_API_KEY`)*

---

## 🚀 Option 1: Deploy on Railway.app (Recommended)

Railway detects Python repositories automatically and is the easiest way to spin up FastAPI applications.

1. **Commit your code to GitHub.** Ensure `.gitignore` is pushing your project minus the `venv` and `.env` files.
2. **Login to Railway** (https://railway.app) and click **"New Project"**.
3. Select **"Deploy from GitHub repo"** and choose your DevDirection repository.
4. **Automatic Detection**:
   Railway will automatically find your `requirements.txt` and `Procfile` in the root and start the build process. No extra configuration is needed!
5. **Add Environment Variables**:
   - Go to your newly deployed project > **Variables** tab.
   - Click **New Variable** and add `GOOGLE_API_KEY` with your actual secret key.
   - Wait 1 minute for Railway to seamlessly redeploy your application.
6. **Generate a Domain**:
   - Go to the **Settings** tab.
   - Under the Environments section, click **Generate Domain**.
   - Your application is now live at the generated HTTPS link!

---

## 🚀 Option 2: Deploy on Render.com

Render is a robust alternative for Python applications offering free-tier Web Services.

1. **Login to Render** (https://render.com) and click **"New"** > **"Web Service"**.
2. Connect your GitHub account and select your repository.
3. Configure the following specific settings for DevDirection:
   * **Name**: `devdirection`
   * **Region**: *Choose closest to you*
   * **Branch**: `main`
   * **Root Directory**: *(Leave blank)*
   * **Runtime**: `Python 3`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   * Scroll down to **Advanced** > **Add Environment Variable**.
   * Key: `GOOGLE_API_KEY` | Value: *Your secret key*
   * Key: `PYTHON_VERSION` | Value: `3.10.0` *(optional but recommended)*
5. Click **"Create Web Service"**.
6. Render will install your dependencies via `pip` and execute uvicorn. In 3-5 minutes, your site will be live!

---

### Verifying the Deployment
Once deployed, navigate your browser to your given host URL. 
- Ensure that the quiz completes correctly and the Roadmap renders. If the roadmap generation crashes or continuously loads, double check that your `GOOGLE_API_KEY` was copy/pasted without extra whitespace in your hosting environment variables panel.
