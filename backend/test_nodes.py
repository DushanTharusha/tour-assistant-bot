import sys
import os
os.environ["OPENWEATHER_API_KEY"] = "506efa32e98e94af86d1b9c3ffc0ae41"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.nodes.chatbot_node import chatbot_node
from data.nodes.hotels_node import hotels_node
from data.nodes.destination_node import destination_node
from data.nodes.weather_node import weather_node

print(chatbot_node({"user_input": "Tell me about cultural spots in Italy"}))
print(hotels_node({"user_input": "Find hotels in Colombo with free WiFi"}))
print(destination_node({"user_input": "I like beaches and hiking"}))
print(weather_node({"user_input": "What's the weather in Paris"}))