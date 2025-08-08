# backend/tools.py
import os
import requests
from typing import List, Dict, Optional

# Local imports (adjust if your package layout differs)
from backend.rag import RAGRetriever
from langchain_community.llms import Ollama

# Initialize singletons (cheap to import)
retriever = RAGRetriever()           # Uses EMBED_MODEL and faiss.index from backend/data
llm = Ollama(model="phi3")           # Local Ollama phi3 model

# Weather
OPENWEATHER_KEY = os.environ.get("OPENWEATHER_API_KEY") or None

# ----- Hotels -----
def search_hotels(query: str, top_k: int = 5) -> List[Dict]:
    """
    Return top_k hotel chunks from RAG retriever.
    Each result is the raw chunk dict loaded from chunks.json.
    """
    results = retriever.retrieve(query, top_k=top_k)
    # If chunks are dicts with 'text' and maybe metadata, pass them through
    return results

# ----- Destinations (LLM-powered) -----
def recommend_destinations(preferences: Optional[str] = None, n: int = 5) -> List[str]:
    """
    Ask the local LLM to recommend destinations based on optional preferences.
    Returns a list of short recommendation strings.
    """
    p = preferences.strip() if preferences else "I like varied experiences (culture, food, nature)."
    prompt = (
        f"You are a helpful travel assistant. The user preferences: {p}\n\n"
        f"Please recommend {n} travel destinations (city/country), each on its own line. "
        "For each give a one-line reason why it is recommended (10-15 words)."
    )
    resp = llm.invoke(prompt).strip()
    # Split by newlines and clean
    lines = [l.strip("-• \t") for l in resp.splitlines() if l.strip()]
    # return top n
    return lines[:n]

# ----- Weather (OpenWeatherMap) -----
def get_weather(city: str, api_key: Optional[str] = None) -> Optional[Dict]:
    """
    Return current weather summary for `city` using OpenWeatherMap.
    Returns: {description, temp_c, feels_like_c, humidity} or None on error.
    """
    key = api_key or os.environ.get("OPENWEATHER_API_KEY") or OPENWEATHER_KEY
    if not key:
        raise ValueError("OpenWeatherMap API key not provided. Set OPENWEATHER_API_KEY env var or pass api_key.")
    # Basic sanitation
    city_q = city.strip()
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_q, "appid": key, "units": "metric"}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"[tools.get_weather] Request error: {e}")
        return None

    data = r.json()
    # Basic safety checks
    if "weather" not in data or "main" not in data:
        return None

    return {
        "city": f"{data.get('name')}, {data.get('sys', {}).get('country', '')}".strip(", "),
        "description": data["weather"][0]["description"],
        "temp_c": data["main"].get("temp"),
        "feels_like_c": data["main"].get("feels_like"),
        "humidity": data["main"].get("humidity"),
    }

# ----- Helper to format hotel search results with LLM (optional) -----
def format_hotels_with_context(query: str, top_k: int = 5) -> str:
    """
    Retrieve hotel chunks, build a context and ask LLM to summarize into a helpful list.
    Returns a single string (assistant response) ready to send to user.
    """
    chunks = search_hotels(query, top_k=top_k)
    context_text = "\n\n".join([c.get("text", str(c)) for c in chunks])
    prompt = (
        "You are a travel assistant. Use the hotel data below to "
        f"answer the user request: {query}\n\n"
        "Hotel data:\n"
        f"{context_text}\n\n"
        "Provide a short, numbered list of the best matches with name, location, price (if available), and 1-sentence reason."
    )
    response = llm.invoke(prompt)
    return response
