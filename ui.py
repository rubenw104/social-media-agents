import streamlit as st
from PIL import Image
import os
from image_retrieve import image_retrieve, clean_folder
from post_generation import generate_post

st.header('Benvenuto in Gengram:')
st.subheader('L\'applicazione che ti suggerisce post da pubblicare su instagram!')
st.write('Inserisci l\'argomento del post che vuoi pubblicare')

with st.form("Argomento"):
    argomento = st.text_input("Argomento:")
    submitted = st.form_submit_button("Cerca immagine")

if submitted and argomento:
    image_retrieve(argomento, max_results=3)

# Cartella immagini
cartella = "downloads"
immagini = os.listdir(cartella)

# Layout a colonne per le anteprime
cols = st.columns(3)

# Variabile per tracciare l'immagine selezionata
if "selezionata" not in st.session_state:
    st.session_state.selezionata = None
    st.session_state.id_selezionata= None

# Mostra le immagini come pulsanti cliccabili
for i, img_file in enumerate(immagini[:3]):
    with cols[i % 3]:  # 3 colonne, a rotazione
        img_path = os.path.join(cartella, img_file)
        if img_path == 'downloads/urls.txt':
            continue

        img = Image.open(img_path)
        st.image(img)

        if st.button(f"Scegli Immagine {i+1}"):
            st.session_state.selezionata = img_file
            st.session_state.id_selezionata = i+1

# Se è stata selezionata un'immagine, la mostriamo in grande
if st.session_state.selezionata is not None:
    st.subheader(f"Stai selezionando: Immagine {st.session_state.id_selezionata}")
    img = Image.open(os.path.join(cartella, st.session_state.selezionata))
    st.image(img)

if st.button(f"Genera Prompt"):
    st.write(generate_post(argomento))