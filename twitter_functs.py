import random

import tweety

from utils import chance_to_do

# twitter data
username = ''
password = ''
test_username = ''
test_password = ''

# Connection Functions
def connect(is_test=False):
    if is_test:
        print("\n>>>>SUBROUTINE: Connecting to host with test account: ____")
        app = tweety.Twitter("session")
        app.sign_in(test_username, test_password)
        print(">>>>SUBROUTINE: Connecting to host with test account: DONE")
        return app

    print(">>>>SUBROUTINE: Connecting to host ____")
    app = tweety.Twitter("session")
    if chance_to_do(7):
        app.sign_in(username, password)
    else:
        app.start(username, password)
    print(">>>>SUBROUTINE: Connecting to host DONE")
    return app


# Content functions
def rand_tweet_id_from_home(number=1):
    res = []
    app = connect()
    tweets = app.get_home_timeline(random.randint(3, 5), random.randint(1, 3))
    for _ in range(number):
        res.append(random.choice(tweets).id)
    return res


def rand_tweet_id_from_a_comment(comment_id, number=1):
    res = []
    app = connect()
    comments = app.get_tweet_comments(comment_id, random.randint(2, 7), random.randint(1, 3))
    for _ in range(number):
        res.append(random.choice(comments).id)
    return res


def most_liked_comment(comment_id, number=1):
    res = []
    app = connect()
    print(f"\n>>>>SUBROUTINE: Getting comments from tweet {comment_id}: ____")
    threads = app.get_tweet_comments(comment_id, random.randint(1, 3), random.randint(1, 3))
    print(f">>>>SUBROUTINE: Getting comments from tweet {comment_id}: DONE")
    most_like = -1
    liked_comment = None
    print(f"\n>>>>SUBROUTINE: Analyzing likes of tweet {comment_id} comments: ____")
    for _ in range(number):
        for thread in threads:
            thread_comments = thread.expand()
            for comment in thread_comments:
                if comment not in res and len(comment.media) == 0:
                    if most_like < 0:
                        most_like = app.tweet_detail(comment.id).likes
                        like_buff = most_like
                        liked_comment = comment
                    else:
                        like_buff = app.tweet_detail(comment.id).likes

                    if most_like < like_buff:
                        most_like = like_buff
                        liked_comment = comment
        if liked_comment not in res:
            res.append(liked_comment)

    print(f">>>>SUBROUTINE: Analyzing likes of tweet {comment_id} comments: DONE")

    return res


# do not use unless infinite tweet limit
def most_liked_comment_conversation(comment_id, depth=2):
    res = []
    app = connect()
    threads = app.get_tweet_comments(comment_id, random.randint(1, 3), random.randint(1, 3))
    most_like = -1
    liked_comment = None
    d_count = 0
    while len(threads) != 0 and d_count < depth:
        for thread in threads:
            thread_comments = thread.expand()
            for comment in thread_comments:
                if len(app.tweet_detail(comment.id).media) != 0:
                    pass
                else:
                    if most_like < 0:
                        most_like = app.tweet_detail(comment.id).likes
                        like_buff = most_like
                        liked_comment = comment
                    else:
                        like_buff = app.tweet_detail(comment.id).likes

                    if most_like < like_buff:
                        most_like = like_buff
                        liked_comment = comment

        res.append(liked_comment)
        threads = app.get_tweet_comments(liked_comment.id, random.randint(1, 3), random.randint(1, 3))

    return liked_comment, res
