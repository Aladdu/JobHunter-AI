# 💼 JobHunter-AI: Autonomous ATS Resume Optimizer & Interview Prep Agent

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/Tests-5%20Passed-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Author](https://img.shields.io/badge/Author-Ajay%20Avunoori-emerald.svg)](https://github.com/Aladdu)

**JobHunter-AI** is an autonomous engineering agent designed to solve the modern job search bottleneck. It analyzes real-world Job Descriptions (JDs), benchmarks candidate resumes against Applicant Tracking System (ATS) filtering algorithms, rewrites bullet points into quantifiable **Google XYZ impact metrics**, and generates role-specific technical interview cheat sheets.

---

## ⚡ Key Features

- **🎯 Real-Time ATS Match Scoring (0–100%):** Evaluates keyword coverage, action verb frequency, quantifiable impact metrics, and single-column ATS formatting compliance.
- **🔍 Skill Taxonomy & Entity Extraction:** Recognizes 80+ engineering technologies (Java, Spring Boot, React, MySQL, Microservices, Docker, AWS, DSA) and maps synonyms to canonical standards.
- **✨ Google XYZ Bullet Point Rewriter:** Automatically elevates passive phrases (*"worked on"*, *"assisted"*) into high-impact accomplishment statements:  
  $$\text{Accomplished [X]} \text{ as measured by [Y]}, \text{ by doing [Z]}$$
- **📄 Dual Export Formats:** Instant export to ATS-optimized Markdown or single-column Microsoft Word (`.docx`) adhering strictly to standard margins, headers, and bullet structures.
- **🧠 Custom Interview Preparation Engine:** Automatically pinpoints skill gaps between your profile and the JD to produce tailored system design, core technical, and STAR-method behavioral interview talking guides.

---

## 🏗️ Architecture

```
                  ┌──────────────────────────────┐
                  │ Target Job Description (JD)  │
                  └──────────────┬───────────────┘
                                 │
  ┌───────────────────────┐      │
  │ Master Candidate Data ├──────┤
  └───────────────────────┘      ▼
                     ┌───────────────────────┐
                     │ Skill Taxonomy Engine │ (core/skill_taxonomy.py)
                     └───────────┬───────────┘
                                 │
             ┌───────────────────┴───────────────────┐
             ▼                                       ▼
  ┌─────────────────────┐                 ┌─────────────────────┐
  │  ATS Scorer Engine  │                 │ Bullet Rewriter &   │
  │ (core/ats_scorer.py)│                 │ Tailoring Agent     │
  │  - Keyword match    │                 │ (core/rewriter.py)  │
  │  - Verb density     │                 │  - Google XYZ       │
  │  - Metric scanner   │                 │  - Interview prep   │
  └──────────┬──────────┘                 └──────────┬──────────┘
             │                                       │
             └───────────────────┬───────────────────┘
                                 ▼
                     ┌───────────────────────┐
                     │ FastAPI REST Endpoints│ (api/main.py)
                     └───────────┬───────────┘
                                 ▼
            ┌─────────────────────────────────────────┐
            │ Interactive Web App & ATS Document (.docx)│
            └─────────────────────────────────────────┘
```

---

## 📂 Project Structure

```bash
JobHunter-AI/
├── api/
│   └── main.py              # FastAPI server & REST endpoints
├── core/
│   ├── __init__.py
│   ├── ats_scorer.py        # ATS scoring & compliance diagnostics
│   ├── docx_generator.py    # Clean single-column Word (.docx) builder
│   ├── rewriter.py          # Google XYZ rewriter & interview generator
│   └── skill_taxonomy.py    # Structured tech skill taxonomy & action verbs
├── static/
│   └── index.html           # Interactive web UI (Tailwind CSS + JS)
├── tests/
│   └── test_agent.py        # Automated test suite (Pytest)
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/Aladdu/JobHunter-AI.git
cd JobHunter-AI
```

### 2. Set up virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Automated Tests
```bash
python3 -m pytest tests/
```

### 4. Start the Application Server
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser and navigate to: `http://localhost:8000`

---

## 🧪 Testing Coverage

The repository includes a comprehensive test suite covering:
- Entity extraction for programming languages, backend frameworks, and databases.
- Strong action verb detection vs. weak phrasing penalties.
- Quantitative metric parsing ($O(n)$, %, ms latency).
- High-probability interview question generation.

Run tests anytime with:
```bash
pytest -v
```

---

## 👨‍💻 Author

**Ajay Avunoori**  
- **GitHub:** [@Aladdu](https://github.com/Aladdu)  
- **Portfolio:** [avunooriajayportfolio1.netlify.app](https://avunooriajayportfolio1.netlify.app/)  
- **Specialization:** Java Full Stack Developer (Java 17/21, Spring Boot, React.js, MySQL, Microservices)
