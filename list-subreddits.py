#! /usr/bin/python3
from datetime import datetime

def main():
    print('Hello world!')

    # Set up praw connection


    # HTTP request to the specified page


    # Parse and get subreddit names


    # Write into an output file

if __name__ == "__main__":
    print('** list-subreddits.py | STARTED **')
    start_time = datetime.now()

    main()
    
    end_time = datetime.now()
    total_time = end_time - start_time
    print(f'Started at {start_time} and finished at {end_time}.\nTotal runtime was {total_time}')
    print('** list-subreddits.py | DONE **')