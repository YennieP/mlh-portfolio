import os
from flask import Flask, render_template, request, url_for
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

@app.route('/jane/hobbies')
def jahabe_hobbies(): 
    hobbies = [
        {"name": "Watching Movies in a theater", "image": "img/jane_hobby1.jpg"},
        {"name": "Traveling & Outdoor Activities", "image": "img/jane_hobby2.jpg"},
    ]
    return render_template('jahabe_hobbies.html', 
                           url=os.getenv("URL"), 
                           hobbies=hobbies)

@app.route('/yanxi')
def yanxi():
    experiences = [
        {"company": "Fanfic Assistant", "role": "Full-Stack Developer", "duration": "Feb 2026 - Present", "description": [
            "Built an AI-powered platform for Chinese long-form creative writing.",
            "Implemented multi-provider LLM support, pgvector-based style retrieval for character consistency, and a bilingual React + FastAPI interface with real-time evaluation metrics."
        ]},
        {"company": "SQL Buddy", "role": "Backend Developer", "duration": "Sep 2025 - Dec 2025", "description": [
            "Developed an AI-powered SQL learning platform that auto-generates graded exercises via the ChatGPT API.",
            "Evaluated solutions in real time against a cloud MySQL database on GCP, built with Python and Django."
        ]},
        {"company": "NLP Semantic Understanding in M2M Communication", "role": "Research Assistant", "duration": "Sep 2024 - Jan 2025", "description": [
            "Researched the semantic fidelity of LLMs (BERT, GPT, RoBERTa) in cross-domain machine-to-machine communication.",
            "Evaluated results with cosine similarity and PCA across multiple domain benchmarks."
        ]},
        {"company": "LLM Medical Dialogue Platform", "role": "LLM Engineer", "duration": "Jul 2024 - Sep 2024", "description": [
            "Built an LLM-based platform for doctor-patient consultation simulation and iterative model evaluation.",
            "Tuned RNALens hyperparameters, improving Spearman correlation from 0.78 to 0.88 across three prompt iterations."
        ]},
    ]
    education = [
        {"school": "Northeastern University - Silicon Valley", "degree": "Master of Science in Computer Science", "duration": "Expected Graduation: TBD"},
        # TODO: 补上你的本科 / 之前的学历（学校、学位、专业、时间）
        {"school": "Undergraduate University", "degree": "Bachelor's Degree, Major", "duration": "Year - Year"},
    ]

    return render_template('yanxi.html',
                           url=os.getenv("URL"),
                           work_experiences=experiences,
                           educations=education,
                           pages=yanxi_pages())

# Menu shown on Yanxi's pages — add an entry here and the menu updates everywhere.
def yanxi_pages():
    return [
        {"name": "About Me", "url": url_for('yanxi')},
        {"name": "Hobbies", "url": url_for('yanxi_hobbies')},
        {"name": "Places", "url": url_for('yanxi_places')},
    ]

@app.route('/yanxi/hobbies')
def yanxi_hobbies():
    hobbies = [
        {"name": "Listening to Music", "description": "I enjoy listening to lyrical, pop, rock, alternative, ballad, and K-pop music.", "image": "img/Yanxi_listening_to_music.jpg"},
        {"name": "Singing", "description": "I love singing along while music plays - alone in my room, swaying and singing my heart out to the beat.", "image": "img/Yanxi_singing.jpg"},
        {"name": "Playing The Sims 4", "description": "I love using The Sims 4 to simulate the lives of people I care about - watching them live the way I'd want, or achieve things I couldn't, makes me genuinely happy.", "image": "img/Yanxi_Sims4.jpg"},
        {"name": "Writing", "description": "I enjoy writing fan fiction - using words to share my thoughts and send my blessings to the characters I love, while imagining the stories they might live out across different worlds and timelines.", "image": "img/Yanxi_writing.jpg"},
        {"name": "Drawing", "description": "I'm working hard on learning to draw. Since it's a completely different form of expression from writing, I hope to express my feelings and emotions from new angles and in new ways.", "image": "img/Yanxi_drawing.jpg"},
        {"name": "Badminton", "description": "A sport that keeps me fit and healthy.", "image": "img/Yanxi_badminton.jpg"},
    ]

    return render_template('yanxi_hobbies.html',
                           url=os.getenv("URL"),
                           pages=yanxi_pages(),
                           hobbies=hobbies)

@app.route('/yanxi/places')
def yanxi_places():
    # Countries/cities I've visited — shown as markers on the Leaflet map.
    visited = [
        {"name": "Russia", "lat": 55.7558, "lng": 37.6173},
        {"name": "Japan", "lat": 35.6762, "lng": 139.6503},
        {"name": "Thailand", "lat": 13.7563, "lng": 100.5018},
        {"name": "United States", "lat": 38.9072, "lng": -77.0369},
        {"name": "China", "lat": 39.9042, "lng": 116.4074},
        {"name": "Hungary (Budapest)", "lat": 47.4979, "lng": 19.0402},
        {"name": "Germany", "lat": 52.5200, "lng": 13.4050},
    ]
    return render_template('yanxi_places.html',
                           url=os.getenv("URL"),
                           pages=yanxi_pages(),
                           visited=visited)