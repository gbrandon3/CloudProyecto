import sys
from google.cloud import storage
import app_settings
import os
from tempfile import SpooledTemporaryFile


class GCPStorage:
    def upload_blob(source_file, destination_blob_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(app_settings.GCP_BUBKET_NAME)
        blob = bucket.blob(destination_blob_name)
        source_file.seek(0)
        blob.upload_from_string(source_file.read())
        print(
            f"File {source_file} uploaded to {destination_blob_name}."
        )

    def upload_file(source_file, destination_blob_name):
        print("Updload " + source_file + " to " + destination_blob_name)
        storage_client = storage.Client()
        bucket = storage_client.bucket(app_settings.GCP_BUBKET_NAME)
        blob = bucket.blob(destination_blob_name)
        source_file.seek(0)
        blob.upload_from_file(source_file)
        print(
            f"File {source_file} uploaded to {destination_blob_name}."
        )
       
    def download_blob(remote_blob_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(app_settings.GCP_BUBKET_NAME)
        blob = bucket.blob(remote_blob_name)
        contents = blob.download_as_string()
        return contents
       
    def download_file(remote_blob_name, local_file_name):
        print(local_file_name)
        storage_client = storage.Client()
        bucket = storage_client.bucket(app_settings.GCP_BUBKET_NAME)
        blob = bucket.blob(remote_blob_name)
        blob.download_to_filename(local_file_name)
        return
       
