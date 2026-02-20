# 🐬 Animal Crossing LLM Mod

**Transform Animal Crossing into an AI-powered conversation experience!** This mod uses Large Language Models (LLMs) to generate dynamic, contextual dialogue for villagers in real-time.

> ⚠️ **EXPERIMENTAL SOFTWARE**: This mod has known bugs and supports Windows and macOS. Note: Newer versions of macOS may have issues reading memory due to System Integrity Protection (SIP). The only supported language is English. Use at your own risk! PRs welcome to help improve it.

---

## ✨ Features

Ever wanted to have meaningful conversations with your Animal Crossing villagers? This mod brings them to life:
- **Smart Dialogue Generation**: Context-aware responses based on game state, utilizing Google Gemini or OpenAI models.
- **Real-time Integration**: Reads dialogue directly from the GameCube memory and writes new AI dialogue back seamlessly.
- **Screenshot Context**: Captures game screens to provide visual context (location, weather, items) to the AI.
- **Gossip System**: Villagers have a persistent memory; they remember past conversations and reference them later.
- **Memory Safety**: Designed to prevent overwriting active memory during conversations.

---

## 📋 Prerequisites

Before starting, ensure you have the following ready:
1. **Python 3.8+** installed on your system ([python.org](https://python.org)).
2. **Dolphin Emulator** installed and configured.
3. **Animal Crossing (GAFE01) ROM** (GameCube version).
4. An **API Key** from either Google Gemini (Free tier available) or OpenAI.

---

## 🚀 Installation

Install the mod by running the easy installer for your platform. This will create a virtual environment (`venv`) and install all required dependencies.

**Windows:**
```cmd
install.bat
```

**macOS/Linux:**
```bash
./install.sh
```

*(Alternatively, you can manually create a virtual environment and run `pip install -r requirements.txt`)*

---

## ⚙️ Configuration

1. Create a `.env` file in the project folder (you can copy `env_template.txt` to `.env`).
2. Add your API keys and configure the mod settings:

```bash
# Choose your primary LLM provider (google or openai)
MODEL_PROVIDER=openai

# Your API Keys (Only the one for your chosen provider is required)
GOOGLE_API_KEY=your_gemini_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here

# Enable/Disable Features (1 = Yes, 0 = No)
ENABLE_SCREENSHOT=1             # Capture screenshots for context
ENABLE_GOSSIP=1                 # Villagers remember past conversations
GENERATION_SUPPRESS_SECONDS=25  # Cooldown between generations
```

---

## 🧪 Experimental Mode (Fix for macOS SIP / Linux)

If you are on **macOS** and see `Error code: 5`, or if you are on **Linux**, you must use the experimental GDB Memory Reader. This mode is platform-agnostic and uses a network socket instead of OS-level memory access.

### 1. Enable GDB in Dolphin
1. Open Dolphin Emulator.
2. Go to **Config** -> **Advanced**.
3. Check the box for **Enable GDB Stub**.
4. (Optional) Ensure the port is set to `2345`.

### 2. Enable in Mod Settings
Add this line to your `.env` file:
```bash
USE_GDB_MEMORY=1
```

*Note: This mode is experimental and may have slightly higher latency than direct memory access.*

---

## 🎮 Usage

**⚠️ IMPORTANT**: Start Animal Crossing in Dolphin and wait until you are *past the loading screen and in the actual game world* before launching the mod.

Before running the scripts, make sure your virtual environment is activated:
- **Windows:** `venv\Scripts\activate`
- **macOS/Linux:** `source venv/bin/activate`

### 1. Watch Mode (Continuous)
This is the recommended mode for general gameplay or streaming. The mod will run in the background, continuously monitoring your interactions and generating dialogue dynamically.

```bash
python ac_parser_encoder.py --watch
```

### 2. One-Shot Mode (Manual)
```bash
# Read memory and PRINT the AI dialogue (does not write to the game)
python ac_parser_encoder.py

# Read memory, generate AI dialogue, and WRITE it back to the game
python ac_parser_encoder.py --write
```

---

## 🧠 How It Works

1. **Memory Engine**: Connects to Dolphin using `dolphin-memory-engine` or the GDB Stub to access the GameCube's live memory.
2. **State Analysis**: Detects when a conversation starts, reads the existing dialogue, and optionally takes a screenshot.
3. **AI Generation**: Sends the game state, visual context, and character personality to an LLM to formulate a response.
4. **Encoding**: Converts the AI response back into Animal Crossing's specific text format (including control codes and animations).
5. **Injection**: Writes the generated text directly back to the dialogue memory address, taking over the conversation in real-time.

---

## ⚠️ Known Issues & Limitations

- **Emulator Only**: This mod requires Dolphin emulator; it cannot run on original hardware.
- **Timing Sensitivity**: The mod must be started *after* entering the game world.
- **Platform Limitations**: While Windows and macOS are supported, newer macOS versions might block memory reading features due to System Integrity Protection (SIP) unless using GDB Mode.
- **Language**: Only English is supported at this time.
- **Stability**: This is experimental software. The mod may occasionally crash or fail to write memory cleanly.

---

## 🤝 Contributing

Found a bug? Want to add features? **Contributions are very welcome!** This mod needs community help to become stable.

**Areas Needing Help:**
- 🐛 **Bug Fixes**: Resolve crashes, improve memory stability, and refine memory injection.
- 🖥️ **Platform Support**: Improve Linux and GDB Mode compatibility.
- 🎮 **Game Versions**: Expand memory address support for different Animal Crossing releases.
- 🧠 **LLM Providers**: Add support for local LLMs (like Ollama).

**How to Contribute:**
1. Open an issue with detailed error logs and system info.
2. Submit a pull request with your fixes or improvements.

**Ready to bring your Animal Crossing villagers to life with AI?** 🎮✨
