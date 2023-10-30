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
    print(location)
    date = request.form.get('date')
    performer = request.form.get('performer')
    # print(master_performer_list)
    psplit = performer.split()
    performerapi = ''
    for i in range(len(psplit)):
        performerapi += psplit[i]
        if i + 1 == len(psplit):
            break
        performerapi += '-'


    url = f'https://api.seatgeek.com/2/events?performers.slug={performerapi}&venue.city={location}&client_id=MTUxNTQyNzZ8MTY5ODA3MjA1NS4yMDAxNzYy'
    req = requests.get(url)

    #i need to figure out a way to save the postal code here so that i can use it as a parameter for reccomendations if my search doesnt return anything
    if req.status_code == 200:
        event_search_results = req.json()
        # print(event_search_results)
        total_events = event_search_results.get('meta', {}).get('total', 0)

        if total_events != 0:
            return render_template('search_results.html', event_search_results=event_search_results)
        else:
            performer_info = f'https://api.seatgeek.com/2/events?performers.slug={performerapi}&client_id=MTUxNTQyNzZ8MTY5ODA3MjA1NS4yMDAxNzYy'
            pid = requests.get(performer_info)
            pid = pid.json()
            pid = pid.get('events')[0].get('performers')[0].get('id')

            postal_code = f'https://api.seatgeek.com/2/venues?city={location}&client_id=MTUxNTQyNzZ8MTY5ODA3MjA1NS4yMDAxNzYy'
            postal_code = requests.get(postal_code)
            postal_code = postal_code.json()
            postal_code = postal_code.get('venues')[0].get('postal_code')
            print(postal_code)

            recommendations = f'https://api.seatgeek.com/2/recommendations?performers.id={pid}&postal_code={postal_code}&client_id=MTUxNTQyNzZ8MTY5ODA3MjA1NS4yMDAxNzYy'
            recommendations = requests.get(recommendations)
            recommendations = recommendations.json()

            print(recommendations)

            return render_template('search_results.html', event_search_results=event_search_results, recommendations=recommendations, artist = performer, location = location)
    else:
        return render_template('index.html', event_search_results=req.json())

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
