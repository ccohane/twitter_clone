#!usr/bin/env python3

from flask import Flask, render_template, request, redirect, session, jsonify, url_for, escape
import model, datetime, time

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Qhgvf8z\n\xec]/'

#----------------------------------------------------------------------------------------
@app.route('/go', methods=['GET'])
def start():
    if request.method == 'GET':
        return render_template('go.html')

@app.route('/')
def index():
    if 'username' in session:
        return redirect("/dashboard")
    return redirect("/go")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']
        suc=model.create_user(username,password)
        if suc:
            return redirect(url_for('index'))
        else:
            return render_template('register.html', message='Username Taken')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        session['username'] = request.form['username']
        if model.check_user(username,password):
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Login error')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/go')

@app.route('/retweet',methods=['GET','POST'])
def retweet():
    if request.method == 'POST':
        user_name='%s' % escape(session['username'])
        date=datetime.datetime.now()
        unix= time.time()
        pk = request.form['arb_guid']
        tweet = model.find_tweet(pk)
        tweet=str(tweet[0])
        model.update_tweets(user_name,tweet,date,unix)
        tweets = model.get_all_tweets()
        tweets.sort(reverse=True)
        return redirect(url_for('dashboard', Username=user_name, newsFeed=tweets))

@app.route('/retweeter',methods=['GET','POST'])
def retweeter():
    if request.method == 'POST':
        user_name='%s' % escape(session['username'])
        date=datetime.datetime.now()
        unix= time.time()
        pk = request.form['arb_guid']
        tweet = model.find_tweet(pk)
        tweet=str(tweet[0])
        model.update_tweets(user_name,tweet,date,unix)
        tweets = model.get_all_tweets()
        tweets.sort(reverse=True)
        return redirect(url_for('profile', Username=user_name, newsFeed=tweets))

@app.route("/dashboard", methods = ['GET','POST'])
def dashboard():
    if request.method == 'GET':
        user_name='%s' % escape(session['username'])
        tweets = model.get_all_tweets()
        tweets.sort(reverse=True)
        return render_template('dashboard.html', Username=user_name ,newsFeed=tweets)
    else:
        user_name='%s' % escape(session['username'])
        date=datetime.datetime.now()
        unix= time.time()
        tweet= request.form['tweet']
        model.update_tweets(user_name,tweet,date,unix)
        tweets = model.get_all_tweets()
        tweets.sort(reverse=True)
        return render_template('dashboard.html', Username=user_name, newsFeed=tweets)


@app.route("/profile", methods = ['GET','POST'])
def profile():
    if request.method == 'GET':
        user_name='%s' % escape(session['username'])
        tweets = model.get_profile_tweets(user_name)
        tweets.sort(reverse=True)
        return render_template('profile.html', Username=user_name, newsFeed=tweets)
    else:
        user_name='%s' % escape(session['username'])
        date=datetime.datetime.now()
        unix= time.time()
        tweet= request.form['tweet']
        model.update_tweets(user_name,tweet,date,unix)
        tweets = model.get_profile_tweets(user_name)
        tweets.sort(reverse=True)
        return render_template('profile.html', Username=user_name, newsFeed=tweets)

if __name__=="__main__":
    import os
    os.system('clear')
    print("Warning")
    print("This server settings are hard coding to values associated with a local or staging environment and ar unfit for production")
    #FIXME change the following server setings from 127.1 to 0.0.0.0
    app.run(host="127.1", port="5000", debug=True)
    #app.run(debug=True)
    #app.run(host="0.0.0.0" ,port="1996",debug=True)
