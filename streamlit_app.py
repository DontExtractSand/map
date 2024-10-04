import streamlit as st
import pandas as pd

# Display title and description of the app
st.title("Député Finder App")
st.write("""
This app helps you find your député based on your département and circonscription.
Simply select your département and circonscription, and the app will display the details of the matching député.
""")

# Function to load the CSV file from GitHub
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/DontExtractSand/map/refs/heads/main/deputes-active.csv"
    data = pd.read_csv(url)
    return data

# Load the data from the GitHub repository
df = load_data()

if df is not None:
    # Extract and sort unique values for departementCode and circo
    departement_codes = sorted(df['departementCode'].unique())  # Sort numerically or alphabetically
    circo_values = sorted(df['circo'].unique())  # Sort numerically or alphabetically

    # Dropdowns for user input
    departement = st.selectbox("Select your Département", departement_codes)
    circonscription = st.selectbox("Select your Circonscription", circo_values)
    
# Find the matching row
matching_row = df[(df['departementCode'] == departement) & (df['circo'] == circonscription)]

# Display results
if not matching_row.empty:
    st.write("Here are the details of the matching député:")
    st.write(matching_row)
else:
    st.write("No matching député found.")
