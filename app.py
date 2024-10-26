import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Function to calculate BMI
def calculate_bmi(weight, height, gender):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    if gender == "Male":
        bmi += 1
    return bmi

# Function to categorize BMI
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "You may be underweight. Consider consulting with a healthcare professional."
    elif 18.5 <= bmi < 25:
        return "Normal weight", "You are within the normal weight range. Keep up the good work!"
    elif 25 <= bmi < 30:
        return "Overweight", f"You are overweight. Consider incorporating more physical activity and healthier eating habits to get to a normal weight. You should reduce your weight by {bmi - 24.9:.2f} kg to reach a normal weight."
    else:
        return "Obese", f"You are obese. It's important to prioritize your health and consider seeking guidance from a healthcare professional. You should reduce your weight by {bmi - 24.9:.2f} kg to reach a normal weight."

# Function to generate BMI report PDF with improved formatting and design
def generate_pdf(name, age, gender, weight, height, bmi, bmi_category, comment, chart_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="BMI Report", ln=True, align="C")
    pdf.ln(10)
    
    # User information
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)
    pdf.ln(10)
    
    # BMI information
    pdf.cell(200, 10, txt=f"Weight (kg): {weight}", ln=True)
    pdf.cell(200, 10, txt=f"Height (cm): {height}", ln=True)
    pdf.cell(200, 10, txt=f"BMI: {bmi:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Category: {bmi_category}", ln=True)
    pdf.ln(10)
    
    # Comment
    pdf.cell(200, 10, txt="Comment:", ln=True)
    pdf.multi_cell(200, 10, txt=comment)
    pdf.ln(10)
    
    # BMI distribution chart
    pdf.cell(200, 10, txt="BMI Distribution", ln=True)
    pdf.image(chart_path, x=10, y=pdf.get_y() + 5, w=180)
    
    return pdf

# Main content
st.title("BMI Calculator and Report")

name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=0, max_value=150)
gender = st.radio("Select your gender:", ("Male", "Female"))
weight = st.number_input("Weight (in kg)", min_value=0.0)
height = st.number_input("Height (in cm)", min_value=0.0)

if st.button("Generate Report"):
    # Calculate BMI
    bmi = calculate_bmi(weight, height, gender)
    bmi_category, comment = get_bmi_category(bmi)

    # Display BMI
    st.subheader("BMI Result:")
    st.write(f"Your BMI is: {bmi:.2f}")
    st.write(f"Category: {bmi_category}")
    st.write(f"Comment: {comment}")

    # Generate BMI distribution bar chart
    categories = ['Underweight', 'Normal weight', 'Overweight', 'Obese']
    counts = [0, 0, 0, 0]
    counts[categories.index(bmi_category)] = 1

    plt.figure(figsize=(8, 6))
    plt.bar(categories, counts, color=['red', 'green', 'blue', 'orange'])
    plt.xlabel('BMI Category')
    plt.ylabel('Count')
    plt.title('BMI Distribution')
    plt.xticks(rotation=45)

    chart_path = "bmi_chart.png"
    plt.savefig(chart_path)
    plt.close()

    st.image(chart_path, use_column_width=True)

    # Generate PDF report and download
    pdf = generate_pdf(name, age, gender, weight, height, bmi, bmi_category, comment, chart_path)
    download_path = "BMI_Report.pdf"
    pdf.output(download_path, 'F')

    with open(download_path, "rb") as f:
        st.download_button(
            label="Download Report",
            data=f.read(),
            file_name="BMI_Report.pdf",
            mime="application/pdf",
        )
