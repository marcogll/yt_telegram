<div align="center">

<a href="https://soul23.mx">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/marcogll/mg_data_storage/refs/heads/main/soul23/logo/soul23_logo_wh.png">
  <img src="https://raw.githubusercontent.com/marcogll/mg_data_storage/refs/heads/main/soul23/logo/soul23_logo_blk.png" alt="Soul23" width="110">
</picture>
</a>

</div>

# Yt Telegram

Bot de Telegram para automatización y gestión de operaciones 🤖

<p>
  <img src="https://img.shields.io/badge/español-111111?style=flat-square&logo=googletranslate&logoColor=white" alt="Español">
</p>

---

<h1 align="center">yt_telegram.git</h1>




## ✨ Características Principales

- **📥 Descarga a Medida:** Extrae el mejor formato de video y audio combinados (hasta la resolución máxima definida, ej. 720p).
- **🔒 Control de Acceso Estricto:** Solo procesa enlaces enviados por usuarios específicos (mediante su ID de Telegram). Ignora al resto.
- **🎯 Monitoreo Específico:** Opera silenciosamente y solo actúa dentro del chat o grupo de destino configurado.
- **🧹 Auto-Limpieza de Disco:** Incluye un recolector de basura en segundo plano que elimina los videos locales tras `X` horas de antigüedad, evitando saturar el almacenamiento local.
- **🔄 Auto-Actualización Inteligente:** Ejecuta una tarea invisible cada 24 horas para actualizar `yt-dlp` vía `pip`. Si encuentra una actualización, el bot se reinicia a sí mismo automáticamente para aplicar los cambios en memoria.
- **▶️ Streaming en Telegram:** Sube los videos permitiendo que los usuarios de Telegram los reproduzcan instantáneamente sin tener que descargarlos por completo.
- **⚡ Compatible con Python Moderno:** Código optimizado para funcionar sin problemas en Python 3.14 y superiores (manejo explícito de *event loops*).

## 🛠️ Requisitos Previos

1. **Python 3.9 o superior** (Testeado en Python 3.14).
2. **FFmpeg** instalado en tu sistema operativo (esencial para que `yt-dlp` fusione el audio y el video).
   - *Arch Linux:* `sudo pacman -S ffmpeg`
   - *Ubuntu/Debian:* `sudo apt install ffmpeg`
   - *MacOS:* `brew install ffmpeg`
3. Credenciales de la API de Telegram (`API_ID` y `API_HASH`), obtenidas en [my.telegram.org](https://my.telegram.org/).

## 📦 Instalación

1. Clona o descarga este repositorio en tu máquina local.
2. Crea un entorno virtual para no interferir con los paquetes de tu sistema operativo (PEP 668):
   ```bash
   python -m venv .venv
   ```
3. Activa el entorno virtual:
   ```bash
   source .venv/bin/activate
   ```
4. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
⚙️ Configuración

Crea un archivo llamado exactamente `.env` en el mismo directorio que el script y añade tu configuración.

> [!IMPORTANT]
> Asegúrate de no compartir este archivo con nadie, ya que contiene tus credenciales de acceso.

```env
# ============================================
# Bot de YouTube para Telegram
# ============================================

# Credenciales de Telegram (obtener de https://my.telegram.org)
API_ID=tu_api_id
API_HASH=tu_api_hash
USUARIOS_AUTORIZADOS=123456789,987654321

# Número de teléfono para autenticación (Incluir código de país, ej: +52...)
PHONE=+521234567890

# Configuración del bot
CARPETA_DESCARGAS=./downloads
MAX_HEIGHT=720
LOG_LEVEL=INFO

# Tiempo de retención de archivos locales (horas) - 168h = 7 días
CLEANUP_HOURS=168

# Grupo destino para enviar descargas (ID del grupo - usualmente con signo negativo)
GRUPO_DESTINO=-1001234567890
```

> [!TIP]
> Usa `CARPETA_DESCARGAS=./downloads` para descargas locales. Si en el futuro migras este proyecto a un contenedor Docker, puedes cambiarlo a `/app/downloads`.
🚀 Uso

Asegúrate de tener tu entorno virtual activado (`source .venv/bin/activate`) y ejecuta el script:

```bash
python script.py
```
🔑 Primer Inicio de Sesión
La primera vez que ejecutes el bot, la terminal te pedirá que ingreses un código de 5 dígitos que Telegram te enviará a través de la app.
Una vez introducido, se creará un archivo llamado sesion_usuario.session. A partir de ese momento, el bot se iniciará automáticamente sin pedir contraseña.
📝 Funcionamiento Interno
Manjeo de Errores Asíncronos: Las descargas utilizan run_in_executor para evitar bloquear el bucle de eventos principal de Telegram. Mientras un video de 1GB se descarga, el bot sigue siendo capaz de leer nuevos mensajes.
Logs Profesionales: El uso de logging permite monitorear cada acción del bot (descargas, eliminación de archivos y actualizaciones de dependencias) con su respectiva marca de tiempo, ideal para servidores, VPS o Docker.


