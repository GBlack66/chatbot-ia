import streamlit as st
from google import genai

# 1. Diseño de la página
st.title("🤖 La IA de Jhosmar")
st.write("Bienvenido. Pregúntame lo que quieras, yo recuerdo nuestra plática.")

# 2. Guardar la CONEXIÓN en la memoria para que nunca se cierre
if "cliente" not in st.session_state:
    st.session_state.cliente = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Crear el CHAT usando esa conexión guardada
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.cliente.chats.create(model="gemini-flash-lite-latest")
    st.session_state.mensajes_visuales = []

# 4. Dibujar los mensajes anteriores en la pantalla
for msg in st.session_state.mensajes_visuales:
    with st.chat_message(msg["rol"]):
        st.markdown(msg["texto"])

# 5. La caja de texto donde el usuario escribe
pregunta = st.chat_input("Escribe tu mensaje aquí...")

if pregunta:
    # Mostrar lo que escribió el usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    st.session_state.mensajes_visuales.append({"rol": "user", "texto": pregunta})
    
    # Enviar la pregunta a la API usando el chat guardado
    with st.chat_message("assistant"):
        respuesta = st.session_state.chat.send_message(pregunta)
        st.markdown(respuesta.text)
    
    # Guardar la respuesta de la IA en la memoria visual
    st.session_state.mensajes_visuales.append({"rol": "assistant", "texto": respuesta.text})