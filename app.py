from flask import Flask, request, jsonify, render_template, send_from_directory
import json
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load JSON data once at startup
with open("indianRecipe.json", encoding="utf-8") as f:
    recipes = json.load(f)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

def fetch_single_recipe(query):
    if not query:
        return None

    query_lower = query.lower()
    # Search by name containing query
    for recipe in recipes:
        if query_lower in recipe.get("name", "").lower():
            # Ensure image key exists
            if not recipe.get("image"):
                recipe["image"] = "/static/noimage.png"
            return recipe
    return None

@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "Query required"}), 400

    recipe = fetch_single_recipe(q)
    if not recipe:
        return jsonify({"result": None, "message": "రెసిపీ కనుగొనబడలేదు"}), 200

    return jsonify({"result": recipe})

@app.route("/api/recipe/<string:recipe_name>")
def get_recipe_image(recipe_name):
    for recipe in recipes:
        if recipe.get("name") == recipe_name:
            image_url = recipe.get("image") or "/static/noimage.png"
            return jsonify({"image": image_url})
    return jsonify({"image": "/static/noimage.png"})

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
