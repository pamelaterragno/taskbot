import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from gestor_tareas import (
    agregar_tarea,
    listar_tareas,
    marcar_hecha,
    filtrar_por_etiqueta,
    eliminar_ultimas_completadas,
    eliminar_tarea_por_indice
)

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
        "<b>Menú de Tareas</b>\n\n"
        "/add <i>texto</i> #etiqueta — Agregá una nueva tarea con etiqueta\n"
        "/list — Mostrá todas tus tareas\n"
        "/done <i>número</i> — Marcá una tarea como hecha\n"
        "/borrar <i>número</i> — Eliminá una tarea específica\n"
        "/borrar_completadas <i>n</i> — Eliminá tus últimas tareas completadas\n"
        "/ver #etiqueta — Ver tareas filtradas por etiqueta\n"
        "/start — Mostrá este menú nuevamente"
    )
    await update.message.reply_text(texto, parse_mode="HTML")


#Old version add
# async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     texto_tarea = " ".join(context.args)
#     if not texto_tarea:
#         await update.message.reply_text("Tenés que escribir una tarea después de /add")
#         return
#     agregar_tarea(str(user.id), texto_tarea)
#     await update.message.reply_text(f"✅ Tarea agregada: {texto_tarea}")
#     logging.info(f"Tarea agregada para {user.first_name}: {texto_tarea}")

#Nueva versión con opción de etiquta
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    texto_tarea = " ".join(context.args)
    if not texto_tarea:
        await update.message.reply_text("Uso: /agregar tarea #etiqueta")
        return
    agregar_tarea(str(user.id), texto_tarea)
    await update.message.reply_text(f"Tarea agregada correctamente con etiqueta (si hay)")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tareas = listar_tareas(str(user.id))
    if not tareas:
        await update.message.reply_text("✅ No tenés tareas pendientes ni completadas")
        return
    texto = ""
    for i, t in enumerate(tareas, start=1):
        status = "✅" if t.get("hecha") else "❌"
        etiqueta = f"#{t['etiqueta']}" if t.get("etiqueta") else ""
        texto += f"{i}. {status} {t['texto']} {etiqueta}\n"
    await update.message.reply_text(texto)

async def borrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Uso: /borrar <número> para eliminar una tarea.")
        return

    idx = int(context.args[0]) - 1
    if eliminar_tarea_por_indice(user_id, idx):
        await update.message.reply_text(f"🗑️ Tarea #{idx + 1} eliminada correctamente.")
    else:
        await update.message.reply_text("❗ Número inválido. Revisá con /list.")



async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)

    if not context.args:
        await update.message.reply_text("Usá /done <id> para marcar como hechas. Ej: /done 1 3 4")
        return

    tareas = listar_tareas(user_id)
    if not tareas:
        await update.message.reply_text("No tenés tareas para marcar.")
        return

    indices = []
    for arg in context.args:
        if arg.isdigit():
            idx = int(arg) - 1
            if 0 <= idx < len(tareas):
                indices.append(idx)

    if not indices:
        await update.message.reply_text("No se encontraron tareas válidas para marcar.")
        return

    exitosas = []
    for idx in indices:
        if marcar_hecha(user_id, idx):
            exitosas.append(idx + 1)  # Mostrar número humano

    if exitosas:
        lista = ", ".join(str(i) for i in exitosas)
        await update.message.reply_text(f"✅ Marcaste las tareas {lista} como completadas.")
    else:
        await update.message.reply_text("❗ No se pudo marcar ninguna tarea.")

async def borrar_completadas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    cantidad = int(context.args[0]) if context.args and context.args[0].isdigit() else 1

    eliminadas = eliminar_ultimas_completadas(user_id, cantidad)
    if eliminadas == 0:
        await update.message.reply_text("No hay tareas completadas para borrar.")
    else:
        await update.message.reply_text(f"🗑️ Se eliminaron las últimas {eliminadas} tareas que habían sido como marcadas recientemente")


async def ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.args:
        await update.message.reply_text("Uso: /ver #etiqueta")
        return
    etiqueta = context.args[0].lstrip('#').lower()
    tareas = filtrar_por_etiqueta(str(user.id), etiqueta)

    if not tareas:
        await update.message.reply_text(f"No hay tareas con la etiqueta #{etiqueta}")
        return

    mensaje = f"Tareas con etiqueta #{etiqueta}:\n"
    for i, t in enumerate(tareas, 1):
        mensaje += f"{i}. {t['texto']}\n"
    await update.message.reply_text(mensaje)

# ----- Main -----

if __name__ == "__main__":
    logging.info("Iniciando bot de tareas...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("ver", ver))
    app.add_handler(CommandHandler("borrar_completadas", borrar_completadas))
    app.add_handler(CommandHandler("borrar", borrar))



    app.run_polling()