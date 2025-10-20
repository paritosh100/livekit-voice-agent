# LiveKit Voice Agent (v0 API)

A real-time voice agent built using **LiveKit Agents v0.12.x** and **OpenAI Realtime API**, compatible with the **MultimodalAgent** and **FunctionContext** classes.  
This version connects to a LiveKit room, listens for audio, and responds in real time using text and speech modalities.

---

## 1. Overview
The project initializes an OpenAI Realtime model (`shimmer` voice), manages a LiveKit session, and greets participants when they join.  
It supports function calling through the `AssistantFnc` class defined in `api.py`.

---

## 2. Requirements
| Component | Version |
|------------|----------|
| Python | ≥ 3.10 |
| livekit | ≥ 0.19.1 |
| livekit-agents | ≥ 0.12.11, < 1.0.0 |
| livekit-plugins-openai | ≥ 0.10.17, < 1.0.0 |
| python-dotenv | ≥ 1.0 |

Install dependencies:
```bash
py -3.10 -m venv livekit_agent\ai
livekit_agent\ai\Scripts\activate
pip install --upgrade pip
pip install livekit>=0.19.1 "livekit-agents>=0.12.11,<1.0.0" "livekit-plugins-openai>=0.10.17,<1.0.0" python-dotenv
```

---

## 3. Project Structure
```
.
├─ agent.py          # Main entrypoint — creates model & starts MultimodalAgent
├─ api.py            # Defines AssistantFnc class inheriting from FunctionContext
├─ prompts.py        # Contains WELCOME_MESSAGE, INSTRUCTIONS, etc.
├─ .env              # LiveKit + OpenAI credentials
└─ requirements.txt  # Optional pinned versions
```

---

## 4. Environment Setup
Create a `.env` file in the project root:
```ini
LIVEKIT_URL=wss://<your-livekit-host>
LIVEKIT_API_KEY=<your-api-key>
LIVEKIT_API_SECRET=<your-api-secret>
OPENAI_API_KEY=<your-openai-key>
```

---

## 5. Running the Agent
```bash
livekit_agent\ai\Scripts\activate
python agent.py
```
The agent connects to your LiveKit server, waits for a participant, and starts streaming when someone joins.

Example log:
```
INFO livekit.agents - job runner initialized
INFO livekit.agents - waiting for participant
```

---

## 6. Using LiveKit Playground
1. Go to [LiveKit Playground](https://playground.livekit.io)  
2. Create a new Room and copy the connection URL  
3. Run your local worker (`python agent.py`)  
4. Speak into the microphone — the agent greets you with the `WELCOME_MESSAGE`  

---

## 7. Extending AssistantFnc
You can extend `api.py` to add more tools or function calls:
```python
async def lookup_vin(self, vin: str):
    return f"Found record for VIN {vin}"
```

All async functions inside the `FunctionContext` subclass become available for the model to call.

---

## 8. Key Concepts
| Component | Purpose |
|------------|----------|
| `MultimodalAgent` | Handles text + audio modalities |
| `RealtimeModel` | Connects to OpenAI’s real-time API |
| `FunctionContext` | Defines callable functions for the agent |
| `session.conversation.item.create()` | Adds a new message to the conversation |
| `session.response.create()` | Generates a model response |

---

## 9. Troubleshooting
| Error | Cause | Fix |
|-------|--------|-----|
| `MultimodalAgent not found` | Installed v1 API | Downgrade: `livekit-agents<1.0.0` |
| `FunctionContext missing` | Wrong version | Same downgrade |
| No response | Worker not connected | Check `.env` keys and LiveKit URL |
| No audio playback | Browser mic permissions | Enable microphone |
| Unexpected arg errors | Mixing v1 imports | Ensure all use `livekit-agents 0.12.x` |

---

## 10. Recommended Versions (requirements.txt)
```
livekit>=0.19.1
livekit-agents>=0.12.11,<1.0.0
livekit-plugins-openai>=0.10.17,<1.0.0
python-dotenv>=1.0
```

---

## 11. Notes
- This README corresponds to your downgraded environment where `MultimodalAgent` and `FunctionContext` are still supported.  
- Keep versions pinned to prevent auto-upgrade to v1.  
- The project is fully compatible with **LiveKit Playground** and **OpenAI Realtime models**.

---

© 2025 — LiveKit Voice Agent (v0 API)
