from flask import Flask, render_template, request
from time import strftime
import time
import os
import urllib.request
from werkzeug.utils import secure_filename

upload_folder = '/Users/BPL/Data_Science_Flatiron/capstone-flask-app-template-seattle-ds-062419/python/profile_uploads'

app = Flask(__name__, static_url_path="/static")
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/")
def index():
    """Return the main page."""
    time_str = strftime("%m/%d/%Y %H:%M")
    print(time_str)
    return render_template("index.html", time_info=time_str)

def upload_file():
    """Upload file into designated directory. Returns path to saved file"""
    file = request.files['linkedin_pdf']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return filepath

def profile_reader(filepath):
    """parse pdf for content, returns text in education and experience sections"""
    from python.PDF_Reader import parse_pdf

    return parse_pdf(filepath)

@app.route("/review", methods=["POST"])
def review_profile():
    """Profile information review page"""
    #data = request.form
    #print(data)
    if "linkedin_pdf" in request.files:
        filepath = upload_file()
        edu_hist, exp_hist = profile_reader(filepath)
    else:
        edu_hist = "enter information"
        exp_hist = "enter information"
    
    return render_template("review.html", edu_hist=edu_hist, exp_hist=exp_hist)

def make_recommendation(education, experience):
    from python.MBA_Finder import recommend_business_school

    return recommend_business_school(education, experience)

@app.route("/results", methods=["POST"])
def results():
   data = request.form
   edu_hist = data["edu_hist"]
   exp_hist = data["exp_hist"]
   
   recs = make_recommendation(edu_hist, exp_hist)
   #recs = ['Stanford', 'Northwestern Kellogg', 'Chicago Booth', 'Cambridge Judge', 'LBS',
   #        'Harvard', 'Yale', 'INSEAD']

   return render_template("results.html", reccos=recs)