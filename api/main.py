"""
JobHunter-AI FastAPI Application Server.
Exposes REST endpoints for ATS analysis, autonomous job discovery,
company callback probability prediction, application dispatch, and adaptive learning feedback loops.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from core.ats_scorer import ATSAnalyzer
from core.rewriter import ResumeTailorAgent
from core.docx_generator import create_ats_docx
from core.job_search import JobDiscoveryEngine
from core.probability_engine import CallbackProbabilityEngine
from core.adaptive_agent import AdaptiveLearningAgent

app = FastAPI(
    title="JobHunter-AI Autonomous Agent",
    description="Autonomous Job Discovery, ATS Resume Tailor, Callback Predictor & Adaptive Feedback Agent",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core singletons
analyzer = ATSAnalyzer()
tailor_agent = ResumeTailorAgent()
discovery_engine = JobDiscoveryEngine()
prob_engine = CallbackProbabilityEngine()
adaptive_agent = AdaptiveLearningAgent()

# Pre-configured Master Profile for Ajay
DEFAULT_PROFILE = {
    "name": "Ajay Avunoori",
    "target_title": "Java Full Stack Developer",
    "email": "ajay.avunoori.dev@gmail.com",
    "phone": "+91 98765 43210",
    "location": "Hyderabad, Telangana, India",
    "github": "https://github.com/Aladdu",
    "linkedin": "https://linkedin.com/in/ajay-avunoori",
    "portfolio": "https://avunooriajayportfolio1.netlify.app/",
    "education": "Master of Computer Applications (MCA), Osmania University (2023)",
    "skills": [
        "Java", "Core Java", "OOP", "Spring Boot", "Spring Data JPA", "Hibernate",
        "REST APIs", "MySQL", "JavaScript", "React.js", "HTML5", "CSS3", "Tailwind CSS",
        "Git", "GitHub", "Maven", "Postman", "DSA", "Problem Solving"
    ],
    "raw_resume": """Ajay Avunoori
Hyderabad, India | ajay.avunoori.dev@gmail.com | +91 98765 43210
GitHub: https://github.com/Aladdu | Portfolio: https://avunooriajayportfolio1.netlify.app/

PROFESSIONAL SUMMARY:
Java Full Stack Developer and MCA Graduate (Osmania University, 2023). Passionate about Java, Spring Boot, React.js, and building clean web applications. Experienced with MySQL database design, REST APIs, and daily problem solving.

TECHNICAL SKILLS:
- Languages: Java, JavaScript, SQL, HTML, CSS
- Backend: Spring Boot, Hibernate, REST APIs, JDBC
- Frontend: React.js, Tailwind CSS, Responsive Design
- Databases & Tools: MySQL, Git, GitHub, Maven, Postman
- Core: OOP, Data Structures and Algorithms

PROJECTS:
- Electric Bill System: Worked on electric billing system using Java and MySQL. Created database tables, calculated bill amounts based on units, and used JDBC connection.
- ATM Simulation Project: Made an ATM simulation in Java and MySQL. Users can check balance, deposit, and withdraw money with PIN validation.
- Developer Portfolio: Built personal portfolio website using React.js and HTML/CSS to showcase education, projects, and skills.
- Daily DSA Practice: Solved coding questions in Java on LeetCode and CodeChef covering arrays, strings, and logic.

EDUCATION:
Master of Computer Applications (MCA) - Osmania University, Hyderabad (2023)
"""
}


class AnalyzeRequest(BaseModel):
    resume_text: str
    jd_text: str


class TailorRequest(BaseModel):
    resume_text: str
    jd_text: str
    profile: Optional[Dict[str, Any]] = None


class ApplyJobRequest(BaseModel):
    job_id: str
    custom_resume_text: Optional[str] = None


class FeedbackRequest(BaseModel):
    app_id: str
    status: str
    user_notes: str


class AddJobRequest(BaseModel):
    company: str
    title: str
    location: str
    experience: str
    salary_range: str
    tags: List[str]
    description: str


# ----------------- Existing Core Endpoints -----------------

@app.get("/api/defaults")
def get_defaults():
    return {
        "profile": DEFAULT_PROFILE,
        "sample_jds": discovery_engine.jobs
    }


@app.post("/api/analyze")
def analyze_match(req: AnalyzeRequest):
    if not req.resume_text.strip() or not req.jd_text.strip():
        raise HTTPException(status_code=400, detail="Resume and Job Description text are required.")

    report = analyzer.evaluate(req.resume_text, req.jd_text)
    prob_report = prob_engine.predict_callback(report, {})
    return {
        **report,
        "callback_prediction": prob_report
    }


@app.post("/api/tailor")
def tailor_resume(req: TailorRequest):
    profile = req.profile or DEFAULT_PROFILE
    report = analyzer.evaluate(req.resume_text, req.jd_text)
    matched_skills = report["skills_analysis"]["matched_skills"]
    missing_skills = report["skills_analysis"]["missing_skills"]

    raw_bullets = [
        "Worked on electric billing system using Java and MySQL to calculate bill amounts based on units.",
        "Made an ATM simulation in Java and MySQL for balance inquiry, deposit, and withdrawals with PIN.",
        "Built personal portfolio website using React.js and CSS to showcase education and projects.",
        "Solved coding questions in Java on LeetCode and CodeChef covering data structures and algorithms."
    ]

    tailored_summary = tailor_agent.generate_tailored_summary(profile, req.jd_text, matched_skills)
    optimized_bullets = tailor_agent.optimize_bullet_points(raw_bullets, missing_skills)
    interview_prep = tailor_agent.generate_interview_prep(req.jd_text, matched_skills, missing_skills)
    markdown_resume = tailor_agent.generate_full_resume_markdown(profile, tailored_summary, optimized_bullets, matched_skills)

    tailored_report = analyzer.evaluate(markdown_resume, req.jd_text)
    callback_prediction = prob_engine.predict_callback(tailored_report, {})

    return {
        "original_report": report,
        "tailored_report": tailored_report,
        "callback_prediction": callback_prediction,
        "tailored_summary": tailored_summary,
        "optimized_bullets": optimized_bullets,
        "markdown_resume": markdown_resume,
        "interview_prep": interview_prep
    }


@app.post("/api/export-docx")
def export_docx(req: TailorRequest):
    profile = req.profile or DEFAULT_PROFILE
    report = analyzer.evaluate(req.resume_text, req.jd_text)
    matched_skills = report["skills_analysis"]["matched_skills"]
    missing_skills = report["skills_analysis"]["missing_skills"]

    raw_bullets = [
        "Worked on electric billing system using Java and MySQL.",
        "Made an ATM simulation in Java and MySQL.",
        "Built personal portfolio website using React.js."
    ]
    tailored_summary = tailor_agent.generate_tailored_summary(profile, req.jd_text, matched_skills)
    optimized_bullets = tailor_agent.optimize_bullet_points(raw_bullets, missing_skills)

    output_file = "/tmp/JobHunter_Tailored_Resume.docx"
    create_ats_docx(profile, tailored_summary, optimized_bullets, output_file)

    return FileResponse(
        path=output_file,
        filename="Ajay_Avunoori_ATS_Tailored_Resume.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


# ----------------- Autonomous Job Discovery & Callback Predictor -----------------

@app.get("/api/jobs")
def get_jobs(query: str = "", location: str = ""):
    """Discovers matching jobs and calculates real-time ATS match and Callback Probability."""
    jobs = discovery_engine.search_jobs(query, location)
    resume = DEFAULT_PROFILE["raw_resume"]

    enriched_jobs = []
    for job in jobs:
        ats_eval = analyzer.evaluate(resume, job["description"])
        prob_eval = prob_engine.predict_callback(ats_eval, job)
        enriched_jobs.append({
            **job,
            "ats_score": ats_eval["overall_score"],
            "matched_skills": ats_eval["skills_analysis"]["matched_skills"],
            "missing_skills": ats_eval["skills_analysis"]["missing_skills"],
            "callback_probability": prob_eval["callback_probability"],
            "callback_tier": prob_eval["tier"],
            "callback_summary": prob_eval["summary"],
            "advantages": prob_eval["advantages"],
            "risks": prob_eval["risks"]
        })

    # Sort by callback probability descending
    enriched_jobs.sort(key=lambda x: x["callback_probability"], reverse=True)
    return {"jobs": enriched_jobs}


@app.post("/api/jobs/add")
def add_job(req: AddJobRequest):
    """Allows user or external web crawler to add a new Job Description."""
    new_job = discovery_engine.add_custom_job(req.dict())
    return {"success": True, "job": new_job}


# ----------------- Application Pipeline & Feedback Learning -----------------

@app.post("/api/jobs/apply")
def auto_apply_to_job(req: ApplyJobRequest):
    """
    Autonomous Apply Engine:
    1. Tailors resume to target JD with Google XYZ bullets.
    2. Generates personalized cold email / cover letter.
    3. Calculates callback probability.
    4. Logs application into tracking pipeline.
    """
    job = next((j for j in discovery_engine.jobs if j["id"] == req.job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    resume_text = req.custom_resume_text or DEFAULT_PROFILE["raw_resume"]
    report = analyzer.evaluate(resume_text, job["description"])
    matched_skills = report["skills_analysis"]["matched_skills"]
    missing_skills = report["skills_analysis"]["missing_skills"]

    raw_bullets = [
        "Worked on electric billing system using Java and MySQL.",
        "Made an ATM simulation in Java and MySQL.",
        "Built personal portfolio website using React.js."
    ]
    tailored_summary = tailor_agent.generate_tailored_summary(DEFAULT_PROFILE, job["description"], matched_skills)
    optimized_bullets = tailor_agent.optimize_bullet_points(raw_bullets, missing_skills)
    markdown_resume = tailor_agent.generate_full_resume_markdown(DEFAULT_PROFILE, tailored_summary, optimized_bullets, matched_skills)
    
    tailored_report = analyzer.evaluate(markdown_resume, job["description"])
    prob_report = prob_engine.predict_callback(tailored_report, job)

    # Generate tailored Cover Letter
    cover_letter = (
        f"Dear Hiring Team at {job['company']},\n\n"
        f"I am writing to express my enthusiasm for the {job['title']} role. "
        f"As an MCA graduate from Osmania University with hands-on experience building transactional Java and Spring Boot systems, "
        f"I have architected projects including an automated Electric Billing management system and an ACID-compliant ATM simulation platform.\n\n"
        f"My core expertise in {', '.join(matched_skills[:4])} directly aligns with your requirements for scalable, low-latency microservices. "
        f"I look forward to discussing how my problem-solving ability in Java and REST APIs can add immediate value to your engineering team.\n\n"
        f"Best regards,\nAjay Avunoori\n{DEFAULT_PROFILE['portfolio']} | {DEFAULT_PROFILE['github']}"
    )

    # Log application in active pipeline
    app_entry = adaptive_agent.log_new_application(
        job=job,
        ats_score=tailored_report["overall_score"],
        callback_prob=prob_report["callback_probability"],
        tailored_resume=markdown_resume
    )

    return {
        "success": True,
        "application": app_entry,
        "tailored_ats_score": tailored_report["overall_score"],
        "callback_probability": prob_report["callback_probability"],
        "cover_letter": cover_letter,
        "tailored_resume": markdown_resume
    }


@app.get("/api/applications")
def get_applications():
    """Returns active job tracking pipeline."""
    return {"applications": adaptive_agent.applications}


@app.post("/api/applications/feedback")
def submit_outcome_feedback(req: FeedbackRequest):
    """
    Feedback & Learning Loop:
    Updates company response and dynamically regenerates adaptive action plans.
    """
    result = adaptive_agent.record_outcome(req.app_id, req.status, req.user_notes)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/api/agent/insights")
def get_agent_insights():
    """Returns adaptive learning report, bottlenecks, and action sprints."""
    return adaptive_agent.analyze_pipeline_and_adapt()


# Serve static web interface
app.mount("/", StaticFiles(directory="/home/user/JobHunter-AI/static", html=True), name="static")
