from flask import Flask, render_template, request, send_file
import PyPDF2
import os
from io import BytesIO

# Initialize Flask app
app = Flask(__name__)

# Folder to store uploaded PDFs temporarily
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the PDF upload and merging
@app.route('/merge', methods=['POST'])
def merge_pdfs():
    # Get the uploaded files from the form
    pdf_files = request.files.getlist('pdfs')

    # Create a PdfMerger object
    pdf_merger = PyPDF2.PdfMerger()

    # Loop through the uploaded PDFs and append them to the merger
    for pdf in pdf_files:
        # Save the uploaded PDF file temporarily
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
        pdf.save(pdf_path)

        # Append to the PDF merger
        pdf_merger.append(pdf_path)

    # Create a BytesIO object to hold the merged PDF in memory
    merged_pdf = BytesIO()
    pdf_merger.write(merged_pdf)

    # Seek to the beginning of the merged PDF
    merged_pdf.seek(0)

    # Return the merged PDF as a downloadable file
    return send_file(merged_pdf, as_attachment=True, download_name='merged_output.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
