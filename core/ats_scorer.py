"""
JobHunter-AI ATS Scorer & Resume Analyzer Engine.
Calculates keyword matching, action verb density, quantitative impact, and ATS formatting compliance.
"""

import re
from typing import Dict, List, Set, Any
from core.skill_taxonomy import TECH_SKILLS, STRONG_ACTION_VERBS, WEAK_WORDS


class ATSAnalyzer:
    def __init__(self):
        self.skills_dict = TECH_SKILLS
        self.strong_verbs = set(STRONG_ACTION_VERBS)
        self.weak_words = WEAK_WORDS

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extracts identified skills and their canonical categories from text."""
        text_lower = " " + text.lower() + " "
        found_skills = {}

        for category, variations in self.skills_dict.items():
            for var in variations:
                # Use word boundary or exact regex
                pattern = r'(?<![a-zA-Z0-9])' + re.escape(var) + r'(?![a-zA-Z0-9])'
                if re.search(pattern, text_lower):
                    display_name = var.title() if len(var) > 4 else var.upper()
                    # Normalizing display names
                    if var in ["spring boot", "springboot"]:
                        display_name = "Spring Boot"
                    elif var in ["react", "react.js", "reactjs"]:
                        display_name = "React.js"
                    elif var in ["rest", "restful", "rest api", "restful api", "rest apis"]:
                        display_name = "RESTful APIs"
                    elif var in ["javascript", "js"]:
                        display_name = "JavaScript"
                    elif var in ["mysql", "postgresql", "postgres"]:
                        display_name = "MySQL / PostgreSQL"
                    elif var in ["docker"]:
                        display_name = "Docker"
                    elif var in ["aws"]:
                        display_name = "AWS"
                    elif var in ["git", "github"]:
                        display_name = "Git / GitHub"
                    elif var in ["java"]:
                        display_name = "Java"

                    if category not in found_skills:
                        found_skills[category] = []
                    if display_name not in found_skills[category]:
                        found_skills[category].append(display_name)
                    break

        return found_skills

    def extract_all_skill_names(self, text: str) -> Set[str]:
        skills_by_cat = self.extract_skills(text)
        all_skills = set()
        for cat, items in skills_by_cat.items():
            all_skills.update(items)
        return all_skills

    def analyze_action_verbs(self, text: str) -> Dict[str, Any]:
        """Detects strong action verbs vs weak filler phrases."""
        text_lower = text.lower()
        found_strong = set()
        for verb in self.strong_verbs:
            pattern = r'\b' + re.escape(verb) + r'\b'
            if re.search(pattern, text_lower):
                found_strong.add(verb.capitalize())

        found_weak = []
        for weak in self.weak_words:
            if weak in text_lower:
                found_weak.append(weak)

        return {
            "strong_verbs_count": len(found_strong),
            "strong_verbs": sorted(list(found_strong)),
            "weak_phrases_count": len(found_weak),
            "weak_phrases": found_weak
        }

    def analyze_quantifiable_metrics(self, text: str) -> Dict[str, Any]:
        """Detects numbers, percentages, currency, and metrics indicating impact."""
        # Find % symbols, numbers with +, ms/seconds, x multiplier
        metrics = re.findall(r'(\b\d+%\b|\b\d+\+\b|\b\d+x\b|\b\d+\s*(?:ms|sec|seconds|users|requests|records|queries|reduction|improvement|growth)\b)', text, re.IGNORECASE)
        return {
            "metric_count": len(metrics),
            "examples": metrics[:8]
        }

    def check_ats_formatting(self, resume_text: str) -> Dict[str, Any]:
        """Checks for essential ATS sections and structure."""
        checks = {}
        text_lower = resume_text.lower()

        checks["has_contact_info"] = bool(re.search(r'[\w\.-]+@[\w\.-]+', resume_text)) or bool(re.search(r'\b\d{10}\b|\+\d{1,3}', resume_text))
        checks["has_skills_section"] = "skill" in text_lower
        checks["has_experience_section"] = "experience" in text_lower or "project" in text_lower
        checks["has_education_section"] = "education" in text_lower or "degree" in text_lower or "university" in text_lower
        checks["no_problematic_chars"] = not bool(re.search(r'[^\x00-\x7F\u2010-\u2022\u25A0-\u25CF]', resume_text))
        
        # Word count check (ideally 350 - 900 words for 1 page)
        words = resume_text.split()
        word_count = len(words)
        checks["word_count"] = word_count
        checks["ideal_length"] = 300 <= word_count <= 1100

        compliance_score = sum([
            25 if checks["has_contact_info"] else 0,
            25 if checks["has_skills_section"] else 0,
            25 if checks["has_experience_section"] else 0,
            25 if checks["has_education_section"] else 0,
        ])
        checks["compliance_score"] = compliance_score

        return checks

    def evaluate(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Calculates full ATS match report between resume and job description."""
        jd_skills = self.extract_all_skill_names(jd_text)
        resume_skills = self.extract_all_skill_names(resume_text)

        matched_skills = sorted(list(jd_skills.intersection(resume_skills)))
        missing_skills = sorted(list(jd_skills - resume_skills))
        extra_skills = sorted(list(resume_skills - jd_skills))

        # 1. Technical Keyword Match Score (0 - 45 pts)
        if len(jd_skills) > 0:
            keyword_ratio = len(matched_skills) / len(jd_skills)
            keyword_score = round(keyword_ratio * 45)
        else:
            keyword_score = 35  # default if generic JD

        # 2. Action Verb Score (0 - 25 pts)
        verb_analysis = self.analyze_action_verbs(resume_text)
        strong_count = verb_analysis["strong_verbs_count"]
        weak_count = verb_analysis["weak_phrases_count"]
        
        verb_score = min(25, max(0, (strong_count * 3) - (weak_count * 4)))

        # 3. Quantifiable Impact Score (0 - 15 pts)
        metric_analysis = self.analyze_quantifiable_metrics(resume_text)
        metric_score = min(15, metric_analysis["metric_count"] * 3)

        # 4. ATS Formatting & Sections Score (0 - 15 pts)
        format_checks = self.check_ats_formatting(resume_text)
        format_score = round((format_checks["compliance_score"] / 100) * 15)

        total_ats_score = min(100, keyword_score + verb_score + metric_score + format_score)

        # Rating tier
        if total_ats_score >= 85:
            rating = "Excellent (Interview Ready)"
            color = "emerald"
        elif total_ats_score >= 70:
            rating = "Good (Minor Keyword Optimizations Needed)"
            color = "blue"
        elif total_ats_score >= 50:
            rating = "Moderate (High Risk of ATS Filter Rejection)"
            color = "amber"
        else:
            rating = "Low (Immediate Rewrite Needed)"
            color = "rose"

        # Actionable recommendations
        recommendations = []
        if missing_skills:
            top_missing = ", ".join(missing_skills[:5])
            recommendations.append(f"Add critical missing skills into projects or skills section: {top_missing}")
        if weak_count > 0:
            recommendations.append(f"Replace {weak_count} weak phrases like '{verb_analysis['weak_phrases'][0]}' with dynamic action verbs (e.g. 'Architected', 'Engineered', 'Optimized').")
        if metric_analysis["metric_count"] < 3:
            recommendations.append("Quantify your achievements using the Google XYZ formula (e.g., 'Reduced query response time by 35%', 'Handled 500+ daily transactions').")
        if not format_checks["has_contact_info"]:
            recommendations.append("Ensure your Email, Phone Number, and LinkedIn/GitHub links are clearly displayed at the top.")
        if len(recommendations) == 0:
            recommendations.append("Your resume has stellar ATS alignment! Ready to submit.")

        return {
            "overall_score": total_ats_score,
            "rating": rating,
            "color": color,
            "score_breakdown": {
                "keywords": {"score": keyword_score, "max": 45},
                "verbs": {"score": verb_score, "max": 25},
                "metrics": {"score": metric_score, "max": 15},
                "formatting": {"score": format_score, "max": 15}
            },
            "skills_analysis": {
                "matched_count": len(matched_skills),
                "matched_skills": matched_skills,
                "missing_count": len(missing_skills),
                "missing_skills": missing_skills,
                "additional_skills": extra_skills[:8]
            },
            "verbs_analysis": verb_analysis,
            "metrics_analysis": metric_analysis,
            "formatting_checks": format_checks,
            "recommendations": recommendations
        }
