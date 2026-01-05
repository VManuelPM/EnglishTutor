# 🇬🇧 EnglishTutor AI - Intelligent Language Learning Assistant

[🇪🇸 Versión en Español](#versión-en-español) | [🇺🇸 English Version](#english-version)

---
<a name="versión-en-español"></a>
## 🇪🇸 Versión en Español

**EnglishTutor AI** es un asistente de aprendizaje de idiomas avanzado que combina inteligencia artificial local, corrección gramatical en tiempo real y memoria inteligente de largo plazo. El sistema no solo responde a los usuarios, sino que recuerda sus errores pasados y evoluciona con ellos para ofrecer una experiencia educativa personalizada.

---

## 🚀 Tecnologías Core

El proyecto utiliza un stack moderno y de alto rendimiento optimizado para ejecución local (Edge Computing):

*   **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Framework asíncrono de alto rendimiento).
*   **IA Generativa (LLM):** [GPT4All](https://gpt4all.io/) ejecutando modelos cuantizados (Llama 3 / Phi-3) localmente.
*   **Memoria Semántica (Vectores):** [ChromaDB](https://www.trychroma.com/) para el almacenamiento de embeddings.
*   **Procesamiento de Lenguaje (Embeddings):** [Sentence-Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) para transformar texto en representaciones vectoriales.
*   **Base de Datos Relacional:** [SQLAlchemy](https://www.sqlalchemy.org/) con **SQLite** para el historial de conversaciones exacto.
*   **Corrección Gramatical:** [LanguageTool](https://languagetool.org/) para el análisis lingüístico inicial.

---

## 🏗️ Arquitectura y Patrones

El proyecto sigue principios de diseño de software de nivel profesional para garantizar mantenibilidad y escalabilidad:

### 1. Arquitectura RAG (Retrieval-Augmented Generation)
A diferencia de los chatbots simples, este proyecto implementa **RAG**. Antes de generar una respuesta, el sistema:
1.  Busca en **SQLite** el contexto de la conversación reciente (Short-term memory).
2.  Busca en **ChromaDB** errores gramaticales o temas relevantes del pasado (Long-term memory).
3.  Inyecta ambos contextos en el prompt para que la IA responda con conocimiento total del historial del alumno.

### 2. Patrones de Diseño
*   **Inyección de Dependencias:** Los servicios (como `VectorMemoryService`) se inyectan en los controladores, facilitando el testing y el desacoplamiento.
*   **Singleton/Lazy Initialization:** Los modelos de IA, que son pesados en RAM, se inicializan solo cuando es necesario o una única vez durante el ciclo de vida de la aplicación (`lifespan`).
*   **Asincronía y Thread Pooling:** Uso intensivo de `async/await` y `run_in_threadpool` para evitar que las tareas intensivas de CPU (IA) bloqueen el Event Loop de FastAPI.

### 3. Estructura del Proyecto
```text
app/
├── database/  # Configuración de sesión y operaciones CRUD (SQLAlchemy)
├── models/    # Modelos de datos para SQLite
├── routers/   # Endpoints de la API (Arquitectura orientada a recursos)
├── schemas/   # Esquemas de validación de datos (Pydantic)
└── services/  # Lógica de negocio (IA, Vectores, Gramática)
```

### 🧠 Características Clave

- **Privacidad Total**: Todo el procesamiento de IA ocurre localmente en tu hardware. Ningún dato de conversación se envía a servidores externos (OpenAI, etc.).
- **Memoria Inteligente**: Gracias a la base de datos vectorial, el tutor puede recordar que cometiste un error con el "Present Perfect" hace tres días y reforzarlo en la charla de hoy.
- **Validación Dual**: Combina reglas gramaticales deterministas (LanguageTool) con la flexibilidad de un LLM.

### 🛠️ Instalación y Uso
1. **Clonar y configurar entorno**:

```shell
    git clone <repository-url>
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
```

2. **Variables de Entorno**: 
Crea un archivo .env basado en los modelos que desees usar (ej. Meta-Llama-3-8B-Instruct.Q4_0.gguf).

3. **Ejecución**:
```shell
python run.py
```

### Tutorial

Puedes encontrar el tutorial completo en [EnglishTutor AI Tutorial](https://amoelcodigo.com/posts/python-local-chatbot-1/).

### 📝 Licencia
Este proyecto es de uso educativo y personal. Desarrollado con ❤️ para dominar el inglés mediante IA.

----

<a name="english-version" id="english-version"></a>

## 🇺🇸 English Version

# 🇬🇧 EnglishTutor AI - Intelligent Language Learning Assistant

**EnglishTutor AI** is an advanced language learning assistant that combines local artificial intelligence, real-time grammar correction, and intelligent long-term memory. The system not only responds to users but also remembers their past mistakes and evolves with them to provide a personalized educational experience.

---

## 🚀 Core Technologies

The project uses a modern, high-performance stack optimized for local execution (Edge Computing):

* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (High-performance asynchronous framework).
* **Generative AI (LLM):** [GPT4All](https://gpt4all.io/) running quantized models (Llama 3 / Phi-3) locally.
* **Semantic Memory (Vectors):** [ChromaDB](https://www.trychroma.com/) for embedding storage.
* **Language Processing (Embeddings):** [Sentence-Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) to convert text into vector representations.
* **Relational Database:** [SQLAlchemy](https://www.sqlalchemy.org/) with **SQLite** for precise conversation history.
* **Grammar Correction:** [LanguageTool](https://languagetool.org/) for initial linguistic analysis.

---

## 🏗️ Architecture and Patterns

The project follows professional software design principles to ensure maintainability and scalability:

### 1. RAG Architecture (Retrieval-Augmented Generation)

Unlike simple chatbots, this project implements **RAG**. Before generating a response, the system:

1. Searches **SQLite** for recent conversation context (Short-term memory).
2. Searches **ChromaDB** for past grammar mistakes or relevant topics (Long-term memory).
3. Injects both contexts into the prompt so the AI responds with full knowledge of the student’s history.

### 2. Design Patterns

* **Dependency Injection:** Services (like `VectorMemoryService`) are injected into controllers, facilitating testing and decoupling.
* **Singleton / Lazy Initialization:** AI models, which are RAM-intensive, are initialized only when needed or once during the application’s lifecycle (`lifespan`).
* **Asynchrony and Thread Pooling:** Intensive use of `async/await` and `run_in_threadpool` to prevent CPU-heavy AI tasks from blocking FastAPI’s Event Loop.

### 3. Project Structure

```text
app/
├── database/  # Session configuration and CRUD operations (SQLAlchemy)
├── models/    # Data models for SQLite
├── routers/   # API endpoints (Resource-oriented architecture)
├── schemas/   # Data validation schemas (Pydantic)
└── services/  # Business logic (AI, Vectors, Grammar)
```

### 🧠 Key Features

* **Full Privacy:** All AI processing happens locally on your hardware. No conversation data is sent to external servers (OpenAI, etc.).
* **Intelligent Memory:** Thanks to the vector database, the tutor can remember that you made a "Present Perfect" mistake three days ago and reinforce it in today’s session.
* **Dual Validation:** Combines deterministic grammar rules (LanguageTool) with the flexibility of an LLM.

### 🛠️ Installation and Usage

1. **Clone and set up environment:**

```shell
git clone <repository-url>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Environment Variables:**
   Create a `.env` file based on the models you want to use (e.g., Meta-Llama-3-8B-Instruct.Q4_0.gguf).

3. **Run the Application:**

```shell
python run.py
```

### Tutorial

you can find the full tutorial on [EnglishTutor AI Tutorial](https://amoelcodigo.com/posts/python-local-chatbot-1/).

### 📝 License

This project is for educational and personal use. Developed with ❤️ to master English through AI.
