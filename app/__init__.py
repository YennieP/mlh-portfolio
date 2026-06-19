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
    return render_template('jane.html', url=os.getenv("URL"))

@app.route('/yanxi')
def yanxi(): 
    return render_template('yanxi.html', url=os.getenv("URL"))