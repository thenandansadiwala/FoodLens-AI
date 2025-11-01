
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

st.set_page_config(
    page_title="FoodLens AI",
    layout="centered"
)

st.title("FoodLens AI 🍽 ")
st.write("Upload a picture of your meal, recognize it, and get the nutritional breakdown.")

if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'food_options' not in st.session_state:
    st.session_state.food_options = []
if 'nutrition_info' not in st.session_state:
    st.session_state.nutrition_info = None
if 'error_message' not in st.session_state:
    st.session_state.error_message = None


uploaded_file = st.file_uploader(
    "Upload an image of your food :",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    if st.session_state.uploaded_image is None or uploaded_file.getvalue() != st.session_state.uploaded_image['bytes']:
        st.session_state.uploaded_image = {"bytes": uploaded_file.getvalue(), "name": uploaded_file.name}
        st.session_state.food_options = []
        st.session_state.nutrition_info = None
        st.session_state.error_message = None

if st.session_state.uploaded_image:
    st.image(st.session_state.uploaded_image['bytes'], caption="Your Meal", use_container_width =True)

    if st.button("Recognize Food", key="recognize_btn"):
        with st.spinner("Analyzing your meal... 🥗"):
            files = {'file': (st.session_state.uploaded_image['name'], st.session_state.uploaded_image['bytes'], 'image/jpeg')}
            try:
                response = requests.post(f"{API_BASE_URL}/recognize-food/", files=files)
                response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
                
                st.session_state.food_options = response.json().get("predictions", [])
                st.session_state.error_message = None
                if not st.session_state.food_options:
                     st.session_state.error_message = "Could not identify food in the image. Please try another one or enter the name manually."

            except requests.exceptions.RequestException as e:
                st.session_state.error_message = f"API Error: {e}"
            except Exception as e:
                st.session_state.error_message = f"An unexpected error occurred: {e}"

if st.session_state.error_message:
    st.error(st.session_state.error_message)

if st.session_state.food_options:
    st.subheader("What food is this?")

    with st.form("nutrition_form"):
        selected_option = st.radio(
            "Select the best match:",
            options=st.session_state.food_options
        )

        manual_input = st.text_input(
            "Or, correct the name here:",
            placeholder="e.g., 'cheese pizza'"
        )

        get_nutrition_button = st.form_submit_button("Get Nutritional Info")

        if get_nutrition_button:
            final_food_name = manual_input.strip() if manual_input.strip() else selected_option

            if final_food_name:
                with st.spinner(f"Fetching details for {final_food_name}..."):
                    try:
                        params = {'food_name': final_food_name}
                        response = requests.get(f"{API_BASE_URL}/get-nutrition/", params=params)
                        response.raise_for_status()

                        st.session_state.nutrition_info = response.json()
                        st.session_state.error_message = None

                    except requests.exceptions.RequestException as e:
                        st.session_state.nutrition_info = None
                        st.session_state.error_message = f"Could not fetch data for '{final_food_name}'. Please try another name."
            else:
                st.warning("Please select or enter a food name.")

if st.session_state.nutrition_info:
    st.subheader(f"Nutritional Breakdown: {st.session_state.nutrition_info.get('food_name', 'N/A')}")
    info = st.session_state.nutrition_info

    st.write(f"**Serving Size:** {info.get('serving_size_grams', 0)}g")

    col1, col2, col3 = st.columns(3)
    col1.metric("Calories (kcal)", f"{info.get('calories', 0)}")
    col2.metric("Protein (g)", f"{info.get('protein_grams', 0)}")
    col3.metric("Fat (g)", f"{info.get('fat_grams', 0)}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Carbs (g)", f"{info.get('carbohydrates_grams', 0)}")
    col5.metric("Fiber (g)", f"{info.get('fiber_grams', 0)}")
    col6.metric("Sugar (g)", f"{info.get('sugar_grams', 0)}")