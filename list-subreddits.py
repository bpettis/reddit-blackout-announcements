#! /usr/bin/python3
import requests, re
from datetime import datetime

# Set location and name of output file here
output = 'output/subreddits.txt'

def http_request(url):
    print(f"GET {url}")
    r = requests.get(url)
    if not r:
        print(f'Error when requesting {url}. Skipping.')
        return False

    return r.text


def parse(string):
    # Regex: <a href=\"\/r\/.*\/\">
    # Matches everything that would be found in a link such as: <a href="/r/iphone/">r/iphone</a>
    # I use this slightly more precise expression to avoid grabbing subreddit links from elsewhere on the page
    matches = re.findall(r"<a href=\"\/r\/.*\/\">", string)

    parsed_matches = []
    # Now we have to run through the list and cleanup - remove the "<a href="/r/" and "</a>" of each
    for subreddit in matches:
        start = subreddit.find("<a href=\"/r/") # find the start of the <a href=""> tag
        start += 12 # shift ahead 12 characters
        end = subreddit.find("\">") # find the end of the <a href=""> tag
        end -= 1 # shift back 1 character

        parsed_matches.append(subreddit[start:end])
    
    print(f'Found {str(len(parsed_matches))} subreddits')
    return parsed_matches

def main():

    # Create a list to store the subreddit names in
    subreddits = []

    # Make HTTP request to the specified pages
    urls = ["https://www.reddit.com/r/ModCoord/comments/1401qw5/incomplete_and_growing_list_of_participating/",
            "https://www.reddit.com/r/ModCoord/comments/143fzf6/incomplete_and_growing_list_of_participating/",
            "https://www.reddit.com/r/ModCoord/comments/146ffpb/incomplete_and_growing_list_of_participating/"]

    for url in urls:
        response = http_request(url)

        # Skip URL if the response failed
        if response == False:
            continue

        # Parse and get subreddit names. Add to the list
        subreddits.extend(parse(response))


    # Write into an output file
    print(f'There is a grand total of {str(len(subreddits))} subreddits')
    with open(output, 'w') as f:
        for line in subreddits:
            f.write(line)
            f.write('\n')

    print(f'Wrote to {output}')

if __name__ == "__main__":
    print('** list-subreddits.py | STARTED **')
    start_time = datetime.now()

    main()
    
    end_time = datetime.now()
    total_time = end_time - start_time
    print(f'Started at {start_time} and finished at {end_time}.\nTotal runtime was {total_time}')
    print('** list-subreddits.py | DONE **')