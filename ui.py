import streamlit as st
from PIL import Image
import os
from image_retrieve import image_retrieve, clean_folder
from post_generation import generate_post

st.header('Welcome to Gengram:')
st.subheader('The app that suggests contents to post on Instagram!')
st.write('Please enter the topic of the post you want to publish.')

if 'cleaned' not in st.session_state:
    st.session_state.cleaned = True
    clean_folder('downloads')

with st.form("Topic"):
    argomento = st.text_input("Topic:")
    submitted = st.form_submit_button("Search for Immages")

# Variabile per tracciare l'immagine selezionata
if "selezionata" not in st.session_state:
    st.session_state.selezionata = None
    st.session_state.id_selezionata= None


if submitted and argomento:
    image_retrieve(argomento, max_results=3)
    st.session_state.selezionata = None
    st.session_state.id_selezionata= None

# Cartella immagini
cartella = "downloads"
immagini = os.listdir(cartella)

# Layout a colonne per le anteprime
cols = st.columns(3)


# Mostra le immagini come pulsanti cliccabili
for i, img_file in enumerate(immagini[:3]):
    with cols[i % 3]:  # 3 colonne, a rotazione
        img_path = os.path.join(cartella, img_file)
        if img_path == 'downloads/urls.txt':
            continue

        img = Image.open(img_path)
        st.image(img)

        if st.button(f"Select Immage {i+1}"):
            st.session_state.selezionata = img_file
            st.session_state.id_selezionata = i+1

# Se è stata selezionata un'immagine, la mostriamo in grande
if st.session_state.selezionata is not None:
    st.subheader(f"You are selecting: Immage {st.session_state.id_selezionata}")
    img = Image.open(os.path.join(cartella, st.session_state.selezionata))
    st.image(img)

    if st.button(f"Generate Caption"):
        st.write(generate_post(argomento))