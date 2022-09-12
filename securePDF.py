from flask import Flask, render_template, request
from PyPDF2 import PdfFileWriter, PdfFileReader
import os


app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main():
    return render_template('secure_pdf.html')

@app.route('/secure_result', methods = ['GET','POST'])
def secureResult():
    if request.method == 'POST':
        file = request.form['file']
        securePassword = request.form['securePassword']

        if file == '' or securePassword == '':
            return 'Do Not Leave The Fields Blank.'
        
        parser = PdfFileWriter()
        splitFile = file.split('\\')
        slashFile = '\\\\'.join(splitFile)

        pdf = PdfFileReader(slashFile)

        for page in range(int(pdf.numPages)):
            parser.addPage(pdf.getPage(page))

        parser.encrypt(securePassword)    

        with open(f'Secure {splitFile[len(splitFile) - 1]}', 'wb') as file:
            parser.write(file)
            file.close()
            
        securePDF_ = '{0}'.format(file.name)
        if os.path.exists(securePDF_):
            return render_template('secure_pdf_result.html', result = [[splitFile[len(splitFile) - 1], securePDF_]])
    
    else:
        return 'For post requests only.'

        
if __name__ == '__main__':
    app.run(debug=True, port=5000)