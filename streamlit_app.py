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

    # Button to submit the selection
    if st.button("Submit"):
        # Find the matching row
        matching_row = df[(df['departementCode'] == departement) & (df['circo'] == circonscription)]

        # Display results
        if not matching_row.empty:
            st.write("Here are the details of the matching député:")
            st.write(matching_row)

            # Extract the Twitter handle from the matching row
            twitter_handle = matching_row['twitter'].values[0]

            # Check if a Twitter handle is available
            if pd.notna(twitter_handle) and twitter_handle != '':
                # Build the tweet message
                tweet_message = f"@{twitter_handle} Sauf erreur de notre part, vous avez été élu·e grâce aux voix du front républicain. Il est encore temps d’en être digne. Votez la censure contre ce Gouvernement qui remet en cause l’état de droit et continuera la casse des services publics."

                # Generate the Twitter URL
                twitter_url = f"https://twitter.com/intent/tweet?text={tweet_message}"

                # Display the link to tweet
                st.write("Click the link below to tweet the following message:")
                st.write(f"**Tweet Message**: {tweet_message}")
                st.markdown(f"[Click here to Tweet]({twitter_url})")
            else:
                st.write("This député does not have a Twitter handle.")
        else:
            st.write("No matching député found.")
else:
    st.write("Data could not be loaded.")
