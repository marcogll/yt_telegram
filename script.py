import os
import sys
import subprocess
import re
import time
import asyncio
import logging
from telethon import TelegramClient, events
import yt_dlp
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# ================= EXTRACCIÓN Y CONFIGURACIÓN =================
# Configurar el sistema de logs
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

try:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    PHONE = os.getenv("PHONE")

    # Procesar usuarios autorizados
    usuarios_str = os.getenv("USUARIOS_AUTORIZADOS", "")
    USUARIOS_AUTORIZADOS = [
        int(u.strip()) for u in usuarios_str.split(",") if u.strip().isdigit()
    ]

    CARPETA_DESCARGAS = os.getenv("CARPETA_DESCARGAS", "./downloads")
    MAX_HEIGHT = int(os.getenv("MAX_HEIGHT", 720))
    CLEANUP_HOURS = int(os.getenv("CLEANUP_HOURS", 168))
    GRUPO_DESTINO = int(os.getenv("GRUPO_DESTINO"))

except TypeError as e:
    logger.error(
        "❌ Faltan variables en el archivo .env o tienen un formato incorrecto."
    )
    exit(1)

# Crear carpeta si no existe
if not os.path.exists(CARPETA_DESCARGAS):
    os.makedirs(CARPETA_DESCARGAS)
    logger.info(f"📁 Carpeta creada: {CARPETA_DESCARGAS}")

# Inicializar cliente de Telethon
client = TelegramClient("sesion_usuario", API_ID, API_HASH)

YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"


def descargar_video(url, carpeta_salida):
    """Descarga el video usando la altura máxima definida en el .env"""
    ydl_opts = {
        "format": f"bestvideo[height<={MAX_HEIGHT}][ext=mp4]+bestaudio[ext=m4a]/best[height<={MAX_HEIGHT}][ext=mp4]",
        "outtmpl": f"{carpeta_salida}/%(title)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        archivo = ydl.prepare_filename(info_dict)
        titulo = info_dict.get("title", "Video sin título")
        return archivo, titulo


async def limpiar_carpeta_periodicamente():
    """Elimina archivos que superen las horas definidas en CLEANUP_HOURS"""
    while True:
        ahora = time.time()
        for filename in os.listdir(CARPETA_DESCARGAS):
            file_path = os.path.join(CARPETA_DESCARGAS, filename)
            if os.path.isfile(file_path):
                fecha_modificacion = os.stat(file_path).st_mtime
                tiempo_limite = CLEANUP_HOURS * 3600

                if fecha_modificacion < ahora - tiempo_limite:
                    try:
                        os.remove(file_path)
                        logger.info(
                            f"🗑️ Archivo eliminado por antigüedad (+{CLEANUP_HOURS}h): {filename}"
                        )
                    except Exception as e:
                        logger.error(f"No se pudo eliminar {filename}: {e}")

        await asyncio.sleep(3600)


async def auto_actualizar_ytdlp():
    """Busca actualizaciones de yt-dlp cada 24 horas y reinicia el script si se actualiza."""
    while True:
        await asyncio.sleep(86400)
        logger.info("🔄 Buscando actualizaciones de yt-dlp en segundo plano...")
        try:
            resultado = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                capture_output=True,
                text=True,
            )

            if (
                "Requirement already satisfied" in resultado.stdout
                and "Successfully installed" not in resultado.stdout
            ):
                logger.info("⚡ yt-dlp ya está en su última versión.")
            else:
                logger.info(
                    "✅ ¡Nueva versión de yt-dlp instalada! Reiniciando el bot..."
                )
                os.execv(sys.executable, [sys.executable] + sys.argv)

        except Exception as e:
            logger.error(f"❌ Error al intentar actualizar yt-dlp: {e}")


@client.on(events.NewMessage(chats=GRUPO_DESTINO))
async def manejador_youtube(event):
    if event.sender_id not in USUARIOS_AUTORIZADOS:
        return

    texto = event.raw_text
    match = re.search(YOUTUBE_REGEX, texto)

    if match:
        url = match.group(0)
        logger.info(f"🔗 Enlace detectado de {event.sender_id}: {url}")
        mensaje_estado = await event.reply(
            f"⏳ Descargando video en {MAX_HEIGHT}p... Por favor espera."
        )

        try:
            # CORRECCIÓN PARA PYTHON 3.14 AQUÍ (get_running_loop en lugar de get_event_loop)
            loop = asyncio.get_running_loop()
            ruta_archivo, titulo = await loop.run_in_executor(
                None, descargar_video, url, CARPETA_DESCARGAS
            )

            await mensaje_estado.edit("📤 Video descargado. Subiendo a Telegram...")

            await client.send_file(
                event.chat_id,
                ruta_archivo,
                caption=titulo,
                reply_to=event.message.id,
                supports_streaming=True,
            )

            await mensaje_estado.delete()
            logger.info(f"✅ Video subido exitosamente: {titulo}")

        except Exception as e:
            await mensaje_estado.edit(f"❌ Ocurrió un error:\n`{str(e)}`")
            logger.error(f"Error procesando enlace {url}: {e}")


async def main():
    await client.start(phone=PHONE)

    logger.info("🤖 Script iniciado y escuchando el grupo...")
    logger.info(f"🎯 Grupo destino: {GRUPO_DESTINO}")
    logger.info(f"🧹 Limpieza configurada a: {CLEANUP_HOURS} horas")

    asyncio.create_task(limpiar_carpeta_periodicamente())
    asyncio.create_task(auto_actualizar_ytdlp())

    await client.run_until_disconnected()


# CORRECCIÓN PARA PYTHON 3.14 AQUÍ (Crear el bucle manualmente)
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido manualmente por el usuario.")
