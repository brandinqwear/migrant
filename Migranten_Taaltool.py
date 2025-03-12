import streamlit as st
import requests
import openai

def ocr_online(image_file):
    url = "https://api.ocr.space/parse/image"
    response = requests.post(
        url,
        files={"file": image_file},
        data={"apikey": "K84938341388957", "language": "nld"},
    )
    return response.json().get("ParsedResults", [{}])[0].get("ParsedText", "")

def simplify_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",  
        messages=[
            {"role": "system", "content": "Herschrijf de volgende tekst in eenvoudige Nederlandse taal."},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content']

st.title("📄 Makkelijk Nederlands: Begrijp je brieven")
st.write("Upload een foto van je brief of typ de tekst handmatig in om een eenvoudige uitleg te krijgen!")

# Mogelijkheid om een foto te uploaden
uploaded_file = st.file_uploader("Upload hier je brief (JPG, PNG of PDF)", type=["jpg", "png", "pdf"])

# Mogelijkheid om handmatig tekst in te voeren
manual_text = st.text_area("Of voer de tekst hier in:")

if uploaded_file or manual_text:
    if uploaded_file:
        text = ocr_online(uploaded_file)
    else:
        text = manual_text
    
    st.subheader("📜 Originele tekst:")
    st.text_area("", text, height=200)
    
    if st.button("📝 Maak het eenvoudiger"):
        simplified_text = simplify_text(text)
        st.subheader("✅ Eenvoudige uitleg:")
        st.text_area("", simplified_text, height=200)
        
        if st.button("🔊 Voorlezen"):
            st.audio("generated_audio.mp3")  # Hier kun je een text-to-speech functie toevoegen

st.write("🔹 Deze tool helpt migranten om brieven beter te begrijpen zonder hulp van anderen!")
