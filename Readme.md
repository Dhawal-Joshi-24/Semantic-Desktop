# 🧠 AI Semantic Desktop

A local Retrieval-Augmented Generation (RAG) architecture that transforms your personal desktop files into a fully searchable, semantic knowledge base using Python, FAISS, and the Google Gemini API.

## 🚀 Architecture Overview
Unlike traditional keyword search, this application utilizes an event-driven ingestion pipeline to generate high-dimensional vector embeddings of local files in real-time. 

* **The Nervous System (Ingestion):** A multi-threaded OS file watcher (`watchdog`) with debouncing logic monitors the local directory.
* **The Shredder (Processing):** Automatically parses unstructured data (PDFs, TXTs) and applies recursive character chunking to maintain semantic continuity.
* **The Memory (Vector Store):** Uses a persistent, local `FAISS` database for instantaneous similarity search, eliminating cloud DB latency.
* **The Brain (LLM Routing):** Bypasses unstable abstraction frameworks to natively interface with the Google GenAI SDK, utilizing dynamic model discovery for endpoint resilience.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **UI Framework:** Streamlit
* **Vector Store:** FAISS (Facebook AI Similarity Search)
* **LLM & Embeddings:** Google GenAI SDK (`gemini-1.5-flash` / `gemini-pro`)
* **Data Processing:** LangChain, PyMuPDF

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Semantic-Desktop.git](https://github.com/YOUR_USERNAME/Semantic-Desktop.git)
   cd Semantic-Desktop

2. **Create a Virtual Environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

4. **Environment Variables:**
Create a .env file in the root directory and add your Google API Key:

##Code snippet
GOOGLE_API_KEY="your_actual_api_key_here"

#🎯 Usage
To run the application, you need to start two separate processes.

1. **Start the Background Watcher:**
This script will monitor the my_documents folder for new files and automatically update the local FAISS vector database.

```bash
python watcher.py
```
2. **Start the Search Interface:**
Open a new terminal window, activate your venv, and run the Streamlit app.

```bash
streamlit run search_app.py
