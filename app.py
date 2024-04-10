from flask import Flask, render_template, request, redirect, url_for
import string
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

urls = {}
url_visits = {}

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for i in range(6))
    return short_url

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    expiration_days = int(request.form.get('expiration_days', 0))

    short_url = generate_short_url()
    while short_url in urls:
        short_url = generate_short_url()

    expiration_date = None
    if expiration_days > 0:
        expiration_date = datetime.now() + timedelta(days=expiration_days)

    urls[short_url] = {'long_url': long_url, 'expiration_date': expiration_date}
    url_visits[short_url] = 0

    return render_template('shortened.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    if short_url in urls:
        url_visits[short_url] += 1
        return redirect(urls[short_url]['long_url'])
    else:
        return 'Short URL not found', 404

@app.route('/stats/<short_url>')
def stats(short_url):
    if short_url in urls:
        return render_template('stats.html', short_url=short_url, long_url=urls[short_url]['long_url'], visits=url_visits[short_url])
    else:
        return 'Short URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
