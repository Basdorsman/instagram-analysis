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
import pandas as pd

def login(L, username, filename='login_session'):
    if not isinstance(L.test_login(),str):
        L.load_session_from_file(username, filename=filename)
    return L

def get_posts(L, myUsername, targetUsername, datetimeEarliest=False, datetimeLatest=False):
    L=login(L, myUsername)
    profile = instaloader.Profile.from_username(L.context, targetUsername)
    posts = [post for post in profile.get_posts()]
    if datetimeEarliest and datetimeLatest:
        posts_within_interval = [post for post in posts if (post.date_utc>datetimeEarliest and post.date_utc<datetimeLatest)]
    elif not datetimeEarliest:
        posts_within_interval = [post for post in posts if post.date_utc<datetimeLatest]
    return posts_within_interval

# get brands
input_data = pd.read_csv('./input_files/green_marketing_brands.csv')
n_brand = 0
n_brands = input_data.shape[0]
for brand in input_data['brand_account_name']:
    if not 'L' in locals():
        print('generating new instaloader instance...')
        L = instaloader.Instaloader()

    # retrieve posts
    n_brand += 1
    print(f'retrieving posts from {brand} ({n_brand}/{n_brands})...')
    
    username = brand
    myUsername = getMyUsername()
    #date_earliest = datetime(2019, 4, 30)
    date_latest = datetime(2022, 4, 30)
    posts = get_posts(L, myUsername, username, datetimeLatest=date_latest)
    
    # select subset of posts
    sample_size = 50
    posts_sampled = {}
    for post in posts[0:sample_size+1]:
        posts_sampled[' '.join(post.caption.split()[0:3])]={'post':post,'number_of_likes':post.likes,'number_of_comments':post.comments,'caption_hashtags':post.caption_hashtags,'date':post.date_utc.strftime("%d/%m/%y"),'caption':post.caption,'caption_length':len(post.caption)}
    
    # retrieve comments for each post
    n_post = 0
    for post in posts_sampled:
        n_post += 1
        print(f'retrieving comments from {brand} ({n_brand}/{n_brands}) from post {n_post}/{len(posts_sampled)}...')
        posts_sampled[post]['comments'] = []
        comments = posts_sampled[post]['post'].get_comments()
        if posts_sampled[post]['number_of_comments']>0:
            for comment in comments._data['edges']:
                posts_sampled[post]['comments'].append({'text':comment['node']['text'],'length':len(comment['node']['text'])})
        else:
            posts_sampled[post]['comments']='None'

    # save output data
    file_location = f'output_files/posts_{brand}.csv'
    print('saving output data in '+file_location)
    output_data = pd.DataFrame.from_dict(posts_sampled, orient='index')
    output_data.to_csv(file_location)
