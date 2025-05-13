# RAG Application

This repository contains the RAG (Retrieval-Augmented Generation) application, which consists of a backend built with FastAPI and a frontend built with React. This application allows users to upload PDF files and interact with a chat interface.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Backend](#running-the-backend)
- [Running the Frontend](#running-the-frontend)
- [Usage](#usage)
- [Notes](#notes)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.9 or higher**: Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
- **Node.js and npm**: Ensure you have Node.js and npm installed. You can download it from [nodejs.org](https://nodejs.org/).
- **OpenAI API Key**: You will need an OpenAI API key to use the backend. Sign up at [OpenAI](https://platform.openai.com/signup) and create an API key.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/rag.git
   cd rag
   ```

2. **Set up the backend**:
   - Navigate to the `rag-backend` directory:
     ```bash
     cd rag-backend
     ```
   - Create a virtual environment:
     ```bash
     python -m venv myenv
     ```
   - Activate the virtual environment:
     ```bash
     # For macOS/Linux
     source myenv/bin/activate
     # For Windows
     myenv\Scripts\activate
     ```
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set up the frontend**:
   - Navigate to the `rag-frontend` directory:
     ```bash
     cd ../rag-frontend
     ```
   - Install the required packages:
     ```bash
     npm install
     ```

## Running the Backend

1. **Set your OpenAI API key**:
   - Create a `.env` file in the `rag-backend` directory and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     HUGGINGFACEHUB_API_TOKEN=your_api_key_here (if used)
     ```

2. **Run the backend**:
   ```bash
   uvicorn main:app --reload
   ```

## Running the Frontend

1. **Start the frontend**:
   ```bash
   npm start
   ```

2. **Open your browser**:
   - Navigate to `http://localhost:3000` to access the frontend application.

## Usage

- Use the upload feature to submit PDF files.
- Interact with the chat interface to ask questions based on the uploaded documents.

## Notes

- Ensure that your OpenAI API key is valid and that you have sufficient quota to make requests.
- If you encounter any issues, check the console for error messages and ensure that both the backend and frontend are running correctly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
