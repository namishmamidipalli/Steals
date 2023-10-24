from flask import Flask, render_template, abort
app = Flask(__name__)
OPTIONS = {
    'eventfinder': {
        'name': 'Find Events',
        'category': '',
        # 'price': 699,
    },
    'trackedevents': {
        'name': "Events you've been tracking",
        'category': '',
        # 'price': 649,
    }
}
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', options=OPTIONS)
@app.route('/option/<key>')
def option(key):
    option = OPTIONS.get(key)
    if not option:
        abort(404)
    return render_template('options.html', option=option)