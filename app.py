import os
from PIL import Image
import sys
from dotenv import load_dotenv
from utils import run_excecuter
from openai import OpenAI
import time
import streamlit as st

# --- D'LOGIA Asistente Virtual ---

# ✅ Configurar la página (tiene que ir PRIMERO)
st.set_page_config(
    page_title="DILO – Asistente Virtual", layout="centered", page_icon="🤖"
)

# ✅ Configurar codificación
sys.stdout.reconfigure(encoding="utf-8")

# ✅ Cargar variables de entorno
load_dotenv()

# ✅ Verificar y obtener las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

if not api_key:
    st.error("❌ No se encontró la clave OPENAI_API_KEY")
    st.stop()

if not assistant_id:
    st.error("❌ No se encontró el ASSISTANT_ID")
    st.stop()

# ✅ Inicializar cliente de OpenAI
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"❌ Error al crear el cliente OpenAI: {e}")
    client = None
    st.stop()

# ✅ Mostrar logo de D'LOGIA
try:
    image = Image.open("images/logo-dlogia.png")
    st.image(image, use_container_width=True)
except FileNotFoundError:
    st.markdown("## 🤖 D'LOGIA - Asistente Virtual")
    st.markdown("*Soluciones empresariales inteligentes*")

# ✅ Título principal
st.title("DILO – Asistente Virtual de D'LOGIA")

# ✅ Inicializar estado de sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    try:
        st.session_state.thread_id = client.beta.threads.create().id
    except Exception as e:
        st.error(f"❌ Error al crear el thread: {e}")
        st.stop()


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
        try:
            # Importar client desde utils
            from utils import client

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
                    client.beta.threads.messages.list(
                        thread_id=st.session_state.thread_id
                    )
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

        except Exception as e:
            st.error(f"❌ Error al procesar el mensaje: {e}")
            print(f"Error detallado: {e}")
