# CodeAlpha FAQ Chatbot

A professional AI-powered FAQ chatbot built with Python, Tkinter, NLTK, scikit-learn, and JSON-based FAQ retrieval. The chatbot uses NLP preprocessing and TF-IDF with cosine similarity to find the most relevant answer from a knowledge base instead of relying on hardcoded rules.

## Introduction

This project was developed as part of the CodeAlpha AI Internship Task 2. It showcases a complete NLP-based chatbot experience with a modern desktop GUI, FAQ dataset storage in JSON, and a similarity-based retrieval engine.

## Features

- Modern desktop GUI built with Tkinter
- Dark-mode interface with chat bubbles
- Scrollable chat history
- FAQ answers stored in JSON
- NLP preprocessing with lowercase conversion, punctuation removal, tokenization, stopword removal, and lemmatization
- TF-IDF vectorization and cosine similarity for retrieval
- Fallback response when similarity is below a threshold
- Clear Chat button and Enter-to-send interaction
- Proper exception handling and modular object-oriented design

## Technologies Used

- Python 3.12+
- Tkinter for the desktop GUI
- NLTK for natural language processing
- scikit-learn for TF-IDF vectorization and cosine similarity
- JSON for FAQ storage

## Installation

1. Clone or download the project folder.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the chatbot:
   ```bash
   python chatbot.py
   ```

## Usage

- Launch the application by running `python chatbot.py`.
- Type a question in the input box.
- Press Enter or click Send.
- The bot will return the closest matching FAQ answer from the dataset.
- If no suitable match is found, it will display a fallback message.

## Project Structure

```text
CodeAlpha_FAQChatbot/
├── chatbot.py
├── faq.json
├── requirements.txt
├── README.md
├── utils.py
├── assets/
└── screenshots/
```

## Future Improvements

- Add persistent chat history
- Support voice input/output
- Integrate a transformer-based model for deeper semantic matching
- Add multilingual FAQ support
- Deploy the chatbot as a web app

## Notes

The project is designed to be Windows-compatible and can be run directly from the project folder.
