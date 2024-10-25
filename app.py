from flask import Flask, request, jsonify, render_template, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_resumes'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

resumes_data = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@app.route('/')
def home():
    return render_template('store.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or not all(k in request.form for k in ['name', 'phone', 'email', 'skills']):
        return jsonify({"error": "Missing file or user details"}), 400

    file = request.files['file']
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    skills = request.form['skills'].split(',')

    if file and allowed_file(file.filename):
        ## TODO - rename file using phone no, 
        # validate phone no and email format - using html
        # pagination
        ## Move to database - use csv or a real databse to store 'resume_data'
        ## improve UI
        ## phone no and email should be unique
        # filter page should name along with link
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        resumes_data.append({
            "filename": file.filename,
            "name": name,
            "phone": phone,
            "email": email,
            "skills": [skill.strip().lower() for skill in skills]
        })
    
        print(resumes_data)
        return render_template('store.html', message="Resume uploaded successfully!")
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/filter', methods=['GET'])
def filter_page():
    filter_type = request.args.get('filter_type')
    filter_value = request.args.get('filter_value', '').lower()
    print(request.args)
    print(filter_type)
    print(filter_value)
    if not filter_type or not filter_value:
        return render_template('filter.html')

    matching_resumes = []
    print (resumes_data)
    for resume in resumes_data:
        if filter_type == 'phone' and filter_value in resume['phone'].lower():
            matching_resumes.append(resume)
        elif filter_type == 'email' and filter_value in resume['email'].lower():
            matching_resumes.append(resume)
        elif filter_type == 'skill' :
            print (resume['skills'])
            for skill in resume['skills']:
                print (skill)
                if filter_value == skill :
                    matching_resumes.append(resume)
    print(matching_resumes)
    return jsonify({"matching_resumes": matching_resumes})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
