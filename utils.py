from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="src/utils/.env")

# gmail
from email.message import EmailMessage
import smtplib

##google sheets
import pandas as pd
import pygsheets

##whatsapp
from heyoo import WhatsApp

# openai
from openai import OpenAI
from time import sleep
import json

##Obtener el api key
from dotenv import load_dotenv
import os

load_dotenv()

##credenciales
APP_PASSWORD_GMAIL = os.getenv("APP_PASSWORD_GMAIL")
CORREO_REMITENTE = os.getenv("EMAIL_REMITENTE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")


client = OpenAI(api_key=OPENAI_API_KEY)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ conexion a email ----------------------------------------------------
def enviar_correo(
    nombre_lead,
    correo_lead,
    mensaje_para_lead,
    telefono_lead=None,
    servicio_interes=None,
):
    try:
        remitente = CORREO_REMITENTE
        destinatario = correo_lead

        # Construir cuerpo del mensaje con variables opcionales
        mensaje = f"{mensaje_para_lead}\n\n"

        if servicio_interes:
            mensaje += f"Servicio de interés: {servicio_interes}\n"
        if telefono_lead:
            mensaje += f"Teléfono registrado: {telefono_lead}\n"

        # Crear objeto de correo
        email = EmailMessage()
        email["From"] = remitente
        email["To"] = destinatario
        email["Subject"] = f"💡 D’LOGIA | ¡Gracias por tu interés, {nombre_lead}!"
        email.set_content(mensaje)

        # Envío seguro
        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        smtp.login(remitente, APP_PASSWORD_GMAIL)
        smtp.send_message(email)
        smtp.quit()

        print(f"✅ Correo enviado con éxito a {correo_lead}")
        return True

    except Exception as e:
        print("❌ Error al enviar correo:", e)
        return False


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------- conexion a google sheets ------------------------------------------------
def registrar_google_sheets(nombre, correo, telefono, programa):
    try:
        # ID y hoja de Google Sheets
        sheet_id = GOOGLE_SHEETS_ID
        sheet_name = "Interesados"
        url_csv = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

        # Leer la hoja actual
        df = pd.read_csv(url_csv)
        print("📄 Datos actuales:")
        print(df)

        # Agregar el nuevo registro (puedes usar un ID único real si deseas)
        nuevo_registro = ["123", nombre, correo, telefono, programa]
        df.loc[len(df.index)] = nuevo_registro

        print("🆕 Nuevo registro agregado:")
        print(df)

        # Autenticación y subida con pygsheets
        service_account_path = "asistente-dlogia-openai.json"
        gc = pygsheets.authorize(service_file=service_account_path)
        sh = gc.open_by_key(sheet_id)
        wks = sh.worksheet_by_title(sheet_name)
        wks.set_dataframe(df, (1, 1))

        print("✅ Datos actualizados en Google Sheets.")
        return True

    except Exception as e:
        print("❌ Error al registrar en Google Sheets:", e)
        return False


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- enviar mensaje por whatsapp ----------------------------------------------
import smtplib
import pandas as pd
import json
import pygsheets
from email.message import EmailMessage
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="src/utils/.env")  # o usa ".env" si lo mueves al root

CORREO_REMITENTE = os.getenv("EMAIL_REMITENTE")
APP_PASSWORD_GMAIL = os.getenv("APP_PASSWORD_GMAIL")
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
print("🔍 Assistant ID:", ASSISTANT_ID)


# Personalización correo HTML (D'LOGIA)
def enviar_correo(nombre_lead, correo_lead, mensaje_para_lead):
    try:
        remitente = CORREO_REMITENTE
        destinatario = correo_lead

        # HTML corporativo simple
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                .logo {{ font-size: 32px; font-weight: bold; margin-bottom: 10px; }}
                .tagline {{ font-size: 14px; opacity: 0.9; }}
                .content {{ padding: 30px; color: #333; line-height: 1.6; }}
                .highlight {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0; }}
                .cta {{ text-align: center; margin: 25px 0; }}
                .btn {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; }}
                .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #e9ecef; }}
                .contact-info {{ margin: 10px 0; }}
                .contact-info a {{ color: #667eea; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">D'LOGIA</div>
                    <div class="tagline">Soluciones empresariales inteligentes</div>
                </div>
                
                <div class="content">
                    <h2>¡Hola {nombre_lead}! 👋</h2>
                    
                    <p><strong>¡Gracias por contactar a D'LOGIA!</strong> 🚀</p>
                    
                    <div class="highlight">
                        {mensaje_para_lead}
                    </div>
                    
                    
                    <div class="cta">
                        <a href="https://juancanchala.github.io" class="btn">Conoce nuestro portafolio</a>
                    </div>
                </div>
                
                <div class="footer">
                    <div class="contact-info">
                        <strong>Equipo D'LOGIA</strong> 💡
                    </div>
                    <div class="contact-info">
                        📧 <a href="mailto:contacto.dlogia@gmail.com">contacto.dlogia@gmail.com</a>
                    </div>
                    <div class="contact-info">
                        📱 <a href="tel:+573104404091">+57 310 4404091</a>
                    </div>
                    <div class="contact-info">
                        🌐 <a href="https://juancanchala.github.io">juancanchala.github.io</a>
                    </div>
                    <br>
                    <small style="color: #666;">"Transformando operaciones con datos, lógica e inteligencia artificial"</small>
                </div>
            </div>
        </body>
        </html>
        """

        # Crear mensaje con HTML
        email = EmailMessage()
        email["From"] = remitente
        email["To"] = destinatario
        email["Subject"] = f"🚀 ¡Gracias por contactar D'LOGIA, {nombre_lead}!"

        # Contenido HTML
        email.set_content(
            "Versión texto del mensaje"
        )  # Fallback para clientes sin HTML
        email.add_alternative(html_content, subtype="html")

        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        smtp.login(remitente, APP_PASSWORD_GMAIL)
        smtp.send_message(email)
        smtp.quit()
        return True

    except Exception as e:
        print("❌ Error al enviar correo:", e)
        return False


# Registrar interesado en Google Sheets (D’LOGIA)
def registrar_google_sheets(nombre, correo, programa):
    sheet_id = GOOGLE_SHEETS_ID
    sheet_name = "Interesados"
    url_csv = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    # Leer datos actuales
    df = pd.read_csv(url_csv)
    print("📄 Datos actuales:")
    print(df)

    # GENERAR ID CONSECUTIVO BASADO EN EL TOTAL DE FILAS
    nuevo_id = (
        len(df) + 1
    )  # Simplemente el siguiente número basado en cantidad de registros

    # Agregar nuevo registro con ID consecutivo real
    df.loc[len(df.index)] = [nuevo_id, nombre, correo, programa]
    print(f"📄 Nuevo registro agregado con ID: {nuevo_id}")
    print(df)

    try:
        service_account_path = "asistente-dlogia-openai.json"
        gc = pygsheets.authorize(service_file=service_account_path)
        sh = gc.open_by_key(sheet_id)
        wks = sh.worksheet_by_title(sheet_name)
        wks.set_dataframe(df, (1, 1))

        print("✅ Datos actualizados en Google Sheets.")
        return True, nuevo_id

    except Exception as e:
        print("❌ Error al registrar en Google Sheets:", e)
        return False, None


# Enviar WhatsApp con mensaje automatizado (D’LOGIA)
def enviar_whatsapp(numero_whatsapp_asesor, mensaje_asesor):
    try:
        messenger = WhatsApp(WHATSAPP_API_TOKEN, phone_number_id=PHONE_NUMBER_ID)
        messenger.send_message(mensaje_asesor, numero_whatsapp_asesor)
        return True
    except Exception as e:
        print("❌ Error al enviar WhatsApp:", e)
        return False


# Ejecutar acciones del asistente virtual (D’LOGIA)
def run_excecuter(run):
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=run.thread_id, run_id=run.id
        )

        if run_status.status == "completed":
            print("✅ Acción completada por el asistente.")
            break

        elif run_status.status == "requires_action":
            print("⚙️ Se requiere acción...")
            list_of_actions = run_status.required_action.submit_tool_outputs.tool_calls

            tools_output_list = []

            for accion in list_of_actions:
                nombre = accion.function.name
                argumentos = json.loads(accion.function.arguments)

                if nombre == "registrar_google_sheets":
                    resultado = registrar_google_sheets(
                        argumentos["nombre_lead"],
                        argumentos["correo_lead"],
                        argumentos["producto_de_interes"],
                    )
                elif nombre == "enviar_correo":
                    resultado = enviar_correo(
                        argumentos["nombre_lead"],
                        argumentos["correo_lead"],
                        argumentos["mensaje_para_lead"],
                    )
                elif nombre == "enviar_whatsapp":
                    resultado = enviar_whatsapp(
                        argumentos["numero_whatsapp_asesor"],
                        argumentos["mensaje_asesor"],
                    )
                else:
                    print("⚠️ Acción no reconocida:", nombre)
                    return "No se encontró la acción"

                tools_output_list.append(
                    {"tool_call_id": accion.id, "output": str(resultado)}
                )

            print("✅ Envío de resultados al asistente finalizado.")
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=run.thread_id, run_id=run.id, tool_outputs=tools_output_list
            )
        else:
            print("⏳ Esperando respuesta del asistente...")
            sleep(3)


# if __name__=="__main__":
#  enviar_correo(correo_lead="contacto.dlogia@gmail.com",mensaje_para_lead="hola", nombre_lead="Juan")
