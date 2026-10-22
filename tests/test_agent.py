"""
Unit & Integration Tests for JobHunter-AI v2.0 Autonomous Agent.
Verifies skill extraction, ATS scoring logic, Google XYZ rewriter,
Job Discovery Radar, Callback Probability Prediction, and Adaptive Learning Loop.
"""

import pytest
from core.ats_scorer import ATSAnalyzer
from core.rewriter import ResumeTailorAgent
from core.job_search import JobDiscoveryEngine
from core.probability_engine import CallbackProbabilityEngine
from core.adaptive_agent import AdaptiveLearningAgent


@pytest.fixture
def analyzer():
    return ATSAnalyzer()


@pytest.fixture
def tailor():
    return ResumeTailorAgent()


@pytest.fixture
def discovery():
    return JobDiscoveryEngine()


@pytest.fixture
def prob_engine():
    return CallbackProbabilityEngine()


@pytest.fixture
def adaptive():
    return AdaptiveLearningAgent()


def test_skill_extraction(analyzer):
    sample_text = "Proficient in Java, Spring Boot, MySQL, and React.js with RESTful APIs."
    skills = analyzer.extract_all_skill_names(sample_text)
    
    assert "Java" in skills
    assert "Spring Boot" in skills
    assert "MySQL / PostgreSQL" in skills
    assert "React.js" in skills
    assert "RESTful APIs" in skills


def test_action_verbs_analysis(analyzer):
    text_with_verbs = "Architected a system, optimized database queries, and was responsible for testing."
    result = analyzer.analyze_action_verbs(text_with_verbs)
    
    assert result["strong_verbs_count"] >= 2
    assert "Architected" in result["strong_verbs"]
    assert "Optimized" in result["strong_verbs"]
    assert "responsible for" in result["weak_phrases"]


def test_ats_evaluation_scoring(analyzer):
    resume = """
    Ajay Avunoori | ajay@example.com | +91 9876543210
    Technical Skills: Java, Spring Boot, MySQL, React.js, Git
    Experience:
    Architected an automated Electric Billing System in Java and MySQL reducing processing time by 40%.
    Engineered an ATM simulation achieving sub-100ms response times.
    Education: Master of Computer Applications
    """
    jd = "Seeking Java developer with Spring Boot, MySQL, and React experience."
    
    report = analyzer.evaluate(resume, jd)
    assert report["overall_score"] >= 70
    assert len(report["skills_analysis"]["matched_skills"]) >= 3


def test_callback_probability_prediction(analyzer, prob_engine):
    resume = "Java Spring Boot MySQL REST APIs developer. Architected an automated billing system reducing processing time by 40%."
    jd = "Java Developer with Spring Boot and MySQL."
    report = analyzer.evaluate(resume, jd)
    prob = prob_engine.predict_callback(report, {})
    
    assert "callback_probability" in prob
    assert prob["callback_probability"] >= 55
    assert "High" in prob["tier"] or "Moderate" in prob["tier"]


def test_job_discovery_search(discovery):
    results = discovery.search_jobs("Java", "Hyderabad")
    assert len(results) >= 1
    assert any("Java" in j["title"] for j in results)


def test_adaptive_feedback_learning_loop(adaptive):
    initial_insights = adaptive.analyze_pipeline_and_adapt()
    assert len(initial_insights["action_plans"]) >= 2
    
    # Simulate logging a new rejection with specific feedback
    result = adaptive.record_outcome(
        app_id="app_003",
        new_status="Rejected",
        user_notes="Company rejected because they required Apache Kafka and Docker."
    )
    assert result["success"] is True
    
    updated_insights = result["adaptive_insights"]
    assert "Apache Kafka" in updated_insights["identified_bottlenecks"] or "Docker" in updated_insights["identified_bottlenecks"]
    # Verify that a 3-Day Technical Sprint is generated for the bottleneck
    assert any("Sprint" in plan["title"] for plan in updated_insights["action_plans"])
