import random

# Load Functions
def calc_today_values():
    values: dict = {
        'averageTweetsPerDay': 60,
        'distraction_averageTweetsPerDay': 25,

        'postsPercentage': 30,
        'distraction_postsPercentage': 3,

        'reTweetPercentage': 35,
        'distraction_reTweetPercentage': 5,
        'reTweetLikePercentage': 55,
        'distraction_reTweetLikePercentage': 15,

        'commentsPercentage': 25,
        'distraction_commentsPercentage': 7,

        'likeHomeTweetPercentage': 25,
        'distraction_likeHomeTweetPercentage': 5
    }
    file = open('config.txt', 'r').readlines()
    for line in file:
        cont = line.split(' ')
        values[cont[0][:-1]] = int(cont[1])

    return values


def get_today_total_tweet_number(values: dict):
    num_post = values.get('averageTweetsPerDay')
    distraction = values.get('distraction_averageTweetsPerDay')
    return calc_with_distraction(num_post, distraction)


def get_today_post_number(values: dict, post_number):
    post_percentage = values.get('postsPercentage')
    distraction = values.get('distraction_postsPercentage')
    return calc_int_percentage_with_distraction(post_number, post_percentage, distraction)


def get_today_retweet_number(values: dict, post_number):
    retweet_percentage = values.get('reTweetPercentage')
    distraction = values.get('distraction_reTweetPercentage')
    return calc_int_percentage_with_distraction(post_number, retweet_percentage, distraction)


def get_today_comment_number(values: dict, post_number):
    comment_percentage = values.get('commentsPercentage')
    distraction = values.get('distraction_commentsPercentage')
    return calc_int_percentage_with_distraction(post_number, comment_percentage, distraction)


def get_today_numbers(values: dict):
    total = get_today_total_tweet_number(values)
    posts = get_today_post_number(values, total)
    retweets = get_today_retweet_number(values, total)
    comments = get_today_comment_number(values, total)
    return {'posts': posts, 'retweets': retweets, 'comments': comments}


# Randomize Functions
def chance_to_do(percentage):
    return random.randint(0, 99) < percentage


def calc_with_distraction(num, distraction):
    return num + random.randint(distraction*(-1), distraction)


def calc_int_percentage_with_distraction(total, percentage, distraction):
    res = total * percentage // 100
    return calc_with_distraction(res, distraction)