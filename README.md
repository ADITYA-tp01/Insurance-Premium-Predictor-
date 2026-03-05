# AI Health Insurance Predictor 🏥

An advanced Machine Learning application that provides instant and accurate health insurance cost predictions based on a user's personal, financial, and health profile. Built with Streamlit, this interactive web application uses trained models to give users a personalized estimate of their potential insurance premiums along with a health risk assessment.

## 🌟 Features

- **Interactive UI**: A modern, clean, and responsive user interface built using Streamlit.
- **Form-Based Inputs**: Collects comprehensive user data across:
  - **Personal Information**: Age, Gender, Marital Status, Dependants, Region, Genetical Risk.
  - **Financial Information**: Annual Income, Employment Status.
  - **Health & Lifestyle**: BMI Category, Smoking Status, Medical History (combinations of Diabetes, BP, Thyroid, Heart Disease).
  - **Insurance Preferences**: Bronze, Silver, or Gold plan types.
- **Accurate Predictions**: Uses distinct Machine Learning models based on age groups (Young: <= 25 years old, Rest: > 25 years old) for tailored insurance cost prediction.
- **Risk Assessment**: Calculates a normalized risk score and provides an intuitive "Low", "Medium", or "High" risk level insight with color-coded indicators.

## 💻 Tech Stack

- **Frontend/App Framework**: [Streamlit](https://streamlit.io/)
- **Data Manipulation**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn, Joblib (for model loading/saving)
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Development**: Python, Jupyter Notebooks (for model training and exploratory data analysis)

## 📁 Project Structure

```text
Insurance Premium/
│
├── artifacts/                           # Contains trained ML models and scalers
│   ├── model_young.joblib
│   ├── model_rest.joblib
│   ├── scaler_young.joblib
│   └── scaler_rest.joblib
│
├── main.py                              # Main Streamlit application file containing the UI
├── prediction_helper.py                 # Helper functions for data preprocessing, scaling, and prediction logic
│
├── premium_prediction*.ipynb            # Jupyter notebooks used for data analysis, exploration, and model training
├── premiums*.xlsx                       # Excel datasets used for training and testing
│
└── requirements.txt                     # Project dependencies
```

## 🚀 Installation & Setup

To run this application locally, follow these steps:

1. **Clone the repository or download the source code.**
2. **Navigate to the project directory:**
   ```bash
   cd "Insurance Premium"
   ```
3. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On MacOS/Linux:
   source venv/bin/activate
   ```
4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the Streamlit app:**
   ```bash
   streamlit run main.py
   ```

## 🎯 Usage

1. Launch the application using the command above.
2. The app will open in your default web browser.
3. Fill in your details in the provided sections (Personal, Financial, Health, and Insurance Plan).
4. Click the **"🎯 PREDICT MY INSURANCE COST"** button.
5. The application will process your inputs and display your estimated health insurance cost along with your calculated health risk level.

## 🧠 Under the Hood (Machine Learning)

The application uses an intelligent pipeline to handle user inputs:
- Data is preprocessed and categorical variables are one-hot encoded or label encoded based on the training set structure.
- A custom normalization function calculates a specific "Risk Score" based on a combination of medical history diseases (like diabetes, heart disease, etc.).
- Based on the user's age, the data is scaled using the appropriate pre-fitted scaler (`scaler_young` or `scaler_rest`).
- Finally, the prediction is made using the corresponding trained model (`model_young` or `model_rest`).
