import io
import os
import yaml
import random
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_file, after_this_request
from azure.storage.blob import BlobServiceClient, ContainerClient
 
app = Flask(__name__)

#Reading the yaml file
def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)

load = load_config()
conn_string = load['azure_storage_connectionstring']
container = load['uploads_container_name']
container_client = ContainerClient.from_connection_string(conn_string, container)
mongo_client = load['mongodb_client']

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'rar', 'zip', 'gzip'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16 MEGABYTES
db = MongoClient(mongo_client).thingsTD.file_id

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AzureBlobFileDownloader:
  def __init__(self):
    # Initialize the connection to Azure storage account
    self.blob_service_client =  BlobServiceClient.from_connection_string(conn_string)
    self.my_container = self.blob_service_client.get_container_client(container)
 
  def save_blob_locally(self,blob):
    bytes = self.my_container.get_blob_client(blob).download_blob().readall()
 
    with open(blob, "wb") as file:
      file.write(bytes)
    return blob

# ERROR HANDLING
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'Error' : 'Are you sure about that?'})

@app.errorhandler(413)
def not_found_error(error):
    return jsonify({'Error' : 'Booty so big, lawd! Have mercy'})

# TWO ENDPOINTS (UPLOAD AND DOWNLOAD/ID)  
@app.route('/upload', methods=['POST'])
def upload_file():
    
    if 'total_files' not in request.files:
        return jsonify({'message' : 'No file part in the request'}),400
    
    for file in request.files.getlist('total_files'):      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload(file, conn_string, container)
            idf = random.randint(1000,10000)
            status = db.file_id.insert_one({
                "_id" : idf,
                "name" : filename
            })
            return jsonify({f'ID {idf}' : 'File(s) successfully uploaded'}),201
        else:
            return jsonify({(file.filename) : 'File type is not allowed'}),415

def upload(file, conn_string, container):
    blob_client = container_client.get_blob_client(secure_filename(file.filename))
    blob_client.upload_blob(file)

@app.route('/download/<idf>')
def download_file(idf):
    idf_search = db.file_id.find_one({"_id":int(idf)})

    @after_this_request
    def removing_file(response):
        try:
            db.file_id.delete_one({"_id":int(idf)})
            container_client.delete_blob(blob=blob_name)
            file_path = os.path.dirname(os.path.abspath(__file__))
            os.remove(file_path+"/"+blob_name)
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    if idf_search:
        blob_name = idf_search['name']
        azure_blob_file_downloader = AzureBlobFileDownloader()
        file_downloaded = azure_blob_file_downloader.save_blob_locally(blob_name)
        return send_file(file_downloaded)

    else:
        return jsonify({'Error':'ID file not Found'}),404

if __name__ == "__main__":
    app.run(host='0.0.0.0')