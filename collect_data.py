#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 14:41:09 2022

@author: bas
"""
#https://instaloader.github.io/as-module.html

import instaloader
from datetime import datetime
from login import getMyUsername
import random
import pandas

def login(L, username, filename='login_session'):
    if not isinstance(L.test_login(),str):
        L.load_session_from_file(username, filename=filename)
    return L

def get_posts(L, myUsername, targetUsername, datetimeEarliest, datetimeLatest):
    L=login(L, myUsername)
    profile = instaloader.Profile.from_username(L.context, targetUsername)
    print('getting all posts...')
    posts = [post for post in profile.get_posts()]
    print('selecting posts...')
    posts_interval = [post for post in posts if (post.date_utc>datetimeEarliest and post.date_utc<datetimeLatest)]
    return posts_interval

if not 'L' in locals():
    L = instaloader.Instaloader()
if not 'posts' in locals():
    username = 'nyenrodebu'
    myUsername = getMyUsername()
    date_earliest = datetime(2020, 1, 1)
    date_latest = datetime(2022, 1, 1)
    posts = get_posts(L, myUsername, username, date_earliest, date_latest)

n = 78
posts_sampled = random.sample(posts, n)

posts_dict = {}
n_post = 0

for post in posts_sampled:
    n_post += 1
    print(f'post {n_post}/{n}')
    post_dict = {}
    post_dict['is_video'] = post.is_video
    post_dict['likes'] = post.likes
    post_dict['video_duration'] = post.video_duration
    post_dict['video_view_count'] = post.video_view_count
    post_dict['title'] = post.title
    post_dict['url'] = f'https://www.instagram.com/p/{post.shortcode}/'
    post_dict['mediacount'] = post.mediacount
    post_dict['caption'] = post.caption
    post_dict['date_utc'] = post.date_utc
    post_dict['comments'] = post.comments
    posts_dict[post.mediaid] = post_dict

df = pandas.DataFrame.from_dict(posts_dict, orient='index')
df.to_csv(f'output_files/username={username}_posts={n}.csv')
