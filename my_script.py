from flask import Flask, render_template, request, session, jsonify  # Import necessary modules
import requests  # Import the requests library for making HTTP requests
import json  # Import the json library for working with JSON data
import random  # Import the random module for generating random numbers

app = Flask(__name__)  # Create a Flask application instance
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# STARWARS
# Function to retrieve character data from the Star Wars API
def get_character_data(character_number):
    response = requests.get(f'https://swapi.py4e.com/api/people/{character_number}')  # Send a GET request to the Star Wars API

    if response.status_code == 200:  # Check if the request was successful (status code 200)
        return json.loads(response.text)  # Parse the JSON response
    else:
        return None  # Return None if the request was not successful

# Function to refresh and store character data in the user's session
def refresh_character_data():
    character_number = str(random.randint(1, 87))  # Generate a random character number
    response_data = get_character_data(character_number)  # Retrieve character data from the API

    if response_data is not None:
        session['character_data'] = {
            'gender': response_data.get('gender', 'Unknown'),
            'eye_color': response_data.get('eye_color', 'Unknown'),
            'hair_color': response_data.get('hair_color', 'Unknown'),
            'skin_color': response_data.get('skin_color', 'Unknown'),
            'birth_year': response_data.get('birth_year', 'Unknown'),
            'name': response_data.get('name', 'Unknown'),
        }  # Store character data in the user's session

# POKEMON
# Function to retrieve data from the Pokémon API
def get_pokemon_data():
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1000')  # Send a GET request to the Pokémon API
    return response.json()  # Parse the JSON response

# Retrieve the data and extract the list of Pokémon names
pokemon_data = get_pokemon_data()  # Retrieve data from the Pokémon API
poke_list = [pokemon['name'] for pokemon in pokemon_data['results']]  # Extract a list of Pokémon names from the data

# Base route
@app.route('/')
def intro():
    temp_name = input('Please enter your name: ')  # Get user's name from the command line input
    message = f'Hola, {temp_name}. Welcome to the Galaxy!'  # Create a welcome message with the user's name
    return f'{message}<br>{render_template("index.html")}'  # Return the welcome message and an HTML template

@app.route('/starwars', methods=['GET', 'POST']) # 'GET' Retrieve data from the Star wars API & 'POST' Submit answer
def star():
    try:
        if 'character_data' not in session:  # Check if character data is not already in the user's session; to ensure that character data is only refreshed when it's not already present in the user's session, avoiding unnecessary API requests when the data has already been retrieved and stored
            refresh_character_data()  # If not, refresh and store character data

        if 'answer' in request.form:  # Check if the 'answer' form has been submitted; once the user clicked the button
            answer_name = session['character_data']['name']  # Get the character's name from the session
            session.pop('character_data')  # Clear the character data from the session
            return f"The character is {answer_name}<br><br><a href='/starwars'>Try again</a> <br> <a href='https://thirsty-jennings-167dbc.netlify.app/'>Check out the answer</a>"  # Display the answer and provide links

        return f"Can you guess which {session['character_data']['gender']} character has {session['character_data']['eye_color']} eye color, {session['character_data']['hair_color']} hair color, {session['character_data']['skin_color']} skin color with the birth year of {session['character_data']['birth_year']}? <form method='POST'><input type='submit' name='answer' value='Answer'></form>"  
        # Present a guessing challenge (no character data and no answer submitted)

    except Exception as e: # Handle exceptions
        return f"An error occurred: {str(e)}"  # Display an error message if an exception occurs
    
@app.route('/getpokemon')
def poke():
    return jsonify(poke_list)  # Return the list of Pokémon names in JSON format

# Create Dynamic url 
@app.route('/getpokemon/<pokemon>') 
def poke_present(pokemon):
    if pokemon in poke_list:  # Check if the requested Pokémon is in the list
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}/')  # Send a GET request for detailed Pokémon data
        if response.status_code == 200:  # Check if the request was successful
            abilities_data = response.json()  # Parse the JSON response for Pokémon abilities
            abilities = [ability['ability']['name'] for ability in abilities_data['abilities']]  # Extract the abilities
            return f'The special abilities of {pokemon} are: {", ".join(abilities)}.'  # Display Pokémon's special abilities

        else:
            return f'Failed to retrieve data for {pokemon}.'  # Return an error message if Pokémon data retrieval fails

    else:
        return f'Pokemon not found! Please input a valid Pokemon name from the list.'  # Return an error message if the requested Pokémon is not in the list


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application in debug mode

