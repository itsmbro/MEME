import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import base64

# Funzione per convertire HEIC in JPEG
def convert_heic_to_jpeg(image_file):
    try:
        from PIL import Image
        image = Image.open(image_file)
        with io.BytesIO() as output:
            image.save(output, format="JPEG")
            return output.getvalue()
    except Exception as e:
        return None

# Funzione per aggiungere testo all'immagine
def aggiungi_testo(img, testo):
    # Carica il font (se hai un file TTF, puoi usarlo. Altrimenti, usa il font predefinito)
    try:
        font = ImageFont.load_default()  # Carica un font di default
        draw = ImageDraw.Draw(img)
        # Posizione e colore del testo
        width, height = img.size
        text_width, text_height = draw.textsize(testo, font=font)
        position = ((width - text_width) // 2, height - text_height - 10)
        draw.text(position, testo, font=font, fill="white")
    except Exception as e:
        st.write("Errore nell'aggiungere il testo:", e)
    return img

# Funzione per visualizzare l'immagine come base64 per l'output HTML
def img_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Streamlit app
st.title("Generatore di Meme Personalizzati")

# Caricamento dell'immagine
uploaded_image = st.file_uploader("Carica un'immagine", type=["jpg", "jpeg", "png", "heic"])

if uploaded_image is not None:
    # Controlla il tipo di immagine e convertila se necessario
    if uploaded_image.name.lower().endswith('.heic'):
        # Converte HEIC in JPEG
        img_data = convert_heic_to_jpeg(uploaded_image)
        if img_data:
            img = Image.open(io.BytesIO(img_data))
            st.image(img, caption="Immagine caricata (HEIC convertita in JPEG)", use_column_width=True)
        else:
            st.error("Impossibile convertire il formato HEIC.")
    else:
        img = Image.open(uploaded_image)
        st.image(img, caption="Immagine caricata", use_column_width=True)

    # Aggiungi campo per inserire il testo
    testo_meme = st.text_input("Scrivi il testo per il meme:")

    if testo_meme:
        # Aggiungi il testo all'immagine
        img_con_testo = aggiungi_testo(img, testo_meme)
        st.image(img_con_testo, caption="Il tuo meme!", use_column_width=True)
        
        # Salva il meme in formato PNG per il download
        with io.BytesIO() as output:
            img_con_testo.save(output, format="PNG")
            meme_data = output.getvalue()
        
        # Genera un link per scaricare il meme
        st.download_button(
            label="Scarica il tuo meme",
            data=meme_data,
            file_name="meme.png",
            mime="image/png"
        )
