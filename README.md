# LLamina -- Quickstart

Ein leichter Gateway/Proxy, der die **LM Studio REST API (`/api/v0`)**
und die **OpenAI-kompatiblen Endpoints (`/v1`)** 1:1 durchreicht.

------------------------------------------------------------------------

## 🚀 Installation

### 1. Repository klonen

``` bash
git clone https://github.com/DEIN_REPO/llamina.git
cd llamina
```

### 2. (Optional) Poetry installieren + lokale venv aktivieren

``` bash
pip install poetry
poetry config virtualenvs.in-project true
```

### 3. Abhängigkeiten installieren

``` bash
poetry install
```

### 4. Virtuelle Umgebung aktivieren (optional)

**Linux / macOS:**

``` bash
source .venv/bin/activate
```

**Windows (PowerShell):**

``` powershell
.\.venv\Scripts\activate
```

> Hinweis: Für den Start per `poetry run` muss die venv **nicht** aktiv
> sein.

------------------------------------------------------------------------

## ⚙️ .env Datei

Erstelle eine Datei `.env` im Projektordner:

``` env
BACKEND_URL=http://localhost:1234
```

> LM Studio muss laufen (`lms server start`).

------------------------------------------------------------------------

## ▶️ Proxy starten

``` bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Der Proxy läuft dann unter:

    http://localhost:8000

Beispiele:

    http://localhost:8000/api/v0/models
    http://localhost:8000/v1/chat/completions

------------------------------------------------------------------------

## 📦 Projektstruktur

``` text
app/
├─ main.py               # FastAPI App
├─ api/
│  ├─ lmstudio_v0.py     # /api/v0/... Proxy
│  └─ openai_v1.py       # /v1/... Proxy
└─ core/
   ├─ config.py          # .env Settings
   └─ proxy.py           # zentraler Proxy
```

------------------------------------------------------------------------

## ✔️ Fertig!

Der Proxy ist sofort einsatzbereit und vollständig LM Studio kompatibel.
