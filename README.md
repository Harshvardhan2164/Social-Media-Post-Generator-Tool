# Social-Media-Post-Generator-Tool

This is a simple tool that helps in creating new posts based on the writing style in related posts. It uses Llama-3.3-versatile from Groq Cloud using an API Key to generate posts based on the user's input.

## Technical Architecture

1. Stage 1: Collect posts from various social media platforms and extract topics, language and length from it.
2. Stage 2: LLM model uses this topic, language and length to generate new post. Some of the past posts that are related to the user's input will be used to guide the LLM about the writing style in order avoid hallucinations.

## Installation

1. Clone the repository
```bash
git clone https://github.com/Harshvardhan2164/Social-Media-Post-Generator-Tool.git
cd Social-Media-Post-Generator-Tool
``` 


2. To get started, we first need an API_KEY from <a href="https://console.groq.com/keys" target="_blank">Groq Cloud</a>. Store inside `.env` and update the value of `GROQ_API_KEY` with your API_KEY.

3. Create a virtual environment after opening the repository (Use Python Versions < 3.11)
```bash
python -m venv env
source env/Scripts/activate
```

4. Install the required Libraries using `requirements.txt`
```bash
pip install -r requirements.txt
```

5. Run `main.py` using Streamlit
```bash
streamlit run main.py
```

## License
This project is licensed under the MIT License.