# RepoPilot: AI-Powered GitHub Project Implementation Guide

# GitHub Repository Analyzer

RepoPilot is an intelligent Streamlit application that analyzes GitHub repositories and generates step-by-step guides for implementing projects locally. It uses AI to understand project structure and provide clear setup instructions.
This Streamlit application analyzes GitHub repositories and generates a project flow guide to help users implement the project locally.
This implementation provides a complete solution that:
- Takes a GitHub repo URL as input
- Analyzes all files in the repository
- Uses LangChain with a free HuggingFace model
- Generates a project flow guide
- Creates a downloadable markdown file
- Handles configuration via config.json

## ✨ Features

- **Automated Analysis**: Scans GitHub repos to identify key components
- **AI-Powered Guidance**: Generates implementation steps using Mistral-7B
- **Smart Filtering**: Focuses on essential files (code, configs, docs)
- **Local Processing**: Runs entirely on your machine via Ollama
- **Downloadable Guides**: Export markdown instructions for offline use

## 🛠️ Tech Stack

| Component               | Technology Used                  |
|-------------------------|----------------------------------|
| **Frontend**            | Streamlit                        |
| **LLM Framework**       | LangChain                        |
| **AI Model**            | Mistral-7B-Instruct (via Ollama) |
| **GitHub Integration**  | PyGithub                         |
| **Text Processing**     | HuggingFace Embeddings           |

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Ollama (for local LLM)
- GitHub account (optional, for private repos)

### Step-by-Step Setup

1. **Install Ollama & Mistral-7B**:
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh

   # Download Mistral-7B (4.1GB)
   ollama pull mistral

## Configuration

Create a `config.json` file with the following structure (huggingface api is optional if local ollama model is used):

```json
{
    "HUGGINGFACEHUB_API_TOKEN": "your_huggingface_api_token",
    "GITHUB_TOKEN": "your_github_token_optional"
}