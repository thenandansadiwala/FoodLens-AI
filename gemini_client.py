import json
import os
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Initialize client once
client = genai.Client(api_key=os.getenv("gemini_api_key"))


def get_food_recognition_options(image_bytes: bytes) -> list:
    """
    Takes an image of food and returns up to 5 possible food names.

    Args:
        image_bytes: The image data in bytes.

    Returns:
        A list of predicted food names.
    """
    MODEL = "gemini-2.5-flash"
    
    SYSTEM_PROMPT = """Please identify the food item in this image.
        Provide a JSON object with a single key "predictions" which is a list of up to 5 possible names for the food, from most to least likely.
        
        Example:
        {"predictions": ["Spaghetti Bolognese", "Pasta with meat sauce", "Spaghetti", "Italian pasta dish", "Noodles with sauce"]}
        
        Return only the JSON object.
    """
    

    system_content = types.Content(
        parts=[types.Part.from_text(text=SYSTEM_PROMPT),
        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")]
    )
    # Attach the Google Search tool
    tools = [ types.Tool(googleSearch=types.GoogleSearch()) ]


    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        tools=tools,
    )

    # Non‐streaming call
    response = client.models.generate_content(
        model=MODEL,
        contents=[system_content],
        config=config,
    )
    print(f"Food Recognition Response: {response.text}")
    try:
        # Clean up the response to extract pure JSON
        json_str = response.text.strip().replace('```json\n', '').replace('\n```', '')
        predictions = json.loads(json_str)
        return predictions.get("predictions", [])
    except (json.JSONDecodeError, KeyError, Exception) as e:
        print(f"Error processing food recognition: {e}")
        return [] # Return an empty list on failure

def get_nutritional_info(food_name: str) -> dict:
    """
    Gets nutritional information for a given food name, tailored for fitness enthusiasts.
    
    Args:
        food_name: The name of the food item.
        
    Returns:
        A dictionary with fixed nutritional attributes.
    """
    MODEL = "gemini-2.5-flash"
    
    SYSTEM_PROMPT = f"""
    You are a nutrition expert for fitness enthusiasts.
    Provide a nutritional breakdown for a standard serving size (around 100g-200g) of the following food: "{food_name}".

    Provide a JSON object with the following fixed attributes:
    - "food_name": The name of the food.
    - "serving_size_grams": The serving size in grams (e.g., 150).
    - "calories": Total calories (in kcal).
    - "protein_grams": Protein in grams.
    - "carbohydrates_grams": Total carbohydrates in grams.
    - "fat_grams": Total fat in grams.
    - "fiber_grams": Fiber in grams.
    - "sugar_grams": Sugar in grams.
    
    All values for the nutritional attributes should be numbers. If a value is unknown, use 0.
    
    Example response for "Grilled Chicken Breast":
    {{
      "food_name": "Grilled Chicken Breast",
      "serving_size_grams": 150,
      "calories": 248,
      "protein_grams": 45,
      "carbohydrates_grams": 0,
      "fat_grams": 7,
      "fiber_grams": 0,
      "sugar_grams": 0
    }}
    
    Return only the JSON object and nothing else.
    """

    system_content = types.Content(
        parts=[types.Part.from_text(text=SYSTEM_PROMPT)])
    # Attach the Google Search tool
    tools = [ types.Tool(googleSearch=types.GoogleSearch()) ]

    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        tools=tools,
    )

    # Non‐streaming call
    response = client.models.generate_content(
        model=MODEL,
        contents=[system_content],
        config=config,
    )
    print(f"Nutritional Info Response: {response.text}")
    try:
        # Clean up the response to extract pure JSON
        json_str = response.text.strip().replace('```json\n', '').replace('\n```', '')
        nutrition_data = json.loads(json_str)
        return nutrition_data
    except (json.JSONDecodeError, KeyError, Exception) as e:
        print(f"Error fetching nutritional data: {e}")
        return {} # Return an empty dict on failure
