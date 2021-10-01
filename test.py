import os
import yaml
from multiprocessing.pool import ThreadPool
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient

def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)

load = load_config()
conn_string = load['azure_storage_connectionstring']
container = load['uploads_container_name']

def upload(file, conn_string, container):
    container_client = ContainerClient.from_connection_string(conn_string, container)
    blob_client = container_client.get_blob_client(file.name)
    blob_client.upload_blob(file)
    print("Ok.")

blob_name = "ToDoList.txt"
container_client = ContainerClient.from_connection_string(conn_string, container)

 
class AzureBlobFileDownloader:
  def __init__(self):
    print("Intializing AzureBlobFileDownloader")
 
    # Initialize the connection to Azure storage account
    self.blob_service_client =  BlobServiceClient.from_connection_string(conn_string)
    self.my_container = self.blob_service_client.get_container_client(container)
 
  def save_blob_locally(self,blob):
    bytes = self.my_container.get_blob_client(blob).download_blob().readall()
 
    with open(blob, "wb") as file:
      file.write(bytes)
    return blob
 
azure_blob_file_downloader = AzureBlobFileDownloader()
azure_blob_file_downloader.save_blob_locally(blob_name)

print("downloaded")
container_client.delete_blob(blob=blob_name)
print("deleted")