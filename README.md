 🧳 Travel Assistant Chatbot

An AI-powered **Travel Assistant** that helps users with **weather updates**, **hotel recommendations**, and **destination suggestions**.  
Built with **LangGraph** for node orchestration, **Groq LLM** for fast natural language responses, and **Streamlit** for the frontend.

---

## 🚀 Features
- **Domain-Specific**: Answers only travel-related questions (weather, hotels, destinations).
- **Weather Updates**: Fetch real-time weather from OpenWeather API.
- **Hotel Recommendations**: Query hotels from a custom dataset using RAG (Retrieval-Augmented Generation).
- **Destination Suggestions**: Get travel destination ideas.
- **LangGraph Orchestration**: Routes queries to the correct node.
- **Groq LLM Integration**: Fast and high-quality language model responses.

---
## 📂 Project Structure
ravel-assistant-bot/
│
├── app.py # Streamlit app entry point
├── backend/
│ ├── graph.py # LangGraph orchestration
│ ├── rag.py # RAG retriever
│ ├── rag_build.py # Build FAISS index from CSV
│ ├── tools.py # Utility functions (weather API, Groq client)
│ ├── nodes/
│ │ ├── chatbot_node.py # General chatbot node
│ │ ├── weather_node.py # Weather query node
│ │ ├── hotels_node.py # Hotel search node
│ │ ├── destination_node.py # Destination suggestions node
│ └── data/
│ ├── stays.csv # Hotel dataset
│ ├── chunks.json # RAG chunks
│ └── faiss.index # FAISS vector index
│
├── .env # API keys (Groq, OpenWeather)
├── requirements.txt # Python dependencies
└── README.md # Project documentation
---
---

## 🔧 Installation

 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/travel-assistant-bot.git
cd travel-assistant-bot
```
2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```
3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
🔑 Environment Variables
Create a .env file in the project root:
```bash
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```
🛠 Build the RAG Index
```bash
python backend/rag_build.py
```
This will process stays.csv into vector embeddings and save them in backend/data/faiss.index.

▶️ Run the App
Streamlit UI
```bash
streamlit run app.py
```
