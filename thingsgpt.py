import subprocess

from UnlimitedGPT import ChatGPT
from cleantext import clean
from twitter_functs import *

session_token = '' # of gpt
TWEET_CONVERSATION_ID = '' # default conversation


def get_gpt_comment(comment, user, no_emoji=True, conversation_id=TWEET_CONVERSATION_ID, hashtags=False):
    comment = clean(comment, no_emoji=True)
    prompt = f'Here is a tweet taken from twitter, from the user  @{user}: "{comment}". Imagine you as twitter page, what would you respond to him to make a joke and get most likes? Respond with only the words you would write in the tweet and although there is 140 characters limit you can use less.'
    api = ChatGPT(session_token=session_token, conversation_id=conversation_id, headless=False, verbose=True)

    try:
        message = api.send_message(
            prompt,
            input_mode="SLOW",
            input_delay=0.1
        )
        ret = message.response

        if no_emoji:
            ret = clean(message.response, no_emoji=no_emoji)
        if not hashtags:
            l = len(ret)
            for _ in range(l):
                if ret[_] == '#':
                    ret = ret[:_]
                    break
        return True, ret[1:-1]

    except:
        return False, None

def two_tweet_gpt(tweets: list, users: list, no_emoji=True, hashtags=False):
    first_user = users[0]
    second_user = users[1]
    first_tweet = tweets[0]
    second_tweet = tweets[1]

    prompt = f'Here is a tweet taken from twitter, from the user @{first_user} : "{first_tweet}". ' \
             f'Then the user @{second_user}  replied to @{first_user} with: "{second_tweet}". Imagine you as a Twitter page, ' \
             f'what would you respond to @{second_user} (remember to include his tag in the message) to make a joke and get most likes? ' \
             'Respond with only the words you would write in the tweet and although there is 140 characters limit you can use less.'

    api = ChatGPT(session_token=session_token, headless=False, verbose=True)

    try:
        message = api.send_message(
            prompt,
            input_mode="INSTANT",
            input_delay=0.1
        )
        ret = message.response
        subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE")

        if no_emoji:
            ret = clean(message.response, no_emoji=no_emoji)
        if not hashtags:
            l = len(ret)
            for _ in range(l):
                if ret[_] == '#':
                    ret = ret[:_]
                    break
        return True, ret[1:-1]

    except:
        return False, None

