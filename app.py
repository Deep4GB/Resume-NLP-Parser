from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Paste your resume parsing function here (from the previous response)

@app.route('/', methods=['GET', 'POST'])

def index():
    parsed_data = None

    if request.method == 'POST':
        resume_file = request.files['resume_file']

        if resume_file:
            # Read the content of the uploaded file
            resume_text = resume_file.read().decode('utf-8')
            parsed_data = parse_resume(resume_text)

    return render_template('index.html', parsed_data=parsed_data)

if __name__ == '__main__':
    app.run(debug=True)
