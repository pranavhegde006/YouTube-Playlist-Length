from flask import Flask, render_template, request, send_from_directory
from main import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def form_post():
    link = request.form['link']
    speed = float(request.form['speed'])
    time1x = playlistLength(link)
    if time1x == -1:
        return render_template('404.html')
    time = faster(time1x, speed)
    number = time['n']
    time = f"{time['h']} hours, {format(time['m'], '02d')} minutes and {format(time['s'], '02d')} seconds"
    return render_template('index.html', time = time, number = number, speed = speed)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/youtube.svg') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'youtube.svg', mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run()
