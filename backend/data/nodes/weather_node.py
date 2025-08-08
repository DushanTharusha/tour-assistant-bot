# backend/nodes/weather_node.py
from typing import TypedDict
from backend.tools import get_weather
from langchain_community.llms import Ollama

llm = Ollama(model="phi3")

class WeatherState(TypedDict):
    user_input: str
    ai_response: str

def weather_node(state: WeatherState):
    # Expect user_input like "weather in Colombo" or "what's the weather in Paris?"
    user_q = state["user_input"]
    # Simple extraction: attempt to grab city name (improve with NER later)
    # naive approach: last token(s) after 'in'
    city = None
    if " in " in user_q.lower():
        city = user_q.split(" in ", 1)[1].strip().rstrip("?")
    else:
        # fallback: attempt to use the whole query
        city = user_q.strip()

    weather = get_weather(city)
    if weather is None:
        # ask LLM to give a fallback answer
        return {"ai_response": "Sorry, I couldn't fetch weather right now. Try specifying the city clearly."}
    # format nicely using LLM (optional)
    prompt = (
        f"User asked: {user_q}\n\n"
        f"Weather data: {weather}\n\n"
        "Provide a concise user-facing answer (2-3 sentences)."
    )
    reply = llm.invoke(prompt)
    return {"ai_response": reply}
