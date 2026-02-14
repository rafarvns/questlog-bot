# Análise do Fluxo de Gravação de Áudio do Craig

Este documento descreve como o Craig (o bot de gravação) lida com os dados de áudio, baseado na análise do código fonte em `services/craig`. Isso é essencial para o planejamento da integração com o **Scribble Scribe**.

## 1. Estrutura de Dados e Armazenamento
Quando o Craig grava uma sessão, ele não cria um arquivo simples de MP3 ou WAV. Em vez disso, ele gera um conjunto de arquivos com o mesmo nome base, mas extensões diferentes, para armazenar dados brutos e metadados de forma eficiente.

- **`.data`**: Contém os pacotes de áudio brutos (geralmente Ogg Opus) envoltos em um fluxo customizado tipo Ogg. Inclui timestamps e identificadores de cada trilha (track).
- **`.header1` / `.header2`**: Armazena os cabeçalhos Ogg (BOS - Beginning of Stream) para cada trilha.
- **`.users`**: Um arquivo tipo JSON que associa os números das trilhas às informações dos usuários do Discord (ID, username, etc).
- **`.log`**: Arquivo de log da sessão de gravação.

## 2. Processo de Gravação (`RecordingWriter`)
1. **Inicialização**: Um `RecordingWriter` é criado com um `fileBase`. Ele abre fluxos de escrita (write streams) para todos os arquivos mencionados acima.
2. **Captura de Áudio**: À medida que os pedaços (chunks) de áudio chegam do Discord (ou da Webapp), eles são enfileirados e gravados no arquivo `.data` usando um `OggEncoder`.
3. **Rastreamento de Usuário**: Quando um usuário começa a falar ou entra na gravação, seus metadados são gravados em `.users` e seus cabeçalhos Ogg nos arquivos `.header`.
4. **Codificação**: O áudio é tratado principalmente como **Opus** (padrão do Discord) ou **FLAC** (para captura de alta qualidade via web).

## 3. Oportunidades de Integração para o Scribble Scribe

Para transcrever o áudio capturado pelo Craig, o Scribble Scribe tem alguns caminhos:

### Caminho A: Processamento Pós-Gravação
- **Gatilho**: Escutar o evento de "gravação encerrada" ou monitorar o sistema de arquivos por novos arquivos `.data`.
- **Ação**: O Scribble Scribe lê os arquivos `.data`, `.header` e `.users`, reconstrói o áudio por usuário e executa a transcrição (ex: usando Whisper).
- **Prós**: Integração mais simples; não interfere na performance da gravação em tempo real.

### Caminho B: "Sidecar" em Tempo Real
- **Gatilho**: Craig emite eventos de "pedaço gravado" via fila de mensagens (Redis) ou um hook no `RecordingWriter`.
- **Ação**: O Scribble Scribe recebe os pedaços Opus ao vivo, faz o buffering e transcreve em tempo quase real.
- **Prós**: Menor latência; permite legendas ao vivo.

## 4. Recomendação Inicial
Para a primeira versão do **Scribble Scribe**, devemos focar no **Caminho A (Pós-Gravação)**.
1. O Craig termina uma gravação.
2. Uma tarefa (possivelmente em `services/craig/apps/tasks`) dispara uma notificação.
3. O Scribble Scribe coleta os arquivos brutos, usa `ffmpeg` ou ferramenta similar para converter os pedaços Opus para um formato que o Whisper aceite (WAV/16kHz), e realiza a transcrição.

---

# Craig Audio Recording Workflow Analysis


This document describes how Craig (the recording bot) handles audio data, based on the `services/craig` source code analysis. This is essential for planning the integration with **Scribble Scribe**.

## 1. Data Structure and Storage
When Craig records a session, it doesn't create a single MP3 or WAV file. Instead, it generates a set of files with the same base name but different extensions to store raw data and metadata efficiently.

- **`.data`**: Contains the raw audio packets (usually Ogg Opus) wrapped in a custom Ogg-like stream. It includes timestamps and track identifiers.
- **`.header1` / `.header2`**: Stores the Ogg headers (BOS - Beginning of Stream) for each track.
- **`.users`**: A JSON-like file mapping track numbers to Discord user information (ID, username, discriminator).
- **`.log`**: Log file for the recording session.

## 2. Recording Process (`RecordingWriter`)
1. **Initialization**: A `RecordingWriter` is created with a `fileBase`. It opens write streams for all the files mentioned above.
2. **Audio Capture**: As audio chunks arrive from Discord (or the Webapp), they are queued and written to the `.data` file using an `OggEncoder`.
3. **User Tracking**: When a user starts speaking or joins the recording, their metadata is written to `.users` and their Ogg headers to `.header` files.
4. **Encoding**: Audio is primarily handled as **Opus** (Standard for Discord) or **FLAC** (for high-quality web capture).

## 3. Integration Opportunities for Scribble Scribe

To transcribe audio captured by Craig, Scribble Scribe has a few paths:

### Path A: Post-Recording Processing
- **Trigger**: Listen for the "recording ended" event or monitor the file system for `.data` files.
- **Action**: Scribble Scribe read the `.data`, `.header`, and `.users` files, reconstructs the audio per user, and runs transcription (e.g., using Whisper).
- **Pros**: Simplest integration; doesn't interfere with real-time recording performance.

### Path B: Real-time "Sidecar"
- **Trigger**: Craig emits "chunk written" events via a message queue (Redis) or a hook in `RecordingWriter`.
- **Action**: Scribble Scribe receives live Opus chunks, buffers them, and transcribes in near real-time.
- **Pros**: Lower latency; allows for live captions.

## 4. Initial Recommendation
For the first version of **Scribble Scribe**, we should focus on **Path A (Post-Recording)**. 
1. Craig finishes a recording.
2. A task (possibly in `services/craig/apps/tasks`) triggers a notification.
3. Scribble Scribe picks up the raw files, uses `ffmpeg` or a similar tool to convert Opus chunks to a format Whisper likes (WAV/16kHz), and performs the transcription.

---
*Note: This is a temporary analysis document for planning purposes.*
