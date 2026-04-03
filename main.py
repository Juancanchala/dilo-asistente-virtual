from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()

# Importar utils intacto — sin modificar
from utils import client, run_excecuter, ASSISTANT_ID

app = FastAPI(title="DILO – Asistente Virtual D'LOGIA", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    prompt: str
    thread_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    thread_id: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "assistant_configured": bool(ASSISTANT_ID),
        "client_ready": bool(client),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not client:
        raise HTTPException(status_code=503, detail="Cliente OpenAI no disponible. Verifica OPENAI_API_KEY.")
    if not ASSISTANT_ID:
        raise HTTPException(status_code=503, detail="ASSISTANT_ID no configurado.")

    # Crear nuevo thread o reutilizar el existente
    if req.thread_id:
        thread_id = req.thread_id
        # Cancelar runs activos antes de enviar un nuevo mensaje
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        for run in runs.data:
            if run.status in ["in_progress", "queued", "requires_action"]:
                client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run.id)
                sleep(1)
    else:
        thread = client.beta.threads.create()
        thread_id = thread.id

    # Enviar mensaje del usuario al thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=req.prompt,
    )

    # Crear el run (ejecutar el asistente)
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
    )

    # Ejecutar — resuelve function calls internamente (registrar_google_sheets, enviar_correo, enviar_whatsapp)
    run_excecuter(run)

    # Obtener la respuesta más reciente del asistente
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for message in messages.data:
        if message.role == "assistant":
            return ChatResponse(
                response=message.content[0].text.value,
                thread_id=thread_id,
            )

    raise HTTPException(status_code=500, detail="No se recibió respuesta del asistente.")


# Servir imágenes estáticas
app.mount("/images", StaticFiles(directory="images"), name="images")

# Servir el frontend (index.html) desde la raíz del proyecto
app.mount("/static", StaticFiles(directory=".", html=True), name="static")


@app.get("/")
def root():
    return FileResponse("index.html")
