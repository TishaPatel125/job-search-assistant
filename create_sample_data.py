import os
from fpdf import FPDF
from datetime import datetime, timedelta

def create_dirs(base_path):
    os.makedirs(os.path.join(base_path, 'sample-data', 'jobs'), exist_ok=True)

def create_resume(base_path):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("helvetica", "B", 24)
    pdf.cell(0, 15, "Tishaben Patel", align="C", new_x="LMARGIN", new_y="NEXT")
    
    # Contact
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 10, "Toronto, ON | (555) 123-4567 | tpatel@example.com", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, "LinkedIn: linkedin.com/in/tishaben | GitHub: github.com/tishaben", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Education
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "EDUCATION", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 8, "Seneca Polytechnic, Toronto, ON", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Advanced Diploma in Computer Programming & Analysis", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Expected Graduation: December 2026", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Student ID: 140240235", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Skills
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "TECHNICAL SKILLS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, "Python, JavaScript, Node.js, React, HTML/CSS, SQL, Git, Docker, REST APIs, AWS basics")
    pdf.ln(5)
    
    # Experience
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "EXPERIENCE", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, "Web Developer Intern | TechNova Solutions | May 2025 - August 2025", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, "- Assisted in developing responsive frontend interfaces using React and HTML/CSS.\n- Collaborated with senior developers to design and implement RESTful APIs using Node.js.\n- Participated in daily stand-ups and agile development processes.")
    pdf.ln(5)
    
    # Projects
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "ACADEMIC PROJECTS", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, "E-Commerce Web Application", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, "Developed a full-stack e-commerce site using React, Node.js, and PostgreSQL. Implemented user authentication and cart functionality.")
    
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, "Sales Data Analysis Tool", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, "Created a Python script using Pandas and Matplotlib to analyze and visualize sales data from a CSV file.")
    
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, "AI Customer Support Chatbot", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, "Built a simple conversational AI chatbot integrating with OpenAI API, deployed using Docker.")
    pdf.ln(5)
    
    # Certifications
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "CERTIFICATIONS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 8, "AWS Certified Cloud Practitioner (In Progress)", new_x="LMARGIN", new_y="NEXT")
    
    output_path = os.path.join(base_path, 'sample-data', 'resume.pdf')
    pdf.output(output_path)
    print(f"Created {output_path}")

def create_job(base_path, filename, title, company, location, salary, skills, responsibilities, date_posted, description):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, f"{company} | {location}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    
    if salary:
        pdf.cell(0, 8, f"Salary: {salary}", align="C", new_x="LMARGIN", new_y="NEXT")
        
    pdf.cell(0, 8, f"Posted: {date_posted}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Description
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "About the Company", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, description)
    pdf.ln(5)
    
    # Responsibilities
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "Responsibilities", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 11)
    for resp in responsibilities:
        pdf.set_x(15)
        pdf.multi_cell(180, 7, f"  - {resp}")
    pdf.ln(5)
    
    # Skills
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "Required & Preferred Skills", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, ", ".join(skills))
    pdf.ln(5)
    
    # Requirements
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "Requirements", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, "Experience Level: Entry to Mid-level\nEducation: Bachelor's degree or Diploma in Computer Science, Software Engineering, or related field.")
    
    output_path = os.path.join(base_path, 'sample-data', 'jobs', filename)
    pdf.output(output_path)
    print(f"Created {output_path}")

def main():
    base_path = r"c:\Users\tisha\OneDrive\Desktop\AIP444NSA\lab1\aip444\assignments\assignment-02"
    create_dirs(base_path)
    create_resume(base_path)
    
    today = datetime.now()
    
    jobs = [
        {
            "filename": "junior-fullstack-shopify.pdf",
            "title": "Junior Full Stack Developer",
            "company": "Shopify",
            "location": "Ottawa, ON - Remote",
            "salary": "$65K-$80K",
            "skills": ["React", "Node.js", "Ruby", "HTML/CSS", "JavaScript", "Git", "REST APIs", "SQL", "Docker", "GraphQL"],
            "responsibilities": ["Develop and maintain web applications", "Write clean, scalable code", "Collaborate with cross-functional teams", "Participate in code reviews", "Troubleshoot and debug issues", "Implement UI components", "Optimize applications for maximum speed"],
            "date_posted": (today - timedelta(days=3)).strftime('%Y-%m-%d'),
            "description": "Shopify is a leading global commerce company, providing trusted tools to start, grow, market, and manage a retail business of any size."
        },
        {
            "filename": "frontend-dev-rbc.pdf",
            "title": "Frontend Developer",
            "company": "RBC",
            "location": "Toronto, ON - Hybrid",
            "salary": "$60K-$75K",
            "skills": ["React", "TypeScript", "CSS", "JavaScript", "HTML", "Redux", "Jest", "Git", "Responsive Design", "Web Accessibility (WCAG)"],
            "responsibilities": ["Build responsive user interfaces", "Work closely with UX/UI designers", "Ensure high performance of applications", "Write unit and integration tests", "Participate in agile ceremonies", "Maintain code quality"],
            "date_posted": (today - timedelta(days=7)).strftime('%Y-%m-%d'),
            "description": "Royal Bank of Canada is a global financial institution with a purpose-driven, principles-led approach to delivering leading performance."
        },
        {
            "filename": "backend-dev-amazon.pdf",
            "title": "Backend Developer",
            "company": "Amazon",
            "location": "Vancouver, BC - Onsite",
            "salary": "$80K-$100K",
            "skills": ["Python", "AWS", "Java", "SQL", "NoSQL", "Microservices", "Linux", "Docker", "Kubernetes", "System Design"],
            "responsibilities": ["Design robust backend services", "Optimize database queries", "Deploy applications on AWS", "Monitor system performance", "Ensure data security", "Collaborate with frontend developers", "Participate in system architecture planning"],
            "date_posted": (today - timedelta(days=2)).strftime('%Y-%m-%d'),
            "description": "Amazon is guided by four principles: customer obsession rather than competitor focus, passion for invention, commitment to operational excellence, and long-term thinking."
        },
        {
            "filename": "software-eng-opentext.pdf",
            "title": "Software Engineer",
            "company": "OpenText",
            "location": "Waterloo, ON - Hybrid",
            "salary": "$55K-$70K",
            "skills": ["Java", "Spring", "SQL", "JavaScript", "Git", "JUnit", "Jenkins", "Hibernate", "Agile methodologies"],
            "responsibilities": ["Develop enterprise software solutions", "Write and maintain backend code", "Perform code reviews", "Write technical documentation", "Assist in software testing", "Work in an Agile environment"],
            "date_posted": (today - timedelta(days=14)).strftime('%Y-%m-%d'),
            "description": "OpenText empowers organizations to manage, secure, and leverage information effectively."
        },
        {
            "filename": "web-dev-freshbooks.pdf",
            "title": "Web Developer",
            "company": "FreshBooks",
            "location": "Toronto, ON - Remote",
            "salary": None,
            "skills": ["React", "Python", "PostgreSQL", "JavaScript", "HTML/CSS", "Git", "Docker", "Flask", "REST APIs"],
            "responsibilities": ["Develop new web features", "Maintain existing codebase", "Optimize database schemas", "Collaborate with product managers", "Write tests for robust code", "Ensure cross-browser compatibility"],
            "date_posted": (today - timedelta(days=5)).strftime('%Y-%m-%d'),
            "description": "FreshBooks is a cloud-based accounting software service designed for small and medium-sized businesses."
        },
        {
            "filename": "junior-dev-telus.pdf",
            "title": "Junior Developer",
            "company": "TELUS",
            "location": "Calgary, AB - Hybrid",
            "salary": "$55K-$65K",
            "skills": ["JavaScript", "Python", "Docker", "Git", "Linux", "Bash scripting", "SQL", "API Integration"],
            "responsibilities": ["Support software development lifecycle", "Write internal automation scripts", "Assist in application deployment", "Debug production issues", "Document system configurations"],
            "date_posted": (today - timedelta(days=10)).strftime('%Y-%m-%d'),
            "description": "TELUS is a dynamic, world-leading communications and information technology company."
        },
        {
            "filename": "fullstack-dev-wealthsimple.pdf",
            "title": "Full Stack Developer",
            "company": "Wealthsimple",
            "location": "Toronto, ON - Remote",
            "salary": "$70K-$90K",
            "skills": ["React", "Ruby", "GraphQL", "PostgreSQL", "TypeScript", "Redis", "Docker", "AWS", "Jest"],
            "responsibilities": ["Build financial technology products", "Implement GraphQL APIs", "Create reusable React components", "Ensure application security", "Improve application performance", "Collaborate with design and product teams", "Write comprehensive test suites"],
            "date_posted": (today - timedelta(days=1)).strftime('%Y-%m-%d'),
            "description": "Wealthsimple is on a mission to help everyone achieve financial freedom, no matter who they are or how much they have."
        },
        {
            "filename": "devops-jr-bell.pdf",
            "title": "Junior DevOps Engineer",
            "company": "Bell Canada",
            "location": "Montreal, QC - Onsite",
            "salary": "$60K-$75K",
            "skills": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD", "Jenkins", "Git", "Python", "Bash", "Terraform"],
            "responsibilities": ["Maintain CI/CD pipelines", "Manage containerized applications", "Monitor system health", "Automate infrastructure deployment", "Assist in cloud migration", "Provide technical support"],
            "date_posted": (today - timedelta(days=8)).strftime('%Y-%m-%d'),
            "description": "Bell is Canada's largest communications company, providing consumers and business customers with solutions to all their communications needs."
        },
        {
            "filename": "software-dev-sap.pdf",
            "title": "Software Developer",
            "company": "SAP",
            "location": "Waterloo, ON - Hybrid",
            "salary": "$65K-$85K",
            "skills": ["JavaScript", "TypeScript", "Node.js", "React", "SQL", "Git", "Cloud Foundry", "REST APIs", "Agile"],
            "responsibilities": ["Design and develop software modules", "Ensure high code quality standards", "Participate in SCRUM meetings", "Collaborate globally", "Write technical specifications", "Debug and resolve complex issues", "Optimize for enterprise scale"],
            "date_posted": (today - timedelta(days=4)).strftime('%Y-%m-%d'),
            "description": "SAP is the world's leading provider of enterprise software and software-related services."
        }
    ]
    
    for job in jobs:
        create_job(base_path, **job)

if __name__ == '__main__':
    main()
