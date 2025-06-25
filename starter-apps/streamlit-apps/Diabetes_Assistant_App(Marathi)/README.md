# 🩺 Diabetes Bilingual Chatbot (Marathi & English) with SUTRA-v2 Multilingual LLM, Mem0 Memory & Gemini AI

A conversational, personalized, diabetes care chatbot built using **Streamlit**, **Google Gemini**, **Mem0 Memory**, and **SUTRA multilingual LLM**.
Supports both **English and Marathi**, remembers past health details, and provides culturally relevant, diabetic-safe guidance to users across sessions.

---

## 🚀 Features

* 🔍 **Multi-user personalized memory** with Mem0 (remembers health data per user ID)
* 🌐 **Bilingual Support** (English / Marathi) — auto-detects language per query
* 🧠 **Context-aware conversations**: Past chat memories influence responses (e.g., medications, symptoms)
* 🍽️ **Diabetes-Safe Lifestyle Guidance** (snacks, meals, activity, doctor consultations)
* 🔄 **Streamlit Form-based Chat UI** — clean, single-enter per query (no multiple Enter presses)
* 💾 **Mem0 Update Guarantee**: Any new user info (e.g., symptoms, location) is stored automatically
* ✅ Works seamlessly for **new and returning users**

---

## 🏗️ Tech Stack

| Technology                  | Purpose                                              |
| --------------------------- | ---------------------------------------------------- |
| **Streamlit**               | Frontend (Interactive Chat UI)                       |
| **Mem0.ai**                 | Long-term per-user memory storage                    |
| **Google Gemini 1.5 Flash** | AI content generation & reasoning                    |
| **SUTRA LLM via Agno**      | Language detection, translation (English ↔️ Marathi) |
| **Python**                  | Backend Logic                                        |

---

## 🔧 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/diabetes-bilingual-chatbot.git
cd diabetes-bilingual-chatbot
```

2. **Install Required Packages**

```bash
pip install -r requirements.txt
```

3. **Update API Keys in `app.py`:**

```python
genai.configure(api_key="YOUR_GEMINI_API_KEY")
client = MemoryClient(api_key="YOUR_MEM0_API_KEY")
sutra_agent = Agent(
    model=OpenAILike(
        api_key="YOUR_SUTRA_API_KEY",
        base_url="https://api.two.ai/v2"
    )
)
```

---

## 💡 How It Works

1. **User ID Detection**:
   On first run, the user enters their unique ID.
   If new → basic health info (age, type of diabetes, medication) is collected and stored to Mem0.

2. **Language Auto-Detection**:
   Each query’s language is detected (Marathi or English) and translated to English for Gemini.

3. **Personalized Context Memory**:
   Mem0 provides prior memories — personal info, symptoms, habits — which Gemini uses to generate relevant, safe, and India-specific responses.

4. **Dynamic Prompt Handling**:
   Gemini's response is tailored based on detected intent (snack, doctor consult, medication etc.) and only the **relevant memories** are included to avoid context confusion.

5. **Response Language & Storage**:
   Gemini's output is re-translated to Marathi if required, and every conversation piece is stored back into Mem0 for future personalization.

---

## 🛡️ Important Notes

* This app **does not replace professional medical advice**.
* All user data stays private — handled via Mem0 secure storage.
* App can support any number of **unique user IDs**.

---

## 🚧 Future Enhancements

* 🩺 **Glucose Spike Prediction** based on user input history
* 📈 Visualization of user health data
* 📲 WhatsApp / Mobile App integration
* 🔍 More regional languages (Hindi, Tamil, Bengali)

---

## 🙏 Acknowledgements

* [Mem0.ai](https://mem0.ai) — Long-term Memory API
* [Google Gemini](https://ai.google.dev) — GenAI Responses
* [Two AI / SUTRA LLM](https://two.ai) — Multilingual LLM
* [Streamlit](https://streamlit.io) — Interactive Web App Framework
* [Agno](https://pypi.org/project/agno/) — Agent management for LLM APIs

---

## 📜 License

MIT License — Free to use, modify, distribute with attribution.

---

