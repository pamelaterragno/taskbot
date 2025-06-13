import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from gestor_tareas import agregar_tarea, listar_tareas, marcar_hecha

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# ----- Handlers -----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🤖 *Menú de Tareas*\n\n"
        "/add _texto_ — Agregá una nueva tarea\n"
        "/list — Mostrá todas tus tareas\n"
        "/done _número_ — Marcá una tarea como hecha\n"
        "/start — Mostrá este menú nuevamente"
    )
    await update.message.reply_text(texto, parse_mode="Markdown")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    texto_tarea = " ".join(context.args)
    if not texto_tarea:
        await update.message.reply_text("Tenés que escribir una tarea después de /add")
        return
    agregar_tarea(str(user.id), texto_tarea)
    await update.message.reply_text(f"✅ Tarea agregada: {texto_tarea}")
    logging.info(f"Tarea agregada para {user.first_name}: {texto_tarea}")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tareas = listar_tareas(str(user.id))
    if not tareas:
        await update.message.reply_text("✅ No tenés tareas pendientes ni completadas.")
        return
    texto = ""
    for i, t in enumerate(tareas, start=1):
        status = "✅" if t.get("hecha") else "❌"
        texto += f"{i}. {status} {t['texto']}\n"
    await update.message.reply_text(texto)

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Usá /done <número> para marcar como hecha.")
        return
    idx = int(context.args[0]) - 1
    if marcar_hecha(str(user.id), idx):
        await update.message.reply_text(f"✅ Marcaste la tarea #{idx+1} como hecha.")
    else:
        await update.message.reply_text("❗ Tarea inválida. Revisá el número.")

# ----- Main -----
if __name__ == "__main__":
    logging.info("Iniciando bot de tareas...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("done", done))

    app.run_polling()

