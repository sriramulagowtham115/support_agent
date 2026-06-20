# 🤖 Persona Adaptive Customer Support Agent

## 📌 Overview

Persona Adaptive Customer Support Agent is an intelligent AI-powered support system that:

* Detects customer communication persona
* Retrieves information from a local knowledge base using RAG (Retrieval-Augmented Generation)
* Adapts responses according to customer persona
* Escalates sensitive or low-confidence issues to a human agent

---

## 🚀 Features

### ✅ Persona Classification

The system classifies customers into one of the following personas:

* **Technical Expert**

  * Uses technical terminology
  * Talks about APIs, tokens, logs, configurations

* **Frustrated User**

  * Uses emotional language
  * Expresses urgency or complaints

* **Business Executive**

  * Focuses on business impact
  * Wants concise answers and timelines

---

### ✅ Retrieval-Augmented Generation (RAG)

The agent uses:

* Gemini Embeddings (`gemini-embedding-001`)
* ChromaDB Vector Database
* Semantic Similarity Search

Knowledge documents are stored in the `data/` folder and indexed into ChromaDB.

---

### ✅ Adaptive Response Generation

Responses are customized based on the detected persona.

Examples:

* Technical Experts receive detailed technical explanations.
* Frustrated Users receive empathetic and simple responses.
* Business Executives receive concise business-focused summaries.

---

### ✅ Human Escalation

The system escalates conversations when:

* Billing or refund issues are detected
* Retrieval confidence is below threshold
* User frustration persists over multiple interactions

A structured JSON handoff is generated for human agents.

---

# 🏗️ Project Structure

```text
persona_support_agent/

│── app.py
│── requirements.txt
│── README.md
│── .env

├── data/
│   ├── api_troubleshooting.md
│   ├── billing_policy.txt
│   └── password_reset_guide.txt

├── chroma_db/

└── src/
    ├── config.py
    ├── classifier.py
    ├── rag_pipeline.py
    ├── escalator.py
    └── generator.py
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone <your-repository-url>

cd persona_support_agent
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure API Key

Create `.env`

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 🧪 Sample Test Cases

### Technical Expert

**Input**

```text
What should I check for 401 Unauthorized?
```

**Expected**

* Persona → Technical Expert
* Retrieve API troubleshooting document
* Technical response

---

### Frustrated User

**Input**

```text
Where is the guide to clear cookies? It's been an hour and nothing is loading!
```

**Expected**

* Persona → Frustrated User
* Empathetic response

---

### Business Executive

**Input**

```text
Our operational uptime is decreasing. We need a timeline.
```

**Expected**

* Persona → Business Executive
* Business-focused response

---

### Escalation

**Input**

```text
My billing statement has duplicate charges. I want a refund immediately.
```

**Expected**

* Escalation triggered
* Human handoff JSON generated

---

# 🛠️ Tech Stack

* Python 3.11+
* Streamlit
* Google Gemini API
* Gemini Embeddings (`gemini-embedding-001`)
* ChromaDB
* PyPDF
* dotenv

---

# 👨‍💻 Author

**Sriramula Gowtham**

B.Tech CSE (2021–2025)

Malla Reddy College of Engineering and Technology

Hyderabad, Telangana
