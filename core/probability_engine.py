"""
JobHunter-AI Company Callback Probability Engine.
Predicts the likelihood of receiving an interview response from a company based on candidate match,
experience tier, ATS screening hurdles, and market competition factors.
"""

from typing import Dict, Any, List


class CallbackProbabilityEngine:
    def __init__(self):
        pass

    def predict_callback(self, ats_report: Dict[str, Any], job_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates predicted company response rate (0-100%).
        Considers ATS score, must-have skills vs nice-to-have, and competitive candidate density.
        """
        ats_score = ats_report.get("overall_score", 50)
        skills_analysis = ats_report.get("skills_analysis", {})
        matched_skills = skills_analysis.get("matched_skills", [])
        missing_skills = skills_analysis.get("missing_skills", [])
        verbs_count = ats_report.get("verbs_analysis", {}).get("strong_verbs_count", 0)
        metrics_count = ats_report.get("metrics_analysis", {}).get("metric_count", 0)

        # Baseline probability from ATS Score (0 - 50 pts)
        # Even a 100% ATS score usually faces a 50-60% recruiter response cap due to applicant volume
        score_component = (ats_score / 100) * 55

        # Dealbreakers evaluation (Java + Spring Boot are primary for our candidate)
        dealbreakers_bonus = 0
        has_java = any("java" in s.lower() for s in matched_skills)
        has_spring = any("spring" in s.lower() for s in matched_skills)
        has_db = any("sql" in s.lower() or "mysql" in s.lower() for s in matched_skills)

        if has_java:
            dealbreakers_bonus += 10
        if has_spring:
            dealbreakers_bonus += 10
        if has_db:
            dealbreakers_bonus += 10

        # Action metrics bonus (Proof of work)
        metrics_bonus = min(10, metrics_count * 2)

        # Penalty for critical missing skills (e.g. Cloud/Kafka if required)
        missing_penalty = min(25, len(missing_skills) * 5)

        # Calculate raw probability
        raw_prob = score_component + dealbreakers_bonus + metrics_bonus - missing_penalty

        # Clamp between 15% and 95% (recruiting is never 0% or 100%)
        final_probability = max(15, min(94, round(raw_prob)))

        # Categorize
        if final_probability >= 75:
            tier = "High Probability"
            badge_color = "emerald"
            summary = "High chance of recruiter outreach. Core requirements and project metrics strongly aligned."
        elif final_probability >= 55:
            tier = "Moderate Probability"
            badge_color = "amber"
            summary = "Competitive candidate. High likelihood if tailored resume highlights relevant microservices experience."
        else:
            tier = "Challenging / Low Response"
            badge_color = "rose"
            summary = "Lower expected response rate due to critical missing technologies (e.g., Cloud, Queues)."

        # Key drivers
        advantages = []
        if has_java and has_spring:
            advantages.append("Core stack match: Direct alignment on Java & Spring Boot backend.")
        if has_db:
            advantages.append("Database foundation: Relational schema design and ACID transaction experience.")
        if metrics_count >= 2:
            advantages.append("Quantifiable metrics: Demonstrates concrete business impact on previous projects.")

        risks = []
        if missing_skills:
            risks.append(f"Missing keywords: {', '.join(missing_skills[:3])} could trigger secondary recruiter filtering.")
        if len(matched_skills) < 4:
            risks.append("Low keyword coverage: Candidate resume lacks secondary stack keywords.")

        return {
            "callback_probability": final_probability,
            "tier": tier,
            "badge_color": badge_color,
            "summary": summary,
            "advantages": advantages,
            "risks": risks,
            "factors": {
                "ats_influence": round(score_component),
                "stack_alignment": dealbreakers_bonus,
                "quantified_proof": metrics_bonus,
                "gap_penalty": -missing_penalty
            }
        }
