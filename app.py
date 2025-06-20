from flask import Flask, render_template, request#, Markup # Added Markup
from markupsafe import Markup
from utils.llm_summary import generate_summary,get_score
from utils.resume_parser import extract_text
import os
import re # For a more robust nl2br
import io
import markdown
from markupsafe import Markup

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Custom Jinja2 filter for nl2br
def nl2br(value):
    if not isinstance(value, str):
        return value
    # More robustly handle different types of newlines and ensure HTML safety
    br = Markup("<br>\n")
    # Replace various newline combinations with <br>
    value = re.sub(r'(\r\n|\r|\n)', br, value)
    return Markup(value)

app.jinja_env.filters['nl2br'] = nl2br

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        jd = request.form['job_description']
        files = request.files.getlist('resumes')

        for file in files:
            if file and file.filename: # Ensure file exists and has a filename
                resume_text = extract_text(file)
                # Ensure resume_text and jd are not None or empty before processing
                if resume_text and jd:
                    summary = generate_summary(resume_text, jd)
                    results.append({
                        'filename': file.filename,
                        'score': get_score(resume_text, jd),
                        'summary': Markup(markdown.markdown(summary))
                    })
                else:
                    # Handle empty resume_text or jd after extraction/input
                    results.append({
                        'filename': file.filename,
                        'score': 10,
                        'summary': "Could not process resume or job description."
                    })
            else:
                print(f"Skipping invalid file: {file}")
                
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
