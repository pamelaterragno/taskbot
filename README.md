# Telegram Task Bot

Bot personal para gestionar tareas directamente desde Telegram. Permite agregar, listar y marcar tareas como completadas, y se ejecuta dentro de un contenedor Docker.

---

## Funcionalidades

* `/add tarea` → Agrega una nueva tarea
* `/list` → Muestra todas tus tareas (pendientes y completadas)
* `/done número` → Marca una tarea como hecha
* `/start` → Muestra el menú de ayuda

---

## Tecnologías utilizadas

* Python 3.12
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* Docker + Docker Compose
* Archivos JSON para almacenamiento de tareas
* Logging con consola

---

## Cómo correrlo localmente

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/telegram-task-bot.git
cd telegram-task-bot
```

### 2. Crear un archivo `.env`

```env
TELEGRAM_TOKEN=tu_token_de_telegram_aqui
```

> No compartas este token.&#x20;

### 3. Construir y ejecutar el contenedor

```bash
docker-compose build
docker-compose up -d
```

### 4. Ver logs

```bash
docker logs -f telegram-task-bot
```

---

## Estructura del proyecto

```
telegram-task-bot/
├── main.py                 # Lógica principal del bot
├── gestor_tareas.py        # Funciones para gestionar tareas por usuario
├── data/                   # (Generado) Contiene tareas guardadas
├── .env                    # Token (no incluido en el repo)
├── Dockerfile              # Imagen de Python + bot
├── docker-compose.yml      # Define el contenedor
├── requirements.txt        # Dependencias
└── .gitignore              # Archivos que no se suben
```