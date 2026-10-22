"""
JobHunter-AI Bullet Rewriter & Resume Tailoring Engine.
Transforms standard bullet points into Google XYZ format and generates ATS-tailored resume content.
"""

from typing import Dict, List, Any
import re
from core.ats_scorer import ATSAnalyzer


class ResumeTailorAgent:
    def __init__(self):
        self.analyzer = ATSAnalyzer()

    def generate_tailored_summary(self, profile: Dict[str, Any], jd_text: str, matched_skills: List[str]) -> str:
        """Generates an executive professional summary tailored to the target role."""
        name = profile.get("name", "Ajay Avunoori")
        title = profile.get("target_title", "Java Full Stack Developer")
        education = profile.get("education", "MCA Graduate (Osmania University)")

        # Extract role title from JD if possible
        jd_first_line = jd_text.strip().split("\n")[0]
        role_match = re.search(r'(Java|Full Stack|Backend|Frontend|Software|Spring Boot)\s+(?:Developer|Engineer|Architect)', jd_text, re.IGNORECASE)
        role = role_match.group(0).title() if role_match else title

        top_skills = ", ".join(matched_skills[:5]) if matched_skills else "Java, Spring Boot, MySQL, REST APIs, and React.js"

        summary = (
            f"Results-oriented {role} with a strong foundation in {top_skills}. "
            f"{education} with proven expertise designing scalable backend microservices, optimizing database performance, "
            f"and creating responsive user interfaces. Passionate about writing clean, maintainable code with SOLID principles, "
            f"robust unit testing, and automated CI/CD workflows to solve high-impact business problems."
        )
        return summary

    def optimize_bullet_points(self, raw_bullets: List[str], missing_skills: List[str]) -> List[Dict[str, str]]:
        """
        Rewrites project/experience bullet points into Google XYZ formula:
        Accomplished [X] as measured by [Y], by doing [Z].
        """
        optimized = []
        
        # High-impact templates mapped to common developer experiences
        transformations = [
            {
                "original_trigger": ["electric", "bill", "billing"],
                "xyz": "Architected an automated Electric Billing & Payment Management System using Java and MySQL, reducing manual billing overhead by 40% through normalized schema design and parameterized queries.",
                "skills_used": ["Java", "MySQL", "JDBC", "Data Validation", "OOP"]
            },
            {
                "original_trigger": ["atm", "simulation", "bank"],
                "xyz": "Engineered a secure multi-user ATM Simulation application in Java with real-time transaction processing, achieving sub-100ms response times and 100% ACID compliance using MySQL transactions.",
                "skills_used": ["Java", "MySQL", "ACID Transactions", "Concurrency", "Security"]
            },
            {
                "original_trigger": ["dsa", "leetcode", "problem"],
                "xyz": "Systematically authored 100+ optimized algorithmic solutions in Java covering HashMaps, Binary Trees, and Dynamic Programming, maintaining average runtime complexity below O(n log n).",
                "skills_used": ["Java", "Data Structures & Algorithms", "Time/Space Complexity", "Clean Code"]
            },
            {
                "original_trigger": ["portfolio", "react", "website"],
                "xyz": "Developed a high-performance responsive web portfolio using React.js and modern CSS, achieving a 98+ Google Lighthouse performance score and seamless mobile compatibility.",
                "skills_used": ["React.js", "JavaScript ES6+", "HTML5/CSS3", "Responsive Design"]
            },
            {
                "original_trigger": ["spring", "api", "rest"],
                "xyz": "Designed and deployed RESTful microservices using Spring Boot and Spring Data JPA, streamlining client-server communication with global exception handling and Swagger/OpenAPI documentation.",
                "skills_used": ["Spring Boot", "REST APIs", "Spring Data JPA", "Hibernate"]
            }
        ]

        for bullet in raw_bullets:
            b_lower = bullet.lower()
            matched = False
            for t in transformations:
                if any(trigger in b_lower for trigger in t["original_trigger"]):
                    optimized.append({
                        "original": bullet,
                        "optimized": t["xyz"],
                        "skills_highlighted": t["skills_used"]
                    })
                    matched = True
                    break

            if not matched:
                # General XYZ upgrade
                cleaned = bullet.strip().lstrip("-*• ")
                # Capitalize and add strong action verb if missing
                verb = "Engineered" if "develop" in b_lower else "Optimized" if "improve" in b_lower else "Implemented"
                metric = "increasing throughput by 25%" if "data" in b_lower else "improving system reliability and user turnaround by 30%"
                upgraded = f"{verb} {cleaned}, {metric} through modular code structure and automated testing."
                optimized.append({
                    "original": bullet,
                    "optimized": upgraded,
                    "skills_highlighted": ["Clean Architecture", "Unit Testing"]
                })

        return optimized

    def generate_interview_prep(self, jd_text: str, matched_skills: List[str], missing_skills: List[str]) -> List[Dict[str, str]]:
        """Generates tailored technical & behavioral interview questions based on this exact JD."""
        questions = []

        # Question on Core Java / Concurrency
        if "Java" in matched_skills or "java" in jd_text.lower():
            questions.append({
                "category": "Technical (Java Deep Dive)",
                "question": "How does Java's ConcurrentHashMap achieve thread safety without locking the entire map like Hashtable?",
                "key_points": "Explain bucket-level / segment locking (Java 7) vs CAS operations and synchronized blocks on node heads (Java 8+). Mention read operations do not block."
            })

        # Question on Spring Boot
        if "Spring Boot" in matched_skills or "spring" in jd_text.lower():
            questions.append({
                "category": "Technical (Spring Boot Architecture)",
                "question": "Walk me through how Spring handles transaction management with `@Transactional`, and what causes transactions to fail or rollback?",
                "key_points": "Explain Spring AOP proxies, self-invocation caveats, unchecked (RuntimeException) vs checked exceptions, and propagation levels (REQUIRED, REQUIRES_NEW)."
            })

        # Question on Database Optimization
        if "MySQL / PostgreSQL" in matched_skills or "sql" in jd_text.lower():
            questions.append({
                "category": "Technical (Database & Performance)",
                "question": "In your Electric Bill or ATM projects, how would you troubleshoot and optimize a slow-running SQL query?",
                "key_points": "Explain EXPLAIN query plans, B-Tree index lookups vs full table scans, composite indexes, avoiding SELECT *, and connection pooling (HikariCP)."
            })

        # Question on Missing Skills (Hiring managers always probe gaps!)
        if missing_skills:
            gap_skill = missing_skills[0]
            questions.append({
                "category": "Bridge Question (Addressing Skill Gaps)",
                "question": f"Our team works heavily with {gap_skill}. How would you get up to speed quickly, and have you used adjacent tools?",
                "key_points": f"Highlight fast learning ability, relate it to existing knowledge, and mention a quick proof-of-concept project you can build in your first week."
            })

        # Behavioral Question
        questions.append({
            "category": "Behavioral (STAR Method)",
            "question": "Describe a challenging bug you encountered in one of your projects and how you diagnosed and resolved it.",
            "key_points": "Situation: What was broken. Task: What had to happen. Action: Root cause analysis (logs, debugger, query profile). Result: Metric or stability achieved."
        })

        return questions

    def generate_full_resume_markdown(self, profile: Dict[str, Any], tailored_summary: str, optimized_bullets: List[Dict[str, str]], matched_skills: List[str]) -> str:
        """Assembles a clean, ATS-compliant Markdown resume."""
        name = profile.get("name", "Ajay Avunoori")
        email = profile.get("email", "ajay.avunoori.dev@gmail.com")
        phone = profile.get("phone", "+91 98765 43210")
        location = profile.get("location", "Hyderabad, India")
        github = profile.get("github", "https://github.com/Aladdu")
        linkedin = profile.get("linkedin", "https://linkedin.com/in/ajay-avunoori")
        portfolio = profile.get("portfolio", "https://avunooriajayportfolio1.netlify.app/")

        # Categorize skills for ATS
        skills_section = (
            f"- **Programming Languages:** Java (Core & Advanced), JavaScript (ES6+), SQL, Python (Basics)\n"
            f"- **Backend & Frameworks:** Spring Boot, Spring MVC, Spring Data JPA, Hibernate, RESTful APIs, Microservices\n"
            f"- **Frontend Technologies:** React.js, HTML5, CSS3, Tailwind CSS, Responsive Design\n"
            f"- **Databases & Tools:** MySQL, PostgreSQL, Git, GitHub, Maven, Postman, Docker (Fundamentals)\n"
            f"- **Concepts:** Object-Oriented Programming (OOP), Data Structures & Algorithms, Design Patterns, Agile/Scrum"
        )

        bullets_md = "\n".join([f"- {b['optimized']}" for b in optimized_bullets])

        md = f"""# {name}
**{location}** | **Email:** {email} | **Phone:** {phone}  
**GitHub:** [{github}]({github}) | **LinkedIn:** [{linkedin}]({linkedin}) | **Portfolio:** [{portfolio}]({portfolio})

---

## PROFESSIONAL SUMMARY
{tailored_summary}

---

## TECHNICAL SKILLS
{skills_section}

---

## FEATURED PROJECTS

### **Automated Electric Billing & Payment Management System** | *Java, MySQL, JDBC*
- Architected an automated Electric Billing & Payment System using Java and MySQL, reducing manual billing overhead by 40% through normalized schema design and parameterized queries.
- Integrated automated tariff calculation logic handling multi-tier consumption slabs with 100% calculation accuracy.
- Enhanced database access efficiency using prepared statements and connection pooling to prevent SQL injection vulnerabilities.

### **Secure Multi-User ATM Simulation System** | *Java, MySQL, OOP*
- Engineered a robust multi-user ATM Simulation platform featuring PIN authentication, balance inquiry, deposit, and fund transfers.
- Enforced strict ACID transactions using MySQL commit/rollback blocks to ensure zero data discrepancies during concurrent withdrawal scenarios.
- Designed clean, decoupled architecture adhering to Object-Oriented Principles (Encapsulation, Polymorphism) and DAO design patterns.

### **Full-Stack Developer Portfolio & Web Applications** | *React.js, JavaScript, Tailwind CSS*
- Developed modern single-page applications (SPA) in React.js featuring dynamic state management, smooth routing, and interactive UI components.
- Optimized asset loading and bundle sizes, achieving 95+ performance ratings on Google Lighthouse audits.

---

## EDUCATION
**Master of Computer Applications (MCA)**  
*Osmania University, Hyderabad* | Graduated: 2023  
- Relevant Coursework: Data Structures & Algorithms, Database Management Systems, Object-Oriented Programming with Java, Web Technologies.

---

## CERTIFICATIONS & ACHIEVEMENTS
- **DSA Problem Solving:** Authored 100+ optimized algorithmic solutions in Java on LeetCode/CodeChef.
- **Java Full Stack Development Specialization** – Spring Boot, REST APIs, Microservices & React.js.
"""
        return md.strip()
