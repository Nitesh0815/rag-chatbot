# AI-Powered RAG Chatbot

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-orange.svg)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-API-red.svg)](https://groq.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)

## Overview

This project implements a Retrieval-Augmented Generation (RAG) chatbot using Groq's LLaMA 3 model, ChromaDB for vector storage, and a simple web interface. Users can upload PDF documents and ask questions about their content.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   LangChain     │
│   (HTML/JS)     │◄──►│   Backend       │◄──►│   + ChromaDB    │
│                 │    │                 │    │                 │
│ - Upload PDF    │    │ - /upload       │    │ - Embeddings    │
│ - Chat Interface│    │ - /chat         │    │ - Retrieval     │
│ - Display       │    │ - /health       │    │ - Generation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────┐
                    │   Groq API      │
                    │   (LLaMA 3)     │
                    └─────────────────┘
```

## Tech Stack

- **Language**: Python 3.11
- **LLM**: Groq API (llama3-8b-8192 model)
- **Vector DB**: ChromaDB (local)
- **Framework**: LangChain + langchain-groq
- **Backend**: FastAPI + Uvicorn
- **Frontend**: Single HTML file (vanilla JS)
- **Containerization**: Docker + Docker Compose
- **Cloud**: AWS EC2 Ubuntu 22.04
- **CI/CD**: GitHub Actions
- **Dev OS**: Windows 11 WSL2 (Ubuntu)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag-chatbot
   ```

2. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   # Edit .env with your Groq API key
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Open `http://localhost:8000/frontend/index.html` in your browser.

## Usage

1. Upload a PDF document using the file input.
2. Ask questions about the document content in the chat interface.
3. The chatbot will retrieve relevant information and generate answers.

## API Docs

### Endpoints

- `GET /health`: Health check
- `POST /upload`: Upload PDF file
  - Body: `multipart/form-data` with `file` field
- `POST /chat`: Send chat message
  - Body: `{"question": "Your question here"}`

## Deploy

### Local Docker

```bash
docker-compose up --build
```

### AWS EC2

1. Set up Terraform:
   ```bash
   cd terraform
   terraform init
   terraform apply
   ```

2. Configure GitHub Secrets:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`
   - `EC2_HOST` (public IP from Terraform)
   - `EC2_KEY` (private key content)
   - `GROQ_API_KEY`

3. Push to `main` branch to trigger deployment.

## CI/CD

GitHub Actions workflow:
- Builds Docker image on push to main
- Pushes to Docker Hub
- Deploys to EC2 via SSH
- Runs `docker-compose up -d`