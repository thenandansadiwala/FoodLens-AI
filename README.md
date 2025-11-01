# 🥗 FoodLens AI

A modern web application that uses the **Google Gemini AI** to recognize food from an image, allowing users to get a detailed nutritional breakdown tailored for fitness enthusiasts.  
This project is built with a **FastAPI backend** and a **Streamlit frontend**.

---

## ✨ Features

- **AI-Powered Food Recognition:** Upload an image of any meal and let the Gemini Vision model identify it.  
- **Multiple Suggestions:** The AI provides up to 5 possible names for the food, ensuring higher accuracy.  
- **Manual Correction:** Users can manually enter or correct the food name.  
- **Detailed Nutritional Analysis:** Get a gym-focused breakdown including calories, protein, carbs, fat, fiber, and sugar.  
- **Decoupled Architecture:** A robust FastAPI backend handles the AI logic, while a user-friendly Streamlit frontend provides the interface.  
- **Interactive UI:** A simple, step-by-step process makes the app intuitive and easy to use.  

---

## 🛠️ Technology Stack

| Component | Technology |
|------------|-------------|
| **Backend** | Python, FastAPI, Uvicorn |
| **Frontend** | Streamlit |
| **AI Model** | Google Gemini Models |
| **Core Libraries** | requests, Pillow, python-dotenv (optional for security) |

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### 1. Prerequisites

- Python 3.8+  
- Git  
- A **Google Gemini API Key** → Get one from [Google AI Studio](https://makersuite.google.com/).

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 3. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.venv\Scripts\activate
```

### 4. Install Dependencies

Install all the required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Configure Your API Key

Open the `gemini_client.py` file and replace the placeholder with your actual Google Gemini API key.  

> 💡 For better security, consider using **environment variables** to store your API key.

---

## ▶️ How to Run the Application

This project has two parts — backend and frontend — that need to be run **simultaneously** in separate terminal windows.

### Step 1: Start the Backend API Server

Run the FastAPI server using Uvicorn:

```bash
uvicorn api:app --reload
```

You should see output indicating that the server is running (usually at [http://127.0.0.1:8000](http://127.0.0.1:8000)).  
Keep this terminal open.

### Step 2: Start the Frontend Streamlit App

Open a new terminal and activate the virtual environment again if necessary. Then, run the Streamlit application:

```bash
streamlit run app.py
```

This will automatically open a new tab in your web browser with the application running.  
You are now ready to upload images! 🎉

---

## 🔌 API Endpoints

You can test the backend endpoints interactively at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **POST** | `/recognize-food/` | Accepts an image file (.jpg, .png) and returns a list of predicted food names. |
| **GET** | `/get-nutrition/` | Accepts a `food_name` query parameter and returns its nutritional information. |
| **GET** | `/` | Root endpoint to check if the API is running. |

---

## 🔮 Future Improvements

This project has a solid foundation that can be extended with more features:

- **User Accounts & History:** Allow users to sign up, log their meals, and track their nutritional intake.  
- **Database Integration:** Store nutritional data and user history in a database like SQLite or PostgreSQL.  
- **Barcode Scanning:** Add functionality to scan barcodes on packaged foods for instant nutritional data.  
- **Dockerize Application:** Containerize the frontend and backend for easier deployment.  
- **CI/CD Pipeline:** Implement a CI/CD pipeline using GitHub Actions to automate testing and deployment.


