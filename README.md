# reddit-blackout preservation

Starting June 12, 2023, [many Reddit communities](https://www.reddit.com/r/ModCoord/comments/1401qw5/incomplete_and_growing_list_of_participating) (subreddits) will be "going dark" - or changing to private mode - as a protest in response to Reddit's plans to [change its API access policies and fee structure](https://www.reddit.com/r/reddit/comments/12qwagm/an_update_regarding_reddits_api/). Supporters of the protest criticize the planned changes for being [prohibitively expensive for 3rd party apps](https://www.reddit.com/r/apolloapp/comments/13ws4w3/had_a_call_with_reddit_to_discuss_pricing_bad/). Beyond 3rd party apps, there is significant concern that the API changes are a move by the platform to increase monetization, degrade the user experience, and eventually kill off other custom features such as the old.reddit.com interface, the Reddit Enhancement Suite browser extension, and more. Additionally, there are concerns that the API changes will impede the ability of subreddit moderators (who are all unpaid users) to access tools to keep their communities on-topic and free of spam.

I am a Reddit user, but I am also an [internet researcher](https://benpettis.com/research). I'm working on a dissertation about how people are constructed as "Users" by platforms, and how this includes and excludes certain groups from assumptions of who the internet is "for." In one section of my dissertation, I am examining moderators and volunteer fact-checkers—users who are in an "elevated" role over other users, but still not employees of the platform. How do they understand their own role? How do they make sense of the power they have over other users? And how do they influence what a platform "is" - even beyond what its corporate owners imagine? So when I learned about the Reddit Blackout, I knew it would be a great opportunity to see these questions I'm thinking about play out in real time.

To that end, I have come up with some ways to preserve content related to the blackout. These scripts will pull the [list of participating subreddits](https://www.reddit.com/r/ModCoord/comments/1401qw5/incomplete_and_growing_list_of_participating/?sort=top) that has been collated in the /r/ModCoord subreddit. Then, using that list, another script looks in those subreddits for stickied announcement posts - e.g. how a subreddit's moderators are explaining their decision to their community.

---

documentation forthcoming...

## Installation

I've created this script for my own research purposes, and so I can't necessarily guarantee that it will work in _your_ environment. These notes are provided as reference, but I fully recognize that how I have things set up may not be best practices.

### Dependencies

- [PRAW (Python Reddit API Wrapper)](https://github.com/praw-dev/praw)

### Install packages:

`pip install -r requirements.txt`

## Configuration

### Google Cloud

The `get-stickies.py` script is set up to save the output data into a Google Cloud Storage Bucket. This can be handy for if you are planning on publicizing the data. You'll need to do a bit of setup.

- You will need to create a Google Cloud project (or use an existing one)
- You will need to create a Storage Bucket (with region/redundancy/privacy settings that fit your needs). 
- You will need to create a Service Account which has permission to write files into that bucket. 
- You will need to download a key for that service account in JSON format

The information of the above should be placed in a `.env` file in the root directory:

```
GCS_BUCKET_NAME='gcs_bucket_name_here'
GCP_PROJECT='project_name_here'
GOOGLE_APPLICATION_CREDENTIALS='keys/path/to/gcs-credentials.json'
```

If you want to disable Google Cloud Storage, just change `use_gcs = True` to `use_gcs = False` toward the top of the script 

#### Cloud Logging

The `get stickies.py` scripy can also log information via Google Cloud logging. If you want to use this option, the service account that you use will need to have permission to write logs as well. 

Set the name of the log by adding a line in the `.env` file in the root directory:

```
LOG_ID='reddit-blackout-announcements'
```

If you want to disable Google Cloud Storage, just change `use_cloud_logging = True` to `use_cloud_logging = False` toward the top of the script 

### Google Cloud Authentication

You will need to save your service account keys as a JSON file and place it in a place that the script can find. Set this file path using the `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### Reddit Authentication:

You'll need to have a Reddit account and generate Oauth2 credentials in order to authenticate to the Reddit API. Yes, this is a bit ironic given that this whole project is emerging in response to API changes.

Head to [https://www.reddit.com/prefs/apps/](https://www.reddit.com/prefs/apps/) to create an app.

### `praw.ini`

Instead of placing Reddit credentials directly in the script, I use an external [`praw.ini` file](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html#praw-ini) to save configuration information. Put your credentials there, and not in the script and/or repo

Example praw.ini:

```
[app_name]
client_id=CLIENT_ID_HERE
client_secret=CLIENT_SECRET_HERE
user_agent=app_name_here:v0.0.1 (by /u/username_here)
```

## Usage

### `list-subreddits.py`

This script looks at three reddit posts and grabs the list of participating subreddits:

- https://www.reddit.com/r/ModCoord/comments/1401qw5/incomplete_and_growing_list_of_participating/
- https://www.reddit.com/r/ModCoord/comments/143fzf6/incomplete_and_growing_list_of_participating/
- https://www.reddit.com/r/ModCoord/comments/146ffpb/incomplete_and_growing_list_of_participating/

It uses the `requests` library to get the HTTP response body. Then it uses `re` to search for links that look like `<a href="/r/iphone/">r/iphone</a>`, e.g. what the list looks like in the post. Next it's just a bit of string cleanup and then writing to an output file.

This script does _not_ use the Reddit API at all. It's just basic HTTP requests.

Set the location and name of the output file at the top of the script

```
# Set location and name of output file here
output = 'output/subreddits.txt'
```

### `get-stickies.py`

This is a slightly modified version of the script that I had previously written to preserve other subreddit info: https://github.com/bpettis/reddit-scrape_mods-rules

It will create a CSV file for each of the listed subreddits. Each row of the CSV represents a stickied post. There currently isn't any logic to try and detect which post is the one announcing the blackout. I'm just saving all of them.

Set the list of input subreddits in `input_list = 'output/subreddits.txt'` at the top of the script

That file should be the one created by `list-subreddits.py`

**NOTE*: This script is only going to get the stickied posts from each of the specified subreddits. If the subreddit doesn't have a sticky about their participation in the blackout, it won't be fully represented here. The script will raise a `prawcore.exceptions.NotFound` exception and continue on. This means you'll get some CSV files that look incomplete.

---

# Data Access

If you're just interested in taking a look at the content that I scraped, I will be making that available:

- List of subreddits: https://storage.googleapis.com/reddit-blackout-announcements/subreddits.txt
- All stickied posts: https://storage.googleapis.com/reddit-blackout-announcements/

The above URL for all stickied posts will give you an XML file of all contents in the storage bucket. Each `<Contents>` element represents a file:

```
<Contents>
    <Key>2023-06-11/stickies/funny.csv</Key>
    <Generation>1686507430668697</Generation>
    <MetaGeneration>1</MetaGeneration>
    <LastModified>2023-06-11T18:17:10.671Z</LastModified>
    <ETag>"ceab42346825f636b26ec470b417aa8d"</ETag>
    <Size>2620</Size>
</Contents>
```

You can use the `<Key>` to build the URL like this:  `https://storage.googleapis.com/reddit-blackout-announcements` + `<Key>`

For example: [`https://storage.googleapis.com/reddit-blackout-announcements/2023-06-11/stickies/funny.csv`](https://storage.googleapis.com/reddit-blackout-announcements/2023-06-11/stickies/funny.csv)