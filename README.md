# DISCOVER MBA Flask App
DISCOVER MBA is a recommendation tool for people interested in applying to full-time Master of Business Administration(MBA) programs offered by business schools in the US and abroad. Recommendations are based on user-based collaborative filtering methods comparing education and professional backgrounds of prospective applicants and a database of professionals with MBA degrees.

Prospective applicants can upload their LinkedIn profile in pdf format to the web app and the app will process the profile with Natural Language Processing packages and compare the incoming profile to a reference LinkedIn profile database.  Result will be a list of business schools based on profile similarity of the applicants to those in the reference database.

Project is deployed on AWS at http://54.190.48.226:5000/

## Raw Data Overview
In order to utilize user-based collaborative filtering, a reference database of LinkedIn profiles of users who have completed/attending full-time MBA programs is needed.  I was able to get a dataset of approximately 3 million LinkedIn profiles from Kaggle (no longer available).  Profiles are stored in a single large JSON file at ~10GB.  Each single profile can be read as a nested dictionary containing fields such as Summary, Education, Experience, Skills, Interets, etc., but each profile may have only a subset of the fields.

## More details to follow

