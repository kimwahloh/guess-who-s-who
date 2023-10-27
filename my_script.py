from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import requests
import json
import random
import secrets


# Function to retrieve character data from the Star Wars API
def get_character_data(character_number):
    response = requests.get(f'https://swapi.py4e.com/api/people/{character_number}')
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

# Function to refresh and store character data in the user's session
def refresh_character_data():
    character_number = str(random.randint(1, 87))
    response_data = get_character_data(character_number)
    if response_data is not None:
        session['character_data'] = {
            'gender': response_data.get('gender', 'Unknown'),
            'eye_color': response_data.get('eye_color', 'Unknown'),
            'hair_color': response_data.get('hair_color', 'Unknown'),
            'skin_color': response_data.get('skin_color', 'Unknown'),
            'birth_year': response_data.get('birth_year', 'Unknown'),
            'name': response_data.get('name', 'Unknown'),
        }

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.secret_key = secrets.token_hex(16)

    @app.route('/')
    def intro():
        return render_template("index.html")

    @app.route('/starwars', methods=['GET', 'POST'])
    def star():
        try:
            if 'character_data' not in session:
                refresh_character_data()

            if 'answer' in request.form:
                answer_name = session['character_data']['name']
                session.pop('character_data')
                return f"The character is {answer_name}<br><br><a href='/starwars'>Try again</a> <br> <a href='https://thirsty-jennings-167dbc.netlify.app/'>Check out the answer</a>"

            return render_template("starwars.html", character_data=session['character_data'])

        except Exception as e:
            return f"An error occurred: {str(e)}"

    @app.route('/getpokemon', methods=['GET', 'POST'])
    def get_pokemon():
        if request.method == 'POST':
            pokemon_name = request.form.get('pokemon_name')
            # Redirect to the individual Pokemon page
            return redirect(url_for('get_pokemon_details', pokemon=pokemon_name))
        
        # Retrieve the list of Pokemon names (this is the same code you had before)
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1000')
        data = response.json()
        pokemon_names = [pokemon['name'] for pokemon in data['results']]
        
        return render_template('getpokemon.html', heading='Choose a Pokemon', names=pokemon_names)

    @app.route('/getpokemon/<pokemon>')
    def get_pokemon_details(pokemon):
        # Get the abilities of the specified Pokémon
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}/')
        
        if response.status_code == 200:
            data = response.json()
            abilities = [ability['ability']['name'] for ability in data['abilities']]
            
            # Render the HTML template and pass the data to it
            return render_template('pokemon_details.html', pokemon_name=pokemon, abilities=abilities)
        else:
            return 'Pokemon not found'

    if __name__ == '__main__':
        app.run(debug=True)

    return app


