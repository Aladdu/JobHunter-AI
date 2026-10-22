"""
JobHunter-AI Autonomous Job Discovery & Feed Engine.
Provides job searching, scraping simulation, and live feed of software engineering roles.
"""

from typing import List, Dict, Any
import datetime

MOCK_DISCOVERED_JOBS = [
    {
        "id": "job_001",
        "company": "Swiggy / FinTech Division",
        "title": "Java Full Stack Developer",
        "location": "Hyderabad / Remote",
        "experience": "0-3 Years",
        "salary_range": "₹8 LPA - ₹15 LPA",
        "tags": ["Java", "Spring Boot", "React.js", "MySQL", "REST APIs"],
        "posted_date": "1 day ago",
        "description": """We are seeking a Java Full Stack Developer to build real-time merchant settlement and payout services.
Responsibilities:
- Build low-latency backend microservices using Java 17 and Spring Boot.
- Create merchant-facing management consoles with React.js and modern state management.
- Write ACID-compliant transactional queries using MySQL and optimize indexes for high transaction volume.
- Collaborate with QA engineers using JUnit testing for 90%+ code coverage.
Requirements:
- Strong core Java, OOP, Spring Boot, and REST API development experience.
- Relational database experience with MySQL or PostgreSQL.
- Experience building responsive web apps with React.js."""
    },
    {
        "id": "job_002",
        "company": "Paytm Payments Bank",
        "title": "Associate Backend Engineer (Java)",
        "location": "Hyderabad / Bengaluru",
        "experience": "0-2 Years",
        "salary_range": "₹7 LPA - ₹12 LPA",
        "tags": ["Java", "Spring Boot", "Microservices", "MySQL", "Docker"],
        "posted_date": "2 days ago",
        "description": """Looking for an energetic Backend Java Engineer to join our UPI & Wallets infrastructure team.
Responsibilities:
- Implement scalable microservices using Spring Boot and Spring Data JPA.
- Handle database schema migrations, query performance tuning, and connection pooling in MySQL.
- Deploy services using Docker containers and monitor application logs.
Requirements:
- Solid background in Data Structures, Algorithms (DSA), and Object-Oriented Design.
- Practical experience in Java, Spring Boot, MySQL.
- Basic understanding of Docker and Linux commands is a plus."""
    },
    {
        "id": "job_003",
        "company": "Tech Mahindra / Enterprise Cloud",
        "title": "Software Engineer - Java & Spring",
        "location": "Hyderabad",
        "experience": "1-3 Years",
        "salary_range": "₹6 LPA - ₹10 LPA",
        "tags": ["Java", "Spring Boot", "Hibernate", "PostgreSQL", "Maven"],
        "posted_date": "3 days ago",
        "description": """Join Tech Mahindra's Digital Transformation practice building enterprise supply chain web applications.
Responsibilities:
- Develop robust backend endpoints using Spring Boot, Hibernate, and PostgreSQL.
- Integrate third-party web services using secure REST APIs and JSON serialization.
- Participate in daily Agile/Scrum standups and code reviews using Git/GitHub.
Requirements:
- Bachelor's or Master's degree in Computer Applications (MCA / B.Tech).
- Proficiency with Java, OOP, Spring Boot, and SQL databases."""
    },
    {
        "id": "job_004",
        "company": "Razorpay",
        "title": "Junior Full Stack Developer",
        "location": "Bengaluru / Remote",
        "experience": "1-3 Years",
        "salary_range": "₹12 LPA - ₹18 LPA",
        "tags": ["Java", "React.js", "Spring Boot", "Kafka", "AWS"],
        "posted_date": "Just now",
        "description": """Razorpay is hiring a Junior Full Stack Developer to help build the next generation of automated payment reconciliation.
Responsibilities:
- Build seamless developer-facing APIs with Java and Spring Boot.
- Create interactive dashboard UI in React.js and TypeScript.
- Work with distributed queues using Apache Kafka and AWS cloud infrastructure.
Requirements:
- Strong problem-solving and algorithmic skills.
- Experience with Java, Spring Boot, and React.js.
- Knowledge of Apache Kafka or AWS is highly desirable."""
    }
]


class JobDiscoveryEngine:
    def __init__(self):
        self.jobs = list(MOCK_DISCOVERED_JOBS)

    def search_jobs(self, query: str = "", location: str = "") -> List[Dict[str, Any]]:
        """Filters jobs based on query and location."""
        results = []
        q_lower = query.lower()
        loc_lower = location.lower()

        for job in self.jobs:
            text = f"{job['title']} {job['company']} {' '.join(job['tags'])} {job['description']}".lower()
            loc_match = loc_lower in job['location'].lower() if location else True
            query_match = q_lower in text if query else True

            if query_match and loc_match:
                results.append(job)

        return results

    def add_custom_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Allows users or crawlers to add new Job Descriptions."""
        job_id = f"job_{len(self.jobs) + 1:03d}"
        new_job = {
            "id": job_id,
            "company": job_data.get("company", "Target Company"),
            "title": job_data.get("title", "Java Developer"),
            "location": job_data.get("location", "Hyderabad / Remote"),
            "experience": job_data.get("experience", "0-3 Years"),
            "salary_range": job_data.get("salary_range", "Competitive"),
            "tags": job_data.get("tags", ["Java", "Spring Boot"]),
            "posted_date": "Today",
            "description": job_data.get("description", "")
        }
        self.jobs.insert(0, new_job)
        return new_job
