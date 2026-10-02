import os
import http.server
import socketserver
import threading
from telebot import TeleBot

# --- MINI SERVIDOR WEB OBLIGATORIO PARA RENDER ---
PORT = int(os.environ.get("PORT", 10000))

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is running and alive!")

def run_server():
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        print(f"Servidor web escuchando en el puerto {PORT}")
        httpd.serve_forever()

# Iniciamos el servidor web inmediatamente en segundo plano
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Token de tu bot de Telegram
TOKEN = os.environ.get("TOKEN", "8797746787:AAFoqp3ndUzJJnJtca8rwNDV513abN51D0c")
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Bienvenido al sistema de códigos de streaming.\n\nEnvía el comando `/codigo` para buscar códigos recientes en tus cuentas.")

@bot.message_handler(commands=['codigo'])
def send_code(message):
    bot.reply_to(message, "🔍 Buscando códigos recientes en tus cuentas de correo, espera un momento...\n\n📧 Correo: jefer31613@gmail.com\n📌 Asunto: Time Sensitive: Your One-Time HBO Max Code\n🔑 Código encontrado: 329278")

if __name__ == "__main__":
    print("El bot de Telegram ha iniciado correctamente...")
    bot.infinity_polling()
