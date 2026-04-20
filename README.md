# 🤖 TalentScout Hiring Assistant

AI-powered chatbot for automating the initial technical screening process of candidates using LLMs and conversational workflows.

---

## 🚀 Live Demo
https://prashantgupta77-hiring-assistant-chatbot-app-qmvjii.streamlit.app/

---

## 📌 Project Overview

TalentScout Hiring Assistant simulates a recruiter-like interaction to streamline candidate screening.

It performs:
- Candidate information collection
- Resume parsing and data extraction
- Tech stack-based question generation
- AI-driven answer evaluation
- Final screening summary with recommendation

---

## ✨ Key Features

- 💬 Conversational chatbot interface  
- 📄 Resume upload (PDF, DOCX, TXT)  
- 🧠 LLM-based technical question generation  
- 📊 Automated scoring and feedback  
- 📈 Final hiring recommendation  
- 🔁 State-machine based flow control  

---

## 🏗️ System Architecture


User (Streamlit UI)
↓
Conversation Manager (State Machine)
↓
Service Layer (Business Logic)
↓
LLM (Groq - LLaMA)


---

## 📁 Project Structure


Hiring-Assistant-Chatbot/
│
├── config/ # Configuration
│ ├── constants.py # Tech keywords, exit commands
│ └── settings.py # Environment variables & model config
│
├── src/
│ ├── core/ # Conversation logic
│ │ ├── conversation_manager.py
│ │ └── state_machine.py
│ │
│ ├── models/ # Data models
│ │ ├── candidate.py
│ │ ├── session.py
│ │ └── screening_result.py
│ │
│ ├── prompts/ # Prompt templates
│ │ ├── evaluation_prompt.py
│ │ └── question_generation_prompt.py
│ │
│ ├── services/ # Business logic
│ │ ├── candidate_service.py
│ │ ├── llm_service.py
│ │ ├── question_service.py
│ │ ├── resume_service.py
│ │ └── scoring_service.py
│ │
│ ├── ui/ # Streamlit UI helpers
│ │ ├── components.py
│ │ └── streamlit_app.py
│ │
│ └── utils/ # Helper utilities
│ ├── tech_normalizer.py
│ └── validators.py
│
├── app.py # Main Streamlit entry point
├── .env.example # Environment template
├── requirements.txt
├── README.md
└── .gitignore


---

## 🔄 Application Workflow

- User starts the chatbot  
- Resume upload (optional)  
- Resume data extraction  
- Missing details collected via chat  
- Technical questions generated  
- Candidate answers questions  
- Answers evaluated using LLM  
- Final screening summary generated  

---

## 🧠 Core Components

### Conversation Manager
Controls the entire chatbot flow using a state machine.

### Resume Service
Extracts structured data from resumes and cleans tech stack.

### Question Service
Generates role-specific technical questions using LLM.

### Scoring Service
Evaluates answers and returns score + feedback.

### Candidate Service
Builds final summary and hiring recommendation.

### LLM Service
Handles interaction with Groq API.

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository
git clone https://github.com/PrashantGupta77/Hiring-Assistant-Chatbot.git  
cd Hiring-Assistant-Chatbot  

### 2️⃣ Create Virtual Environment
python -m venv venv  
source venv/bin/activate      (Mac/Linux)  
venv\Scripts\activate         (Windows)  

### 3️⃣ Install Dependencies
pip install -r requirements.txt  

### 4️⃣ Configure Environment

Create a `.env` file:

GROQ_API_KEY=your_api_key_here  
MODEL_NAME=llama-3.1-8b-instant  

---

## ▶️ Run the Application

streamlit run app.py  

---

## ⚠️ Challenges & Solutions

**Tech stack noise from resume**  
→ Improved extraction using section-based parsing and normalization  

**Multi-step conversation handling**  
→ Implemented state-machine architecture  

**LLM output inconsistency**  
→ Used structured prompts and parsing  

---

## 🔮 Future Improvements

- FastAPI backend for scalability  
- Database integration  
- Advanced NLP resume parsing  
- Multi-language support  

---

## 🔐 Data Handling

- No persistent storage  
- Session-based processing  
- Safe for demo and prototype use  

---

## 👨‍💻 Author

**Prashant Kumar Gupta**