from flask import Flask, render_template, request, send_file
import PyPDF2
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    pdf_files = request.files.getlist('pdfs')
    pdf_merger = PyPDF2.PdfMerger()

    for pdf in pdf_files:
        pdf_merger.append(pdf)

    merged_pdf = BytesIO()
    pdf_merger.write(merged_pdf)
    merged_pdf.seek(0)

    return send_file(
        merged_pdf,
        as_attachment=True,
        download_name='merged_output.pdf',
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run()
