import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from gemini_client import get_food_recognition_options, get_nutritional_info

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


app = FastAPI(
    title="FoodLens API",
    description="API to recognize food from images and get nutritional data.",
    version="1.0.0"
)

@app.post("/recognize-food/")
async def recognize_food_from_image(file: UploadFile = File(...)):
    """
    Accepts an image file, recognizes the food, and returns a list of predictions.

    - **file**: An image file (jpeg, png).
    """
    logging.info("Received request for /recognize-food/")

    if file.content_type not in ["image/jpeg", "image/png"]:
        logging.warning(f"Invalid file type received: {file.content_type}")
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a JPG or PNG image."
        )

    try:
        image_bytes = await file.read()
        logging.info(f"Successfully read image file: {file.filename}")

        predictions = get_food_recognition_options(image_bytes)

        if not predictions:
            logging.warning("Food recognition returned no predictions.")
            raise HTTPException(
                status_code=404,
                detail="Could not recognize any food item in the image."
            )

        logging.info(f"Successfully recognized food. Predictions: {predictions}")
        return {"predictions": predictions}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logging.error(f"An unexpected error occurred in /recognize-food/: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred while processing the image."
        )
    
@app.get("/get-nutrition/")
async def get_nutrition_details(food_name: str):
    """
    Accepts a food name and returns its nutritional information.

    - **food_name**: The name of the food item to look up.
    """
    logging.info(f"Received request for /get-nutrition/ with food_name: '{food_name}'")
    
    try:
        nutrition_data = get_nutritional_info(food_name)

        if not nutrition_data or not nutrition_data.get("calories"):
             logging.warning(f"Could not find nutritional data for '{food_name}'.")
             raise HTTPException(
                status_code=404,
                detail=f"Nutritional information could not be found for '{food_name}'."
            )

        logging.info(f"Successfully fetched nutritional data for '{food_name}'")
        return nutrition_data

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logging.error(f"An unexpected error occurred in /get-nutrition/: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred while fetching nutritional data."
        )


@app.get("/")
def read_root():
    logging.info("Health check endpoint / was called.")
    return {"status": "API is running"}

