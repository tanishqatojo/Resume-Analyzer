# AI Resume Analyzer

AI Resume Analyzer is a web-based tool that helps users analyze their resumes and match them with job descriptions. By utilizing Natural Language Processing (NLP), the tool extracts keywords from both the resume and job description to suggest improvements and calculate the similarity between the two. The goal is to help users tweak their resumes to better align with specific job postings.

## Features

- Extracts text from PDF and DOCX resumes
- Analyzes and matches keywords between resumes and job descriptions
- Provides a similarity score between a resume and a job description
- Suggests missing keywords that can improve resume relevance

## Technologies Used

- **Backend**: Python, Flask
  - **NLP**: SpaCy, Scikit-learn
  - **PDF Parsing**: pdfminer.six
  - **Word Document Parsing**: python-docx
- **Frontend**: HTML, CSS, JavaScript
