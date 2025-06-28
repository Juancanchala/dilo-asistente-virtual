import streamlit as st
from PIL import Image
import time
import os
from dotenv import load_dotenv
from utils import run_excecuter
from openai import OpenAI

# 🔹 Configurar la página (tiene que ir PRIMERO)
st.set_page_config(
    page_title="DILO – Asistente Virtual", layout="centered", page_icon="🤖"
)

# 🔹 Cargar variables de entorno
load_dotenv()

# 🔹 Inicializar cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv("ASSISTANT_ID")

# 🔹 Mostrar logo de D’LOGIA
image = Image.open("images/logo-dlogia.png")
st.image(image, use_container_width=True)

# 🔹 Título de la app
st.title("DILO – Asistente Virtual de D’LOGIA")

# 🔹 Inicializar estado de sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = client.beta.threads.create().id

# 🔹 Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# 🔹 Función efecto máquina de escribir
def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)


# 🔹 Capturar entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    # Mostrar y guardar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 🔹 Enviar a OpenAI y generar respuesta
    with st.chat_message("assistant"):
        message_box = client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id, role="user", content=prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id, assistant_id=assistant_id
        )

        with st.spinner("DILO está escribiendo..."):
            st.toast("¡Gracias por contactarnos!", icon="🤖")
            run_excecuter(run)
            message_assistant = (
                client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
                .data[0]
                .content[0]
                .text.value
            )

        # Mostrar respuesta del asistente con efecto
        typewriter(message_assistant, 50)

    # Guardar respuesta del asistente
    st.session_state.messages.append(
        {"role": "assistant", "content": message_assistant}
    )
