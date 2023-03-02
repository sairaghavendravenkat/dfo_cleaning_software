import os
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
# from utils import excel_file_generator, data_count_calculator_acc_to_test_reasons
from datacleaning_dfo_28022022 import dane_logic
from datetime import datetime as dt
# Get current path
path = os.getcwd()

# Here we will store the uploaded files
UPLOAD_FOLDER_master = os.path.join(path, "static/media/input_files/master_DFO")
UPLOAD_FOLDER_DFO_latest = os.path.join(path, "static/media/input_files/DFO_latest_sheets")


# the set of allowed file extensions
ALLOWED_EXTENSIONS = {"xlsx"}

# Intialising and declaring app for flask
app = Flask(__name__)

# configuring the location where the file will store after uploading
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

log_contents =""
log_contents_newlines =""

def clear_folders():
    folder1_path = os.path.join(path, "static/media/input_files/master_DFO")
    folder2_path = os.path.join(path, "static/media/input_files/DFO_latest_sheets")
    
    # Delete all files in folder1
    for filename in os.listdir(folder1_path):
        file_path = os.path.join(folder1_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
    
    # Delete all files in folder2
    for filename in os.listdir(folder2_path):
        file_path = os.path.join(folder2_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
    return "folders are cleared"
def allowed_file(filename):
    """
    The purpose of this function is to return true for any files that end with a allowed extensions'.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Declaring route for the home page
@app.route("/", methods=["GET", "POST"])
def upload_file():
    """
    Helps in uploading file and merging excel files and redirect the page to the download panel after submitting.
    """
    response = {"status": True, 'message': "Sucessful !"}
    
    if request.path =='/':
        if ((len(os.listdir(UPLOAD_FOLDER_master))!=0) or (len(os.listdir(UPLOAD_FOLDER_DFO_latest)) != 0)):
          a = clear_folders()
        #   return redirect(request.url)
          
    print(len(os.listdir(UPLOAD_FOLDER_master)))
    print(len(os.listdir(UPLOAD_FOLDER_DFO_latest)))
    
    if request.method == "POST":
        try:
            #execute when we doesn't upload any file in the input
            if ("handwritten_file" not in request.files or "software_file" not in request.files):
                return redirect(request.url)

            handwritten_file = request.files.getlist("handwritten_file")
            print (handwritten_file)
            software_file = request.files.get("software_file")
            # print("this is the uploaded file",handwritten_file)
            print("this is the uploaded file",software_file)
            dfolist_flask = []         
            for multi in handwritten_file:
                if (multi and allowed_file(multi.filename)):
                    handwritten_filename = secure_filename(multi.filename)
                    dfolist_flask.append(handwritten_filename)
                    multi.save(os.path.join(UPLOAD_FOLDER_DFO_latest, handwritten_filename))           


           
            if (software_file and allowed_file(software_file.filename)):
                # Pass a filename to the function and it will return a secure version of it                
                software_filename = secure_filename(software_file.filename)                
                software_file.save(os.path.join(UPLOAD_FOLDER_master, software_filename))
                print("I am here in main page")
                # return redirect(f"/loading/{software_filename}")               
                
                start_time = dt.now()
                response_DFO_cleaning,output_filename1,output_filename2 = dane_logic(software_filename)                   
                end_time = dt.now()
                # print(f"Task Successfully completed in {end_time - start_time} seconds.")
                if(response_DFO_cleaning == 'Programme is successfully executed'):
                    print(f"Programme Task Successfully completed in {end_time - start_time} seconds.")
                    return redirect(f"/download/{output_filename1}/{output_filename2}")
                elif(response_DFO_cleaning == "Programme is hindered"):
                    print(f"Programme Task hindered in {end_time - start_time} seconds.")
                    return redirect(f"/download/{output_filename1}/{output_filename2}")
                elif(response_DFO_cleaning == 'Programme crashed'):
                    print(f"programme Task crashed in {end_time - start_time} seconds.")
                    return redirect(f"/download/{output_filename1}/{output_filename2}") 
            
                else:
                    return render_template("form.html")       
                

        except Exception as e:
            print("Something Went Wrong in uploading files !", e)
    return render_template('form.html')

  
    
#Declaring route for download panel
@ app.route("/download/<string:filename1>/<string:filename2>")
def download_file(filename1,filename2):
    """
    Args:
        filename : storing the name of the file which is generated
    """
    try:
        output_file_path1 = ("/static/media/output_files/") + filename1 + ".xlsx"
        output_file_path2 = ("/static/media/output_files/") + filename2 + ".xlsx"
        a = clear_folders()
        with open('log.txt', 'r') as f:
            log_contents = f.read()
            log_contents_newlines = log_contents.split('\n')
        data = {
            "path1": output_file_path1,
            "filename1": filename1,
            "path2":output_file_path2,
            "filename2":filename2,
            "log_contents":log_contents_newlines
        }
    except Exception as e:
        print("Something went wrong in download file route")
    return render_template("download.html", **data)


if __name__ == "__main__":
    """
    This statement allows You to Execute Code When the File Runs as a Script
    """
    app.run(host="localhost", debug=True, port=8888)
