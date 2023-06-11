#! /usr/bin/python3

import praw, prawcore, csv, os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
from google.cloud import storage
import google.cloud.logging

# set up some global variables:
reddit = praw.Reddit("modscraper")
input_list = 'output/subreddits.txt'

# enable/disable google cloud storage
use_gcs = True

# enable/disbale Google Cloud Logging
use_cloud_logging = True

# load environment variables
load_dotenv(find_dotenv())
bucket_name = os.environ.get("GCS_BUCKET_NAME")
project_id = os.environ.get("GCP_PROJECT")
log_name = os.environ.get("LOG_ID")


# Set up Google cloud logging:
log_client = google.cloud.logging.Client(project=project_id)
logger = log_client.logger(name=log_name)

def write_log(payload):
    # takes an input dictionary and writes it to cloud logging - but only after checking if we want to log or not
    if use_cloud_logging:
        write_log(payload)
    else:
        return

def get_subreddits():
    subreddit_list = []
    with open(input_list, "r") as file:
        data = file.read()
        subreddit_list = data.split("\n")
    return subreddit_list

def csv_setup(sub):
    today = datetime.today().strftime('%Y-%m-%d')
    Path("output/" + today + "/stickies").mkdir(parents=True, exist_ok=True)
    filename = "output/" + today + "/stickies/" + sub + ".csv"
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'created', 'author', 'title', 'url', 'text'])
    print(f'Created {filename} for /r/{sub}')
    return filename

def get_stickies(sub, output):
    # Specify which sticky to return. 1 appears at the top (default: 1).
    # https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.sticky
    counter = 1
    lastid = ''
    while counter > 0:
        # Depreciation Notice
        # DeprecationWarning: Positional arguments for 'Subreddit.sticky' will no longer be supported in PRAW 8
        # Call this function with 'number' as a keyword argument.
        print(f'Sticky #{str(counter)}')
        try:
            sticky = reddit.subreddit(sub).sticky(counter)

            if (sticky.id == lastid):
                break
            else:
                lastid = sticky.id

            row = [sticky.id, sticky.created_utc, sticky.author.name, sticky.title, sticky.url, sticky.selftext]
            with open(output, 'a') as file:
                writer = csv.writer(file)
                writer.writerow(row)
            counter += 1
        except prawcore.exceptions.NotFound:
            print('Not found')
            write_log(
                {
                    "message": "Not Found (prawcore.exceptions.NotFound)",
                    "severity": "WARNING",
                    "subreddit": sub,
                    "counter": str(counter),
                    "output": output
                })
            break
        except Exception as e:
            print(f'Got some other error: {type(e).__name__}')
            break

    print(f'Saved {str(counter - 1)} stickies from /r/{sub} to {output}')

    # if > 0 stickies saved AND if gcs == True, upload the file to GCS 
    if (counter > 1) and (use_gcs == True):
        write_log(
        {
            "message": "Uploading file to GCS",
            "severity": "INFO",
            "count": str(counter - 1),
            "output": output,
            "subreddit": sub,
            "target-metadata": "stickies"
        })
        blob_name = output[7:] # slice the "output/" at the beginning of the filename to be used as the blob name in Google Cloud
        try:
            upload_blob(output, blob_name)
        except Exception as e:
            write_log(
                {
                    "message": "Exception when Uploading to GCS",
                    "severity": "WARNING",
                    "target-metadata": "stickies",
                    "type": str(type(e)),
                    "exception": str(e)
                })
    else:
        write_log(
        {
            "message": "Not Uploading to GCS",
            "severity": "INFO",
            "subreddit": sub,
            "target-metadata": "stickies",
            "count": str(counter - 1),
            "output": output
        })

def upload_blob(filename, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client(project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(filename)

    print(
        f"{destination_blob_name} was uploaded to {bucket_name}."
    )
    write_log(
        {
            "message": "File was uploaded",
            "target-metadata": "stickies",
            "severity": "INFO",
            "destination-name": destination_blob_name,
            "bucket-name": bucket_name
        })

def main():
    
    write_log(
        {
            "message": "** get_stickies.py | Retrieving Stickied Posts **",
            "severity": "NOTICE",
            "target-metadata": "stickies"
        })

    subreddit_list = get_subreddits()
    for sub in subreddit_list:
        output = csv_setup(sub)
        get_stickies(sub, output)

    write_log(
        {
            "message": "** get_stickies.py | DONE **",
            "target-metadata": "stickies",
            "severity": "NOTICE"
        })

if __name__ == "__main__":
    print('** get_stickies.py | Retrieving Stickied Posts **')
    start_time = datetime.now()
    
    main()

    end_time = datetime.now()
    total_time = end_time - start_time
    print(f'Started at {start_time} and finished at {end_time}.\nTotal runtime was {total_time}')
    print('** get_stickies.py | DONE **')