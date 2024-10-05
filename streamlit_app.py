import streamlit as st
import pandas as pd
import urllib.parse

# Display title and description of the app
st.title("Les suites du front républicain")
st.write("""
Cette application vous aide à trouver les coordonnées de votre député puis vous permet de l'appeler à voter la censure de ce gouvernement.
Si vous avez besoin d'aide pour trouver votre circonscription, vous pouvez utiliser cette carte :
""")
st.page_link("https://www2.assemblee-nationale.fr/recherche-localisee/carte/FRANCE", label="https://www2.assemblee-nationale.fr/recherche-localisee/carte/FRANCE")

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
    departement = st.selectbox("Choisissez votre département", departement_codes)
    circonscription = st.selectbox("Choisissez votre circonscription", circo_values)

    # Button to submit the selection
    if st.button("Soumettre"):
        # Find the matching row
        matching_row = df[(df['departementCode'] == departement) & (df['circo'] == circonscription)]

        # Display results
        if not matching_row.empty:
            st.write("Voici les coordonnées du député correspondant :")
            st.write(matching_row)

            # Extract the Twitter handle from the matching row
            twitter_handle = matching_row['twitter'].values[0]
            facebook_handle = matching_row['facebook'].values[0]

            ### Twitter Message ###
            if pd.notna(twitter_handle) and twitter_handle != '':
                # Build the tweet message
                tweet_message = f"{twitter_handle} Sauf erreur de notre part, vous avez été élu·e grâce aux voix du front républicain. Il est encore temps d’en être digne. Votez la censure contre ce Gouvernement qui remet en cause l’état de droit et continuera la casse des services publics."

                # URL encode the tweet message to handle special characters
                encoded_tweet_message = urllib.parse.quote(tweet_message)

                # Generate the Twitter URL
                twitter_url = f"https://twitter.com/intent/tweet?text={encoded_tweet_message}"

                # Display the link to tweet
                st.write("**Solution 1 : Interpeler votre député sur X/Twitter** avec le message suivant :")
                st.write(f"**Votre tweet **: {tweet_message}")
                st.markdown(f"[Cliquer ici pour twitter ce message]({twitter_url})")
            else:
                st.write("Ce député n'a pas de compte Twitter connu dans notre base.")
            
            ### Facebook Message ###
            if pd.notna(facebook_handle) and facebook_handle != '':
                # Build the Facebook message
                facebook_message = f"""
                Le 7 juillet dernier, un formidable élan s’est levé dans le pays pour battre dans les urnes l’extrême-droite, ses idées et son programme. Pourtant, Emmanuel Macron refuse d’entendre l’appel des urnes. Pire, il s’entête et forme un gouvernement sans légitimité politique ou populaire, en nommant Michel Barnier, dont le gouvernement réactionnaire perpétuera une politique de mépris et de casse sociale, grâce à la bienveillance du RN. Les propos scandaleux du ministre de l’Intérieur Retailleau sur l’immigration et sur l’Etat de droit en sont les premières preuves. @{facebook_handle}, montrez-vous digne du front républicain, et refusez l’alliance de fait entre Emmanuel Macron, la droite radicalisée et l’extrême-droite. Votez la censure.
                """

                # URL encode the tweet message to handle special characters
                encoded_facebook_message = urllib.parse.quote(facebook_message)

                # Generate the Facebook share URL
                facebook_url = f"https://www.facebook.com/sharer/sharer.php?u=https://yourwebsite.com&quote={encoded_facebook_message}"

                # Display the link to post on Facebook
                st.write("**Solution 1 : Interpeler votre député sur Facebook** avec le message suivant :")
                st.write(f"**Message Facebook**: {facebook_message}")
                st.markdown(f"[Cliquer ici pour poster sur Facebook]({facebook_url})")
            else:
                st.write("Ce député n'a pas de compte Facebook connu dans notre base.")
        else:
            st.write("Nous n'avons pas trouvé de député correspondant.")
else:
    st.write("Erreur : la donnée source n'est pas disponible.")
