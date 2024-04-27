import praw
import requests
import os
import time

reddit_id = ''
secret = ''
agent = ''
subreddit = ''

def load_full_record(nome_file="record.txt"):
    record = []
    try:
        with open(nome_file, 'r') as file:
            for line in file:
                record.append(line.strip())
        print("Successfully loaded record")

    finally:
        return record

def update_full_record(record, nome_file="record.txt"):
    res = True
    try:
        with open(nome_file, 'w') as file:
            for line in record:
                file.write(line + '\n')

    except FileNotFoundError:
        res = False

    return res

def download(id, secret, agent, subreddit, num):
    reddit = praw.Reddit(client_id=id,
                         client_secret=secret,
                         user_agent=agent)

    subreddit_name = subreddit
    num_photos = num
    downloaded_count = 0
    limit = 1000

    checked = 0

    posts = reddit.subreddit(subreddit_name).hot(limit=limit)
    record = load_full_record()

    while downloaded_count < num_photos:
        count = 0
        if checked == limit:
            break
        for post in posts:
            count += 1
            if count >= checked:
                checked += 1

                if checked == limit:
                    break

                time.sleep(3)

                if post.url.endswith('.jpg') or post.url.endswith('.png') or post.url.endswith('.jpeg'):

                    name = os.path.basename(post.url).split('.')[0]
                    response = requests.get(post.url)

                    if not (name in record):
                        if response.status_code == 200:  # Check if the download was successful
                            with open(os.path.join('memes', 'posts', f"{name}.jpg"), 'wb') as f:
                                f.write(response.content)
                            with open(os.path.join('memes', 'captions', f"{name}.txt"), 'w', encoding='utf-8') as f:
                                f.write(post.title)
                            print(f'Downloaded {name}.jpg with caption {name}.txt')
                            record.append(name)
                            downloaded_count += 1

                            if downloaded_count >= num_photos:
                                break  # Stop the loop when desired number of images is downloaded
                    else:
                        print("Already posted image")

    if update_full_record(record):
        print("Record Updated")

    return downloaded_count




