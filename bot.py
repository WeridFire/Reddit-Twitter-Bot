import time

import reddit
import os
from datetime import datetime

from thingsgpt import two_tweet_gpt
from utils import *
from twitter_functs import *

MAX_CYCLES_PER_DAY = 14
BASE_DELAY = 30 * 60

reddit_id = ''
secret = ''
agent = ''
subreddit = ''

def prefix():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]>> ")

# posting functs
def post_image_from_reddit(reply=None):
    if not os.path.isdir("memes/posts"):
        os.mkdir("memes/posts")
    if not os.path.isdir("memes/captions"):
        os.mkdir("memes/captions")
    memes = os.listdir("memes/posts")
    if len(memes) == 0:
        print("\n------------------------Initiating reddit download------------------------")
        count = reddit.download(reddit_id, secret, agent, subreddit, 50)
        print(prefix() + f"Successfully downloaded {count} images\n"
              + "--------------------------Ending reddit download--------------------------\n")

    captions = os.listdir("memes/captions")
    memes = os.listdir("memes/posts")

    with open(f"memes/captions/{captions[0]}") as f:
        try:
            caption = f.readline()
        except UnicodeDecodeError:
            caption = " "
            pass
    meme = f"memes/posts/{memes[0]}"

    try:
        app = connect()
    except:
        print(prefix() + "CANT POST")
        return False

    response = app.create_tweet(caption, meme, reply_to=reply)

    os.remove(f"memes/posts/{memes[0]}")
    os.remove(f"memes/captions/{captions[0]}")

    print(prefix() + "Successfully posted")
    print(prefix() + "Response id : " + str(response.id))
    return True

def retweet(number):
    try:
        app = connect()
    except:
        print(prefix() + "CANT CONNECT")
        return False

    tweets_id = rand_tweet_id_from_home(number)
    for idd in tweets_id:
        time.sleep(random.randint(1, 10))
        try:
            app.retweet_tweet(idd)
            if chance_to_do(68):
                app.like_tweet(idd)
            print(prefix() + "Tweet " + idd + " successfully retweeted")
        except:
            pass

    return True

def comment(number):
    try:
        app = connect()
    except:
        print(prefix() + "CANT CONNECT")
        return False

    tweets_id = rand_tweet_id_from_home(number)
    if not os.path.isdir("memes/captions"):
        os.mkdir("memes/captions")
        reddit.download(id, secret, agent, 'reactionpics', 70)

    for tw in tweets_id:
        time.sleep(random.randint(1, 10))
        meme = random.choice(os.listdir("memes/reactions"))
        try:
            if chance_to_do(37):
                response = app.create_tweet('', f'memes/reactions/{meme}', reply_to=tw)
            else:
                response = post_image_from_reddit(tw)
            print(prefix() + "Tweet " + tw + " successfully commented")
            print(prefix() + "With reponse id: " + str(response.id))
            if chance_to_do(99):
                app.like_tweet(tw)
        except:
            pass

    return True

def gpt_comment():
    try:
        app = connect()
    except:
        print(prefix() + "CANT CONNECT")
        return False

    timeline = app.get_home_timeline(random.randint(3, 5), random.randint(1, 3))
    c = 0

    for tweet in timeline:
        if len(tweet.media) == 0:
            c += 1
            liked = most_liked_comment(tweet.id)[0]
            tweets = [tweet.text, liked.text]
            users = [tweet.author.name, liked.author.name]
            valid, resp = two_tweet_gpt(tweets, users)

            if valid:
                response = app.create_tweet(resp, reply_to=liked.id)
                print(prefix() + "Tweet " + tweet.id + " successfully commented with GPT")
                print(prefix() + "With reponse id: " + str(response.id))

            break

    if c == 0:
        print(prefix() + "Found no tweet without media in timeline")
    return True


# LOOP
def botloop():
    print("-------------------------------BOT STARTING-------------------------------")

    yesterday = datetime.now().day
    last_hour = datetime.now().hour
    today_cycles_count = 0
    wait_till_next_cycle = random.randint(-600, 600)

    values = calc_today_values()
    today_numbers = get_today_numbers(values)
    max_posts, max_retweet, max_comments = today_numbers.get('posts'), today_numbers.get('retweets'), today_numbers.get('comments')

    today_posts, today_retweets, today_comments = 0, 0, 0
    this_hour_post, this_hour_comment, this_hour_retweet = False, False, False
    print("\n" + prefix() + "Today limits: ")
    print(today_numbers)
    print("\n" + prefix() + "Today values: ")
    print(values)
    print()

    while True:
        # START LOGIC

        print("-------------------------------LOOP STARTED-------------------------------")
        today_cycles_count += 1

        # reset orario dei flag
        if datetime.now().hour != last_hour:
            print(prefix() + "Resetting hourly parameters\n")
            this_hour_post, this_hour_comment, this_hour_retweet = False, False, False
            last_hour = datetime.now().hour

        # controllo del cambio giorno
        if datetime.now().day != yesterday or today_cycles_count == MAX_CYCLES_PER_DAY:
            print(prefix() + "Resetting daily parameters\n")
            today_cycles_count = 0
            yesterday = datetime.now().day
            values = calc_today_values()
            today_numbers = get_today_numbers(values)
            max_posts, max_retweet, max_comments = today_numbers.get('posts'), today_numbers.get('retweets'), today_numbers.get('comments')
            today_posts, today_retweets, today_comments = 0, 0, 0

        # CORE LOGIC

        # posting
        print("\n" + prefix() + "STARTING POST LOGIC")
        if today_posts < max_posts:
            if this_hour_post:
                if random.randint(1, 10) == 3:
                    if post_image_from_reddit():
                        today_posts += 1
                        this_hour_post = True
            else:
                if chance_to_do(50):
                    if post_image_from_reddit():
                        today_posts += 1
                        this_hour_post = True

        # retweeting
        print("\n" + prefix() + "STARTING RETWEET LOGIC")
        if today_retweets < max_retweet:
            if this_hour_retweet:
                if chance_to_do(10):
                    r = random.randint(1, 5)
                    if retweet(r):
                        today_retweets += r
                        this_hour_retweet = True
            else:
                if chance_to_do(20):
                    r = random.randint(1, 6)
                    if retweet(r):
                        today_retweets += r
                        this_hour_retweet = True

        # commenting
        print("\n" + prefix() + "STARTING COMMENT LOGIC")

        # GPT response change this -1 to the chance to comment
        if chance_to_do(-1):
            if gpt_comment():
                today_comments += 1
                this_hour_comment = True

        if today_comments < max_comments:
            if this_hour_comment:
                if chance_to_do(40):
                    r = random.randint(1, 5)
                    if comment(r):
                        today_comments += r
                        this_hour_comment = True
            else:
                if chance_to_do(70):
                    r = random.randint(1, 6)
                    if comment(r):
                        today_comments += r
                        this_hour_comment = True

        # END LOGIC

        # aspetta prima del prox giro
        print("--------------------------------LOOP ENDED--------------------------------")
        print(prefix() + f"Will try to cycle again in {int((BASE_DELAY + wait_till_next_cycle) / 60 / 60)} hours and {int((BASE_DELAY + wait_till_next_cycle) / 60) % 60} minutes\n\n")
        time.sleep(BASE_DELAY + wait_till_next_cycle)
        wait_till_next_cycle = random.randint(-600, 600)

        # 4 su 5 possibilita di connettersi
        if random.randint(1, 5) == 3:
            print(prefix() + f"Will sleep again for {int((BASE_DELAY + wait_till_next_cycle) / 60 / 60)} hours and {int((BASE_DELAY + wait_till_next_cycle) / 60) % 60} minutes\n\n")
            time.sleep(BASE_DELAY + wait_till_next_cycle)
            wait_till_next_cycle = random.randint(-600, 600)
            today_cycles_count += 1


if __name__ == '__main__':
    botloop()
