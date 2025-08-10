

# backend/nodes/weather_node.py
from typing import TypedDict
from backend.tools import get_weather, get_groq_client
import re

class WeatherState(TypedDict):
    user_input: str
    ai_response: str

client = get_groq_client()

def extract_city(user_q: str) -> str:
    """Extract city name from a user's weather query."""
    user_q = user_q.lower().strip()

    match = re.search(r"in\s+([a-zA-Z\s]+)", user_q)
    if match:
        return match.group(1).strip().title()

    prefixes = [
        "what is the weather in",
        "what's the weather in",
        "weather in",
        "what is the weather",
        "what's the weather",
        "weather"
    ]
    for p in prefixes:
        if user_q.startswith(p):
            city = user_q[len(p):].strip(" ?.").title()
            return city

    return user_q.title()

def weather_node(state: WeatherState):
    """Fetch weather info for a city and format using Groq LLM."""
    user_q = state["user_input"]
    city = extract_city(user_q)

    weather = get_weather(city)
    if weather is None:
        return {"ai_response": f"Sorry, I couldn't fetch the weather for {city} right now."}

    prompt = (
        f"User asked: {user_q}\n\n"
        f"Weather data: {weather}\n\n"
        "Provide a concise, user-friendly answer (2-3 sentences)."
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"Sorry, I couldn't process the weather request: {e}"

    return {"ai_response": reply}
