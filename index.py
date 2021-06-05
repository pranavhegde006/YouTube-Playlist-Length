from flask import Flask, render_template, request, send_from_directory
from main import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def form_post():
    link = request.form['link']
    time = playlistLength(link)
    number = time['n']
    time = f"{time['h']} hours, {format(time['m'], '02d')} minutes and {format(time['s'], '02d')} seconds"
    return render_template('index.html', time = time)



@app.route('/youtube.svg') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'youtube.svg', mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)
