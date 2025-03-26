import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import tempfile

# Autenticación con Google Sheets desde secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Crear archivo temporal desde secrets
temp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
temp_json.write(json.dumps(st.secrets["gcp_service_account"]).encode())
temp_json.close()

creds = ServiceAccountCredentials.from_json_keyfile_name(temp_json.name, scope)
client = gspread.authorize(creds)

# Abre la hoja de Google
sheet = client.open("anunciatext_clientes").worksheet("Hoja 1")

st.set_page_config(page_title="Anunciatext", layout="centered")
st.title("📲 Regístrate para recibir promociones")

with st.form("registro_form"):
    nombre = st.text_input("Nombre completo")
    telefono = st.text_input("Teléfono o WhatsApp")
    correo = st.text_input("Correo electrónico (opcional)", placeholder="example@email.com")
    enviar = st.form_submit_button("Recibir promociones")

    if enviar:
        if nombre and telefono:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([nombre, telefono, correo, fecha])
            st.success("🎉 ¡Gracias! Tus datos fueron registrados con éxito.")
        else:
            st.warning("Por favor completa al menos tu nombre y teléfono.")
