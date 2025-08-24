import streamlit as st
import pandas as pd
import os

# File to store user data
DATA_FILE = "bmi_data.csv"

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_m = height / 100  # convert cm to meters
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

# Function to determine category
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Meal plan and exercise suggestions
meal_plans = {
    "Underweight": "High protein diet, nuts, milk, rice, banana smoothies.",
    "Normal": "Balanced diet with fruits, vegetables, whole grains, lean protein.",
    "Overweight": "Low-carb diet, more vegetables, avoid fried foods.",
    "Obese": "Very low-carb, high-fiber diet. Avoid sugar. More salads & soups."
}

exercises = {
    "Underweight": "Light weight training, yoga, brisk walking.",
    "Normal": "30 mins daily exercise, jogging, yoga.",
    "Overweight": "Cardio, brisk walking, cycling 40 mins/day.",
    "Obese": "Start with walking, light aerobics, gradually increase intensity."
}

# Streamlit app UI
st.title("🏋️ BMI Calculator with Meal & Exercise Suggestions")

name = st.text_input("Enter your Name")
age = st.number_input("Enter your Age", min_value=1, max_value=120, step=1)
gender = st.radio("Select Gender", ["Male", "Female", "Other"])
height = st.number_input("Enter Height (cm)", min_value=50, max_value=250)
weight = st.number_input("Enter Weight (kg)", min_value=10, max_value=300)

if st.button("Calculate BMI"):
    if name and age and height and weight:
        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)
        
        st.success(f"Hello {name}, your BMI is **{bmi}**")
        st.info(f"You are categorized as: **{category}**")
        
        st.write(f"🍽️ Suggested Meal Plan: {meal_plans[category]}")
        st.write(f"💪 Suggested Exercises: {exercises[category]}")

        # Save data
        new_data = pd.DataFrame([[name, age, gender, height, weight, bmi, category]],
                                columns=["Name", "Age", "Gender", "Height", "Weight", "BMI", "Category"])
        
        if os.path.exists(DATA_FILE):
            old_data = pd.read_csv(DATA_FILE)
            updated_data = pd.concat([old_data, new_data], ignore_index=True)
        else:
            updated_data = new_data
        
        updated_data.to_csv(DATA_FILE, index=False)
        st.success("✅ Your data has been saved!")

# Show saved data
if os.path.exists(DATA_FILE):
    st.subheader("📊 Saved User Data")
    df = pd.read_csv(DATA_FILE)
    st.dataframe(df)
