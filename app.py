from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from werkzeug.utils import secure_filename
import os
import time

# form filename import classname
from EntityExtractor import EntityExtractor
app = FastAPI()

# Configure Temporary Data Storage
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configure Templates
templates = Jinja2Templates(directory="templates")

@app.get('/',response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse(request=request,name='index.html')

@app.post('/resumeanalyzer/',response_class=HTMLResponse)
async def resumeAnalyzer(request:Request,file: UploadFile):
    # Delete all previous uploads 
    if len(os.listdir('uploads')) > 0:
        os.remove(os.path.join('uploads',os.listdir('uploads')[0]))

    file_name = secure_filename(file.filename)
    # Check if file is uploaded or not
    if file_name:
        # Save if it is a PDF file and return "<filename> uploaded successfully"
        if file_name.endswith('.pdf'):
            with open(os.path.join('uploads',file.filename),'wb') as write_file:
                write_file.write(file.file.read())
            message = f"{file_name} uploaded successfully"

        # Else return "Error: Only PDF files are allowed"
        else:
            message='Error: Only PDF files are allowed'

    # If no file is uploaded return "No file uploaded"
    else:
        message = f'Error: No file uploaded'

    if 'Error' not in message:
        return RedirectResponse(app.url_path_for('uploaded_file',message=message))

    return templates.TemplateResponse(request=request,
                                      name='resumeanalyzerpage.html',
                                      context={'message':message})
    
@app.get('/resumeanalyzer/',response_class=HTMLResponse)
async def resumeAnalyzer(request:Request):
    return templates.TemplateResponse(request=request,
                                      name='resumeanalyzerpage.html')

@app.post('/resumeanalyzer/{message}/')
async def uploaded_file(request:Request, message: str):
    ee = EntityExtractor('uploads')
    output = ee.extract_data()

    # time.sleep(6)
    return templates.TemplateResponse(request=request,
                                        name='output.html',
                                        context={"output":output})

# @app.get('/resumeanalyzer/<message>/hi/', methods=['POST'])
# async def add_resume(message):
#     ee = EntityExtractor(app.config['UPLOAD_FOLDER'])
#     dict_string = ee.extract_data()
#     # return jsonify({'message': 'User added', 'username': username}), 201
#     # return dict_string
#     # return redirect(url_for('uploaded_file',message=message))
#     return render_template('resumeanalyzerpage.html',message=message,output=dict_string)

#     # render_template('resumeanalyzerpage.html', message="message",output=output)

# # @app.get('/resumeanalyzer/<args>')
# # async def uploaded_file(args):
# #     if not('.pdf' in args):
# #         return render_template('resumeanalyzerpage.html', message=args)
# #     return render_template('resumeanalyzerpage.html', filename=args)
