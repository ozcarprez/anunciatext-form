import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Carga las credenciales desde el archivo secreto
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
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
