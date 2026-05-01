import streamlit as st
import torch
import cv2
import numpy as np
import time
import os
from transformers import BlipProcessor, BlipForConditionalGeneration
import requests
import tempfile
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

device = "cuda" if torch.cuda.is_available() else "cpu"


@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    ).to(device)
    return processor, model


processor, model = load_model()

if "audio_files" not in st.session_state:
    st.session_state.audio_files = []


def translate_text(text, src="en", dest="fr"):
    try:
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair={src}|{dest}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            translated = data.get("responseData", {}).get("translatedText", "")
            if translated:
                return translated
        return text
    except Exception:
        return text


def describe_image(image):
    inputs = processor(image, return_tensors="pt").to(device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=100)
    description_en = processor.decode(output[0], skip_special_tokens=True)
    description_fr = translate_text(description_en, src="en", dest="fr")
    description_wo = translate_text(description_en, src="en", dest="wo")
    return description_en, description_fr, description_wo


def text_to_speech(text, lang):
    try:
        tts = gTTS(text, lang=lang)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        st.session_state.audio_files.append(temp_file.name)
        return temp_file.name
    except Exception:
        return None


def delete_audio(file):
    try:
        if os.path.exists(file):
            os.remove(file)
    except OSError:
        pass
    if file in st.session_state.audio_files:
        st.session_state.audio_files.remove(file)
    st.rerun()


def load_font(size=40):
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Windows/Fonts/arial.ttf",
    ]
    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def overlay_text(img_pil, description, font):
    draw = ImageDraw.Draw(img_pil)
    text_x, text_y = 20, 50
    text_bbox = draw.textbbox((0, 0), description, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    padding = 20
    border_radius = 15
    bg_color = (173, 216, 230, 180)

    overlay = Image.new("RGBA", img_pil.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    x1, y1 = text_x - padding, text_y - padding
    x2, y2 = text_x + text_width + padding, text_y + text_height + padding
    overlay_draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=border_radius, fill=bg_color)

    img_pil = Image.alpha_composite(img_pil.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img_pil)
    draw.text((text_x, text_y), description, font=font, fill=(255, 255, 255))
    return img_pil


# Interface
st.title("Vision AI : Analyse Video en Direct")

st.subheader("Audios generes :")
with st.container():
    for idx, audio_file in enumerate(list(st.session_state.audio_files)):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.audio(audio_file, format="audio/mp3")
        with col2:
            if st.button("Supprimer", key=f"delete_{idx}"):
                delete_audio(audio_file)

run = st.checkbox("Demarrer la video")
lang_choice = st.selectbox("Choisissez la langue :", ["Anglais", "Francais", "Wolof"])

font = load_font(size=40)

if run:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Impossible d'acceder a la webcam. Verifiez qu'elle est connectee et autorisee.")
    else:
        stframe = st.empty()
        last_analysis_time = 0
        description_en, description_fr, description_wo = "", "", ""

        while run:
            ret, frame = cap.read()
            if not ret:
                st.error("Erreur lors de la capture video.")
                break

            img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            now = time.time()

            if now - last_analysis_time >= 5:
                description_en, description_fr, description_wo = describe_image(img_pil)
                last_analysis_time = now

                if lang_choice == "Anglais":
                    description = description_en
                    audio_lang = "en"
                elif lang_choice == "Francais":
                    description = description_fr
                    audio_lang = "fr"
                else:
                    description = description_wo
                    audio_lang = "fr"

                audio_path = text_to_speech(description, audio_lang)
                if audio_path:
                    st.audio(audio_path, format="audio/mp3")
            else:
                if lang_choice == "Anglais":
                    description = description_en
                elif lang_choice == "Francais":
                    description = description_fr
                else:
                    description = description_wo

            if description:
                img_pil = overlay_text(img_pil, description, font)

            frame_out = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            stframe.image(frame_out, channels="BGR")

        cap.release()
