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
    posts = [post for post in profile.get_posts()]
    posts_interval = [post for post in posts if (post.date_utc>datetimeEarliest and post.date_utc<datetimeLatest)]
    return posts_interval

if not 'L' in locals():
    L = instaloader.Instaloader()
if not 'posts' in locals():
    username = 'uva_amsterdam'
    myUsername = getMyUsername()
    date_earliest = datetime(2020, 9, 1)
    date_latest = datetime(2021, 7, 31)
    posts = get_posts(L, myUsername, username, date_earliest, date_latest)

n = 80
posts_sampled = random.sample(posts, n)

posts_dict = {}


for post in posts_sampled:
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
df.to_csv(f'data_for_{username}_posts={n}.csv')
