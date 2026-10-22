"""
JobHunter-AI Skill Taxonomy & Action Verb Catalog.
Provides structured entity recognition for technical skills, soft skills, and action verbs.
"""

TECH_SKILLS = {
    # Languages
    "java": ["java", "core java", "advanced java", "j2ee", "jdk"],
    "python": ["python", "python3", "py"],
    "javascript": ["javascript", "js", "es6", "ecmascript"],
    "typescript": ["typescript", "ts"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "oracle", "pl/sql", "sqlite", "mssql"],
    "html_css": ["html", "html5", "css", "css3", "tailwind", "bootstrap", "sass", "scss"],
    "c_cpp": ["c++", "c language", "cpp"],
    "c_sharp": ["c#", ".net", "dotnet"],
    "go": ["golang", "go"],

    # Backend Frameworks
    "spring_boot": ["spring boot", "springboot", "spring framework", "spring mvc", "spring data", "spring security"],
    "hibernate": ["hibernate", "jpa", "spring data jpa"],
    "node_js": ["node.js", "nodejs", "express", "express.js", "nest.js", "nestjs"],
    "django": ["django", "fastapi", "flask"],
    "microservices": ["microservices", "microservice", "distributed systems", "service-oriented architecture", "soa"],
    "rest_api": ["rest", "restful", "rest api", "rest apis", "restful api", "web services", "json", "api development"],
    "graphql": ["graphql", "apollo"],

    # Frontend Frameworks
    "react": ["react", "react.js", "reactjs", "next.js", "nextjs", "redux", "redux toolkit"],
    "angular": ["angular", "angularjs"],
    "vue": ["vue", "vue.js", "vuejs"],

    # Databases & Caching
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "nosql", "documentdb"],
    "redis": ["redis", "in-memory cache", "caching"],
    "kafka": ["kafka", "apache kafka", "message broker", "rabbitmq"],

    # Cloud & DevOps
    "docker": ["docker", "containerization", "containers"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda", "rds"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],
    "git": ["git", "github", "gitlab", "bitbucket", "version control"],
    "ci_cd": ["ci/cd", "ci-cd", "jenkins", "github actions", "pipelines"],
    "linux": ["linux", "unix", "bash", "shell scripting"],

    # Testing & Tools
    "testing": ["junit", "mockito", "jest", "pytest", "unit testing", "integration testing", "tdd"],
    "build_tools": ["maven", "gradle", "npm", "vite", "webpack"],
    "postman": ["postman", "swagger", "openapi"],

    # Architecture & Practices
    "oop": ["oop", "object-oriented programming", "oops", "design patterns", "solid principles"],
    "dsa": ["data structures", "algorithms", "dsa", "problem solving", "time complexity", "space complexity"],
    "agile": ["agile", "scrum", "jira", "sprint"],
    "system_design": ["system design", "scalability", "high availability", "load balancing"]
}

STRONG_ACTION_VERBS = [
    "accelerated", "achieved", "architected", "automated", "built", "centralized", 
    "championed", "collaborated", "configured", "consolidated", "constructed", "created",
    "debugged", "decreased", "delivered", "deployed", "designed", "developed", 
    "devised", "eliminated", "engineered", "enhanced", "established", "executed", 
    "expanded", "expedited", "fabricated", "formulated", "generated", "implemented", 
    "improved", "increased", "initiated", "innovated", "installed", "instituted", 
    "integrated", "launched", "maximized", "migrated", "minimized", "modernized", 
    "optimized", "orchestrated", "overhauled", "pioneered", "reduced", "refactored", 
    "resolved", "restructured", "revamped", "scaled", "simplified", "spearheaded", 
    "standardized", "streamlined", "strengthened", "transformed", "upgraded"
]

WEAK_WORDS = [
    "responsible for", "helped", "assisted", "worked on", "handled", "participated in",
    "involved in", "did", "tasked with", "was part of", "contributed to", "tried to",
    "familiar with", "learning"
]
