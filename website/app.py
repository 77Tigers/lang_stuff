import json
from flask import Flask, render_template, request, jsonify
import pickle
import converter
from lib import *
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

def open_song(song_name):
    with open(f'songs/{song_name}/chunks.pkl', 'rb') as f:
        song_data = pickle.load(f)
    modified = False
    for (line, meaning) in song_data:
        for i, chunk in enumerate(line):
            if chunk[1] in converter.CORE or is_roman(chunk[1]):
                line[i] = (chunk[0], chunk[1], "")
                modified = True
    if modified:
        with open(f'songs/{song_name}/chunks.pkl', 'wb') as f:
            pickle.dump(song_data, f)
            print("saving modified song")
    return song_data

@app.route('/')
def home():
    # Render the HTML template with the list of songs
    return render_template('index.html', song_options=song_options)

@app.route('/songs/<song_name>', methods=['GET'])
def song(song_name):
    return render_template('index.html', song_options=song_options)

@app.route('/flashcards/get', methods=['GET'])
def get_flashcard():
    # load learning_state.json
    with open("learning_state.json", "r") as f:
        data = json.load(f)
    deck = data["card_deck"]
    # check for ?card=4 in url
    card = request.args.get('card')
    q = "please specify a number"
    a = "this is probably a bug"
    if card is not None:
        try:
            q, a = deck[int(card)]
        except:
            pass

    return jsonify({
        "question": q,
        "answer": a
    })

@app.route('/flashcards')
def flashcards():
    print("NO")
    return render_template('flashcards.html')

@app.route('/request-song', methods=['POST'])
def request_song():
    data = request.get_json()  # Get the JSON data from the request
    song_name = data.get('song')  # Extract the song name from the data

    # Print the requested song name to the console
    print(f"Song requested: {song_name}")

    if song_name in song_options:
        # Unpickle and return song data
        song_data = open_song(song_name)
        return jsonify(song_data)
    else:
        return jsonify({"error": "Invalid song name"})

@app.route('/process-action', methods=['POST'])
def process_action():
    data = request.get_json()
    line = data.get('line')
    position = data.get('position')
    action = data.get('action')

    # Log the action
    print(f"Action '{action}' performed on line {line}, position {position}")

    # Here you can process the action (e.g., update the database, modify the song structure, etc.)
    match action:
        case "add-to-core":
            ...
    
    return jsonify({"status": "success", "line": line, "position": position, "action": action})

# add to code action
@app.route('/add-to-core', methods=['POST'])
def add_to_core_request():
    data = request.get_json()
    word = data.get('word')
    converter.add_to_core(word)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True, port=5001)
