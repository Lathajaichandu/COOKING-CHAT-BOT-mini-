from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load recipes
with open('data/indianRecipe (1).json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    q = request.args.get('q', '').lower()
    if not q:
        return jsonify({'found': False})

    for r in recipes:
        if q in r['TranslatedRecipeName'].lower() or q in r['TranslatedIngredients'].lower():
            return jsonify({
                'found': True,
                'name': r['TranslatedRecipeName'],
                'time': r['TotalTimeInMins'],
                'cuisine': r['Cuisine'],
                'ingredients': r['TranslatedIngredients'],
                'instructions': r['TranslatedInstructions'].replace('\n', '<br>'),
                'url': r['URL']
            })
    
    return jsonify({'found': False, 'query': q})

if __name__ == '__main__':
    print("OPEN THIS IN BROWSER → http://127.0.0.1:5000")
    app.run(debug=True)