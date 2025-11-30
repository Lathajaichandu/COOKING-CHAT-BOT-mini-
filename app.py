from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load recipes from data folder
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'indianRecipe (1).json')

try:
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        recipes = json.load(f)
    print(f"Loaded {len(recipes)} recipes successfully!")  # Debug log
except Exception as e:
    print(f"ERROR loading JSON: {e}")
    recipes = []  # Fallback empty list

@app.route('/')
def home():
    print("Serving index.html")  # Debug log
    return render_template('index.html')

@app.route('/search')
def search():
    q = request.args.get('q', '').lower().strip()
    print(f"Searching for: {q}")  # Debug log
    
    if not q:
        return jsonify({'found': False})

    for r in recipes:
        name = r.get('TranslatedRecipeName', '').lower()
        ingredients = r.get('TranslatedIngredients', '').lower()
        if q in name or q in ingredients:
            print(f"Found match: {r['TranslatedRecipeName']}")  # Debug log
            return jsonify({
                'found': True,
                'name': r['TranslatedRecipeName'],
                'time': r.get('TotalTimeInMins', 0),
                'cuisine': r.get('Cuisine', 'Unknown'),
                'ingredients': r['TranslatedIngredients'],
                'instructions': r['TranslatedInstructions'].replace('\n', '<br>'),
                'url': r['URL']
            })
    
    return jsonify({'found': False, 'query': q})

if __name__ == '__main__':
    print("Starting Indian Recipe Bot on Render...")
    port = int(os.environ.get('PORT', 5000))  # Render requires this
    app.run(host='0.0.0.0', port=port, debug=True)