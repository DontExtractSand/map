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
            facebook_handle = matching_row['facebook'].values[0]

            ### Twitter Message ###
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
            
            ### Facebook Message ###
            if pd.notna(facebook_handle) and facebook_handle != '':
                # Build the Facebook message
                facebook_message = f"""
                Le 7 juillet dernier, un formidable élan s’est levé dans le pays pour battre dans les urnes l’extrême-droite, ses idées et son programme.

                Pourtant, Emmanuel Macron refuse d’entendre l’appel des urnes. Pire, il s’entête et forme un gouvernement sans légitimité politique ou populaire, en nommant Michel Barnier, dont le gouvernement réactionnaire perpétuera une politique de mépris et de casse sociale, grâce à la bienveillance du RN. Les propos scandaleux du ministre de l’Intérieur Retailleau sur l’immigration et sur l’Etat de droit en sont les premières preuves. 

                @{facebook_handle}, montrez-vous digne du front républicain, et refusez l’alliance de fait entre Emmanuel Macron, la droite radicalisée et l’extrême-droite. Votez la censure.
                """

                # Generate the Facebook share URL
                facebook_url = f"https://www.facebook.com/sharer/sharer.php?u=https://yourwebsite.com&quote={facebook_message}"

                # Display the link to post on Facebook
                st.write("Click the link below to post the following message on Facebook:")
                st.write(f"**Facebook Message**: {facebook_message}")
                st.markdown(f"[Click here to Post on Facebook]({facebook_url})")
            else:
                st.write("This député does not have a Facebook handle.")
        else:
            st.write("No matching député found.")
else:
    st.write("Data could not be loaded.")
