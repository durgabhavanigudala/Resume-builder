from flask import Flask, render_template, request, send_file, make_response
from xhtml2pdf import pisa
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_resume():
    # Collect data from form
    data = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'skills': request.form.get('skills'),
        'experience': request.form.get('experience')
    }
    
    # Render the HTML template with user data
    rendered = render_template('resume.html', data=data)
    
    # Convert HTML to PDF
    pdf_out = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(rendered), dest=pdf_out)
    
    if pisa_status.err:
        return "Error generating PDF", 500
    
    pdf_out.seek(0)
    return send_file(pdf_out, as_attachment=True, download_name="resume.pdf")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)