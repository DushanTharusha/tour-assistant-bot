# backend/test_tools.py
from backend.tools import recommend_destinations, search_hotels, get_weather, format_hotels_with_context
import os
os.environ["OPENWEATHER_API_KEY"] = "506efa32e98e94af86d1b9c3ffc0ae41"

def t1():
    print("=== Destinations ===")
    print(recommend_destinations("I like beaches and history", n=3))

def t2():
    print("=== Hotels (RAG) ===")
    r = search_hotels("hotels in Colombo near beach", top_k=3)
    for i, item in enumerate(r, 1):
        print(i, item.get("text") if isinstance(item, dict) else item)

def t3():
    print("=== Weather ===")
    w = get_weather("Colombo")
    print(w)

def t4():
    print("=== Hotels Summary (LLM formatted) ===")
    print(format_hotels_with_context("budget hotels in Kandy", top_k=3))

if __name__ == "__main__":
    t1(); t2(); t3(); t4()
