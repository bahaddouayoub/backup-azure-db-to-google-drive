#!/usr/bin/env python3

import datetime
import subprocess
from googleapiclient.discovery import build
from azure.mgmt.rdbms.postgresql.models import *
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from dotenv import load_dotenv

# Variables
FILE_PATH = "/PATH_TO_STORE_BACKUPS/backup_data/" # Replace with the desired path to store backups
BACKUP_FILE = os.path.join(FILE_PATH, "file_name_{}.sql".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
os.environ['BACKUP_FILE'] = BACKUP_FILE


os.environ['PGPASSFILE'] = '~/.pgpass'


cmd = "PGPASSFILE=~/.pgpass pg_dump --host=your_host--username=username --dbname=db --file={}".format(BACKUP_FILE)
subprocess.run(cmd, shell=True, check=True)

# connect to google drive and upload file
gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("/PATH_TO_YOUR_CDENTIALS/mycredentials.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("/PATH_TO_YOUR_CDENTIALS/mycredentials.txt")

drive = GoogleDrive(gauth)
gfile = drive.CreateFile({'parents': [{'id': 'folder_id'}]})