from requests import Session
from flask import Flask, render_template, request, make_response, redirect
import sqlite3
import tweepy
from textblob import TextBlob


new_tweets =[]

app = Flask(__name__)

conn = sqlite3.connect('twitter.db')




conn.execute('''CREATE TABLE IF NOT EXISTS tweets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet TEXT,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES user(id) )''')


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
    username = request.cookies.get('userID')
    user_id = cur.execute("SELECT id FROM User WHERE username=?", (username,)).fetchone()[0]
    print(user_id)

    if request.method == 'POST':
        query = "INSERT INTO tweets(tweet, user_id) VALUES('{}', {})".format(tweet, user_id)
        
        cur.execute(query)
        conn.commit()

    cur.execute("SELECT * FROM tweets where user_id=?", (user_id,))

    rows = cur.fetchall()

    
    return render_template('twitter_clone.html', rows=rows)


 # @app.route("/logout")
 # return render_template('logout.html')

@app.route("/register", methods=['GET' , 'POST'])
def register():
        #insert into database
    conn = sqlite3.connect('twitter.db')
    cur = conn.cursor()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "INSERT INTO User(username, password) VALUES('{}', '{}')".format(username, password)
        

        cur.execute(query)
        conn.commit()

        resp = make_response(redirect('/twitter_clone', 302))
        resp.set_cookie('userID', username)

        return resp

    return render_template('register.html')



@app.route("/login", methods=['GET' ,'POST'])
def login():
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()

    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password'] 
        login_user = user(username,password,c)
        conn.commit()
        resp = make_response(redirect('/twitter_clone'))
        resp.set_cookie('userID', username)

        return resp

    return render_template('login.html')


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