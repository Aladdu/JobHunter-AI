"""
JobHunter-AI Adaptive Learning & Feedback Loop Engine.
Analyzes application results (callbacks, rejections, feedback notes) and dynamically
generates new learning plans, resume upgrades, and tactical targeting pivots.
"""

from typing import List, Dict, Any
import datetime


class AdaptiveLearningAgent:
    def __init__(self):
        # Initial application logs with realistic seed data
        self.applications = [
            {
                "id": "app_001",
                "job_id": "job_001",
                "company": "Swiggy / FinTech",
                "title": "Java Full Stack Developer",
                "applied_date": "2026-10-18",
                "ats_score": 88,
                "predicted_callback": 84,
                "status": "Interview Scheduled",  # Applied, Interview Scheduled, Rejected, Ghosted, Offer
                "user_notes": "Recruiter liked the Electric Bill & ATM project ACID transactions. Technical round next Tuesday on Spring Boot & MySQL indexing.",
                "missing_skills_at_apply": ["Docker"]
            },
            {
                "id": "app_002",
                "job_id": "job_004",
                "company": "Razorpay",
                "title": "Junior Full Stack Developer",
                "applied_date": "2026-10-15",
                "ats_score": 68,
                "predicted_callback": 48,
                "status": "Rejected",
                "user_notes": "Automated email: Looking for candidates with production Kafka or AWS experience.",
                "missing_skills_at_apply": ["Kafka", "AWS"]
            },
            {
                "id": "app_003",
                "job_id": "job_003",
                "company": "Tech Mahindra",
                "title": "Software Engineer - Java & Spring",
                "applied_date": "2026-10-19",
                "ats_score": 85,
                "predicted_callback": 82,
                "status": "Applied",
                "user_notes": "Under review by hiring team.",
                "missing_skills_at_apply": []
            }
        ]

    def record_outcome(self, app_id: str, new_status: str, user_notes: str) -> Dict[str, Any]:
        """Updates the status of an application and triggers strategic adaptation."""
        target_app = None
        for app in self.applications:
            if app["id"] == app_id:
                app["status"] = new_status
                app["user_notes"] = user_notes
                target_app = app
                break

        if not target_app:
            return {"error": "Application not found"}

        # Re-run cognitive analysis
        insights = self.analyze_pipeline_and_adapt()
        return {
            "success": True,
            "updated_app": target_app,
            "adaptive_insights": insights
        }

    def log_new_application(self, job: Dict[str, Any], ats_score: int, callback_prob: int, tailored_resume: str) -> Dict[str, Any]:
        """Registers a new dispatched job application."""
        app_id = f"app_{len(self.applications) + 1:03d}"
        new_app = {
            "id": app_id,
            "job_id": job.get("id", "custom"),
            "company": job.get("company", "Tech Company"),
            "title": job.get("title", "Java Developer"),
            "applied_date": datetime.date.today().isoformat(),
            "ats_score": ats_score,
            "predicted_callback": callback_prob,
            "status": "Applied",
            "user_notes": "Application dispatched with tailored Google XYZ resume and cover letter.",
            "missing_skills_at_apply": job.get("missing_skills", [])
        }
        self.applications.insert(0, new_app)
        return new_app

    def analyze_pipeline_and_adapt(self) -> Dict[str, Any]:
        """
        Synthesizes feedback from rejections and interviews to adapt plans and generate sprints.
        """
        total = len(self.applications)
        if total == 0:
            return {}

        interviews = [a for a in self.applications if a["status"] in ["Interview Scheduled", "Offer"]]
        rejections = [a for a in self.applications if a["status"] == "Rejected"]
        applied = [a for a in self.applications if a["status"] == "Applied"]

        interview_rate = round((len(interviews) / total) * 100) if total > 0 else 0
        rejection_rate = round((len(rejections) / total) * 100) if total > 0 else 0

        # Pattern Recognition: Why are rejections happening?
        rejection_reasons = []
        missing_skills_freq = {}
        for r in rejections:
            notes = r.get("user_notes", "").lower()
            for s in r.get("missing_skills_at_apply", []):
                missing_skills_freq[s] = missing_skills_freq.get(s, 0) + 1
            if "kafka" in notes:
                missing_skills_freq["Apache Kafka"] = missing_skills_freq.get("Apache Kafka", 0) + 2
            if "docker" in notes:
                missing_skills_freq["Docker"] = missing_skills_freq.get("Docker", 0) + 2
            if "aws" in notes:
                missing_skills_freq["AWS"] = missing_skills_freq.get("AWS", 0) + 2

        sorted_bottlenecks = sorted(missing_skills_freq.items(), key=lambda x: x[1], reverse=True)
        primary_bottlenecks = [item[0] for item in sorted_bottlenecks[:3]]

        # Strengths: What creates interview invites?
        interview_drivers = [
            "Strong Java 17 + Spring Boot foundation",
            "Real-world ACID transaction projects (ATM & Electric Billing)",
            "High ATS match score (>80%) on entry/mid-tier applications"
        ]

        # Dynamic Action Sprints (New Plans for the User)
        action_plans = []
        if primary_bottlenecks:
            top_gap = primary_bottlenecks[0]
            action_plans.append({
                "title": f"🚀 3-Day Technical Sprint: Integrate {top_gap}",
                "urgency": "High Impact",
                "why": f"Identified as the #1 rejection filter in recent applications ({top_gap}).",
                "action_steps": [
                    f"Day 1: Watch a 45-minute crash course on {top_gap} architecture & concepts.",
                    f"Day 2: Add a {top_gap} integration to your existing Electric Bill System or ATM project.",
                    f"Day 3: Commit the new module to GitHub and add the XYZ bullet to your master profile."
                ]
            })

        action_plans.append({
            "title": "🎯 Tactical Application Filter Update",
            "urgency": "Immediate",
            "why": "Maximize immediate callback velocity while expanding your skill breadth.",
            "action_steps": [
                "Focus next 10 applications on companies requiring: Java, Spring Boot, MySQL, REST APIs, React.",
                "Target roles offering 0-3 years experience in FinTech & Product-driven startups.",
                "Avoid applying to roles requiring 2+ years of senior Kubernetes/AWS until Docker sprint is complete."
            ]
        })

        if interviews:
            target_company = interviews[0]["company"]
            action_plans.append({
                "title": f"💼 Active Interview Prep: {target_company}",
                "urgency": "Critical",
                "why": "You have an active interview pipeline! Preparation directly influences offer rates.",
                "action_steps": [
                    "Review Spring Boot `@Transactional` propagation levels and HikariCP connection pooling.",
                    "Practice 2 LeetCode Medium Java problems (Two Pointers & HashMaps).",
                    "Rehearse STAR responses for your Electric Billing system schema design."
                ]
            })

        return {
            "metrics": {
                "total_applications": total,
                "interview_count": len(interviews),
                "rejection_count": len(rejections),
                "pending_count": len(applied),
                "interview_rate": f"{interview_rate}%",
                "rejection_rate": f"{rejection_rate}%"
            },
            "identified_bottlenecks": primary_bottlenecks or ["Docker Fundamentals"],
            "strengths": interview_drivers,
            "action_plans": action_plans,
            "agent_verdict": (
                f"Your core Java & Spring Boot profile is competitive (yielding a {interview_rate}% interview rate). "
                f"Closing the gap on {primary_bottlenecks[0] if primary_bottlenecks else 'Docker'} will unlock the remaining tier of high-paying product roles."
            )
        }
