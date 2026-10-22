"""
JobHunter-AI ATS-Friendly Word Document (.docx) Generator.
Creates clean, single-column, ATS-parseable Word documents.
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from typing import Dict, Any, List


def create_ats_docx(
    profile: Dict[str, Any],
    tailored_summary: str,
    optimized_bullets: List[Dict[str, str]],
    output_path: str = "output_resume.docx"
) -> str:
    """Generates an ATS-optimized .docx resume adhering to top formatting standards."""
    doc = Document()

    # Set 0.75-inch margins for clean single-page density
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # 1. Candidate Name (Header)
    name_p = doc.add_paragraph()
    name_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_name = name_p.add_run(profile.get("name", "Ajay Avunoori").upper())
    run_name.font.size = Pt(18)
    run_name.bold = True
    run_name.font.color.rgb = RGBColor(15, 23, 42)

    # Contact line
    contact_p = doc.add_paragraph()
    contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_text = f"{profile.get('location', 'Hyderabad, India')} | {profile.get('email', 'ajay.dev@example.com')} | {profile.get('phone', '+91 98765 43210')}"
    run_contact = contact_p.add_run(contact_text)
    run_contact.font.size = Pt(9.5)

    # Links line
    links_p = doc.add_paragraph()
    links_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    links_text = f"GitHub: {profile.get('github', 'github.com/Aladdu')} | Portfolio: {profile.get('portfolio', 'avunooriajayportfolio1.netlify.app')}"
    run_links = links_p.add_run(links_text)
    run_links.font.size = Pt(9.5)
    run_links.font.color.rgb = RGBColor(37, 99, 235)

    # Helper function for Section Headings
    def add_section_header(title: str):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
        run = h.add_run(title.upper())
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(15, 23, 42)

    # 2. Professional Summary
    add_section_header("Professional Summary")
    sum_p = doc.add_paragraph()
    sum_p.paragraph_format.space_after = Pt(6)
    sum_p.add_run(tailored_summary)

    # 3. Technical Skills
    add_section_header("Technical Skills")
    skills = [
        ("Programming Languages: ", "Java (Core & Advanced), JavaScript (ES6+), SQL, Python (Basics)"),
        ("Backend Frameworks: ", "Spring Boot, Spring MVC, Spring Data JPA, Hibernate, RESTful APIs, Microservices"),
        ("Frontend Technologies: ", "React.js, HTML5, CSS3, Tailwind CSS, Responsive Web Design"),
        ("Databases & Tools: ", "MySQL, PostgreSQL, Git, GitHub, Maven, Postman, Docker (Basics)"),
        ("Core Concepts: ", "Object-Oriented Programming (OOP), Data Structures & Algorithms, Design Patterns, Agile/Scrum")
    ]
    for label, val in skills:
        sp = doc.add_paragraph(style='List Bullet')
        sp.paragraph_format.space_after = Pt(2)
        run_label = sp.add_run(label)
        run_label.bold = True
        sp.add_run(val)

    # 4. Featured Projects
    add_section_header("Featured Projects")

    # Project 1
    p1_title = doc.add_paragraph()
    p1_title.paragraph_format.space_before = Pt(4)
    p1_title.paragraph_format.space_after = Pt(1)
    r1 = p1_title.add_run("Automated Electric Billing & Payment Management System")
    r1.bold = True
    p1_title.add_run(" | Java, MySQL, JDBC")
    
    b1_1 = doc.add_paragraph(style='List Bullet')
    b1_1.add_run("Architected an automated Electric Billing & Payment System using Java and MySQL, reducing manual billing overhead by 40% through normalized schema design and parameterized queries.")
    b1_2 = doc.add_paragraph(style='List Bullet')
    b1_2.add_run("Integrated automated tariff calculation logic handling multi-tier consumption slabs with 100% calculation accuracy.")
    b1_3 = doc.add_paragraph(style='List Bullet')
    b1_3.add_run("Enhanced database access efficiency using prepared statements and connection pooling to prevent SQL injection vulnerabilities.")

    # Project 2
    p2_title = doc.add_paragraph()
    p2_title.paragraph_format.space_before = Pt(4)
    p2_title.paragraph_format.space_after = Pt(1)
    r2 = p2_title.add_run("Secure Multi-User ATM Simulation System")
    r2.bold = True
    p2_title.add_run(" | Java, MySQL, OOP")

    b2_1 = doc.add_paragraph(style='List Bullet')
    b2_1.add_run("Engineered a robust multi-user ATM Simulation platform featuring PIN authentication, balance inquiry, deposit, and fund transfers.")
    b2_2 = doc.add_paragraph(style='List Bullet')
    b2_2.add_run("Enforced strict ACID transactions using MySQL commit/rollback blocks to ensure zero data discrepancies during concurrent withdrawal scenarios.")
    b2_3 = doc.add_paragraph(style='List Bullet')
    b2_3.add_run("Designed clean, decoupled architecture adhering to Object-Oriented Principles (Encapsulation, Polymorphism) and DAO design patterns.")

    # Project 3
    p3_title = doc.add_paragraph()
    p3_title.paragraph_format.space_before = Pt(4)
    p3_title.paragraph_format.space_after = Pt(1)
    r3 = p3_title.add_run("Full-Stack Developer Portfolio & Web Applications")
    r3.bold = True
    p3_title.add_run(" | React.js, JavaScript, Tailwind CSS")

    b3_1 = doc.add_paragraph(style='List Bullet')
    b3_1.add_run("Developed modern single-page applications (SPA) in React.js featuring dynamic state management, smooth routing, and interactive UI components.")
    b3_2 = doc.add_paragraph(style='List Bullet')
    b3_2.add_run("Optimized asset loading and bundle sizes, achieving 95+ performance ratings on Google Lighthouse audits.")

    # 5. Education
    add_section_header("Education")
    edu_p = doc.add_paragraph()
    edu_p.paragraph_format.space_after = Pt(1)
    r_edu = edu_p.add_run("Master of Computer Applications (MCA)")
    r_edu.bold = True
    edu_p.add_run(" | Osmania University, Hyderabad (2023)")
    edu_sub = doc.add_paragraph()
    edu_sub.paragraph_format.space_after = Pt(4)
    edu_sub.add_run("Coursework: Data Structures & Algorithms, DBMS, OOP with Java, Web Technologies.")

    # Save
    doc.save(output_path)
    return output_path
