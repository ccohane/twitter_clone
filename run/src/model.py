#!/usr/bin/env python3
from orm import Database
import time
import uuid
import copy


def create_table():
    with Database() as db:
        db.c.execute('''CREATE TABLE IF NOT EXISTS users(
                        pk INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_names VARCHAR,
                        password VARCHAR);''')

        db.c.execute('''CREATE TABLE IF NOT EXISTS friends(
                        pk INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_names VARCHAR,
                        friends VARCHAR);''')

        db.c.execute('''CREATE TABLE IF NOT EXISTS tweets(
                        pk INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_names VARCHAR,
                        allTweets VARCHAR,
                        date DATE,
                        unix FLOAT);''')

def create_user(user_name , password):

    with Database() as db:
        create_table()
        user_name_taken = check_user_exist(user_name)
        if user_name_taken==False:
            sql='''INSERT INTO users(user_names,password) 
                            Values(?,?);'''
            db.c.execute(sql, (user_name, password))
            return True
        else:
            return False

def check_user_exist(user_name):
    with Database() as db:
        db.c.execute('''SELECT * FROM users WHERE user_names='{}';'''.format(user_name))
        result=db.c.fetchone()

        if result:
            return True
        else:
            return False

def check_user(user_name, password):
    with Database() as db:
        db.c.execute('''SELECT * FROM users WHERE user_names='{}'
                        AND password='{}';'''.format(user_name, password))
        result=db.c.fetchone()

        if result:
            return True
        else:
            return False

def update_tweets(user_name, tweet,date,unix):
    with Database() as db:
        sql='''INSERT INTO tweets(user_names,allTweets,date,unix)
                        VALUES(?,?,?,?);'''
        db.c.execute(sql,(user_name,tweet,date,unix))

def get_all_tweets():
    with Database() as db:
        db.c.execute('''SELECT * FROM tweets;''')
        tweets=db.c.fetchall()
        return(tweets)

def get_profile_tweets(user_name):
    with Database() as db:
        db.c.execute('''SELECT * FROM tweets WHERE user_names='{}';'''.format(user_name))
        tweets=db.c.fetchall()
        return(tweets)

def find_tweet(pk):
    with Database() as db:
        db.c.execute('''SELECT allTweets FROM tweets where pk={};'''.format(pk))
        tweets=db.c.fetchone()
        return(tweets)