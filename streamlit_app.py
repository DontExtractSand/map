import streamlit as st
import pandas as pd
import urllib.parse

# Display title and description of the app
st.title("Parce que le barrage républicain ne s'arrête pas après l'élection !")
st.write("""
Cette application vous aide à trouver les coordonnées complètes de votre député puis vous permet de l'appeler à voter la censure de ce gouvernement. **Le texte vise les parlementaires élu.e.s avec les voix du barrage républicain, mais à vous de vous assurer que c'est le cas pour votre député**.
Si vous avez besoin d'aide pour trouver votre circonscription, vous pouvez utiliser cette carte :
""")
st.page_link("https://www2.assemblee-nationale.fr/recherche-localisee/carte/FRANCE", label="https://www2.assemblee-nationale.fr/recherche-localisee/carte/FRANCE")

# Function to load the CSV file from GitHub
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/DontExtractSand/map/refs/heads/main/deputes-active-hors-RN.csv"
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
            email_address = matching_row['mail'].values[0]
            first_name = matching_row['prenom'].values[0]
            last_name = matching_row['nom'].values[0]
            civ = matching_row['civ'].values[0]
            permanence = matching_row['permanence'].values[0]

            ### Twitter Message ###
            if pd.notna(twitter_handle) and twitter_handle != '':
                # Build the tweet message
                tweet_message = f"{twitter_handle} Sauf erreur de notre part, vous avez été élu·e grâce aux voix du front républicain. Il est encore temps d’en être digne. Votez la censure contre ce Gouvernement qui remet en cause l’état de droit et continuera la casse des services publics."

                # URL encode the tweet message to handle special characters
                encoded_tweet_message = urllib.parse.quote(tweet_message)

                # Generate the Twitter URL
                twitter_url = f"https://twitter.com/intent/tweet?text={encoded_tweet_message}"

                # Display the link to tweet
                st.header("**Solution 1 : interpeler votre député sur X/Twitter** avec le message suivant :")
                st.write(f"Votre tweet : {tweet_message}")
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
                st.header("**Solution 2 : interpeler votre député sur Facebook** avec le message suivant :")
                st.write(f"Votre message Facebook : {facebook_message}")
                st.markdown(f"[Cliquer ici pour poster sur Facebook]({facebook_url})")
            else:
                st.write("Ce député n'a pas de compte Facebook connu dans notre base.")

            ### Email Message ###
            if pd.notna(email_address) and email_address != '':
                # Build the email subject and body
                email_subject = "Votez la censure pour être digne du front républicain"
                email_body = f"""
                {civ} {first_name} {last_name}, Le 7 juillet dernier, un formidable élan s’est levé dans le pays pour battre dans les urnes l’extrême-droite, ses idées et son programme. Pourtant, Emmanuel Macron refuse d’entendre l’appel des urnes. Pire, il s’entête et forme un gouvernement sans légitimité politique ou populaire, en nommant Michel Barnier, dont le gouvernement réactionnaire perpétuera une politique de mépris et de casse sociale, grâce à la bienveillance du RN. Les propos scandaleux du ministre de l’Intérieur Retailleau sur l’immigration et sur l’Etat de droit en sont les premières preuves. Montrez-vous digne du front républicain, et refusez l’alliance de fait entre Emmanuel Macron, la droite radicalisée et l’extrême-droite. Votez la censure.
                """

                # URL encode the subject and body for the mailto link
                encoded_subject = urllib.parse.quote(email_subject)
                encoded_body = urllib.parse.quote(email_body)

                # Create mailto link
                mailto_link = f"mailto:{email_address}?subject={encoded_subject}&body={encoded_body}"

                # Display the link to send an email
                st.header("**Solution 3 : écrivez par email à votre député** avec le message suivant :")
                st.write(f"L'adresse : {email_address}")
                st.write(f"Le sujet du message : {email_subject}")
                st.write(f"Votre email : {email_body}")
                st.markdown(f"[Cliquez ici pour envoyer un email]({mailto_link})")
            else:
                st.write("Ce député n'a pas d'adresse email connue dans notre base.")

            # Postcard text
            if permanence != '':
                address=permanence
            else:
                address="Assemblée nationale - 126 Rue de l'Université, 75355 Paris 07 SP"
            postcard_image_url="https://raw.githubusercontent.com/DontExtractSand/map/refs/heads/main/postcard.jpg"
            postcard_pdf_url="https://www.ecologistes-an.fr/s/Carte-postale-macronistes-1.pdf"
            
            postcard_text = f"""
            Chèr.e député.e, Le 7 juillet dernier, sauf erreur de ma part, vous avez été élu.e, lors des élections législatives, grâce aux voix du barrage républicain contre l'extrême-droite. Merci de vous montrer digne de ce barrage et de voter la censure du gouvernement Barnier. Cordialement,
            """

            # Display the postcard preview (image)
            st.header("**Solution 4 : envoyez une carte postale à votre député** avec le message suivant :")
            st.write(f"{postcard_text}")
            st.image(postcard_image_url, use_column_width=True)
            st.page_link(postcard_pdf_url, label="Lien vers le PDF pour impression")

            # Display recipient and address
            st.write(f"**Destinataire** à préciser : {first_name} {last_name}")
            st.write(f"**Addresse** (à défaut de permance connue, l'adresse de l'assemblée est utilisée) : {address}")
        
        else:
            st.write("Nous n'avons pas trouvé de député correspondant.")
else:
    st.write("Erreur : la donnée source n'est pas disponible.")
