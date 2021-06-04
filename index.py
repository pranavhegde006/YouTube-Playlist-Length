from flask import Flask, render_template, request
from main import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/form', methods=['POST'])
def form_post():
    link = request.form['link']
    time = playlistLength(link)
    time = f"There are a total of {time['n']} videos in this playlist. \nIt would take you {time['h']} hours, {time['m']} minutes and {time['s']} seconds to watch the complete playlist."
    return render_template('time.html', time = time)

if __name__ == '__main__':
    app.run(debug=True)
