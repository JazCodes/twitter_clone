from requests import Session
from flask import Flask
from flask import render_template
from flask import request

import sqlite3
import tweepy
from textblob import TextBlob


new_tweets =[]

app = Flask(__name__)

conn = sqlite3.connect('twitter.db')




conn.execute('''CREATE TABLE IF NOT EXISTS tweets(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	tweet TEXT)''')


conn.execute('''CREATE TABLE IF NOT EXISTS User(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT,
	password TEXT)''')


conn.commit()
conn.close()


@app.route('/')
def home_page():
    text = request.args.get('text')
    tweets = []
    if text is not None:
        tweets = get_tweets(text)
        print("These are tweets", tweets)

        return render_template('homepage.html', tweets=tweets)
    return render_template('homepage.html')


@app.route("/twitter_clone", methods=['POST', 'GET'])
def twitter_clone():
	if request.form:
		tweet = request.form['text']

	conn = sqlite3.connect('twitter.db')
	cur = conn.cursor()

	if request.method == 'POST':
		query = "INSERT INTO tweets(tweet) VALUES('{}')".format(tweet)
		
		cur.execute(query)
		conn.commit()

	if request.method == 'GET':
		cur.execute('''SELECT tweet FROM tweets''')

		rows = cur.fetchall()
		
		return render_template('twitter_clone.html', rows=rows)
	return render_template('twitter_clone.html')

	




@app.route("/register", methods=['GET'])
def register():
	return render_template('register.html')



@app.route("/login", methods=['GET', 'POST'])
def register():
	return render_template('register.html')



@app.route("/tweets_list", methods=['POST', 'GET'])
def tweet_dict():
    if request.form:
        new_tweets.append(request.form['text'])
        return render_template('tweets_list.html', new_tweets=new_tweets)
    return render_template('tweets_list.html')




@app.route("/tweets_file", methods=['POST', 'GET'])
def tweets_store():
    if request.method == 'POST':
        tweet = request.form['text']
        write_files(tweets)
        return render_template('tweets_file.html', store_tweets=store_tweets)
   


def write_tweets():
    with open('tweets.txt.', 'w') as f:
        return f.write()


def read_tweets():
    with open('tweets.txt', 'r') as f:
       return  f.read()

def get_tweets(searchitem):
    consumer_key = 'PXxPG9cU45j6NkvdCzNE79dG9'
    consumer_secret = 'ysVaagCxgaiWcjNbLh9QC7LwiiIWaQRWTcn1oJEQ6TtXn7GCqG'
    access_token = '1090376644412420096-VoD1NveDQKD9tHGGcpXblxBvruHOS7' 
    access_token_secret = 'FnvOg0HTzYlBqkAljCjmvWOlbPLUVjYmMWNXBXyOWAhxj'
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    public_tweets = api.search(searchitem)

    tweets = []

    for tweet in public_tweets:
        tweets.append(tweet.text)
        analysis = TextBlob(tweet.text)
    

    return analysis.sentiment , tweets

   


if __name__ == '__main__':
    app.run()