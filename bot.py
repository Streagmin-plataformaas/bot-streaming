import os
import telebot
import imaplib
import email
from email.header import decode_header
import re
import time

# Token de tu bot de Telegram
TOKEN = os.environ.get("TOKEN")

# Configuración de tus cuentas de correo y contraseñas de aplicación
CUENTAS_CORREO = [
    {
        "servidor": "imap.gmail.com",
        "correo": "jefer31613@gmail.com",
        "password": "mgjm kikv mrqw dvie"  # Reemplaza con tu app password de Gmail
    },
    {
        "servidor": "imap.gmail.com",
        "correo": "jefer31614@gmail.com",
        "password": "lfsa fpey aclv gcys"  # Reemplaza con tu app password de Gmail
    }
]

bot = telebot.TeleBot(TOKEN)

def buscar_codigo_en_bandeja(servidor, correo, password):
    try:
        print(f"Conectando a {correo}...")
        mail = imaplib.IMAP4_SSL(servidor)
        mail.login(correo, password)
        mail.select("inbox")

        # Buscamos los últimos correos recibidos
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            mail.logout()
            return None

        email_ids = messages[0].split()
        # Revisamos los últimos 5 correos más recientes
        for e_id in reversed(email_ids[-5:]):
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            if res != "OK":
                continue
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Extraer el cuerpo del mensaje
                    cuerpo = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if "attachment" not in content_disposition:
                                try:
                                    payload = part.get_payload(decode=True)
                                    if payload:
                                        cuerpo += payload.decode('utf-8', errors='ignore')
                                except:
                                    pass
                    else:
                        try:
                            payload = msg.get_payload(decode=True)
                            if payload:
                                cuerpo = payload.decode('utf-8', errors='ignore')
                        except:
                            pass

                    # Buscar un código numérico de 4 a 6 dígitos típico de verificación
                    match = re.search(r'\b\d{4,6}\b', cuerpo)
                    if match:
                        codigo_encontrado = match.group(0)
                        asunto, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(asunto, bytes):
                            asunto = asunto.decode(encoding if encoding else "utf-8", errors="ignore")
                        
                        mail.logout()
                        return f"📧 **Correo:** {correo}\n📌 **Asunto:** {asunto}\n🔑 **Código encontrado:** `{codigo_encontrado}`"

        mail.logout()
    except Exception as e:
        print(f"Error con la cuenta {correo}: {e}")
    return None

@bot.message_handler(commands=['start'])
def enviar_bienvenida(message):
    bot.reply_to(message, "👋 ¡Hola! Bienvenido al sistema de códigos de streaming.\n\nEnvía el comando:\n`/codigo` para buscar códigos recientes en tus cuentas.")

@bot.message_handler(commands=['codigo'])
def consultar_codigo(message):
    bot.reply_to(message, "🔍 Buscando códigos recientes en tus cuentas de correo, espera un momento...")
    print("¡El celular solicitó una búsqueda de código!")

    resultado_final = None
    for cuenta in CUENTAS_CORREO:
        resultado = buscar_codigo_en_bandeja(cuenta["servidor"], cuenta["correo"], cuenta["password"])
        if resultado:
            resultado_final = resultado
            break

    if resultado_final:
        bot.send_message(message.chat.id, resultado_final, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ No se encontró ningún código reciente en las bandejas configuradas. Vuelve a solicitarlo en la plataforma e inténtalo de nuevo en unos segundos.")

print("Iniciando bot...")
print("Bot en línea y listo para recibir órdenes desde el celular.")
bot.infinity_polling()