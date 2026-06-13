# Medical AI Assistant: Clinical Scribe & Dictation System

A professional, premium web application designed to act as an AI-powered Medical Scribe. The application transcribes consultations (from live dictation or audio file upload) and extracts structured clinical notes (SOAP format), custom formats, or raw text transcripts, utilizing serverless Hugging Face Large Language Models (LLMs) and Automatic Speech Recognition (ASR).

---

## Key Features

1. **Output Modes**:
   - **Structured Clinical Note (SOAP)**: Chief Complaint, HPI, Assessment, Plan, Prescription, Recommended Tests, and Follow-up.
   - **Custom Prompt / Instruction**: Free-form instruction (e.g., referral letter, surgery report, gynecology note).
   - **Raw Transcript**: Serves only the speech-to-text output without AI formatting.

2. **Strict Extraction (No Hallucinations)**:
   - Evaluates note content sentence-by-sentence using token grounding algorithms.
   - Preserves actual symptoms, diagnoses, and follow-up advice mentioned in the transcript.
   - Prevents AI hallucinations of unmentioned dosages, frequencies, vital signs, lab values, or medical history.

3. **Bulleted Prescription Layout**:
   - Formats medication details cleanly with clear newline markers:
     ```
     Medication:
     * Amoxicillin
     Dosage:
     Not specified
     Frequency:
     Not specified
     Duration:
     Not specified
     ```

4. **Robust API Rate-Limit Mapping**:
   - Maps serverless API rate-limiting errors (HTTP 429) to clean, user-friendly toast notifications advising users to retry or configure their own token.

5. **Settings Persistence**:
   - Persists all selected LLM models, ASR models, specialties, dictation languages, and prompts under browser local storage.

---

## Technology Stack

- **Backend**: FastAPI (Python 3.13)
- **Frontend**: HTML5, Vanilla JavaScript, CSS3 (Premium dark-theme styling, glassmorphism, responsive grid, loading micro-animations)
- **AI Integration**: Hugging Face Inference API / Router (`huggingface_hub`)
- **Production Adapter**: `a2wsgi` (ASGI-to-WSGI translation layer for hosting on WSGI platforms)

---

## Local Setup and Installation

### Prerequisites
- Python 3.10+ installed

### Step-by-Step Local Run
1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd medical-ai-assistant
   ```

2. **Create and Activate a Virtual Environment**:
   - **Windows**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file at the root of the project:
   ```env
   HF_TOKEN=your_huggingface_write_token_here
   ```
   *Note: If no token is provided, the application defaults to **Demo Mode** which simulates Note Generation and transcription templates.*

5. **Run the Application Locally**:
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   Open `http://127.0.0.1:8000` in your web browser.

6. **Run Tests**:
   ```bash
   pytest tests/
   ```

---

## Production Deployment on PythonAnywhere

Since PythonAnywhere is a WSGI-based hosting platform, running an ASGI FastAPI application requires wrapping it with `a2wsgi` to adapt it to the WSGI standard. We have bundled a `wsgi.py` adapter at the root of the project to facilitate this.

### Deployment Guide

1. **Upload the Codebase**:
   Upload your code to PythonAnywhere (using Git clone or the Files tab). Let's assume the path is `/home/yourusername/medical-ai-assistant`.

2. **Create a Python 3.10+ Virtualenv**:
   Open a Bash console in PythonAnywhere and run:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 venv
   pip install -r /home/yourusername/medical-ai-assistant/requirements.txt
   ```

3. **Configure the Web App**:
   - Go to the **Web** tab on the PythonAnywhere dashboard.
   - Click **Add a new web app**.
   - Choose **Manual Configuration** (since we are using a custom WSGI wrapper).
   - Select the Python version matching your virtualenv (e.g. Python 3.10).

4. **Configure Web Application Settings**:
   - **Code**:
     - Source code path: `/home/yourusername/medical-ai-assistant`
     - Working directory: `/home/yourusername/medical-ai-assistant`
   - **WSGI configuration file**:
     - Click the link to edit your WSGI configuration file (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`).
     - Replace the entire content of that file with:
       ```python
       import sys
       import os

       # Set up project home path
       path = '/home/yourusername/medical-ai-assistant'
       if path not in sys.path:
           sys.path.insert(0, path)

       # Wrap FastAPI ASGI app to WSGI
       from a2wsgi import ASGIMiddleware
       from app.main import app

       application = ASGIMiddleware(app)
       ```
     - Save the file.
   - **Virtualenv**:
     - Set the path to `/home/yourusername/.virtualenvs/venv` (or the folder where your `mkvirtualenv` was created).
   - **Static files** (highly recommended for performance):
     - Add a mapping under the **Static files** section:
       - **URL**: `/static/`
       - **Directory**: `/home/yourusername/medical-ai-assistant/app/static`
   - **Environment Variables**:
     - In the root of the application on PythonAnywhere (`/home/yourusername/medical-ai-assistant`), create a `.env` file containing your production API keys:
       ```env
       HF_TOKEN=your_real_huggingface_access_token_here
       ```

5. **Reload the Web App**:
   - Click the green **Reload** button at the top of the **Web** tab.
   - Your Medical AI Assistant is now live at `http://yourusername.pythonanywhere.com`!

---

## Production Deployment on Render

Render natively supports ASGI/FastAPI applications and Python web services. We have pre-configured a `render.yaml` Blueprint file for quick deployment.

### Step-by-Step Render Setup

1. **Push your code to GitHub/GitLab**.
2. **Create a new Web Service**:
   - Log in to your [Render Dashboard](https://dashboard.render.com).
   - Click **New +** on the top right and select **Web Service**.
   - Connect your Git repository.
3. **Configure Web Service Settings**:
   - **Name**: `medical-ai-assistant`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Configure Environment Variables**:
   - Scroll down to the **Environment Variables** section.
   - Click **Add Environment Variable**:
     - **Key**: `HF_TOKEN`
     - **Value**: `your_real_huggingface_access_token_here`
   - Click **Add Environment Variable** to select Python version (optional but recommended):
     - **Key**: `PYTHON_VERSION`
     - **Value**: `3.10.0`
5. **Deploy**:
   - Click **Create Web Service** at the bottom. Render will automatically build the environment, install the dependencies, and deploy the application.
   - Once the deploy completes successfully, your app will be live at the provided `.onrender.com` URL!

