# app.py

import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import spacy

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Load spaCy NLP model
nlp = spacy.load('en_core_web_sm')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message')
    response = process_user_input(user_message)
    return jsonify({'message': response})

def process_user_input(user_input):
    doc = nlp(user_input)
    entities = {ent.label_: ent.text for ent in doc.ents}
    
    if 'GPE' in entities:
        destination = entities['GPE']
        hotels = get_hotels(destination)
        attractions = get_attractions(destination)
        
        if hotels and attractions:
            hotel_names = [hotel['name'] for hotel in hotels[:3]]
            top_attractions = attractions[:3]  # Pass the attraction dictionaries
            itinerary = generate_itinerary(top_attractions)
            response = f"Here are some top hotels in {destination}:\n" + "\n".join(hotel_names) + "\n\n"
            response += "Here's a suggested itinerary:\n" + "\n".join(itinerary)
        else:
            response = f"Sorry, I couldn't find sufficient information for {destination}."
    else:
        response = "Please specify a destination you'd like to travel to."
        
    return response

def get_hotels(destination):
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: Google API Key is not set.")
        return None
    
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    
    params = {
        'query': f'hotels in {destination}',
        'key': api_key,
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        hotels = data.get('results', [])
        return hotels
    else:
        print(f"Error fetching hotels: {response.status_code}")
        return None

def get_attractions(destination):
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: Google API Key is not set.")
        return None
    
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    
    params = {
        'query': f'points of interest in {destination}',
        'key': api_key,
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        attractions = data.get('results', [])
        return attractions
    else:
        print(f"Error fetching attractions: {response.status_code}")
        return None

def generate_itinerary(attractions):
    itinerary = []
    for idx, attraction in enumerate(attractions, start=1):
        attraction_name = attraction.get('name', 'Unknown Attraction')
        itinerary.append(f"Day {idx}: Visit {attraction_name}")
    return itinerary

if __name__ == '__main__':
    app.run(debug=True)
