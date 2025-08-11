

from typing import TypedDict
from backend.tools import get_weather, get_groq_client

class WeatherState(TypedDict):
    user_input: str
    ai_response: str

client = get_groq_client()

def extract_city(user_q: str) -> str:
    """Use Groq LLM to extract the city name from the user query."""
    prompt = f"""
    Extract only the city name from the following question.
    Do not include country names, dates, or extra words.
    Just return the city name exactly as it should appear in a weather API query.

    Question: "{user_q}"
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Faster model for extraction
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=20
        )
        city = completion.choices[0].message.content.strip()
        return city
    except Exception as e:
        print(f"[extract_city] Groq error: {e}")
        return user_q  # Fallback to original input

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
        "Provide a concise, friendly answer (2-3 sentences)."
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Main model for full response
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
