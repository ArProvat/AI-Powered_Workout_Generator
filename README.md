# Workout Generator API

A professional FastAPI application for generating personalized workout plans and motivational messages using LangChain and GROQ LLM.

## Features

- 🏋️ **Personalized Workout Generation**: Create custom workout plans based on user goals, equipment, and time constraints
- 💪 **Progressive Training**: 4-week progressive workout programs with session history
- 🎯 **Motivational Messages**: Generate inspiring, personalized motivational content
- 🔄 **Session Memory**: Uses Redis to maintain conversation history for better continuity
- 📊 **Structured Output**: Clean JSON responses with validated data models

# 🚀 Complete Setup Guide

This guide will walk you through setting up the AI-Powered Workout Generator from scratch.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Getting Groq API Key](#getting-groq-api-key)
3. [Local Setup](#local-setup)

---
## Project Structure
```
ai_component/
    ├── chains/
        ├── __init__.py
        ├── genarate_motivation.py
        └── generate_daily_workout.py
    ├── LLMs/
        ├── __init__.py
        └── Groq_llm.py
    ├── prompts/
        ├── __init__.py
        └── prompts.py
    ├── schemas/
        ├── __init__.py
        └── response_sehema.py
    ├── short_term_memory/
        ├── __init__.py
        └── redis_short_term_memory.py
    └── __init__.py
app/
    └── main.py
notebook/
    └── Workout_Generator.ipynb
output/
    ├── image.png
    ├── screencapture-127-0-0-1-8000-docs-2025-10-16-13_44_51.png
    └── screencapture-127-0-0-1-8000-docs-2025-10-16-13_45_38.png
.gitignore
.python-version
pyproject.toml
README.md
requirements.txt
uv.lock
```

## Prerequisites

### Required Software
- **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/downloads)
- **UV** (for venv )

### Optional
- **Postman** - [Download here](https://www.postman.com/downloads/) (for API testing)

---

## Getting Groq API Key

1. **Visit Groq Console**
   - Go to [https://console.groq.com](https://console.groq.com)

2. **Create an Account**
   - Sign up with your email or GitHub account
   - Verify your email if required

3. **Generate API Key**
   - Navigate to the "API Keys" section
   - Click "Create API Key"
   - Give it a name (e.g., "Workout Generator")
   - Copy the API key immediately (you won't be able to see it again)

4. **Store Securely**
   - Save your API key in a secure location
   - Never commit it to version control

---

## Local Setup

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-workout-generator.git

# Navigate to project directory
cd ai-workout-generator
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
# Create virtual environment
uv venv (Recommend)
or
python -m venv venv

# Activate virtual environment
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when activated.

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
uv pip install -r requirements.txt
 or
uv add install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create .env file 

Add your Groq API key:
```
GROQ_API_KEY=gsk_your_actual_api_key_here
UPSTASH_REDIS_REST_URL ="your rest url"
UPSTASH_REDIS_REST_TOKEN='your rest token'
```

Save and close the file.

### Step 5: Run the Application

```bash
python -m app.main
```

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 6: Test the API

Open your browser and visit:
- **Swagger UI**: http://localhost:8000/docs
- **Root Endpoint**: http://localhost:8000/


---



### Step 4: Access the API

The API will be available at http://localhost:8000

---

## Testing

### Using Swagger UI (Easiest)

1. Open http://localhost:8000/docs
2. Click on any endpoint (e.g., `/generate-daily-workout`)
3. Click "Try it out"
4. Modify the request body
5. Click "Execute"
6. View the response


**Single Day Workout:**
```bash
curl -X POST "http://localhost:8000/generate-daily-workout?day=1" \
  -H "Content-Type: application/json" \
  -d '{
    "mission": "Build Strength",
    "time_commitment": "20–30 min",
    "gear": "Dumbbells",
    "squad": "Warrior"
  }'
```

**30-Day Plan:**
```bash
curl -X POST "http://localhost:8000/generate-workout" \
  -H "Content-Type: application/json" \
  -d '{
    "mission": "Build Strength",
    "time_commitment": "20–30 min",
    "gear": "Dumbbells",
    "squad": "Warrior"
  }'
```

### Using Postman
postman documentation : [host_doc_link](https://documenter.getpostman.com/view/33935662/2sB3QNq8oU)

---


## Next Steps

1. ✅ Read the main [README.md](README.md) for detailed API documentation
2. ✅ Import Postman collection for easy testing
3. ✅ Check the `/output` folder for sample responses
4. ✅ Customize the system prompts in `prompts.py` for different workout styles

---


**Happy Coding! 💪🏋️‍♂️**
