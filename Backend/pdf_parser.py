import sys
sys.path.append('/Users/lilmoltojo/Library/Python/3.9/lib/python/site-packages')
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io
import re

def extract_keywords(text, top_n=10):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([text])
    feature_names = tfidf.get_feature_names_out()
    sorted_items = sorted(zip(tfidf_matrix.tocsr().data, feature_names), reverse=True)
    return [item[1] for item in sorted_items[:top_n]]

def extract_resume_text(pdf_file):
    with open(pdf_file, 'rb') as file:
        pdf_content = file.read()
    text = extract_text(io.BytesIO(pdf_content))
    return ' '.join(text.split())  # This removes extra whitespace

def analyze_resume(pdf_file):
    resume_text = extract_resume_text(pdf_file)
    resume_keywords = extract_keywords(resume_text)
    return resume_text, resume_keywords

def calculate_similarity(text1, text2):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

def keyword_score(resume_text, job_text):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())
    matched_words = resume_words.intersection(job_words)
    return len(matched_words) / len(job_words)

def experience_score(resume_text, required_years):
    experience = re.findall(r'(\d+)\s*(?:years?|yrs?)', resume_text.lower())
    if experience:
        max_experience = max(map(int, experience))
        return min(max_experience / required_years, 1)
    return 0

def education_score(resume_text, required_degree):
    degrees = ['bachelor', 'master', 'phd', 'doctorate']
    resume_degree = max((d for d in degrees if d in resume_text.lower()), default=None)
    if not required_degree:
        return 1  
    try:
        required_index = degrees.index(required_degree.lower())
    except ValueError:
        return 0 
    if resume_degree:
        resume_index = degrees.index(resume_degree)
        return 1 if resume_index >= required_index else 0.5
    return 0

def skills_score(resume_text, required_skills):
    resume_skills = set(extract_keywords(resume_text))
    matched_skills = resume_skills.intersection(required_skills)
    return len(matched_skills) / len(required_skills)

def calculate_ats_score(resume_text, job_text, required_years, required_degree, required_skills):
    keyword_weight = 0.3
    experience_weight = 0.25
    education_weight = 0.2
    skills_weight = 0.25

    k_score = keyword_score(resume_text, job_text)
    e_score = experience_score(resume_text, required_years)
    ed_score = education_score(resume_text, required_degree)
    s_score = skills_score(resume_text, required_skills)

    total_score = (k_score * keyword_weight +
                   e_score * experience_weight +
                   ed_score * education_weight +
                   s_score * skills_weight)

    return {
        'total_score': total_score * 100,  
        'keyword_score': k_score * 100,
        'experience_score': e_score * 100,
        'education_score': ed_score * 100,
        'skills_score': s_score * 100
    }
