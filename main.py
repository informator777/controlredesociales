import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Registro Redes Digitales", page_icon="🧡", layout="centered")

# --- FUNCIONES DE APOYO (Definidas antes de la interfaz) ---
def conectar_hoja():
    # En Streamlit Cloud, usamos st.secrets en lugar de un archivo local
    try:
        # Cargamos la estructura del JSON desde los secretos de la plataforma
        creds_dict = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key('1Ba6c9QIwsxKLHG0i_Z6ZZVXWHNBh-t3EHQzmwGfAlKs').get_worksheet(0)
        return sheet
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

def cargar_grupos():
    try:
        df = pd.read_csv('grupos.csv')
        return df['Nombre'].tolist()
    except:
        return ["General", "Distrito 1", "Distrito 2"]

# --- INTERFAZ DE USUARIO ---

# 1. Logo de cabecera
if os.path.exists("revilla_porlapaz.jpg"):
    # REEMPLAZA ESTA LÍNEA:
    # st.image("revilla_porlapaz.jpg", use_container_width=True)
    
    # POR ESTA (Ajusta el 300 a tu gusto: 100, 200, 400, etc.):
    st.image("revilla_porlapaz.jpg", width=100) 
else:
    st.title("🧡 Alianza Patria Sol")
    st.subheader("Revilla Por La Paz")

st.markdown("### Registro de cuentas Redes Digitales")

# 2. Carga de datos iniciales
lista_grupos = cargar_grupos()

# 3. Formulario Único (Todo el contenido de entrada debe ir aquí dentro)
with st.form("registro_form", clear_on_submit=True):
    st.info("Complete sus datos personales y sus perfiles de redes sociales.")
    
    # Fila 1: Datos Personales
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre Completo")
        edad = st.number_input("Edad", min_value=15, max_value=95, step=1)
    with col2:
        telefono = st.text_input("Teléfono / WhatsApp")
        area = st.selectbox("Área", ["Urbano", "Rural"])
    
    # Fila 2: Grupo de WhatsApp
    grupo_wa = st.selectbox("Grupo WhatsApp (Distrito)", lista_grupos)

    st.markdown("---")
    
    # --- SECCIÓN FACEBOOK CON LOGO PREPARADO ---
    col_fb_img, col_fb_txt = st.columns([0.1, 0.9]) # Columnas proporcionales
    with col_fb_img:
        if os.path.exists("fb_logo.png"):
            st.image("fb_logo.png", width=30)
        else:
            st.write("🔵") # Respaldo si no encuentra el archivo
    with col_fb_txt:
        st.write("**Cuentas de Facebook (Máximo 5)**")
    
    fb_urls = [st.text_input(f"URL Facebook {i+1}", key=f"fb_new_{i}", placeholder="https://facebook.com/...") for i in range(5)]
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECCIÓN TIKTOK CON LOGO PREPARADO ---
    col_tk_img, col_tk_txt = st.columns([0.1, 0.9])
    with col_tk_img:
        if os.path.exists("tk_logo.png"):
            st.image("tk_logo.png", width=30)
        else:
            st.write("⚫") # Respaldo si no encuentra el archivo
    with col_tk_txt:
        st.write("**Cuentas de TikTok (Máximo 5)**")
    
    tk_urls = [st.text_input(f"URL TikTok {i+1}", key=f"tk_new_{i}", placeholder="https://tiktok.com/@...") for i in range(5)]

    st.markdown("---")

    # Botón de envío
    submit = st.form_submit_button("REGISTRAR AHORA")
    
    if submit:
        if nombre and telefono:
            with st.spinner('Guardando en el sistema...'):
                sheet = conectar_hoja()
                if sheet:
                    estado_auto = "Registrada"
                    # Estructura de la fila: Personales + 5 FB + 5 TK + Estado
                    fila = [nombre, edad, area, telefono, grupo_wa] + fb_urls + tk_urls + [estado_auto]
                    
                    try:
                        sheet.append_row(fila)
                        st.success(f"✅ ¡{nombre} ha sido registrado exitosamente!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error al escribir en la hoja: {e}")
        else:
            st.warning("⚠️ El nombre y el teléfono son obligatorios.")

# Pie de página fuera del formulario
st.markdown("<p style='text-align: center; color: orange; font-size: 0.9em;'><b>Sistema de Registro Digital v2.0 - Alianza Patria Sol</b></p>", unsafe_allow_html=True)