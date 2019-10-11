from flask import Flask, render_template, request, jsonify
from time import strftime
import time
import os
import urllib.request
from werkzeug.utils import secure_filename
from waitress import serve

upload_folder = './python/profile_uploads/'

app = Flask(__name__, static_url_path="/static")
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/")
def index():
    """Return the main page."""
    date_str = strftime("%B %d, %Y")
    print(date_str)
    return render_template("index.html", date_info=date_str)

@app.route("/upload", methods=["POST"])
def upload_profile():
    return render_template("upload.html")

def upload_file():
    """Upload file into designated directory. Returns path to saved file"""
    file = request.files['linkedin_pdf']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return filepath

def read_profile_pdf(filepath):
    """Parse profile pdf for content, returns text in education and experience sections"""
    from python.PDF_Reader import parse_pdf

    return parse_pdf(filepath)

#comment out read link feature
#def read_profile_link(prof_link):
#    from python.profile_info_retrieval import retrieve_profile_info_by_link
#
#    return retrieve_profile_info_by_link(prof_link)

@app.route("/review", methods=["POST"])
def review_profile():
    """Profile information review page"""
    data = request.form
    #file = request.files
    #print(data)
    #print(request.files)
    if "linkedin_pdf" in request.files and request.files["linkedin_pdf"].filename != "":
        filepath = upload_file()
        edu_hist, exp_hist = read_profile_pdf(filepath)
    #elif "linkedin_url" in data and data["linkedin_url"] != "":
    #    edu_hist, exp_hist = read_profile_link(data["linkedin_url"])
    else:
        edu_hist, exp_hist = "Please enter information", "Please enter information"
    
    return render_template("review.html", edu_hist=edu_hist, exp_hist=exp_hist)

def make_recommendation(education, experience):
    from python.Core_Engine import recommend_business_school

    return recommend_business_school(education, experience)

@app.route("/make_recs", methods=["POST"])
def process_inputs():
    data = request.get_json()
    edu_hist = data["edu_hist"]
    exp_hist = data["exp_hist"]
   
    recs = make_recommendation(edu_hist, exp_hist)
    
    #dummy recs for page testing
    #recs = ['Stanford', 'Northwestern Kellogg', 'Chicago Booth', 'Cambridge Judge', 'LBS',
    #       'Harvard', 'Yale', 'INSEAD']
    #time.sleep(2)

    return jsonify({"recs":recs})

@app.route("/results", methods=["POST"])
def results():
   data = request.form
   edu_hist = data["edu_hist"]
   exp_hist = data["exp_hist"]
   
   #recs = make_recommendation(edu_hist, exp_hist)

   return render_template("results.html", edu_hist=edu_hist, exp_hist=exp_hist)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)