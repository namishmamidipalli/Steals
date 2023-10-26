from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Sample data for tracked events and event search results (you will replace this with a database)
tracked_events = []
event_search_results = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_events():
    location = request.form.get('location')
    date = request.form.get('date')
    print(date)
    url = f'https://api.seatgeek.com/2/venues?city={location}&client_id=MTUxNTQyNzZ8MTY5ODA3MjA1NS4yMDAxNzYy'
    req = requests.get(url)
    if req.status_code == 200:
        event_search_results = req.json()
        print(event_search_results)
        return render_template('search_results.html', event_search_results=event_search_results)
    else:
        return "Error: Unable to retrieve event data"

    # return render_template('index.html', event_search_results=req.json())

@app.route('/track_event/<event_id>')
def track_event(event_id):
    # Add the selected event to the tracked_events list (or your database)
    
    return redirect(url_for('index'))

@app.route('/set_threshold', methods=['POST'])
def set_price_threshold():
    event_id = request.form.get('event')
    threshold = float(request.form.get('threshold'))
    
    # Set the price threshold for the specified event
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
