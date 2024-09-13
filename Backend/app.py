import sys
sys.path.append('/Users/lilmoltojo/Library/Python/3.9/lib/python/site-packages')
from flask import Flask, request, jsonify, render_template
from pdf_parser import analyze_resume, extract_keywords, calculate_similarity, calculate_ats_score
import tempfile
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('frontpage.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume_route():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file uploaded'}), 400
    
    resume_file = request.files['resume']
    job_description_text = request.form.get('job', '')
    required_years = int(request.form.get('years', 0))
    required_degree = request.form.get('degree', '')
    required_skills = request.form.get('skills', '').split(',')
    
    if resume_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if job_description_text == '':
        return jsonify({'error': 'No job description provided'}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.filename)[1]) as temp_file:
            resume_file.save(temp_file.name)
            temp_filename = temp_file.name

        resume_text, resume_keywords = analyze_resume(temp_filename)
        
        os.unlink(temp_filename)

        job_keywords = extract_keywords(job_description_text)
        similarity_score = calculate_similarity(resume_text, job_description_text)
        ats_score = calculate_ats_score(resume_text, job_description_text, required_years, required_degree, required_skills)
        missing_keywords = list(set(job_keywords) - set(resume_keywords))
        
        ats_scores = calculate_ats_score(resume_text, job_description_text, required_years, required_degree, required_skills)
        
        result = {
            'resume_keywords': resume_keywords,
            'job_keywords': job_keywords,
            'similarity_score': similarity_score,
            'ats_scores': ats_scores,
            'missing_keywords': missing_keywords
        }
        
        return render_template('result.html', result=result)
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return render_template('error.html', error=str(e))
if __name__ == "__main__":
    app.run(debug=True, port=5003)