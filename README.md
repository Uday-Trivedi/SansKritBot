# 🙏 Sanskrit Chatbot

A simple chatbot that takes questions in **English** and answers in **Sanskrit** (Devanagari script).

## Technologies Used

- **Python** — programming language
- **Streamlit** — web UI framework
- **Google Gemini API** — AI model for generating Sanskrit answers
- **python-dotenv** — loads API key from `.env` file
- **Docker** — containerization

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env` file

Create a file named `.env` in the project root:

```
GEMINI_API_KEY=your_actual_api_key_here
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

### 3. Run locally

```bash
streamlit run main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## Docker

### Build the image

```bash
docker build -t sanskrit-chatbot .
```

### Run the container

```bash
docker run --env-file .env -p 8501:8501 sanskrit-chatbot
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

> **Note:** The API key is passed at runtime using `--env-file .env`. It is never stored inside the Docker image.

## How It Works

```
User enters English question
        ↓
Question sent to Gemini API
        ↓
Gemini generates answer in Sanskrit
        ↓
Streamlit displays Sanskrit answer
```
