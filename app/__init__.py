import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', 
                           title1="Jane Choi", 
                           title2="Yanxi Pan", 
                           url=os.getenv("URL"))

@app.route('/jane')
def jane(): 
    experiences = [
        {"company": "META X MLH Fellowship", "role": "Production Engineering Fellow", "duration": "June 2026 - Sep 2026", "description": ["Summer Fellowship"]}, 
        {"company": "DAIS Group", "role": "Undergrad Research MLE", "duration": "May 2025 - Present", "description": [
            "Contributing to DeepTracer generative AI pipeline for 3D protein structure prediction.",
            "Debugging and stabilizing deep learning training workflows, focusing on data integrity and model convergence."
        ]},
        {"company": "University of Washington", "role": "CS Grader", "duration": "Jan 2026 - Jun 2026", "description": ["Evaluated C++ algorithms assignments for 120+ students across two core CS courses"]}, 
        {"company": "Washington State Opportunity Scholarship", "role": "STEM Scholar Lead", "duration": "Oct 2024 - Present", "description": ["Led a cohort of 60+ scholars, managing quarter timelines and tracking academic, career, and scholarship milestones"]}, 
        {"company": "Microsoft", "role": "Software Product Manager (Capstone)", "duration": "Nov 2025 - Jun 2026", "description": ["Contributing to the software architecture and Windows-side system design for a Microsoft-sponsored research project focused on Surface Laptop keyboard skin detection and OS configuration."]}, 
        {"company": "Innovators Hub", "role": "Co-Founder", "duration": "Oct 2024 - Jun 2026", "description": ["Student-led community for CS, design, and entrepreneurship students building real-world products, hosting technical workshops, and connecting with industry mentors | UW branch"]}, 
        {"company": "IDEA Enterprises LLC", "role": "UX Design Intern", "duration": "Jul 2025 - Sep 2025", "description": ["Redesigned core workflows for an AI-based security camera platform by conducting user interviews, identifying navigation bottlenecks, and building an incident flow that reduced issue submission time while delivering technical UX specifications for the engineering team."]}, 

    ]
    education = [
        {"school": "University of Washington", "degree": "Bachelors of Science in Computer Science", "duration": "Expected Graduation: Winter 2027", "description": "Description"}, 
    ]
    hobbies = [
        {"name": "Hobby Name", "description": "Description", "image": "img/hobby1.jpg"}, 
    ]

    return render_template('jane.html', 
                           url=os.getenv("URL"), 
                           work_experiences=experiences, 
                           educations=education, 
                           hobbies=hobbies)

@app.route('/yanxi')
def yanxi(): 
    return render_template('yanxi.html', url=os.getenv("URL"))