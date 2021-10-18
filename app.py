import os
import redis
import random
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from azure.storage.blob import ContainerClient

load_dotenv()
app = FastAPI()

CONN_STRING = os.getenv('azure_storage_connectionstring')
CONTAINER = os.getenv('uploads_container_name')
HOST = os.getenv('redis_host')
PORT = os.getenv('redis_port')
PASSWORD = os.getenv('redis_password')
CONTAINER_CLIENT = ContainerClient.from_connection_string(CONN_STRING, CONTAINER)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'rar', 'zip', 'mp3', 'mp4', '3gp', 'avi', 'wav'])
conn = redis.Redis(host=HOST, port=PORT, password=PASSWORD)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class BlobAzureDownloader:
  def save_blob_locally(self,blob):
    bytes = CONTAINER_CLIENT.get_blob_client(blob).download_blob().readall()
 
    with open(blob, "wb") as file:
      file.write(bytes)
    return blob 
 
@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):

    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type is not allowed")

    blob_client = CONTAINER_CLIENT.get_blob_client(file.filename)
    blob_client.upload_blob(file.file)
    id_file = random.randint(1000,9999)
    conn.set(id_file, file.filename)
    return {"success":True,
            "details":{
            "fileName":file.filename,
            "fileType":file.content_type,
            "ID":id_file
            }
        }

@app.get('/download/{id_file}', response_class=FileResponse)
async def download_file(id_file):
    idf = conn.get(id_file)

    if not idf:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        blob_name = str(idf).split("'")[1]
        azure_blob_file_downloader = BlobAzureDownloader()
        file_downloaded = azure_blob_file_downloader.save_blob_locally(blob_name)
        conn.delete(id_file)
        CONTAINER_CLIENT.delete_blob(blob=blob_name)
        return blob_name

    except:
        return {"success":False,
                "details":"Something went wrong"}
