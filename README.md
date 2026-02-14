# Questlog Bot Monorepo ⚔️📜

Welcome to the **Questlog Bot** monorepo. This project is a specialized ecosystem designed for tabletop RPG players, combining high-quality voice recording with automated AI transcription.

## 🚀 Project Overview

This monorepo contains two primary services:

1.  **Craig (Recording Bot)**: A powerful multi-track voice recording bot for Discord. It captures every participant's audio in high fidelity.
2.  **Scribble Scribe (AI Transcription)**: A dedicated Python service that uses **OpenAI Whisper** to process recordings, generating chronological logs and storing them in a database for future web access.

## 🛠️ Infrastructure

The project is fully containerized and includes:
- **PostgreSQL**: Central database for bot data and transcriptions.
- **Redis**: Fast storage for Craig's recording coordination.
- **Docker Compose**: Orchestrates all services, making it easy to deploy on a homelab or VPS.

---

## ⚙️ Configuration & Setup

### 1. Discord Bot Setup
To connect Craig to your Discord server, you must create an application in the [Discord Developer Portal](https://discord.com/developers/applications):

1.  **Create Application**: Click "New Application" and give it a name.
2.  **Bot Token**: Go to the "Bot" tab, click "Reset Token" to get your **`DISCORD_BOT_TOKEN`**.
3.  **Privileged Gateway Intents**: In the same "Bot" tab, enable:
    - `Presence Intent`
    - `Server Members Intent`
    - `Message Content Intent` (REQUIRED for commands)
4.  **Client ID**: Go to "OAuth2" -> "General" to find your **`DISCORD_APP_ID`**.
5.  **Invite Bot**: Go to "OAuth2" -> "URL Generator":
    - Select Scopes: `bot`, `applications.commands`.
    - Bot Permissions: `Administrator` (easiest for setup) or at least `Connect`, `Speak`, `Use Slash Commands`.
6.  **Guild ID**: Enable "Developer Mode" in Discord settings, right-click your server icon, and "Copy Server ID" to get **`DEVELOPMENT_GUILD_ID`**.

### 2. Environment Variables
Copy the example environment file and fill in your credentials from the steps above:
```bash
cp .env.example .env
```

You **must** provide:
- `DISCORD_BOT_TOKEN`, `DISCORD_APP_ID`, and `DEVELOPMENT_GUILD_ID` for the bot to function.
- `POSTGRES` credentials for database access.

### 2. Whisper Transcription Settings
The **Scribble Scribe** service uses Whisper. You can configure the model size in the `.env` file via `WHISPER_MODEL`:

| Model | Parameters | Required VRAM | Relative Speed | Accuracy |
| :--- | :--- | :--- | :--- | :--- |
| **tiny** | 39 M | ~1 GB | ~32x | Base |
| **base** | 74 M | ~1 GB | ~16x | Good |
| **small** | 244 M | ~2 GB | ~6x | Better |
| **medium** | 769 M | ~5 GB | ~2x | High |
| **large** | 1550 M | ~10 GB | 1x | State of the art |

*Note: For RPG sessions with mixed accents or background noise, **small** or **medium** is recommended for a good balance of speed and accuracy.*

### 3. Hardware Acceleration (GPU)
If you have an NVIDIA GPU, set `WHISPER_DEVICE=cuda` in `.env`. Ensure you have the `NVIDIA Container Toolkit` installed on your host machine to allow Docker to access the GPU.

---

## 🏃 How to Execute

### Using Docker Compose (Recommended)
This monorepo is configured to avoid common port conflicts in homelabs.

| Service | Internal Port | External Port (Host) |
| :--- | :--- | :--- |
| **PostgreSQL** | 5432 | **5435** |
| **Redis** | 6379 | **6385** |
| **Craig Web** | 3000 | **3080** |
| **Craig API** | 5029 | **5080** |

**To start everything:**
```bash
docker-compose up --build
```

### Manual Mode (pnpm)
The monorepo uses `pnpm` workspaces. To install dependencies across all JS services:
```bash
pnpm install
```

---

## 📂 Repository Structure

- `/services/craig`: The voice recording engine (Node.js).
- `/services/scribble-scribe`: The AI transcription service (Python).
- `/packages/*`: Shared utilities and libraries.
- `docker-compose.yml`: Root orchestration file.

---
*Created for adventurers. Transcribed by machines.*
