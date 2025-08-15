
# backend/tools.py
import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
from groq import Groq

# Local imports
from backend.rag import RAGRetriever

# Load environment variables from .env
load_dotenv()

# --- GROQ CLIENT ---
def get_groq_client() -> Groq:
    """Return a Groq API client instance."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in environment variables.")
    return Groq(api_key=api_key)

# Initialize singletons
retriever = RAGRetriever()  # Uses EMBED_MODEL and faiss.index from backend/data
client = get_groq_client()  # Shared Groq client

# Weather API key
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY") or None


# ----- Hotels -----
def search_hotels(query: str, top_k: int = 5) -> List[Dict]:
    """
    Return top_k hotel chunks from RAG retriever.
    Each result is the raw chunk dict loaded from chunks.json.
    """
    return retriever.retrieve(query, top_k=top_k)


# ----- Destinations  -----
def recommend_destinations(preferences: Optional[str] = None, n: int = 5) -> List[str]:
    """
    Ask Groq LLM to recommend destinations based on optional preferences.
    Returns a list of short recommendation strings.
    """
    p = preferences.strip() if preferences else "I like varied experiences (culture, food, nature)."
    prompt = (
        f"You are a helpful travel assistant. The user preferences: {p}\n\n"
        f"Please recommend {n} travel destinations (city/country), each on its own line. "
        "For each give a one-line reason why it is recommended (10-15 words)."
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        resp = completion.choices[0].message.content.strip()
        lines = [l.strip("-• \t") for l in resp.splitlines() if l.strip()]
        return lines[:n]
    except Exception as e:
        print(f"[tools.recommend_destinations] Error: {e}")
        return ["Sorry, I couldn't fetch recommendations right now."]


# ----- Weather (OpenWeatherMap) -----
def get_weather(city: str, api_key: Optional[str] = None) -> Optional[Dict]:
    """
    Return current weather summary for `city` using OpenWeatherMap.
    Returns: {description, temp_c, feels_like_c, humidity} or None on error.
    """
    HARD_CODED_API_KEY = "506efa32e98e94af86d1b9c3ffc0ae41"
    key = api_key or os.getenv("OPENWEATHER_API_KEY") or HARD_CODED_API_KEY
    if not key:
        raise ValueError("OpenWeatherMap API key not provided. Set OPENWEATHER_API_KEY env var or pass api_key.")

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
    if "weather" not in data or "main" not in data:
        return None

    return {
        "city": f"{data.get('name')}, {data.get('sys', {}).get('country', '')}".strip(", "),
        "description": data["weather"][0]["description"],
        "temp_c": data["main"].get("temp"),
        "feels_like_c": data["main"].get("feels_like"),
        "humidity": data["main"].get("humidity"),
    }


# ----- Hotels with Context -----
def format_hotels_with_context(query: str, top_k: int = 5) -> str:
    """
    Retrieve hotel chunks, build a context and ask Groq LLM to summarize into a helpful list.
    Returns a single string (assistant response) ready to send to user.
    """
    chunks = search_hotels(query, top_k=top_k)
    context_text = "\n\n".join([c.get("text", str(c)) for c in chunks])
    prompt = (
        "You are a travel assistant. Use the hotel data below to "
        f"answer the user request: {query}\n\n"
        "Hotel data:\n"
        f"{context_text}\n\n"
        "Provide a short, numbered list of the best matches with name, location, "
        "price (if available), and 1-sentence reason."
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"[tools.format_hotels_with_context] Error: {e}")
        return "Sorry, I couldn't fetch hotel details right now."




