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

---

# Data Access

If you're just interested in taking a look at the content that I scraped, I will be making that available: <somewhere, check back later>